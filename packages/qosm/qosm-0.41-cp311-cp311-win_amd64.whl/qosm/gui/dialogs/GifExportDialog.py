from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,QGridLayout, QGroupBox, QDialog,
                               QDialogButtonBox, QDoubleSpinBox, QCheckBox)


class GifExportDialog(QDialog):
    """Dialog for configuring GIF export options"""

    def __init__(self, use_db=False, db_min=-50.0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Animated GIF")
        self.setModal(True)
        self.resize(300, 280)

        layout = QVBoxLayout(self)

        # Display mode selection
        mode_group = QGroupBox("Display Mode")
        mode_layout = QVBoxLayout(mode_group)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['magnitude_all', 'magnitude_x', 'magnitude_y', 'magnitude_z',
                                  'phase_x', 'phase_y', 'phase_z'])
        mode_layout.addWidget(self.mode_combo)

        # dB options
        db_layout = QHBoxLayout()
        self.db_checkbox = QCheckBox("Use dB scale for magnitude")
        self.db_checkbox.setChecked(use_db)
        self.db_checkbox.toggled.connect(self.on_db_toggled)
        db_layout.addWidget(self.db_checkbox)

        db_layout.addWidget(QLabel("Min:"))
        self.db_min_spinbox = QDoubleSpinBox()
        self.db_min_spinbox.setRange(-200, 0)
        self.db_min_spinbox.setValue(db_min)
        self.db_min_spinbox.setSuffix(" dB")
        self.db_min_spinbox.setEnabled(use_db)
        db_layout.addWidget(self.db_min_spinbox)

        mode_layout.addLayout(db_layout)
        layout.addWidget(mode_group)

        # Timing settings
        timing_group = QGroupBox("Animation Settings")
        timing_layout = QGridLayout(timing_group)

        timing_layout.addWidget(QLabel("Duration per frame (seconds):"), 0, 0)
        self.duration_spinbox = QDoubleSpinBox()
        self.duration_spinbox.setRange(0.1, 10.0)
        self.duration_spinbox.setValue(0.5)
        self.duration_spinbox.setSingleStep(0.1)
        self.duration_spinbox.setDecimals(1)
        timing_layout.addWidget(self.duration_spinbox, 0, 1)

        timing_layout.addWidget(QLabel("DPI (resolution):"), 1, 0)
        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setRange(50, 300)
        self.dpi_spinbox.setValue(100)
        self.dpi_spinbox.setSingleStep(10)
        timing_layout.addWidget(self.dpi_spinbox, 1, 1)

        layout.addWidget(timing_group)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def on_db_toggled(self, checked):
        """Enable/disable dB minimum spinbox"""
        self.db_min_spinbox.setEnabled(checked)

    def get_settings(self):
        """Get the export settings"""
        return {
            'display_mode': self.mode_combo.currentText(),
            'duration_per_frame': self.duration_spinbox.value(),
            'dpi': self.dpi_spinbox.value(),
            'use_db': self.db_checkbox.isChecked(),
            'db_min': self.db_min_spinbox.value()
        }
