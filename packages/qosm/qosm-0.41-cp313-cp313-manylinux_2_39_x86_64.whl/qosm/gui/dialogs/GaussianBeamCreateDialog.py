from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox,
                               QMessageBox, QComboBox, QFormLayout)
from PySide6.QtGui import QDoubleValidator


class GaussianBeamCreateDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        if data is None:
            self.setWindowTitle("Create Gaussian Beam")
        else:
            self.setWindowTitle("Edit Gaussian Beam")
        self.setModal(True)
        self.resize(450, 400)

        self.data = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create main form
        self.create_form()

        # OK/Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)

        # Connect validation signals
        self.connect_validation_signals()

        if data:
            self.fill_form(data)

    def fill_form(self, data):
        self.source_name_edit.setText(data['source_name'])
        self.w0_edit.setText(f"{data['w0']: .4f}")
        self.z0_edit.setText(f"{data['z0']: .4f}")
        self.freq_edit.setText(f"{data['frequency_GHz']: .2f}")

        if data['polarization'] == 'X':
            self.pol_combo.setCurrentIndex(0)
        elif data['polarization'] == 'Y':
            self.pol_combo.setCurrentIndex(1)
        else:
            self.pol_combo.setCurrentIndex(2)

        self.pol_x_edit.setText(f"{data['polarization']['x']: .4f}")
        self.pol_y_edit.setText(f"{data['polarization']['y']: .4f}")

    def create_form(self):
        """Create the parameter input form"""
        # Source name at the top
        source_group = QGroupBox("Source Information")
        source_layout = QFormLayout()

        self.source_name_edit = QLineEdit()
        self.source_name_edit.setPlaceholderText("e.g., GaussianBeam1")
        source_layout.addRow("Source name:", self.source_name_edit)

        source_group.setLayout(source_layout)
        self.layout().addWidget(source_group)

        # GroupBox for beam parameters
        beam_group = QGroupBox("Gaussian Beam Parameters")
        beam_layout = QFormLayout()

        # w0 - Waist radius (in mm)
        self.w0_edit = QLineEdit()
        self.w0_edit.setPlaceholderText("e.g., 10.0")
        validator_w0 = QDoubleValidator(0.001, 1000.0, 3)
        validator_w0.setNotation(QDoubleValidator.StandardNotation)
        self.w0_edit.setValidator(validator_w0)
        beam_layout.addRow("Waist radius w0 [mm]:", self.w0_edit)

        # Frequency [GHz]
        self.freq_edit = QLineEdit()
        self.freq_edit.setPlaceholderText("e.g., 2.4")
        validator_freq = QDoubleValidator(0.001, 1000.0, 3)
        validator_freq.setNotation(QDoubleValidator.StandardNotation)
        self.freq_edit.setValidator(validator_freq)
        beam_layout.addRow("Frequency [GHz]:", self.freq_edit)

        # z0 - Waist position offset [mm]
        self.z0_edit = QLineEdit()
        self.z0_edit.setPlaceholderText("e.g., 0.0")
        self.z0_edit.setText("0.0")  # Default value
        validator_z0 = QDoubleValidator(-10.0, 10.0, 3)
        validator_z0.setNotation(QDoubleValidator.StandardNotation)
        self.z0_edit.setValidator(validator_z0)
        beam_layout.addRow("Waist position offset z0 [mm]:", self.z0_edit)

        beam_group.setLayout(beam_layout)
        self.layout().addWidget(beam_group)

        # GroupBox for polarization
        pol_group = QGroupBox("Polarization")
        pol_layout = QVBoxLayout()

        # ComboBox for polarization type
        pol_type_layout = QHBoxLayout()
        pol_type_layout.addWidget(QLabel("Polarization type:"))
        self.pol_combo = QComboBox()
        self.pol_combo.addItems(["X", "Y", "Custom"])
        self.pol_combo.currentTextChanged.connect(self.on_polarization_changed)
        pol_type_layout.addWidget(self.pol_combo)
        pol_type_layout.addStretch()
        pol_layout.addLayout(pol_type_layout)

        # Custom polarization inputs (initially hidden)
        self.custom_pol_widget = QGroupBox("Custom Polarization Components")
        custom_pol_layout = QFormLayout()

        # X component
        self.pol_x_edit = QLineEdit()
        self.pol_x_edit.setPlaceholderText("e.g., 1.0")
        self.pol_x_edit.setText("1.0")
        validator_pol_x = QDoubleValidator(-1000.0, 1000.0, 6)
        validator_pol_x.setNotation(QDoubleValidator.StandardNotation)
        self.pol_x_edit.setValidator(validator_pol_x)
        custom_pol_layout.addRow("X component:", self.pol_x_edit)

        # Y component
        self.pol_y_edit = QLineEdit()
        self.pol_y_edit.setPlaceholderText("e.g., 0.0")
        self.pol_y_edit.setText("0.0")
        validator_pol_y = QDoubleValidator(-1000.0, 1000.0, 6)
        validator_pol_y.setNotation(QDoubleValidator.StandardNotation)
        self.pol_y_edit.setValidator(validator_pol_y)
        custom_pol_layout.addRow("Y component:", self.pol_y_edit)

        self.custom_pol_widget.setLayout(custom_pol_layout)
        self.custom_pol_widget.setVisible(False)  # Initially hidden
        pol_layout.addWidget(self.custom_pol_widget)

        pol_group.setLayout(pol_layout)
        self.layout().addWidget(pol_group)

    def on_polarization_changed(self, text):
        """Handle polarization type change"""
        if text == "Custom":
            self.custom_pol_widget.setVisible(True)
        else:
            self.custom_pol_widget.setVisible(False)
        self.validate_form()

    def connect_validation_signals(self):
        """Connect signals for form validation"""
        self.w0_edit.textChanged.connect(self.validate_form)
        self.freq_edit.textChanged.connect(self.validate_form)
        self.z0_edit.textChanged.connect(self.validate_form)
        self.source_name_edit.textChanged.connect(self.validate_form)
        self.pol_x_edit.textChanged.connect(self.validate_form)
        self.pol_y_edit.textChanged.connect(self.validate_form)
        self.pol_combo.currentTextChanged.connect(self.validate_form)

    def validate_form(self):
        """Validate form inputs and enable/disable OK button"""
        # Check required fields
        w0_valid = bool(self.w0_edit.text().strip())
        freq_valid = bool(self.freq_edit.text().strip())
        z0_valid = bool(self.z0_edit.text().strip())

        # Check custom polarization if selected
        pol_valid = True
        if self.pol_combo.currentText() == "Custom":
            pol_x_valid = bool(self.pol_x_edit.text().strip())
            pol_y_valid = bool(self.pol_y_edit.text().strip())
            pol_valid = pol_x_valid and pol_y_valid

            # Check that at least one component is non-zero
            if pol_valid:
                try:
                    x_val = float(self.pol_x_edit.text())
                    y_val = float(self.pol_y_edit.text())
                    pol_valid = (x_val != 0.0 or y_val != 0.0)
                except ValueError:
                    pol_valid = False

        # Enable OK button if all validations pass
        self.ok_button.setEnabled(w0_valid and freq_valid and z0_valid and pol_valid)

    def accept(self):
        """Override accept to collect form data"""
        try:
            # Get polarization data
            pol_type = self.pol_combo.currentText()
            if pol_type == "X":
                polarization = {"type": "X", "x": 1.0, "y": 0.0}
            elif pol_type == "Y":
                polarization = {"type": "Y", "x": 0.0, "y": 1.0}
            else:  # Custom
                polarization = {
                    "type": "Custom",
                    "x": float(self.pol_x_edit.text()),
                    "y": float(self.pol_y_edit.text())
                }

            # Collect all data
            self.data = {
                "w0": float(self.w0_edit.text()),
                "frequency_GHz": float(self.freq_edit.text()),
                "z0": float(self.z0_edit.text()),
                "source_name": self.source_name_edit.text().strip(),
                "polarization": polarization
            }

            super().accept()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input",
                                f"Please check your input values:\n{str(e)}")

    def get_data(self):
        """Return form data"""
        if not self.data:
            return None
        return self.data