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



# 计算两个向量的点积，v1和v2都是3d向量
def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


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


def direction_hit(scene, dg, origin, direction):
    normal_set = []
    count = 0

    is_hit, loc, normal, index, hit_obj, _ = scene.ray_cast(
        dg, origin, direction,
        distance=1000
    )
    e = 1e-6

    while(is_hit):
        dot_result = dot_product(normal, direction)
        # convert to +- 1
        dot_result = 1 if dot_result > 0 else -1
        normal_set.append(dot_result)
        count += 1

        origin = loc + e * direction
        is_hit, loc, normal, index, hit_obj, _ = scene.ray_cast(
            dg, origin, direction,
            distance=1000
        )
    print("hit normal set: {}".format(normal_set))
    return count


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
    if is_hit:
        return is_hit, hit_obj.name_full, index, loc
    else:
        return is_hit, None, None


def is_occluded(camera, boneVec, threshold=1):
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
    c2b = occlusion_ray(
        scene, dg, camera.matrix_world.translation, pixel_vector, 100, "cam2bone")

    print(direction_hit(scene, dg, boneVec, -pixel_vector))

    if c2b[0] and b2c[0]:
        return (c2b != b2c)
    else:
        return True


if __name__ == '__main__':
    print("======================= occlusion test =======================")
    # get bone position in world space
    b_name = "forearm.L"
    boneVec = get_bone_pos_global(armature, b_name)



    if is_occluded(camera, boneVec):
        print("{} occluded".format(b_name))
    else:
        print("{} not occluded".format(b_name))
