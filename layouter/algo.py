import bpy
import mathutils as U
from bpy.types import GizmoGroup, WorkSpaceTool
import numpy as np



def orbit_wrt_worldZ(obj_w, center, drad):
    '''orbit obj around center, wrt. axis world-Z'''
    # Calc Mat of obj around center
    # obj_w = obj.matrix_world.copy()
    center_w = U.Matrix.Translation( center ) # NOTE a surrogate Center Coord with ZERO-ROTATION wrt. world
    w_center = center_w.inverted()
    obj_center = w_center @ obj_w

    # Rotation by drads
    rot = U.Matrix.Rotation(drad, 4, 'Z')

    # Apply Constraint
    robj_rcenter = obj_center

    # Calc Mat of rotated-obj wrt. world
    rcenter_w = center_w @ rot
    robj_w = rcenter_w @ robj_rcenter

    # Apply
    # obj.rotation_euler = robj_w.to_euler('XYZ')  # TODO need global
    # obj.location = robj_w.to_translation()

    return robj_w

# NOTE rotation wrt objx does NOT keep skyline's slope (But not change too mush)
def orbit_wrt_objX(obj_w, center, drad):
    '''orbit obj around center, wrt. axis obj-X'''
    # obj_w = obj.matrix_world.copy()
    center_w = U.Matrix.Translation( center )
    center_obj = obj_w.inverted() @ center_w

    center_obj = U.Matrix.Translation( center_obj.to_translation() ) # NOTE a surrogate Center Coord with ZERO-ROTATION wrt. obj
    center_w = obj_w @ center_obj

    # Rotation by drads
    rot = U.Matrix.Rotation(drad, 4, 'X')

    # Apply Constraint
    robj_rcenter = center_obj.inverted()

    # Calc Mat of rotated-obj wrt. world
    rcenter_w = center_w @ rot
    robj_w = rcenter_w @ robj_rcenter

    # Apply
    # obj.rotation_euler = robj_w.to_euler('XYZ')  # TODO need global
    # obj.location = robj_w.to_translation()

    return robj_w

def orbit_wrt_orient(obj_w, center, drad):
    if center == obj_w.to_translation():
        axis = U.Vector((0, 0, -1))
    else:
        center_w = U.Matrix.Translation(center)
        center_obj = obj_w.inverted() @ center_w
        axis = center_obj.to_translation()

    rot = U.Matrix.Rotation(drad, 4, axis)
    robj_w = obj_w @ rot

    return robj_w

def track_wrt_orient(obj_w, center, d):
    if center == obj_w.to_translation():
        axis = U.Vector((0, 0, -10))
    else:
        center_w = U.Matrix.Translation(center)
        center_obj = obj_w.inverted() @ center_w
        axis = center_obj.to_translation()

    tran = U.Matrix.Translation(axis * d)
    tobj_w = obj_w @ tran

    return tobj_w

def track(obj_w, d):
    axis = U.Vector((0, 0, -10))
    tran = U.Matrix.Translation(axis * d)
    tobj_w = obj_w @ tran
    return tobj_w

def is_front_cam(cam, obj):
    if cam == obj or obj is None: return False
    obj_cam = cam.matrix_world.inverted() @ obj.matrix_world
    return - obj_cam.to_translation()[2] > cam.data.clip_start

def is_mat_front_cam(cam, mat):
    obj_cam = cam.matrix_world.inverted() @ mat
    return - obj_cam.to_translation()[2] > cam.data.clip_start

