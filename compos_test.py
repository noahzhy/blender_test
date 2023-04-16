import os
import sys
import glob
import datetime

import bpy
import numpy as np
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view


# function to delete all file in given directory
def delete_all_file(path="data/*.png"):
    files = glob.glob(path)
    for f in files:
        os.remove(f)


# function to print timestamp
def print_timestamp():
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


def render_single_layer(layer_name):
    print(layer_name)

    bpy.context.scene.render.use_single_layer = False
    bpy.context.scene.view_layers[layer_name].use = False
    bpy.ops.render.render()
    bpy.ops.render.render(write_still=False, layer=layer_name)


if __name__ == "__main__":
    print()
    print_timestamp()
    delete_all_file("/Users/haoyu/Documents/project/blender_test/data/*")
    render_single_layer(layer_name="V1")
    render_single_layer(layer_name="V2")
