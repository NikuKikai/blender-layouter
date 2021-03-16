
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


import bpy

from .ops import register as ops_reg
from .ops import unregister as ops_ureg

def register():
    ops_reg()

def unregister():
    ops_ureg()