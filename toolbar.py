import time
import math
import random

import bpy
from bpy.props import *


# custom operator
class BatchRenderOperator(bpy.types.Operator):
    bl_idname = 'opr.custom_operator'
    bl_label = 'Render'

    def execute(self, context):
        time_start = time.time()

        # gen 10000 random numbers
        for i in range(10000):
            # caclulate cosin and sin
            cos = math.cos(i)
            sin = math.sin(i)

        # report time cost
        time_cost = time.time() - time_start
        self.report({'INFO'}, 'Time cost: {:.2f} seconds'.format(time_cost))
        
        # print focus on
        focus_on = context.scene['focus on']
        # get enum value
        focus_on = context.scene.bl_rna.properties['focus on'].enum_items[focus_on].name
        print(focus_on)

        return {'FINISHED'}


class PreviewPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_preview_panel'
    bl_label = 'Preview'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        col = self.layout.column()

        col.label(text="Focus On")
        for (prop_name, _) in FOCUS_PROPS:
            col.row().prop(context.scene, prop_name)

        # file save part
        col.separator()
        col.label(text="File")
        for (prop_name, _) in FILE_PROPS:
            col.row().prop(context.scene, prop_name)

        # camera part
        col.separator()
        col.label(text="Camera")
        for (prop_name, _) in CAM_PROPS:
            col.row().prop(context.scene, prop_name)

        # divider
        col.separator()
        col.label(text="Debug")
        # button to render
        col.operator('render.render', icon='RENDER_STILL')

        # batch render part
        col.separator()
        col.label(text="Batch Render")
        for (prop_name, _) in BATCH_PROPS:
            col.row().prop(context.scene, prop_name)
        # custom button
        col.operator('opr.custom_operator')


CLASSES = [
    PreviewPanel,
    BatchRenderOperator,
]

FOCUS_PROPS = [
    ('focus on', bpy.props.EnumProperty(
        name='Bones',
        items=[
            ('random', 'Random', ''),
            ('camera', 'Camera', ''),
            ('object', 'Object', ''),
            ('point', 'Point', ''),
        ],
        default='random',
    )),
]

FILE_PROPS = [
    ('is save', bpy.props.BoolProperty(name='Save', default=False)),
    ('dir path', bpy.props.StringProperty(name='Directory Path', default='', subtype='DIR_PATH', options={'HIDDEN'})),
]

CAM_PROPS = [
    ('min scope', bpy.props.FloatProperty(
        name='Min Distance', default=0.1, min=0.1, max=10.0,
        # add event handler
        update=lambda self, context: setattr(context.scene, 'max scope', max(context.scene['min scope'], context.scene['max scope']))
    )),
    ('max scope', bpy.props.FloatProperty(
        name='Max Distance', default=1.0, min=0.1, max=10.0,
        # add event handler
        update=lambda self, context: setattr(context.scene, 'min scope', min(context.scene['min scope'], context.scene['max scope']))
    )),

    # deviate from the center
    ('deviation', bpy.props.FloatProperty(
        name='Deviation', default=0.0, min=0.0, max=1.0,
        description='Deviate from the center',
    )),
]

BATCH_PROPS = [
    ('amount', bpy.props.IntProperty(name='Amount', default=10, min=1)),
]

TOTAL_PROPS = [
    FOCUS_PROPS,
    FILE_PROPS,
    CAM_PROPS,
    BATCH_PROPS,
]

TOTAL_PROPS = [item for sublist in TOTAL_PROPS for item in sublist]


def register():
    # stack PROPS and BATCH_PROPS
    for (prop_name, prop_value) in TOTAL_PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():
    for (prop_name, _) in TOTAL_PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()
    # unregister()