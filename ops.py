import bpy
import mathutils as U
from bpy.types import GizmoGroup, WorkSpaceTool
import numpy as np

from .algo import *
from . import ICON_NAME


class OP_orbit_xz_pin_obj(bpy.types.Operator):
    bl_idname = "layouter.op_orbit_xz_pin_obj"
    bl_label = "Modal Operator that Orbits camera with object pinned."
    bl_options = {'UNDO'}

    def modal(self, context, event):
        cam = context.scene.camera

        dx = -(event.mouse_x - self.last_mouse_x)/100
        dy =  (event.mouse_y - self.last_mouse_y)/100

        # Orbit
        if self._center_mat:
            rcam_w = orbit_wrt_worldZ(cam.matrix_world, self._center_mat.to_translation(), dx)
            rcam_w = orbit_wrt_objX(rcam_w, self._center_mat.to_translation(), dy)
        else:
            rcam_w = orbit_wrt_worldZ(cam.matrix_world, cam.matrix_world.to_translation(), dx)
            rcam_w = orbit_wrt_objX(rcam_w, cam.matrix_world.to_translation(), dy)
        # Apply
        cam.rotation_euler = rcam_w.to_euler('XYZ')  # TODO need global
        cam.location = rcam_w.to_translation()

        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        self._center_mat = None
        if context.scene.layouter_use_cursor:
            center = context.scene.cursor
            if center:
                self._center_mat = center.matrix
        else:
            center = context.object
            if center:
                self._center_mat = center.matrix_world

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class OP_orbit_y_pin_obj(bpy.types.Operator):
    bl_idname = "layouter.op_orbit_y_pin_obj"
    bl_label = "Modal Operator that Orbits camera with object pinned."
    bl_options = {'UNDO'}

    def modal(self, context, event):
        cam = context.scene.camera

        dx = -(event.mouse_x - self.last_mouse_x)/200
        # dy =  (event.mouse_y - self.last_mouse_y)/100

        # Orbit
        if self._center_mat:
            rcam_w = orbit_wrt_orient(cam.matrix_world, self._center_mat.to_translation(), dx)
        else:
            rcam_w = orbit_wrt_orient(cam.matrix_world, cam.matrix_world.to_translation(), dx)
        # Apply
        cam.rotation_euler = rcam_w.to_euler('XYZ')  # TODO need global
        cam.location = rcam_w.to_translation()

        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        self._center_mat = None
        if context.scene.layouter_use_cursor:
            center = context.scene.cursor
            if center:
                self._center_mat = center.matrix
        else:
            center = context.object
            if center:
                self._center_mat = center.matrix_world

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class OP_track_pin_obj(bpy.types.Operator):
    bl_idname = "layouter.op_track_pin_obj"
    bl_label = "Modal Operator that Track camera with object pinned."
    bl_options = {'UNDO'}

    is_fix_size : bpy.props.BoolProperty(name='is Fix Size', default=False)

    def modal(self, context, event):
        cam = context.scene.camera

        # dx = -(event.mouse_x - self.last_mouse_x)/200
        dy =  (event.mouse_y - self.last_mouse_y)/100

        # Track
        if self._pinned:
            tcam_w = track_wrt_orient(cam.matrix_world, self._center_mat.to_translation(), dy)
        else:
            tcam_w = track(cam.matrix_world, dy)

        # Dolly zoom
        if self.is_fix_size and self._pinned:
            # obj_cam = cam.matrix_world.inverted() @ self._center_mat
            obj_tcam = tcam_w.inverted() @ self._center_mat
            # z1 = - obj_cam.to_translation()[2]
            z2 = - obj_tcam.to_translation()[2]

            # adjust fov
            new_angle = 2 * np.arctan( self._initial_z_tanfov / z2 )
            cam.data.angle = new_angle

            # pin obj pos by rotate camera orientation
            orient = U.Vector((0,0,-1))
            a1 = obj_tcam.to_translation().angle(orient)
            a2 = np.arctan( self._initial_obj_loc_scr * np.tan(new_angle/2) )
            # axis = orient.cross( obj_cam.to_translation() )
            rot = U.Matrix.Rotation(a1-a2, 4, self._initial_obj_axis)
            rcam_w = tcam_w @ rot
            # self.report({'INFO'}, f'a1 {a1} , a2 {a2}')

            cam.rotation_euler = rcam_w.to_euler('XYZ')

        # Apply
        cam.location = tcam_w.to_translation()

        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        if event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.last_mouse_x = event.mouse_x
        self.last_mouse_y = event.mouse_y

        cam = context.scene.camera

        self._pinned = False
        if context.scene.layouter_use_cursor:
            center = context.scene.cursor
            if center:
                self._center_mat = center.matrix
                self._pinned = is_mat_front_cam(cam, self._center_mat)
        else:
            center = context.object
            if center:
                self._center_mat = center.matrix_world
                self._pinned = is_mat_front_cam(cam, self._center_mat)

        if self._pinned:
            # init for fov
            obj_cam = cam.matrix_world.inverted() @ self._center_mat
            z1 = - obj_cam.to_translation()[2]
            self._initial_z_tanfov = z1 * np.tan( cam.data.angle/2 )

            # init for obj loc on screen
            orient = U.Vector((0,0,-1))
            a1 = obj_cam.to_translation().angle(orient)
            self._initial_obj_loc_scr = np.tan(a1) / np.tan( cam.data.angle/2 )
            self._initial_obj_axis = orient.cross( obj_cam.to_translation() )

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}




class Tool(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'
    bl_idname = "layouter.tool_pin_obj"
    bl_label = "Orbit Camera with object pinned."
    bl_description = ""
    bl_icon = ICON_NAME
    bl_widget = None
    bl_keymap = (
        ("layouter.op_orbit_xz_pin_obj", {"type": 'LEFTMOUSE', "value": 'PRESS'},
         {"properties": []}),
        ("layouter.op_orbit_y_pin_obj", {"type": 'MIDDLEMOUSE', "value": 'PRESS', "alt": True},
         {"properties": []}),
        ("layouter.op_track_pin_obj", {"type": 'RIGHTMOUSE', "value": 'PRESS', "alt": True},
         {"properties": []}),
        ("layouter.op_track_pin_obj", {"type": 'RIGHTMOUSE', "value": 'PRESS', "alt": True, "ctrl": True},
         {"properties": [('is_fix_size', True)]}),
    )

    def draw_settings(context, layout, tool):
        layout.prop(context.scene, "layouter_use_cursor")



classes = [
    OP_orbit_xz_pin_obj,
    OP_orbit_y_pin_obj,
    OP_track_pin_obj,
]


def register():
    bpy.types.Scene.layouter_use_cursor = bpy.props.BoolProperty(name='Use Cursor', default=False)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.utils.register_tool(Tool, separator=True)

def unregister():
    bpy.utils.unregister_tool(Tool)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.layouter_use_cursor


