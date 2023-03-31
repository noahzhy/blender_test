import os
import sys

from mathutils import Vector

import bpy
import bmesh
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view


armature = bpy.data.objects["metarig"]
camera = bpy.data.objects["Camera"]
empty = bpy.data.objects["Empty"]
# get object which named cube
cube = bpy.data.objects["Cube"]


# function to get bones' length via given bone name
def get_bone_length(armature, bone_name):
    bone = armature.data.bones[bone_name]
    return bone.length


def direction_hit(scene, dg, loc, direction, dist=1):
    normal_list = []
    e = 1e-6

    is_hit, loc, _, _, _, _ = scene.ray_cast(
        dg, loc, direction, distance = dist
    )

    if not is_hit:
        return False

    while(is_hit):
        is_hit, loc, normal, _, _, _ = scene.ray_cast(
            dg, loc + e * direction, direction, distance = dist
        )
        normal_list.append(normal.dot(direction) >= 0)

    return all(normal_list)


# function to get bone position
def get_bone_pos_global(armature, bone_name):
    bone = armature.pose.bones[bone_name]
    return armature.matrix_world @ bone.head


def is_occluded(camera, boneVec, threshold=1):
    # get current scene
    scene = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    # get vectors which define view frustum of camera
    top_left = camera.data.view_frame(scene=scene)[-1]

    # convert [0, 1] to [-.5, .5]
    x, y, _ = world_to_camera_view(scene, camera, boneVec)
    pix_vec = Vector((x-.5, y-.5, top_left[2]))
    pix_vec.rotate(camera.matrix_world.to_quaternion())

    return direction_hit(scene, dg, boneVec, -pix_vec, dist=threshold)


if __name__ == '__main__':
    print("======================= occlusion test =======================")
    # get bone position in world space
    b_name = "forearm.L"
    boneVec = get_bone_pos_global(armature, b_name)

    b_len = get_bone_length(armature, b_name)
    print("bone length: {}".format(b_len))

    is_visible = is_occluded(camera, boneVec)
    print("is visible: {}".format(is_visible))
