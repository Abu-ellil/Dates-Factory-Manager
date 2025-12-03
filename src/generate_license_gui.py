"""
License Key Generator GUI for Date Factory Manager
Use this application to generate valid license keys for clients
"""
import sys
import os
from datetime import datetime, timedelta

# Add the src directory to Python path so we can import license_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import license_manager
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                          QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit,
                          QMessageBox, QDateEdit, QRadioButton, QButtonGroup, QGroupBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class LicenseGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Date Factory Manager - License Key Generator")
        self.setGeometry(100, 100, 600, 500)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Title
        title_label = QLabel("License Key Generator")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Machine ID section
        machine_id_group = QGroupBox("Machine Information")
        machine_id_layout = QVBoxLayout()

        self.machine_id_label = QLabel()
        self.machine_id_label.setFont(QFont("Arial", 10))
        machine_id_layout.addWidget(self.machine_id_label)

        # Add manual machine ID input
        manual_id_layout = QHBoxLayout()
        manual_id_layout.addWidget(QLabel("Or enter custom Machine ID:"))
        self.custom_machine_id_input = QLineEdit()
        self.custom_machine_id_input.setPlaceholderText("Enter machine ID for other computers")
        manual_id_layout.addWidget(self.custom_machine_id_input)
        machine_id_layout.addLayout(manual_id_layout)

        refresh_btn = QPushButton("Refresh Machine ID")
        refresh_btn.clicked.connect(self.refresh_machine_id)
        machine_id_layout.addWidget(refresh_btn)

        machine_id_group.setLayout(machine_id_layout)
        layout.addWidget(machine_id_group)

        # Client information section
        client_group = QGroupBox("Client Information")
        client_layout = QVBoxLayout()

        client_name_layout = QHBoxLayout()
        client_name_layout.addWidget(QLabel("Client Name:"))
        self.client_name_input = QLineEdit("User")
        client_name_layout.addWidget(self.client_name_input)
        client_layout.addLayout(client_name_layout)

        client_group.setLayout(client_layout)
        layout.addWidget(client_group)

        # Expiration options section
        expiration_group = QGroupBox("Expiration Options")
        expiration_layout = QVBoxLayout()

        # Radio buttons for expiration options
        self.expiration_options = QButtonGroup()

        self.lifetime_radio = QRadioButton("Lifetime (no expiration)")
        self.lifetime_radio.setChecked(True)
        self.expiration_options.addButton(self.lifetime_radio)

        self.one_month_radio = QRadioButton("1 month")
        self.expiration_options.addButton(self.one_month_radio)

        self.six_months_radio = QRadioButton("6 months")
        self.expiration_options.addButton(self.six_months_radio)

        self.one_year_radio = QRadioButton("1 year")
        self.expiration_options.addButton(self.one_year_radio)

        self.custom_radio = QRadioButton("Custom date:")
        self.expiration_options.addButton(self.custom_radio)

        # Custom date picker
        self.custom_date_picker = QDateEdit()
        self.custom_date_picker.setDate(QDate.currentDate().addDays(30))
        self.custom_date_picker.setEnabled(False)
        self.custom_date_picker.setCalendarPopup(True)

        # Add radio buttons to layout
        expiration_layout.addWidget(self.lifetime_radio)
        expiration_layout.addWidget(self.one_month_radio)
        expiration_layout.addWidget(self.six_months_radio)
        expiration_layout.addWidget(self.one_year_radio)

        custom_layout = QHBoxLayout()
        custom_layout.addWidget(self.custom_radio)
        custom_layout.addWidget(self.custom_date_picker)
        expiration_layout.addLayout(custom_layout)

        # Connect custom radio button
        self.custom_radio.toggled.connect(self.custom_date_picker.setEnabled)

        expiration_group.setLayout(expiration_layout)
        layout.addWidget(expiration_group)

        # Generate button
        generate_btn = QPushButton("Generate License Key")
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        generate_btn.clicked.connect(self.generate_license)
        layout.addWidget(generate_btn)

        # Results section
        results_group = QGroupBox("Generated License")
        results_layout = QVBoxLayout()

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Courier New", 10))

        results_layout.addWidget(self.results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Save button
        save_btn = QPushButton("Save License Key")
        save_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        save_btn.clicked.connect(self.save_license)
        save_btn.setEnabled(False)
        self.save_btn = save_btn
        layout.addWidget(save_btn)

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Initialize machine ID
        self.refresh_machine_id()

    def refresh_machine_id(self):
        try:
            machine_id = license_manager.get_machine_id()
            self.machine_id_label.setText(f"Machine ID: {machine_id}")
            self.status_bar.showMessage("Machine ID refreshed successfully")
        except Exception as e:
            self.machine_id_label.setText(f"Error getting machine ID: {str(e)}")
            self.status_bar.showMessage(f"Error: {str(e)}")

    def get_expiration_date(self):
        if self.lifetime_radio.isChecked():
            return None
        elif self.one_month_radio.isChecked():
            return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        elif self.six_months_radio.isChecked():
            return (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")
        elif self.one_year_radio.isChecked():
            return (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        elif self.custom_radio.isChecked():
            return self.custom_date_picker.date().toString("yyyy-MM-dd")
        return None

    def generate_license(self):
        try:
            # Get machine ID - use custom if provided, otherwise use current machine
            custom_machine_id = self.custom_machine_id_input.text().strip()
            if custom_machine_id:
                machine_id = custom_machine_id
                self.status_bar.showMessage(f"Using custom Machine ID: {machine_id}")
            else:
                machine_id = license_manager.get_machine_id()
                self.status_bar.showMessage(f"Using current Machine ID: {machine_id}")

            # Get client name
            client_name = self.client_name_input.text().strip() or "User"

            # Get expiration date
            expiration_date = self.get_expiration_date()

            self.status_bar.showMessage("Generating license key...")

            # Generate license key
            license_key = license_manager.generate_license_key(
                machine_id=machine_id,
                client_name=client_name,
                expiration_date=expiration_date
            )

            # Display results
            result_text = f"Machine ID: {machine_id}\n"
            result_text += f"Client Name: {client_name}\n"
            result_text += f"Expiration: {expiration_date if expiration_date else 'Lifetime'}\n\n"
            result_text += "LICENSE KEY:\n"
            result_text += "=" * 60 + "\n"
            result_text += license_key + "\n"
            result_text += "=" * 60

            self.results_text.setText(result_text)
            self.save_btn.setEnabled(True)

            # Verify the key
            is_valid, message = license_manager.verify_license_key(license_key, machine_id)

            if is_valid:
                self.status_bar.showMessage("✓ License key is VALID")
            else:
                self.status_bar.showMessage(f"✗ License key verification failed: {message}")

        except Exception as e:
            self.status_bar.showMessage(f"Error generating license: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to generate license:\n\n{str(e)}")

    def save_license(self):
        license_key = self.results_text.toPlainText()

        # Extract just the key (between the = lines)
        lines = license_key.split('\n')
        key_line = None
        for line in lines:
            if len(line.strip()) > 20 and not line.startswith('='):
                key_line = line.strip()
                break

        if key_line:
            try:
                license_manager.save_license(key_line)
                self.status_bar.showMessage("✓ License key saved successfully!")
                QMessageBox.information(self, "Success", "License key saved successfully!")
            except Exception as e:
                self.status_bar.showMessage(f"Error saving license: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to save license:\n\n{str(e)}")
        else:
            self.status_bar.showMessage("Could not extract license key")
            QMessageBox.warning(self, "Warning", "Could not extract license key from results")

def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    window = LicenseGeneratorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
