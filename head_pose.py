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
def get_bone_pose(armature, bone_name=None):
    if bone_name is None: bone_name = "Head"
    # get bone
    bone = armature.pose.bones[bone_name]
    rotation = armature.matrix_world @ bone.matrix
    # convert to euler
    pitch, roll, yaw = rotation.to_euler()
    # convert to degree
    pitch = math.degrees(pitch - camera.rotation_euler[0])
    yaw = math.degrees(yaw - camera.rotation_euler[1])
    roll = math.degrees(roll - camera.rotation_euler[2])
    # keep 6 decimal places
    return round(pitch, 4), round(yaw, 4), round(roll, 4)


if __name__ == "__main__":
    b_name = "spine.006"
    pitch, yaw, roll = get_bone_pose(armature, b_name)
    print("pitch: ", pitch, "yaw: ", yaw, "roll: ", roll)
