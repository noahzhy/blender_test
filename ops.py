import time
import math
import random

import mathutils
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import bpy
import bpy_extras
from bpy_extras import view3d_utils
from bpy_extras.object_utils import world_to_camera_view


# function to convert world space coordinates to camera space coordinates 2d
# normalized return value is in range [0, 1] if clamp is True
def to_camera_space_2d(vector, camera=None, clamp=True):
    if camera is None:
        camera = bpy.context.scene.camera

    scene = bpy.context.scene
    co = bpy_extras.object_utils.world_to_camera_view(scene, camera, vector)
    # flip y axis
    co.y = 1 - co.y
    if clamp:
        # clamp to [0, 1]
        co.x = max(0, min(1, co.x))
        co.y = max(0, min(1, co.y))
    # keep 6 decimal places
    return (round(co.x, 6), round(co.y, 6))


# function to get bone position in camera view using view3d_utils
def get_bone_pos_global(armature, bone_name):
    bone = armature.pose.bones[bone_name]
    bone_pos = armature.matrix_world @ bone.head
    return bone_pos


if __name__ == "__main__":
    # find the bone which name is "Bone"
    armature = bpy.data.objects["metarig"]
    bone_pos_in_camera_space = get_bone_pos_global(armature, "hand.L")
    print(bone_pos_in_camera_space)

    # create a cube with scale 0.1 to bone_pos_in_camera_space
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=bone_pos_in_camera_space)
    # wait 3 seconds then delete the cube
    # update the viewport using
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    # random rotate the cube in 3 seconds
    start = time.time()
    while time.time() - start < 3:
        # rotate
        bpy.ops.transform.rotate(value=0.1, orient_axis='Z', orient_type='LOCAL')
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    
    # delete the cube
    bpy.ops.object.delete()

    # armature is which named "Armature"
    # object_ is which named "Cube"
    # camera is which named "Camera"
    obj = bpy.data.objects["Cube"]
    camera = bpy.data.objects["Camera"]
