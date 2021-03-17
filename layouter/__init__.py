
bl_info = {
    "name" : "Layouter",
    "author" : "NikuKikai",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Interface"
}

ICON_NAME = 'ops.interface.layouter'

import bpy

from .ops import register as ops_reg
from .ops import unregister as ops_ureg


# import os
# from shutil import copyfile

# def _copy_icon():
#     src = os.path.join(
#         os.path.abspath(os.path.dirname(__file__)), "icons", ICON_NAME+".dat")
#     blpath = os.path.split(bpy.app.binary_path)[0]
#     ver = f'{bpy.app.version[0]}.{bpy.app.version[1]}'
#     dst = os.path.join(blpath, ver, "datafiles", "icons", ICON_NAME+".dat")

#     if os.path.isfile(src):
#         try:
#             copyfile(src, dst)
#         except:
#             pass

# def _remove_icon():
#     blpath = os.path.split(bpy.app.binary_path)[0]
#     ver = f'{bpy.app.version[0]}.{bpy.app.version[1]}'
#     path = os.path.join(blpath, ver, "datafiles", "icons", ICON_NAME+".dat")

#     if os.path.isfile(path):
#         try:
#             os.remove(path)
#         except:
#             pass


def register():
    # _copy_icon()
    ops_reg()

def unregister():
    bpy.ops.wm.tool_set_by_id(name='builtin.move', space_type='VIEW_3D')
    ops_ureg()
    # _remove_icon()