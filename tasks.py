import bpy_extras
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
import math


armature = bpy.data.objects["metarig"]
camera = bpy.data.objects["Camera"]
cube = bpy.data.objects["Cube"]


# get face maps via given name
def get_face_maps(mesh, name=None):
    if name is None: name = "head"
    # get face maps
    face_maps = []
    for face_map in mesh.face_maps:
        if name in face_map.name:
            face_maps.append(face_map)
    return face_maps


if __name__ == "__main__":
    # get mesh from cube
    mesh = cube.data
    # get face maps
    face_maps = get_face_maps(mesh)
    # get face map
    face_map = face_maps[0]
    # get face map indices
    face_map_indices = face_map.data.values()
    # get face map faces
    face_map_faces = [mesh.polygons[i] for i in face_map_indices]

    for face in face_map_faces:
        print(face.index)
