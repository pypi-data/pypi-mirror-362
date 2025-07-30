import math

import numpy as np
from PySide6.QtGui import QPalette
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtWidgets import QApplication
from numpy import array

from scipy.spatial.transform import Rotation as R

from qosm.gui.managers import SimulationManager

from qosm.gui.managers.RequestManager import RequestType


class GLViewer(QOpenGLWidget):
    def __init__(self, parent=None, src_manager=None, obj_manager=None, req_manager=None):
        super().__init__(parent)
        # Managers
        self.source_manager = src_manager
        self.object_manager = obj_manager
        self.request_manager = req_manager

        self.angle_x = 30
        self.angle_y = -45
        self.zoom = -0.7
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.last_pos = None

        # Projection mode
        self.is_perspective = True
        self.ortho_size = 2.0  # Taille de la vue orthogonale

        # Changed from list to dictionary with UUID keys
        self.objects = {}  # {uuid: object}
        self.filenames = {}  # {uuid: filename} for StepMesh objects
        self.selected_uuid = None
        self.setFocusPolicy(Qt.StrongFocus)

        # Object movement mode
        self.object_move_mode = False
        self.move_axis = None

        # Callbacks - now pass UUIDs instead of indices
        self.selection_callback = None
        self.log_callback = None

    def toggle_projection(self):
        """Switch between perspective and orthogonal projection"""
        self.is_perspective = not self.is_perspective
        self.update_projection()

        mode = "perspective" if self.is_perspective else "orthogonal"
        self.log_callback(f"Projection switched to {mode} mode")

        self.update()

    def update_projection(self):
        """Update projection matrix"""
        self.makeCurrent()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Calculer le ratio d'aspect
        aspect = self.width() / self.height() if self.height() != 0 else 1.0

        # Paramètres de clipping
        near_plane = 0.0001
        far_plane = 1000.0

        if self.is_perspective:
            # Projection perspective
            gluPerspective(45.0, aspect, near_plane, far_plane)
        else:
            # Projection orthogonale
            # Ajuster la taille orthogonale basée sur le zoom pour une transition fluide
            ortho_size = abs(self.zoom) * 0.5 if abs(self.zoom) > 0.1 else self.ortho_size
            glOrtho(-ortho_size * aspect, ortho_size * aspect,
                    -ortho_size, ortho_size,
                    near_plane, far_plane)

        glMatrixMode(GL_MODELVIEW)

    def fit_all_objects(self):
        """Adjust view to see all objects"""
        #todo à refaire !
        if not self.object_manager.objects:
            return

        return
        # Calculate bounding box of all objects
        min_bounds = np.array([float('inf'), float('inf'), float('inf')])
        max_bounds = np.array([float('-inf'), float('-inf'), float('-inf')])

        for _obj in self.object_manager.objects.values():
            pass

        # Calculate center and size
        center = (min_bounds + max_bounds) / 2
        size = np.max(max_bounds - min_bounds)

        if size == 0:  # Handle case with no objects or single point
            size = 1.0

        # Adjust view to center and zoom to fit
        self.pan_x = -center[0]
        self.pan_y = -center[1]
        # Improved zoom calculation based on object size
        self.zoom = -size * 1.5  # Better fit factor

        # Ensure zoom stays within reasonable bounds
        self.zoom = max(-500.0, min(-0.01, self.zoom))

        if self.log_callback:
            self.log_callback(f"View adjusted to fit all objects (size: {size:.2f})")

        self.update()

    def set_source_view(self):
        if self.log_callback:
            self.log_callback("View updated with active source")
        self.update()

    def set_view_xy(self):
        """Set view to XY plane (front view) - looking at xOy plane"""
        self.angle_x = 0
        self.angle_y = 0
        if self.log_callback:
            self.log_callback("View set to XY plane (front view)")
        self.update()

    def set_view_xz(self):
        """Set view to XZ plane (side view) - looking at xOz plane"""
        self.angle_x = 90
        self.angle_y = 90
        if self.log_callback:
            self.log_callback("View set to XZ plane (side view)")
        self.update()

    def set_view_yz(self):
        """Set view to YZ plane (top view) - looking at yOz plane"""
        self.angle_x = 0
        self.angle_y = 90
        if self.log_callback:
            self.log_callback("View set to YZ plane (top view)")
        self.update()

    def reset_view(self):
        """Reset view to default (XZ plane)"""
        self.angle_x = 90
        self.angle_y = 90
        self.zoom = -2.5
        self.pan_x = 0.0
        self.pan_y = 0.0
        if self.log_callback:
            self.log_callback("View reset to default (XZ plane)")
        self.update()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.8, 0.8, 0.8, 1.0)

        light_pos = [0.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        distance = 100.0
        height = distance * 0.7071  # sin(45°) ≈ 0.7071


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        """glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Adjust near and far clipping planes for better zoom behavior
        # Near plane: very close to avoid clipping when zooming in
        # Far plane: very far to avoid clipping large scenes
        near_plane = 0.0001
        far_plane = 1000.0
        gluPerspective(45.0, w / h if h != 0 else 1.0, near_plane, far_plane)
        glMatrixMode(GL_MODELVIEW)"""
        self.update_projection()

    def render_object(self, obj, picking_mode=False, selected_mode=False, domain_mode=False):
        """Unified object rendering method"""
        if obj['type'] == 'StepMesh' or obj['type'] == 'ShapeMesh':
            self.render_mesh(obj, picking_mode, selected_mode, domain_mode)
        elif obj['type'] in ['GBE', RequestType.NEAR_FIELD.name]:
            self.render_grid(obj, picking_mode, selected_mode)
        elif obj['type'] == RequestType.FAR_FIELD.name:
            self.render_far_field(obj, picking_mode, selected_mode)

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Propriétés de la lumière
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Blanc
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Blanc
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])  # Ambiance faible

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_lighting()

        glLoadIdentity()

        # Apply view transformations
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        self.draw_axes(length=0.1)

        # display the source if possible
        source = self.source_manager.get_active_source()
        if source:
            glPushMatrix()
            self.render_transform(source)
            if source['type'] == 'NearFieldSource':
                self.render_feko_grid(source['parameters']['grid_info'], picking_mode=False, selected_mode=False)
            elif source['type'] == 'Horn':
                self.render_horn(source['parameters'], picking_mode=False, selected_mode=False)
            elif source['type'] == 'GaussianBeam':
                self.render_gaussian_beam(source['parameters'], picking_mode=False, selected_mode=False)
            glPopMatrix()

        # get the selected domain (if any)
        selected_obj = self.object_manager.get_active_object()
        if selected_obj is not None and selected_obj['type'] == 'Domain':
            pre_selected = selected_obj['parameters']['meshes']
        else:
            pre_selected = []
        items = self.object_manager.get_ordered_objects() + self.request_manager.get_ordered_requests()
        for object_uuid, obj in items:
            if not obj:
                continue
            glPushMatrix()
            self.render_transform(obj)

            # Render object
            self.render_object(obj,
                               picking_mode=False,
                               selected_mode=(object_uuid == self.object_manager.active_object_uuid
                                              or object_uuid == self.request_manager.active_request_uuid
                                              or object_uuid in pre_selected),
                               domain_mode=object_uuid in pre_selected)

            glPopMatrix()

    def render_for_picking(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        glDisable(GL_LIGHTING)
        glDisable(GL_DITHER)

        # Create mapping from color to UUID for picking
        self.picking_color_map = {}

        items = self.object_manager.get_ordered_objects() + self.request_manager.get_ordered_requests()
        for idx, (object_uuid, obj) in enumerate(items):
            glPushMatrix()
            self.render_transform(obj)

            # Set picking color using index (but map back to UUID)
            color_id = idx + 1
            r = ((color_id >> 16) & 0xFF) / 255.0
            g = ((color_id >> 8) & 0xFF) / 255.0
            b = (color_id & 0xFF) / 255.0
            glColor3f(r, g, b)

            # Store mapping for later retrieval
            self.picking_color_map[color_id] = object_uuid

            # Render object in picking mode
            self.render_object(obj, picking_mode=True)

            glPopMatrix()

        glEnable(GL_LIGHTING)
        glEnable(GL_DITHER)

    def pick_mesh_at(self, x, y):
        self.makeCurrent()
        self.render_for_picking()
        glFlush()

        pixel = glReadPixels(x, self.height() - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        rgb = np.frombuffer(pixel, dtype=np.uint8)
        if rgb.size < 3:
            return None

        r, g, b = rgb
        color_id = (r << 16) | (g << 8) | b

        # Map color back to UUID
        if color_id in self.picking_color_map:
            object_uuid = self.picking_color_map[color_id]
            if self.object_manager.exists(object_uuid):
                self.object_manager.set_active_object(object_uuid)
                display_name = self.object_manager.get_object_display_name(object_uuid)
            else:
                self.request_manager.set_active_request(object_uuid)
                display_name = self.request_manager.get_request_display_name(object_uuid)

            self.object_move_mode = False
            self.move_axis = None

            if self.log_callback:
                self.log_callback(f"Object selected: {display_name}")

            if self.selection_callback:
                self.selection_callback(object_uuid)
        else:
            if self.log_callback and (self.object_manager.get_active_object() is not None or
                    self.request_manager.get_active_request() is not None):
                self.log_callback("No object selected")

            self.object_manager.set_active_object(None)
            self.request_manager.set_active_request(None)
            self.object_move_mode = False
            self.move_axis = None

            if self.selection_callback:
                self.selection_callback(None)

        self.update()
        return object_uuid if color_id in self.picking_color_map else None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            self.pick_mesh_at(pos.x(), pos.y())
        else:
            self.last_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton and self.last_pos:
            dx = event.position().x() - self.last_pos.x()
            dy = event.position().y() - self.last_pos.y()
            self.angle_x += dy * 0.5
            self.angle_y += dx * 0.5
            self.last_pos = event.position().toPoint()
            self.update()

    def wheelEvent(self, event):

        delta = event.angleDelta().y() / 120
        # Adjust zoom step based on current zoom level for smoother zooming
        zoom_step = abs(self.zoom) * 0.1 if abs(self.zoom) > 0.1 else 0.05
        self.zoom += delta * zoom_step

        # Limit zoom to prevent extreme values that could cause clipping issues
        self.zoom = max(-500.0, min(-0.01, self.zoom))

        # En mode orthogonale, mettre à jour la projection
        if not self.is_perspective:
            self.update_projection()

        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        angle_step = 5.0
        move_step = 0.001

        # Delete key to remove selected object
        if key == Qt.Key_Delete:
            if self.object_manager.active_object_uuid is not None:
                # Delegate to main window for deletion with confirmation
                if hasattr(self.parent(), 'delete_object'):
                    self.parent().delete_object()
            return

        # Movement mode management with G
        if key == Qt.Key_G:
            if self.object_move_mode:
                self.object_move_mode = False
                self.move_axis = None
                if self.log_callback:
                    self.log_callback("Movement mode: DISABLED")
            else:
                if (self.object_manager.active_object_uuid is not None
                        and self.object_manager.get_active_object()['type'] == 'StepMesh'):
                    self.object_move_mode = True
                    self.move_axis = None
                    if self.log_callback:
                        self.log_callback("Movement mode: ENABLED - Select an axis (X/Y/Z)")
            self.update()
            return

        # Axis selection in movement mode
        if self.object_move_mode and self.object_manager.active_object_uuid is not None:
            if key == Qt.Key_X:
                self.move_axis = 'x'
                if self.log_callback:
                    self.log_callback("Movement axis: X")
                self.update()
                return
            elif key == Qt.Key_Y:
                self.move_axis = 'y'
                if self.log_callback:
                    self.log_callback("Movement axis: Y")
                self.update()
                return
            elif key == Qt.Key_Z:
                self.move_axis = 'z'
                if self.log_callback:
                    self.log_callback("Movement axis: Z")
                self.update()
                return

        # CTRL + arrows for lateral view movement
        if modifiers & Qt.ControlModifier:
            if key == Qt.Key_Left:
                self.pan_x -= move_step
            elif key == Qt.Key_Right:
                self.pan_x += move_step
            elif key == Qt.Key_Up:
                self.pan_y += move_step
            elif key == Qt.Key_Down:
                self.pan_y -= move_step
            else:
                super().keyPressEvent(event)
                return

        # Object movement mode activated with axis selected
        elif self.object_move_mode and self.object_manager.active_object_uuid is not None and self.move_axis:
            position, rotation_deg = self.object_manager.get_object_pose()
            if key == Qt.Key_Left or key == Qt.Key_Down:
                if self.move_axis == 'x':
                    position[0] -= move_step
                elif self.move_axis == 'y':
                    position[1] -= move_step
                elif self.move_axis == 'z':
                    position[2] -= move_step
            elif key == Qt.Key_Right or key == Qt.Key_Up:
                if self.move_axis == 'x':
                    position[0] += move_step
                elif self.move_axis == 'y':
                    position[1] += move_step
                elif self.move_axis == 'z':
                    position[2] += move_step
            else:
                super().keyPressEvent(event)
                return

            # Update Frame with new position
            self.object_manager.update_object_pose(position, rotation_deg)
            self.selection_callback(self.object_manager.active_object_uuid)
            self.update()

        # View rotation mode (default behavior)
        else:
            if key == Qt.Key_Left:
                self.angle_y -= angle_step
            elif key == Qt.Key_Right:
                self.angle_y += angle_step
            elif key == Qt.Key_Up:
                self.angle_x -= angle_step
            elif key == Qt.Key_Down:
                self.angle_x += angle_step
            else:
                super().keyPressEvent(event)
                return

        self.update()

    @staticmethod
    def set_to_selected_color():
        palette = QApplication.palette()
        selection_bg = palette.color(QPalette.Highlight)
        r = selection_bg.red() / 255.0
        g = selection_bg.green() / 255.0
        b = selection_bg.blue() / 255.0
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])
        glColor4f(r, g, b, 0.8)

    def render_mesh(self, obj, picking_mode=False, selected_mode=False, domain_mode=False):
        """Render a StepMesh object"""
        if obj is None:
            return
        mesh = obj['parameters']

        if not picking_mode:
            # Define material and color (only in normal mode)
            if domain_mode:
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.1, 0.5, 0.3, 1.0])
            elif selected_mode:
                if self.object_move_mode:
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0, 1.0, 1.0, 1.0])
                else:
                    self.set_to_selected_color()
            else:
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.6, 0.6, 0.6, 1.0])

            # frame transformation already applied by render_transform
            _vertices = mesh['vertices']
            glBegin(GL_TRIANGLES)
            for tri in mesh['triangles']:
                for i in tri:
                    normal = mesh['normals'][i] if i < mesh['normals'].shape[0] else (0.0, 0.0, 1.0)
                    glNormal3f(*normal)
                    glVertex3f(*_vertices[i])
            glEnd()

            # Draw triangle edges (wireframe overlay)
            glDisable(GL_LIGHTING)  # Disable lighting to ensure pure color for lines
            glColor4f(0.0, 0.0, 0.0, .8)  # Black color for edges
            glLineWidth(2.0)

            glBegin(GL_LINES)
            for tri in mesh['triangles']:
                i0, i1, i2 = tri
                v0, v1, v2 = _vertices[i0], _vertices[i1], _vertices[i2]

                glVertex3f(*v0)
                glVertex3f(*v1)  # Edge v0-v1
                glVertex3f(*v1)
                glVertex3f(*v2)  # Edge v1-v2
                glVertex3f(*v2)
                glVertex3f(*v0)  # Edge v2-v0
            glEnd()

            glEnable(GL_LIGHTING)  # Re-enable lighting for subsequent objects
        else:
            # Picking mode - no normals needed
            # frame transformation already applied by render_transform
            _vertices = mesh['vertices']
            glBegin(GL_TRIANGLES)
            for tri in mesh['triangles']:
                for i in tri:
                    glVertex3f(*_vertices[i])
            glEnd()

    @staticmethod
    def render_feko_grid(grid_info, picking_mode=False, selected_mode=False):
        if not picking_mode:
            # Enable transparency
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # Enable depth testing for 3D masking
            glEnable(GL_DEPTH_TEST)
            # Disable lighting to avoid shading
            glDisable(GL_LIGHTING)

        # Determine plane type and create corners
        if grid_info['y_range'][2] == 1:
            # ZX plane (Y constant)
            y = grid_info['y_range'][0]
            corners = [
                [grid_info['x_range'][0], y, grid_info['z_range'][0]],
                [grid_info['x_range'][1], y, grid_info['z_range'][0]],
                [grid_info['x_range'][1], y, grid_info['z_range'][1]],
                [grid_info['x_range'][0], y, grid_info['z_range'][1]]
            ]
            normal = [0, 1, 0]
        elif grid_info['x_range'][2] == 1:
            # ZY plane (X constant)
            x = grid_info['x_range'][0]
            corners = [
                [x, grid_info['y_range'][0], grid_info['z_range'][0]],
                [x, grid_info['y_range'][1], grid_info['z_range'][0]],
                [x, grid_info['y_range'][1], grid_info['z_range'][1]],
                [x, grid_info['y_range'][0], grid_info['z_range'][1]]
            ]
            normal = [1, 0, 0]
        else:
            # XY plane (Z constant)
            z = grid_info['z_range'][0]
            corners = [
                [grid_info['x_range'][0], grid_info['y_range'][0], z],
                [grid_info['x_range'][1], grid_info['y_range'][0], z],
                [grid_info['x_range'][1], grid_info['y_range'][1], z],
                [grid_info['x_range'][0], grid_info['x_range'][1], z]
            ]
            normal = [0, 0, 1]

        # Draw semi-transparent plane
        glColor4f(0.1, 0.3, 0.6, 0.9)

        glBegin(GL_QUADS)
        glNormal3f(*normal)
        for corner in corners:
            glVertex3f(*corner)
        glEnd()

        # Optional: Draw grid lines for better visualization
        if not picking_mode:
            if selected_mode:
                glColor4f(0.8, 0.3, 0.1, 0.7)  # Darker orange for lines
            else:
                glColor4f(0.1, 0.1, 0.5, 0.7)  # Darker blue for lines

            glLineWidth(1.0)
            # You could add grid line drawing here if needed

            # Draw border
            glBegin(GL_LINE_LOOP)
            for corner in corners:
                glVertex3f(*corner)
            glEnd()

        # Restore OpenGL state
        if not picking_mode:
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)

    def render_grid(self, grid, picking_mode=False, selected_mode=False):
        """Render a Grid object as a semi-transparent plane"""
        if grid is None:
            return

        if not picking_mode:
            # Enable transparency
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            # Enable depth testing for 3D masking
            glEnable(GL_DEPTH_TEST)

            # Disable lighting to avoid shading
            glDisable(GL_LIGHTING)

            glEnable(GL_POLYGON_OFFSET_FILL)
            if grid['type'] == 'GBE':
                glPolygonOffset(2, 2)
            else:
                glPolygonOffset(.5, .5)

        # Get grid points
        # don't apply translation to grid point as this will be done by opengl
        if grid['type'] == 'GBE':
            points = SimulationManager.gbe_grid_from_parameters(grid, do_translation=False).points.numpy()
        else:
            points = SimulationManager.nf_grid_from_parameters(grid).points.numpy()

        # Calculate bounds for each dimension
        min_coords = np.min(points, axis=0)
        max_coords = np.max(points, axis=0)

        # Determine plane type and create corners
        if grid['parameters']['plane'] == 'ZX':
            # ZX plane (Y constant)
            y = points[0, 1]
            corners = [
                [min_coords[0], y, min_coords[2]],
                [max_coords[0], y, min_coords[2]],
                [max_coords[0], y, max_coords[2]],
                [min_coords[0], y, max_coords[2]]
            ]
            normal = [0, 1, 0]
        elif grid['parameters']['plane'] == 'ZY':
            # ZY plane (X constant)
            x = points[0, 0]
            corners = [
                [x, min_coords[1], min_coords[2]],
                [x, max_coords[1], min_coords[2]],
                [x, max_coords[1], max_coords[2]],
                [x, min_coords[1], max_coords[2]]
            ]
            normal = [1, 0, 0]
        else:
            # Fallback to XY plane
            z = points[0, 2] if points.shape[0] > 0 else 0
            corners = [
                [min_coords[0], min_coords[1], z],
                [max_coords[0], min_coords[1], z],
                [max_coords[0], max_coords[1], z],
                [min_coords[0], max_coords[1], z]
            ]
            normal = [0, 0, 1]

        # Draw semi-transparent plane
        if not picking_mode:
            if selected_mode:
                self.set_to_selected_color()
            else:
                if grid['type'] == 'GBE':
                    glColor4f(0.5, 0.5, 1.0, 0.7)  # Blue when not selected
                else:
                    if grid.get('enabled', True):
                        glColor4f(0.5, 1.0, 0.5, 0.3)  # Blue when not selected AND enabled
                    else:
                        glColor4f(0.65, 0.65, 0.65, 0.3)  # Grey when not selected AND disabled

        glBegin(GL_QUADS)
        glNormal3f(*normal)
        for corner in corners:
            glVertex3f(*corner)
        glEnd()

        # Optional: Draw grid lines for better visualization
        if not picking_mode:
            if selected_mode:
                self.set_to_selected_color()
            else:
                if grid['type'] == 'GBE':
                    glColor4f(0.3, 0.3, 0.7, 0.7)  # Darker blue for lines
                else:
                    if grid.get('enabled', True):
                        glColor4f(0.3, 0.7, 0.3, 0.7)  # Darker Green for lines
                    else:
                        glColor4f(0.6, 0.6, 0.6, 0.7)


            glLineWidth(1.0)
            # You could add grid line drawing here if needed

            # Draw border
            glBegin(GL_LINE_LOOP)
            for corner in corners:
                glVertex3f(*corner)
            glEnd()

        # Restore OpenGL state
        if not picking_mode:
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glDisable(GL_POLYGON_OFFSET_FILL)

    def render_gaussian_beam(self, beam_data, picking_mode=False, selected_mode=False):
        """
        Render a Gaussian Beam source as a disk aperture with polarization arrow
        Note: Center is at (0, 0, z0)

        Args:
            beam_data: Dictionary containing beam parameters
            picking_mode: Boolean, if True render for object picking
            selected_mode: Boolean, if True render with selected colors
        """
        if beam_data is None:
            return

        if not picking_mode:
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_LIGHTING)

        # Extract beam parameters
        w0 = beam_data['w0'] * 1e-3  # Beam waist radius
        z0 = beam_data['z0'] * 1e-3  # Z-offset
        polarization = beam_data['polarization']

        # Set colors
        if not picking_mode:
            if selected_mode:
                self.set_to_selected_color()
            else:
                if beam_data.get('enabled', True):
                    glColor3f(0.2, 0.8, 0.2)  # Green color for Gaussian beam
                else:
                    glColor3f(0.5, 0.5, 0.5)  # Grey when disabled

        # Render disk aperture directly at z0
        num_segments = 32  # Number of segments for circle

        # Render filled disk
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 0, 1)

        # Center vertex
        glVertex3f(0, 0, z0)

        # Circle vertices
        for i in range(num_segments + 1):
            angle = 2.0 * math.pi * i / num_segments
            x = w0 * math.cos(angle)
            y = w0 * math.sin(angle)
            glVertex3f(x, y, z0)

        glEnd()

        # Render circle outline for better visibility
        if not picking_mode:
            current_color = glGetFloatv(GL_CURRENT_COLOR)
            glColor3f(0.1, 0.1, 0.1)  # Dark outline
            glLineWidth(2.0)

            glBegin(GL_LINE_LOOP)
            for i in range(num_segments):
                angle = 2.0 * math.pi * i / num_segments
                x = w0 * math.cos(angle)
                y = w0 * math.sin(angle)
                glVertex3f(x, y, z0)
            glEnd()

            # Restore original color for arrow
            glColor4fv(current_color)

            # Render polarization arrow
            arrow_length = 1.5 * w0

            # Normalize polarization vector (use only x,y components for 2D arrow)
            pol_x = polarization['x']
            pol_y = polarization['y']

            # Normalize to arrow length
            pol_magnitude = math.sqrt(pol_x * pol_x + pol_y * pol_y)
            pol_x = (pol_x / pol_magnitude) * arrow_length
            pol_y = (pol_y / pol_magnitude) * arrow_length

            # Set arrow color (contrasting with beam color)
            glColor3f(0.8, 0.2, 0.2)  # Red arrow
            glLineWidth(3.0)

            # Draw main arrow line
            glBegin(GL_LINES)
            glVertex3f(0, 0, z0 - 0.0001)  # Slightly above disk to avoid z-fighting
            glVertex3f(pol_x, pol_y, z0 - 0.0001)
            glEnd()

            # Draw arrowhead
            arrowhead_length = 0.2 * arrow_length
            arrowhead_angle = math.pi / 6  # 30 degrees

            # Calculate arrowhead direction (opposite to arrow direction)
            arrow_angle = math.atan2(pol_y, pol_x)

            # Arrowhead points
            head1_angle = arrow_angle + math.pi - arrowhead_angle
            head2_angle = arrow_angle + math.pi + arrowhead_angle

            head1_x = pol_x + arrowhead_length * math.cos(head1_angle)
            head1_y = pol_y + arrowhead_length * math.sin(head1_angle)

            head2_x = pol_x + arrowhead_length * math.cos(head2_angle)
            head2_y = pol_y + arrowhead_length * math.sin(head2_angle)

            glBegin(GL_LINES)
            # First arrowhead line
            glVertex3f(pol_x, pol_y, z0 - 0.0001)
            glVertex3f(head1_x, head1_y, z0 - 0.0001)

            # Second arrowhead line
            glVertex3f(pol_x, pol_y, z0 - 0.0001)
            glVertex3f(head2_x, head2_y, z0 - 0.0001)
            glEnd()

        # Restore OpenGL state
        if not picking_mode:
            glEnable(GL_LIGHTING)

    def render_horn(self, horn_data, picking_mode=False, selected_mode=False):
        """
        Render a Horn object as a pyramid structure
        Note: Base (aperture) center is always positioned at the origin (0,0,0)

        Args:
            horn_data: Dictionary containing horn parameters
            picking_mode: Boolean, if True render for object picking
            selected_mode: Boolean, if True render with selected colors
        """
        if horn_data is None:
            return

        if not picking_mode:
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_LIGHTING)

        # Extract horn parameters
        aperture_a = horn_data.get('a', 0.015)  # Aperture width
        aperture_b = horn_data.get('b', 0.015)  # Aperture height
        length = horn_data.get('length', 0.01)  # Horn length

        # Set colors
        if not picking_mode:
            if selected_mode:
                self.set_to_selected_color()
            else:
                if horn_data.get('enabled', True):
                    glColor3f(0.8, 0.6, 0.2)  # Golden color
                else:
                    glColor3f(0.5, 0.5, 0.5)  # Grey when disabled

        # Define pyramid
        half_a = aperture_a / 2
        half_b = aperture_b / 2

        # Base corners at z=0 (aperture)
        base_corners = [
            (-half_a, -half_b, 0),  # Bottom-left
            (half_a, -half_b, 0),  # Bottom-right
            (half_a, half_b, 0),  # Top-right
            (-half_a, half_b, 0)  # Top-left
        ]

        # Apex point at z=-length
        apex = (0, 0, -length)

        # Render pyramid faces
        glBegin(GL_TRIANGLES)

        # Base face (at z=0)
        glNormal3f(0, 0, 1)
        glVertex3f(*base_corners[0])
        glVertex3f(*base_corners[1])
        glVertex3f(*base_corners[2])

        glVertex3f(*base_corners[0])
        glVertex3f(*base_corners[2])
        glVertex3f(*base_corners[3])

        # Side faces (triangles from base edges to apex)
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(*base_corners[0])
        glVertex3f(*base_corners[1])
        glVertex3f(*apex)

        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(*base_corners[1])
        glVertex3f(*base_corners[2])
        glVertex3f(*apex)

        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(*base_corners[2])
        glVertex3f(*base_corners[3])
        glVertex3f(*apex)

        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(*base_corners[3])
        glVertex3f(*base_corners[0])
        glVertex3f(*apex)

        glEnd()

        # Draw edges for better visibility
        if not picking_mode:
            glColor3f(0.2, 0.2, 0.2)  # Dark edges
            glLineWidth(2.0)

            # Base edges
            glBegin(GL_LINE_LOOP)
            for corner in base_corners:
                glVertex3f(*corner)
            glEnd()

            # Edges from base to apex
            glBegin(GL_LINES)
            for corner in base_corners:
                glVertex3f(*corner)
                glVertex3f(*apex)
            glEnd()

        # Restore OpenGL state
        if not picking_mode:
            glEnable(GL_LIGHTING)

    def render_far_field(self, ff_request, picking_mode=False, selected_mode=False):
        """Render a Far Field Request object as a portion of circle (arc)"""
        if ff_request is None:
            return

        if not picking_mode:
            # Enable transparency
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            # Enable depth testing for 3D masking
            glEnable(GL_DEPTH_TEST)

            # Disable lighting to avoid shading
            glDisable(GL_LIGHTING)

            glEnable(GL_POLYGON_OFFSET_FILL)
            glPolygonOffset(1.0, 1.0)

            # Get parameters
        params = ff_request['parameters']
        phi = math.radians(params['phi'])  # Cut-plane angle (rotation around z-axis)
        theta_start = math.radians(params['theta_range'][0])  # Start angle
        theta_stop = math.radians(params['theta_range'][1])  # Stop angle
        theta_step = math.radians(params['theta_range'][2])  # Step angle

        # Arc radius for visualization (adjust as needed)
        radius = 0.1

        # Generate arc points
        theta_angles = np.arange(theta_start, theta_stop + theta_step, theta_step)
        arc_points = []

        # Calculate 3D points for the arc
        for theta in theta_angles:
            # Spherical to Cartesian conversion
            # theta is angle from z-axis (elevation)
            # phi is angle around z-axis (azimuth)
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            arc_points.append([x, y, z])

        # Add center point for creating triangular sectors
        center = [0, 0, 0]

        # Draw the arc as a series of triangular sectors
        if picking_mode:
            if len(arc_points) > 1:
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(*center)  # Center vertex
                for point in arc_points:
                    glVertex3f(*point)
                glEnd()

        # Draw the arc outline
        if not picking_mode:
            if selected_mode:
                self.set_to_selected_color()
            else:
                if ff_request.get('enabled', True):
                    glColor4f(0.3, 0.7, 0.3, 0.7)   # Darker red for lines
                else:
                    glColor4f(0.6, 0.6, 0.6, 0.7)  # Grey for lines

            glLineWidth(1.0)

            # Draw arc outline
            glBegin(GL_LINE_STRIP)
            for point in arc_points:
                glVertex3f(*point)
            glEnd()

            # Draw radial lines from center to arc endpoints
            glBegin(GL_LINES)
            # Line to start point
            glVertex3f(*center)
            glVertex3f(*arc_points[0])
            # Line to end point
            glVertex3f(*center)
            glVertex3f(*arc_points[-1])
            glEnd()

        # Optional: Draw theta angle indicators
        if not picking_mode and len(arc_points) > 1:
            glLineWidth(1.0)
            # Draw small tick marks at regular intervals
            for i, point in enumerate(arc_points[::max(1, len(arc_points) // theta_angles.shape[0])]):  # Show ~8 ticks max
                tick_inner = [p * 1 for p in point]
                tick_outer = [p * 1.02 for p in point]
                glBegin(GL_LINES)
                glVertex3f(*tick_inner)
                glVertex3f(*tick_outer)
                glEnd()

        # Restore OpenGL state
        if not picking_mode:
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glDisable(GL_POLYGON_OFFSET_FILL)

    def render_transform(self, obj):
        if obj is None:
            return

        """ Apply individual mesh position and rotation (Frame rotation matrix) """
        if 'position' in obj['parameters']:
            position = list(obj['parameters']['position'])
            rotation_deg = - array(obj['parameters'].get('rotation', [0, 0, 0]))

            reference_uuid = obj['parameters'].get('reference', None)
            if reference_uuid is not None:
                reference_pos = self.object_manager.get_object_pose(reference_uuid)[0]
                for i in range(3):
                    position[i] += reference_pos[i]

            glTranslatef(position[0], position[1], position[2])
            gl_matrix = np.eye(4)
            gl_matrix[:3, :3] = R.from_rotvec(rotation_deg, degrees=True).as_matrix()
            glMultMatrixf(gl_matrix.flatten())
        elif 'rot_z_deg' in obj['parameters']:
            rotation_deg = (0, 0, -obj['parameters'].get('rot_z_deg', 0))
            gl_matrix = np.eye(4)
            gl_matrix[:3, :3] = R.from_rotvec(rotation_deg, degrees=True).as_matrix()
            glMultMatrixf(gl_matrix.flatten())

    @staticmethod
    def draw_axes(length=0.1):
        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        glColor3f(0, .8, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        glEnable(GL_LIGHTING)
