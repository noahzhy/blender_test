import bpy
from bpy.props import *


class PreviewPanel(bpy.types.Panel):
    bl_idname = 'preview_panel'
    bl_label = 'Preview'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        col = self.layout.column()
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)

        # button to render
        col.operator('render.render')


CLASSES = [
    PreviewPanel,
]

PROPS = [
    ('prefix', bpy.props.StringProperty(name='Prefix', default='Pref')),
    ('suffix', bpy.props.StringProperty(name='Suffix', default='Suff')),
    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
    ('version', bpy.props.IntProperty(name='Version', default=1)),
]


def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()