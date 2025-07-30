import pickle

import sys
from datetime import datetime

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTabWidget, QTextEdit,
                               QMessageBox, QFileDialog, QLabel)

from qosm.gui.dialogs import StepMeshEdit, ShapeMeshEdit
from qosm.gui.dialogs.GBEGridCreateDialog import GBEGridEdit
from qosm.gui.tabs import ConstructionTab, RequestsTab, ParametersTab
from qosm.gui.view import GLViewer
from qosm.gui.managers import ObjectManager, RequestManager, SourceManager


class ConsoleWidget(QTextEdit):
    """Log console widget"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup console UI"""
        self.setMaximumHeight(150)
        self.setMinimumHeight(100)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
                border: 1px solid #555555;
            }
        """)

    def log_message(self, message, type: str = 'log'):
        """Add message to log console"""
        color = {'log': '#aaa', 'error': '#ff4444', 'warning': '#ffcc66', 'success': '#66ee66'}
        style = {'log': 'normal', 'error': 'bold', 'warning': 'normal', 'success': 'normal'}
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f'<span style="color:{color[type]}; font-weight:{style[type]}" class="log_{type}">' + \
                            f'[{timestamp}] {message}</span>'
        self.append(formatted_message)
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class SidebarTabs(QTabWidget):
    """Sidebar tabs widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.construction_tab = None
        self.requests_tab = None
        self.information_tab = None
        self.setup_ui()

    def setup_ui(self):
        """Setup sidebar tabs"""
        self.setMaximumWidth(255)

        # Construction tab
        self.construction_tab = ConstructionTab(self.parent_window)
        self.addTab(self.construction_tab, "Construction")

        # Requests tab
        self.requests_tab = RequestsTab(self.parent_window)
        self.addTab(self.requests_tab, "Requests")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QOSM - GUI")

        # Initialize variables
        self.viewer = None
        self.console = None
        self.tabs = None
        self.view_controls = None
        self.parameters_tab = None

        # Sources management
        self.source_manager = SourceManager()

        # objects management
        self.object_manager = ObjectManager()

        # Requests management
        self.request_manager = RequestManager()

        # Create interface
        self.setup_ui()

    def setup_ui(self):
        """User interface setup"""

        # Create main horizontal layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Viewer section (center) with view controls and console
        viewer_section = QWidget()
        viewer_layout = QVBoxLayout()
        viewer_section.setLayout(viewer_layout)

        # Viewer in the middle
        self.viewer = GLViewer(src_manager=self.source_manager, obj_manager=self.object_manager,
                               req_manager=self.request_manager)
        viewer_layout.addWidget(self.viewer)

        # Console at the bottom
        self.console = ConsoleWidget()
        viewer_layout.addWidget(self.console)

        # Create tabs on the left (full height)
        self.tabs = SidebarTabs(self)

        self.parameters_tab = ParametersTab(self)
        self.tabs.construction_tab.connect_parameters(self.parameters_tab)
        self.tabs.requests_tab.connect_parameters(self.parameters_tab)

        # Menu bar
        self.create_menu_bar()

        main_layout.addWidget(self.tabs, 1)
        main_layout.addWidget(viewer_section, 2)
        main_layout.addWidget(self.parameters_tab, 3)

        # Connect callbacks after creating viewer
        self.connect_callbacks()

        # Welcome messages
        self.log_message("=== QOSM - GUI ===")

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        new_action = file_menu.addAction('New Project')
        new_action.triggered.connect(self.new)
        new_action.setShortcut('Ctrl+N')
        open_action = file_menu.addAction('Open Project')
        open_action.triggered.connect(self.open)
        open_action.setShortcut('Ctrl+O')
        save_action = file_menu.addAction('Save Project')
        save_action.triggered.connect(self.save)
        save_action.setShortcut('Ctrl+S')
        quit_action = file_menu.addAction('Exit')
        quit_action.setShortcut('Ctrl+Q')
        # @todo confirmation before, and propose to save !
        quit_action.triggered.connect(self.close)

        # Construction menu
        build_menu = menubar.addMenu('Construction')
        import_step_action = build_menu.addAction('Import STEP')
        import_step_action.setShortcut('Ctrl+I')
        import_step_action.triggered.connect(self.tabs.construction_tab.import_step_file)
        shape_action = build_menu.addAction('Create Shape')
        shape_action.setShortcut('Ctrl+Shift+S')
        shape_action.triggered.connect(self.tabs.construction_tab.create_shape)
        build_menu.addSeparator()

        grid_action = build_menu.addAction('Create GBE Grid')
        grid_action.setShortcut('Ctrl+G')
        grid_action.triggered.connect(self.tabs.construction_tab.create_gbe_grid)

        domain_action = build_menu.addAction('Create GBT Domain')
        domain_action.setShortcut('Ctrl+D')
        domain_action.triggered.connect(self.tabs.construction_tab.create_domain)
        build_menu.addSeparator()

        # Sources menu
        sources_menu = menubar.addMenu('Sources')
        feko_action = sources_menu.addAction('Near Field')
        feko_action.setShortcut('Ctrl+F')
        feko_action.setStatusTip('Create a near field source')
        feko_action.triggered.connect(self.tabs.construction_tab.create_nf_source)

        vsrc_action = sources_menu.addAction('Gaussian Beam')
        vsrc_action.setShortcut('Ctrl+B')
        vsrc_action.setStatusTip('Create a Gaussian beam source')
        vsrc_action.triggered.connect(self.tabs.construction_tab.create_gaussian_beam_source)

        horn_action = sources_menu.addAction('Horn')
        horn_action.setShortcut('Ctrl+H')
        horn_action.setStatusTip('Create a Horn')
        horn_action.triggered.connect(self.tabs.construction_tab.create_horn_source)

        # Request menu
        requests_menu = menubar.addMenu('Requests')
        nf_action = requests_menu.addAction('Near Fields')
        nf_action.triggered.connect(self.tabs.requests_tab.create_near_field_request)
        nf_action.setShortcut('Ctrl+Shift+F')
        nf_action.setStatusTip('Add a Near Fields request associated to a domain')
        nf_action = requests_menu.addAction('Far Fields')
        nf_action.triggered.connect(self.tabs.requests_tab.create_far_field_request)
        nf_action.setShortcut('Ctrl+Alt+F')
        nf_action.setStatusTip('Add a Far Fields request associated to a horn')
        requests_menu.addSeparator()

        pipe_action = requests_menu.addAction('Build pipeline and simulate ')
        pipe_action.setShortcut(QKeySequence("Ctrl+Return"))
        pipe_action.setStatusTip('Build simulation pipeline and run it')
        pipe_action.triggered.connect(self.tabs.requests_tab.build)
        results_action = requests_menu.addAction('Display results')
        results_action.triggered.connect(lambda: self.tabs.requests_tab.display_results(None))
        results_action.setShortcut('Ctrl+R')
        results_action.setStatusTip('Display the simulated requests ')

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        delete_action = edit_menu.addAction('Delete Selected Object')
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.delete_item)
        rename_action = edit_menu.addAction('Rename Selected Object')
        rename_action.setShortcut('F2')
        rename_action.triggered.connect(self.rename_item)

        # View menu
        view_menu = menubar.addMenu('View')
        fit_all_action = view_menu.addAction('Fit All objects')
        fit_all_action.setShortcut('F')
        fit_all_action.triggered.connect(self.viewer.fit_all_objects)
        view_menu.addSeparator()
        xy_view_action = view_menu.addAction('XY View (Front)')
        xy_view_action.setShortcut('1')
        xy_view_action.triggered.connect(self.viewer.set_view_xy)
        xz_view_action = view_menu.addAction('XZ View (Side)')
        xz_view_action.setShortcut('2')
        xz_view_action.triggered.connect(self.viewer.set_view_xz)
        yz_view_action = view_menu.addAction('YZ View (Top)')
        yz_view_action.setShortcut('3')
        yz_view_action.triggered.connect(self.viewer.set_view_yz)
        proj_toogle_view_action = view_menu.addAction('Perspective / Orthogonal View')
        proj_toogle_view_action.setShortcut('5')
        proj_toogle_view_action.triggered.connect(self.viewer.toggle_projection)

    def log_message(self, message, type: str = 'log'):
        """Add message to log console"""
        if self.console:
            self.console.log_message(message, type)

    def connect_callbacks(self):
        """Connect callbacks after viewer creation"""
        if self.viewer:
            self.tabs.construction_tab.selection_callback = self.update_gui
            self.tabs.requests_tab.selection_callback = self.update_gui
            self.viewer.selection_callback = self.update_gui
            self.viewer.log_callback = self.log_message

    def update_gui(self, item_uuid: str | None):
        if self.object_manager.exists(item_uuid):
            self.request_manager.set_active_request(None)
            self.tabs.setCurrentIndex(0)
        elif self.request_manager.exists(item_uuid):
            self.object_manager.set_active_object(None)
            self.tabs.setCurrentIndex(1)

        self.tabs.construction_tab.update_lists(update_params=False)
        self.tabs.requests_tab.update_lists(update_params=False)
        self.parameters_tab.display_parameters()

        self.viewer.update()

    def rename_item(self):
        if self.object_manager.exists(None):
            self.tabs.construction_tab.rename_object(None)
        elif self.request_manager.exists(None):
            self.tabs.requests_tab.rename_request(None)

    def delete_item(self,):
        if self.object_manager.exists(None):
            self.tabs.construction_tab.delete_object(None)
        elif self.request_manager.exists(None):
            self.tabs.requests_tab.delete_request(None)

    def reconnect_managers(self):
        # Construction tab
        self.tabs.construction_tab.object_manager = self.object_manager
        self.tabs.construction_tab.source_manager = self.source_manager
        # Request tab
        self.tabs.requests_tab.object_manager = self.object_manager
        self.tabs.requests_tab.request_manager = self.request_manager
        self.tabs.requests_tab.source_manager = self.source_manager
        # Parameters tab
        self.parameters_tab.object_manager = self.object_manager
        self.parameters_tab.request_manager = self.request_manager
        self.parameters_tab.source_manager = self.source_manager
        # 3D Viewer
        self.viewer.object_manager = self.object_manager
        self.viewer.source_manager = self.source_manager
        self.viewer.request_manager = self.request_manager

        self.update_gui(None)

    def new(self):

        reply = QMessageBox.question(
            self, "Create a new project ?",
            "Are you sure to discard any modification and create a new project ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.object_manager = ObjectManager()
            self.source_manager = SourceManager()
            self.request_manager = RequestManager()
            self.reconnect_managers()

    def save(self):
        """Save objects and sources to a binary .qosm file"""
        # Open file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QOSM File",
            "",
            "QOSM files (*.qosm);;All files (*.*)"
        )
        try:

            if file_path:
                # Add .qosm extension if not present
                if not file_path.endswith('.qosm'):
                    file_path += '.qosm'

                # Prepare data to save
                data = {
                    'object_manager': self.object_manager,
                    'source_manager': self.source_manager,
                    'request_manager': self.request_manager,
                }

                # @todo save the pipeline

                # Save to binary file using dill
                with open(file_path, 'wb') as file:
                    pickle.dump(data, file)

                self.log_message(f"File saved successfully to {file_path}", type='success')
                QMessageBox.information(self, "Success", f"File saved successfully to {file_path}")

        except Exception as e:
            self.log_message(f"Failed to save file: {file_path}", type='success')
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def open(self):
        """Load objects and sources from a binary .qosm file"""
        # Open file dialog to choose file to load
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open QOSM File",
            "",
            "QOSM files (*.qosm);;All files (*.*)"
        )
        try:
            if file_path:
                # Load data from binary file
                with open(file_path, 'rb') as file:
                    data = pickle.load(file)
                # Restore objects and sources
                self.object_manager = data.get('object_manager', ObjectManager())
                self.source_manager = data.get('source_manager', SourceManager())
                self.request_manager = data.get('request_manager', RequestManager())

                self.reconnect_managers()

                self.log_message(f"File loaded successfully from {file_path}", type='success')

        except Exception as e:
            self.log_message(f"Failed to load file: {file_path}", type='error')
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")


def gui():
    app = QApplication()
    window = MainWindow()
    window.resize(1200, 800)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    gui()
