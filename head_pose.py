import bpy
import bmesh
import math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view


armature = bpy.data.objects["metarig"]
camera = bpy.data.objects["Camera"]

# function to get pose of bone named via given name
def get_bone_pose(armature, bone_name):
    # get bone
    bone = armature.pose.bones[bone_name]
    # get location and rotation
    location = bone.location
    rotation = bone.rotation_quaternion
    # convert to dregee of pitch, yaw, roll
    pitch, yaw, roll = rotation.to_euler()
    # convert to relative angle to camera
    pitch = pitch - camera.rotation_euler[0]
    yaw = yaw - camera.rotation_euler[1]
    roll = roll - camera.rotation_euler[2]

    # convert to degree
    pitch = pitch * 180 / math.pi
    yaw = yaw * 180 / math.pi
    roll = roll * 180 / math.pi

    # add 90 degree to pitch
    pitch += 90

    # return pitch, yaw, roll
    return pitch, yaw, roll


if __name__ == "__main__":
    b_name = "spine.006"
    pitch, yaw, roll = get_bone_pose(armature, b_name)
    print("pitch: ", pitch, "yaw: ", yaw, "roll: ", roll)
