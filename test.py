import os
import sys

from mathutils import Vector

import bpy
import bmesh
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view


# function to print timestamp
def print_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")


armature = bpy.data.objects["metarig"]
camera = bpy.data.objects["Camera"]
empty = bpy.data.objects["Empty"]
# get object which named cube
cube = bpy.data.objects["Cube"]


# function to get bone's parent name
def get_bone_parent(armature, bone_name):
    bone = armature.data.bones[bone_name]
    return bone.parent.name if bone.parent else None


# function to get bones' length via given bone name
def get_bone_length(armature, bone_name):
    bone = armature.data.bones[bone_name]
    return bone.length


def direction_hit(scene, loc, direction, dist=1):
    init_status = False
    dg = bpy.context.evaluated_depsgraph_get()
    e = 1e-6

    is_hit, loc, _, _, _, _ = scene.ray_cast(
        dg, loc, direction, distance=dist
    )
    # does not hit anything, be occluded by other bones
    if not is_hit: return False

    while(is_hit):
        loc += e * direction
        is_hit, loc, normal, _, _, _ = scene.ray_cast(
            dg, loc, direction
        )
        # hit normal direction is opposite to ray direction
        if normal.dot(direction) < 0: return False

    return True


# function to get bone position
def get_bone_pos_global(armature, bone_name):
    bone = armature.pose.bones[bone_name]
    return armature.matrix_world @ bone.head


def is_visible(camera, boneVec, threshold=1):
    scene = bpy.context.scene
    # get vectors which define view frustum of camera
    top_left = camera.data.view_frame(scene=scene)[-1]

    # convert [0, 1] to [-.5, .5]
    x, y, _ = world_to_camera_view(scene, camera, boneVec)
    pix_vec = Vector((x-.5, y-.5, top_left[2]))
    pix_vec.rotate(camera.matrix_world.to_quaternion())

    return direction_hit(scene, boneVec, -pix_vec, dist=threshold)


if __name__ == '__main__':
    print("\n====== occlusion test")
    print("====== {}".format(print_timestamp()))

    # get bone position in world space
    b_name = "forearm.L"
    b_vec = get_bone_pos_global(armature, b_name)

    # get bone parent name
    b_parent = get_bone_parent(armature, b_name)
    print("bone parent: {}".format(b_parent))
    # get bone length
    b_len = get_bone_length(armature, b_parent)
    print("{} \tlength: {}".format(b_parent, b_len))

    b_len = get_bone_length(armature, b_name)
    print("{} \tlength: {}".format(b_name, b_len))

    is_visible = is_visible(camera, b_vec, threshold=1.6)
    print("is visible: {}".format(is_visible))
