import os
import sys

from mathutils import Vector
from mathutils.bvhtree import BVHTree

import bpy
import bmesh
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view


armature = bpy.data.objects["metarig"]
camera = bpy.data.objects["Camera"]
empty = bpy.data.objects["Empty"]
# get object which named cube
cube = bpy.data.objects["Cube"]


# function to calculate distance between two vectors
def distance(v1, v2):
    return (v1 - v2).length


def select_face_loop(bm, face_index):
    # Get the selected face
    bm.faces.ensure_lookup_table()
    selected_face = bm.faces[face_index]

    # Find the face loop that includes the selected face
    face_loop = []
    current_face = selected_face
    while True:
        # Add the current face to the face loop
        face_loop.append(current_face)

        # Find the next face in the loop
        next_face = None
        for e in current_face.edges:
            for f in e.link_faces:
                if f != current_face and f.select:
                    next_face = f
                    break
            if next_face:
                break

        # If no next face was found, we've reached the end of the loop
        if not next_face:
            break

        # Update the current face to the next face
        current_face = next_face

    # Select the face loop
    for f in face_loop:
        f.select = True

    return face_loop



# function to get location of given face index
def get_face_location(bm, face_index):
    # ensure_lookup_table
    bm.faces.ensure_lookup_table()
    face = bm.faces[face_index]
    face_loc = face.calc_center_bounds()

    # select face loops via given face index

    


    return face_loc


# function to select face loops via given face index and bvhtree
def select_face_loops(bvhtree, face_index):
    print("select face loops")
    # debug face index
    print("face index: {}".format(face_index))
    
    


# function to get bone position
def get_bone_pos_global(armature, bone_name):
    bone = armature.pose.bones[bone_name]
    bone_pos = armature.matrix_world @ bone.head
    return bone_pos


# description: ray cast from origin to direction
def occlusion_ray(scene, dg, origin, direction, distance=1000, description="cam2bone"):
    direction.normalized()
    is_hit, loc, _, index, hit_obj, _ = scene.ray_cast(
        dg, origin, direction,
        distance=distance
    )
    empty.location = loc
    if is_hit:
        print("{} hit idx: {}".format(description, index))
        return is_hit, hit_obj.name_full, index, loc
    else:
        return is_hit, None, None


def get_nearest_bvh(obj, vector):
    # find nearest bvh
    nearest_bvh = None

    dg = bpy.context.evaluated_depsgraph_get()
    # get bvh tree of given object

    mesh = obj.evaluated_get(dg).to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)
    bvh = BVHTree.FromBMesh(bm)

    # get nearest bvh
    nearest_bvh = bvh.find_nearest_range(vector, .1)
    nearest_bvh.sort(key=lambda x: x[-1])


    # 

    f_loop = select_face_loop(bm, nearest_bvh[0][2])
    for f in f_loop:
        print(f.index)

    vca = get_face_location(bm, nearest_bvh[0][2])
    # new a empty to the face center
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=vca)

    # get first 20 items
    nearest_bvh = nearest_bvh[:20]
    # get average distance
    avg_dist = sum([item[-1] for item in nearest_bvh]) / len(nearest_bvh)

    nearest_bvh = bvh.find_nearest_range(vector, avg_dist*3)

    # new the cubes to the face center
    # for item in nearest_bvh:
    #     # new a primitive cube
    #     bpy.ops.mesh.primitive_cube_add(size=0.01, location=item[0])

    # keep index only
    nearest_bvh = [item[2] for item in nearest_bvh]
    return nearest_bvh


c2b_idx = -1

def is_occluded(camera, boneVec, threshold=1):
    global c2b_idx
    # get current scene
    scene = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    # get vectors which define view frustum of camera
    _, _, _, top_left = camera.data.view_frame(scene=scene)

    # convert [0, 1] to [-.5, .5]
    x, y, _ = world_to_camera_view(scene, camera, boneVec)
    pixel_vector = Vector((x-.5, y-.5, top_left[2]))
    pixel_vector.rotate(camera.matrix_world.to_quaternion())

    # bone -> camera
    b2c = occlusion_ray(scene, dg, boneVec, -pixel_vector, threshold, "bone2cam")
    # camera -> bone
    c2b = occlusion_ray(scene, dg, camera.matrix_world.translation, pixel_vector, 100, "cam2bone")

    if c2b[0] and b2c[0]:
        c2b_idx = c2b[-2]
        # the difference between b2c and c2b
        diff = distance(b2c[-1], c2b[-1])
        diff = abs(c2b[-2] - b2c[-2]) / diff
        print("diff: {}".format(diff))
        
        return (c2b != b2c)
    else:
        return True


if __name__ == '__main__':
    print("======================= occlusion test =======================")
    # get bone position in world space
    b_name = "forearm.L"
    boneVec = get_bone_pos_global(armature, b_name)
    n_idx = get_nearest_bvh(cube, boneVec)
    print("nearest bvh: {}".format(n_idx))

    if is_occluded(camera, boneVec):
        print("{} occluded".format(b_name))
    else:
        print("{} not occluded".format(b_name))

    if c2b_idx in n_idx:
        print("{} in nearest".format(b_name))
    else:
        print("{} not in nearest".format(b_name))

    print("c2b_idx: {}".format(c2b_idx))
