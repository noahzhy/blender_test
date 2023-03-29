import bpy
import bmesh
import bpy_extras
from bpy_extras import view3d_utils
from bpy_extras.object_utils import world_to_camera_view
import mathutils
from mathutils import Vector
from mathutils.bvhtree import BVHTree


obj = bpy.data.objects["Cube"]

dg = bpy.context.evaluated_depsgraph_get()
# get bvh tree of given object
mesh = obj.evaluated_get(dg).to_mesh()
bm = bmesh.new()
bm.from_mesh(mesh)
bm.transform(obj.matrix_world)


# convert vector to screen space using world_to_camera_view
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


# function to get bmface to vectorsarray
def get_bmface_to_vectorsarray(bmface):
    vectors = []
    for v in bmface.verts:
        vectors.append(v.co)
    return vectors


# function to get face maps via given name
def get_face_maps(name):
    face_maps = []
    for face_map in mesh.face_maps:
        print(face_map.name)

    return face_maps


# get max and min xy coordinates
def get_max_min_xy(vectors):
    x = []
    y = []
    for vector in vectors:
        x.append(vector[0])
        y.append(vector[1])
    return min(x), min(y), max(x), max(y)


if __name__ == "__main__":
    # data = get_face_maps(name="Head")
    # print(data)
    # enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # print(obj.face_maps['Head'].items())

    # select face map
    obj.face_maps.active_index = obj.face_maps['Head'].index
    bpy.ops.object.face_map_select()

    vectors = []
    
    # get selected face
    selected_faces = [f for f in bm.faces if f.select]
    for face in selected_faces:
        tmp_vectors = get_bmface_to_vectorsarray(face)
        for vector in tmp_vectors:
            # convert vector to screen space
            screen_space = to_camera_space_2d(vector)
            vectors.append(screen_space)

    # get max and min xy coordinates
    min_x, min_y, max_x, max_y = get_max_min_xy(vectors)
    print(min_x, min_y, max_x, max_y)



    # 

    # 

    # sele