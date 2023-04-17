import time
import math
import random

import bpy
from bpy.props import *


# custom operator
class CustomOperator(bpy.types.Operator):
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

        # divider
        col.separator()
        col.label(text="Camera")

        for (prop_name, _) in CAM_PROPS:
            col.row().prop(context.scene, prop_name)

        # button to render
        col.operator('render.render')

        # divider
        col.separator()
        col.label(text="Batch Render")

        for (prop_name, _) in BATCH_PROPS:
            col.row().prop(context.scene, prop_name)

        # custom button
        col.operator('opr.custom_operator')


CLASSES = [
    PreviewPanel,
    CustomOperator,
]

FOCUS_PROPS = [
    ('focus on', bpy.props.EnumProperty(
        name='Bones',
        items=[
            ('camera', 'Camera', ''),
            ('object', 'Object', ''),
            ('point', 'Point', ''),
            ('random', 'Random', ''),
        ],
        default='random',
    )),
]

CAM_PROPS = [
    ('min scope', bpy.props.FloatProperty(name='Min Distance', default=0.1, min=0.1, max=10.0)),
    ('max scope', bpy.props.FloatProperty(name='Max Distance', default=1.0, min=0.1, max=10.0)),
]

BATCH_PROPS = [
    ('amount', bpy.props.IntProperty(name='Amount', default=10, min=1)),
]

TOTAL_PROPS = FOCUS_PROPS + CAM_PROPS + BATCH_PROPS


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