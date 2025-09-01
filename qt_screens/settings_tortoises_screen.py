"""
Tortoise Management Screen - Add, edit, and manage tortoise profiles
"""

import os
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QDateEdit, QTextEdit, QCheckBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class AddTortoiseDialog(QDialog):
    """Dialog for adding new tortoises"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Tortoise')
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name field (required)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter tortoise name')
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow('Name *:', self.name_input)
        
        # Species field
        self.species_input = QLineEdit()
        self.species_input.setText("Hermann's Tortoise")
        self.species_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addRow('Species:', self.species_input)
        
        # Subspecies field
        self.subspecies_combo = QComboBox()
        self.subspecies_combo.addItems([
            'Unknown',
            'T. h. hermanni (Western)',
            'T. h. boettgeri (Eastern)',
            'Other'
        ])
        self.subspecies_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        form_layout.addRow('Subspecies:', self.subspecies_combo)
        
        # Sex field
        self.sex_combo = QComboBox()
        self.sex_combo.addItems(['Unknown', 'Male', 'Female'])
        self.sex_combo.setStyleSheet(self.subspecies_combo.styleSheet())
        form_layout.addRow('Sex:', self.sex_combo)
        
        # Birth date
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDate(QDate.currentDate().addYears(-5))
        self.birth_date.setStyleSheet("""
            QDateEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        form_layout.addRow('Birth Date:', self.birth_date)
        
        # Unknown birthdate checkbox
        self.unknown_birthdate_checkbox = QCheckBox('Birth date unknown - use acquisition date instead')
        self.unknown_birthdate_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #666;
                margin: 5px 0;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.unknown_birthdate_checkbox.stateChanged.connect(self.toggle_birthdate_handling)
        form_layout.addRow('', self.unknown_birthdate_checkbox)
        
        # Acquisition date
        self.acquisition_date = QDateEdit()
        self.acquisition_date.setCalendarPopup(True)
        self.acquisition_date.setDate(QDate.currentDate())
        self.acquisition_date.setStyleSheet(self.birth_date.styleSheet())
        form_layout.addRow('Acquisition Date:', self.acquisition_date)
        
        # Current weight
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText('Weight in grams (e.g. 450)')
        self.weight_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addRow('Current Weight (g):', self.weight_input)
        
        # Physical description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Physical description (shell patterns, scars, unique markings, size, etc.)')
        self.description_input.setMaximumHeight(80)
        self.description_input.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow('Physical Description:', self.description_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText('Additional notes, health information, etc.')
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow('Notes:', self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                min-width: 80px;
            }
            QDialogButtonBox QPushButton[text="OK"] {
                background-color: #4CAF50;
                color: white;
            }
            QDialogButtonBox QPushButton[text="OK"]:hover {
                background-color: #45a049;
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background-color: #757575;
                color: white;
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background-color: #616161;
            }
        """)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def toggle_birthdate_handling(self, state):
        """Toggle between using birthdate or acquisition date"""
        print(f"Checkbox state changed to: {state}")  # Debug
        if state == 2:  # Qt.CheckState.Checked = 2
            print("Checkbox is checked - syncing dates")  # Debug
            # When checked, disable birth date editing and sync with acquisition date
            self.birth_date.setEnabled(False)
            self.birth_date.setDate(self.acquisition_date.date())
            self.birth_date.setStyleSheet("""
                QDateEdit {
                    font-size: 14px;
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                    color: #777;
                }
            """)
            # Connect acquisition date changes to update birth date
            self.acquisition_date.dateChanged.connect(self.sync_birthdate_with_acquisition)
        else:
            print("Checkbox is unchecked - enabling birth date")  # Debug
            # When unchecked, re-enable birth date editing
            self.birth_date.setEnabled(True)
            self.birth_date.setStyleSheet("""
                QDateEdit {
                    font-size: 14px;
                    padding: 8px;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                }
            """)
            # Disconnect the sync connection
            try:
                self.acquisition_date.dateChanged.disconnect(self.sync_birthdate_with_acquisition)
            except TypeError:
                pass  # Connection may not exist
    
    def sync_birthdate_with_acquisition(self, date):
        """Sync birth date with acquisition date when checkbox is checked"""
        if self.unknown_birthdate_checkbox.isChecked():
            self.birth_date.setDate(date)
        
    def get_tortoise_data(self):
        """Get tortoise data from form"""
        name = self.name_input.text().strip()
        species = self.species_input.text().strip()
        subspecies = self.subspecies_combo.currentText()
        sex = self.sex_combo.currentText()
        birth_date = self.birth_date.date().toString(Qt.ISODate)
        acquisition_date = self.acquisition_date.date().toString(Qt.ISODate)
        physical_description = self.description_input.toPlainText().strip()
        notes = self.notes_input.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a tortoise name.')
            return None
        
        # Parse weight
        current_weight = None
        weight_text = self.weight_input.text().strip()
        if weight_text:
            try:
                current_weight = float(weight_text)
            except ValueError:
                QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid weight (numbers only).')
                return None
                
        return {
            'name': name,
            'species': species,
            'subspecies': subspecies if subspecies != 'Unknown' else None,
            'sex': sex if sex != 'Unknown' else None,
            'birth_date': birth_date,
            'acquisition_date': acquisition_date,
            'current_weight': current_weight,
            'physical_description': physical_description,
            'notes': notes
        }

class SettingsTortoisesScreen(BaseScreen):
    """Tortoise Management Screen"""
    
    def build_ui(self):
        """Build tortoise management UI"""
        # Header
        header = self.create_header('🐢 Tortoise Management', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        # Add tortoise button
        add_tortoise_btn = create_icon_button('plus', 'Add New Tortoise', (24, 24), self.add_tortoise)
        add_tortoise_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """)
        add_tortoise_btn.setMinimumHeight(50)
        action_layout.addWidget(add_tortoise_btn)
        
        
        self.main_layout.addLayout(action_layout)
        
        # Tortoises list area
        self.create_tortoises_list_area()
        
        # Load tortoises
        self.refresh_tortoises()
        
    def create_tortoises_list_area(self):
        """Create scrollable tortoises list area"""
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
        # Container widget for tortoises
        self.tortoises_container = QWidget()
        self.tortoises_layout = QVBoxLayout(self.tortoises_container)
        self.tortoises_layout.setSpacing(10)
        self.tortoises_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.tortoises_container)
        self.main_layout.addWidget(self.scroll_area)
        
    def refresh_tortoises(self):
        """Refresh the tortoises list"""
        # Clear existing tortoises
        for i in reversed(range(self.tortoises_layout.count())):
            child = self.tortoises_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get tortoises from database
        try:
            tortoises = self.db_manager.get_tortoises()
            
            if not tortoises:
                # No tortoises message
                no_tortoises_label = QLabel('No tortoises found. Click "Add New Tortoise" to get started.')
                no_tortoises_label.setAlignment(Qt.AlignCenter)
                no_tortoises_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #666;
                        padding: 40px;
                        background-color: #f5f5f5;
                        border-radius: 8px;
                        border: 2px dashed #ccc;
                    }
                """)
                self.tortoises_layout.addWidget(no_tortoises_label)
            else:
                # Display tortoises
                for tortoise in tortoises:
                    tortoise_widget = self.create_tortoise_widget(tortoise)
                    self.tortoises_layout.addWidget(tortoise_widget)
                    
        except Exception as e:
            error_label = QLabel(f'Error loading tortoises: {str(e)}')
            error_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    background-color: #ffebee;
                    border-radius: 5px;
                }
            """)
            self.tortoises_layout.addWidget(error_label)
        
        # Add stretch to push content to top
        self.tortoises_layout.addStretch()
        
    def create_tortoise_widget(self, tortoise):
        """Create a widget for displaying tortoise information"""
        tortoise_widget = QWidget()
        tortoise_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        # Make each entry optimal for 7-inch landscape display (1280x720) for critical photo identification
        tortoise_widget.setMinimumHeight(420)  # Increased height for larger photos for better identification
        
        layout = QHBoxLayout(tortoise_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Photo section - rounded corners for both photos and placeholders
        photo_label = QLabel()
        photo_label.setFixedSize(400, 400)  # Even larger for better tortoise identification
        photo_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
            }
        """)
        photo_label.setAlignment(Qt.AlignCenter)
        
        # Load photo if available
        if tortoise.get('photo_path') and os.path.exists(tortoise['photo_path']):
            try:
                pixmap = QPixmap(tortoise['photo_path'])
                if not pixmap.isNull():
                    # Create a rounded version of the photo
                    rounded_pixmap = self.create_rounded_pixmap(pixmap, 400, 400, 25)
                    photo_label.setPixmap(rounded_pixmap)
                else:
                    photo_label.setText('📷\n\nNo Photo\nAvailable')
                    photo_label.setStyleSheet("""
                        QLabel {
                            border-radius: 15px;
                            background-color: #f5f5f5;
                            color: #666;
                            font-size: 24px;
                            font-weight: bold;
                            border: 2px solid #ddd;
                        }
                    """)
            except Exception as e:
                print(f"Error loading photo: {e}")
                photo_label.setText('📷\n\nPhoto\nError')
                photo_label.setStyleSheet("""
                    QLabel {
                        border-radius: 15px;
                        background-color: #ffe6e6;
                        color: #d32f2f;
                        font-size: 24px;
                        font-weight: bold;
                        border: 2px solid #f44336;
                    }
                """)
        else:
            photo_label.setText('📷\n\nNo Photo\nAvailable')
            photo_label.setStyleSheet("""
                QLabel {
                    border-radius: 15px;
                    background-color: #f5f5f5;
                    color: #666;
                    font-size: 24px;
                    font-weight: bold;
                    border: 2px solid #ddd;
                }
            """)
        
        layout.addWidget(photo_label)
        
        # Tortoise info
        info_layout = QVBoxLayout()
        
        # Name and species
        name_label = QLabel(f"{tortoise['name']} ({tortoise.get('species', 'Unknown Species')})")
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
            }
        """)
        info_layout.addWidget(name_label)
        
        # Details grid
        details_layout = QGridLayout()
        details_layout.setSpacing(5)
        
        row = 0
        
        # Sex
        if tortoise.get('sex'):
            sex_label = QLabel('Sex:')
            sex_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold;")
            sex_value = QLabel(tortoise['sex'])
            sex_value.setStyleSheet("font-size: 12px; color: #333;")
            details_layout.addWidget(sex_label, row, 0)
            details_layout.addWidget(sex_value, row, 1)
            row += 1
        
        # Weight
        if tortoise.get('current_weight'):
            weight_label = QLabel('Weight:')
            weight_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold;")
            weight_value = QLabel(f"{tortoise['current_weight']}g")
            weight_value.setStyleSheet("font-size: 12px; color: #333;")
            details_layout.addWidget(weight_label, row, 0)
            details_layout.addWidget(weight_value, row, 1)
            row += 1
        
        # Birth date - check if using acquisition date as birthdate
        if tortoise.get('birth_date'):
            # If birth date equals acquisition date, show "Birthday:" instead of "Born:"
            if (tortoise.get('acquisition_date') and 
                tortoise.get('birth_date') == tortoise.get('acquisition_date')):
                birth_label = QLabel('Birthday:')
            else:
                birth_label = QLabel('Born:')
            birth_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold;")
            birth_value = QLabel(tortoise['birth_date'])
            birth_value.setStyleSheet("font-size: 12px; color: #333;")
            details_layout.addWidget(birth_label, row, 0)
            details_layout.addWidget(birth_value, row, 1)
            row += 1
        
        info_layout.addLayout(details_layout)
        
        # Physical description
        if tortoise.get('physical_description'):
            desc_label = QLabel('Physical Description:')
            desc_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold; margin-top: 5px;")
            desc_value = QLabel(tortoise['physical_description'])
            desc_value.setStyleSheet("font-size: 12px; color: #333; margin-bottom: 5px;")
            desc_value.setWordWrap(True)
            desc_value.setMaximumWidth(250)
            info_layout.addWidget(desc_label)
            info_layout.addWidget(desc_value)
        
        # Notes preview
        if tortoise.get('notes'):
            notes_preview = tortoise['notes'][:100] + '...' if len(tortoise['notes']) > 100 else tortoise['notes']
            notes_label = QLabel(f"Notes: {notes_preview}")
            notes_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #777;
                    font-style: italic;
                }
            """)
            info_layout.addWidget(notes_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Action buttons - Edit button aligned with Active button
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)
        
        # Edit button
        edit_button = self.create_button('Edit', 
                                       lambda checked=False, t=tortoise: self.edit_tortoise(t), 
                                       'secondary')
        edit_button.setMaximumWidth(80)
        edit_button.setMaximumHeight(35)
        buttons_layout.addWidget(edit_button)
        
        # Add spacing to match Active button position
        buttons_layout.addSpacing(10)  # Match the spacing to Active button
        
        layout.addLayout(buttons_layout)
        
        # Status indicator
        status_label = QLabel('Active' if tortoise.get('is_active', 1) else 'Inactive')
        status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 12px;
                color: white;
                background-color: #4CAF50;
            }
        """ if tortoise.get('is_active', 1) else """
            QLabel {
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 12px;
                color: white;
                background-color: #757575;
            }
        """)
        layout.addWidget(status_label)
        
        return tortoise_widget
    
    def create_rounded_pixmap(self, original_pixmap, width, height, radius):
        """Create a rounded version of a pixmap"""
        # Scale the original pixmap maintaining aspect ratio
        scaled_pixmap = original_pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Create a new pixmap with transparency
        rounded_pixmap = QPixmap(width, height)
        rounded_pixmap.fill(Qt.transparent)
        
        # Create a painter
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # Create rounded rectangle path for the full container
        path = QPainterPath()
        path.addRoundedRect(0, 0, width, height, radius, radius)
        
        # Set the clipping path
        painter.setClipPath(path)
        
        # Center the scaled image in the container
        x_offset = (width - scaled_pixmap.width()) // 2
        y_offset = (height - scaled_pixmap.height()) // 2
        
        # Fill background with same color as "no photo" background
        from PySide6.QtGui import QColor
        painter.fillRect(0, 0, width, height, QColor("#f5f5f5"))
        
        # Draw the centered scaled image
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        painter.end()
        
        return rounded_pixmap
        
    def add_tortoise(self):
        """Show add tortoise dialog"""
        dialog = AddTortoiseDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            tortoise_data = dialog.get_tortoise_data()
            if tortoise_data:
                try:
                    # Add tortoise to database
                    tortoise_id = self.db_manager.add_tortoise(**tortoise_data)
                    
                    # Show success message
                    QMessageBox.information(self, 'Success', 
                                          f'Tortoise "{tortoise_data["name"]}" added successfully!')
                    
                    # Refresh tortoises list
                    self.refresh_tortoises()
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to add tortoise: {str(e)}')
    
    def edit_tortoise(self, tortoise):
        """Edit existing tortoise"""
        # Set editing flag to hide deactivate buttons
        self._editing_tortoise_id = tortoise['id']
        
        # Create edit dialog (reuse AddTortoiseDialog)
        dialog = AddTortoiseDialog(self)
        dialog.setWindowTitle('Edit Tortoise')
        
        # Pre-populate fields
        dialog.name_input.setText(tortoise.get('name', ''))
        dialog.species_input.setText(tortoise.get('species', ''))
        
        subspecies = tortoise.get('subspecies')
        if subspecies:
            index = dialog.subspecies_combo.findText(subspecies)
            if index >= 0:
                dialog.subspecies_combo.setCurrentIndex(index)
        
        sex = tortoise.get('sex')
        if sex:
            index = dialog.sex_combo.findText(sex)
            if index >= 0:
                dialog.sex_combo.setCurrentIndex(index)
        
        if tortoise.get('birth_date'):
            birth_date = QDate.fromString(tortoise['birth_date'], Qt.ISODate)
            dialog.birth_date.setDate(birth_date)
        
        if tortoise.get('acquisition_date'):
            acq_date = QDate.fromString(tortoise['acquisition_date'], Qt.ISODate)
            dialog.acquisition_date.setDate(acq_date)
        
        if tortoise.get('current_weight'):
            dialog.weight_input.setText(str(tortoise['current_weight']))
        
        if tortoise.get('physical_description'):
            dialog.description_input.setPlainText(tortoise['physical_description'])
        
        if tortoise.get('notes'):
            dialog.notes_input.setPlainText(tortoise['notes'])
        
        # Check the unknown birthdate checkbox if birth date equals acquisition date
        if (tortoise.get('birth_date') and tortoise.get('acquisition_date') and
            tortoise.get('birth_date') == tortoise.get('acquisition_date')):
            dialog.unknown_birthdate_checkbox.setChecked(True)
        
        # Add deactivate/activate buttons to edit dialog
        button_box = dialog.findChild(QDialogButtonBox)
        if button_box:
            if tortoise.get('is_active', 1):
                deactivate_btn = button_box.addButton('Deactivate', QDialogButtonBox.ActionRole)
                deactivate_btn.clicked.connect(lambda: self.deactivate_tortoise_in_edit(tortoise, dialog))
            else:
                activate_btn = button_box.addButton('Activate', QDialogButtonBox.ActionRole)
                activate_btn.clicked.connect(lambda: self.activate_tortoise_in_edit(tortoise, dialog))
        
        if dialog.exec() == QDialog.Accepted:
            tortoise_data = dialog.get_tortoise_data()
            if tortoise_data:
                try:
                    # Update tortoise in database
                    self.db_manager.update_tortoise(tortoise['id'], **tortoise_data)
                    
                    # Show success message
                    QMessageBox.information(self, 'Success', 
                                          f'Tortoise "{tortoise_data["name"]}" updated successfully!')
                    
                    # Refresh tortoises list
                    self.refresh_tortoises()
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to update tortoise: {str(e)}')
        
        # Clear editing flag
        self._editing_tortoise_id = None
    
    def deactivate_tortoise_in_edit(self, tortoise, dialog):
        """Deactivate tortoise from edit dialog"""
        reply = QMessageBox.question(
            dialog, 'Confirm Deactivation',
            f'Are you sure you want to deactivate "{tortoise["name"]}"?\n\n'
            'This will hide the tortoise from care entry screens but preserve all data.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db_manager.deactivate_tortoise(tortoise['id'])
                QMessageBox.information(dialog, 'Success', 
                                      f'Tortoise "{tortoise["name"]}" deactivated successfully!')
                dialog.accept()  # Close the dialog
                self.refresh_tortoises()
            except Exception as e:
                QMessageBox.critical(dialog, 'Error', 
                                   f'Failed to deactivate tortoise: {str(e)}')
    
    def activate_tortoise_in_edit(self, tortoise, dialog):
        """Activate tortoise from edit dialog"""
        try:
            self.db_manager.activate_tortoise(tortoise['id'])
            QMessageBox.information(dialog, 'Success', 
                                  f'Tortoise "{tortoise["name"]}" activated successfully!')
            dialog.accept()  # Close the dialog
            self.refresh_tortoises()
        except Exception as e:
            QMessageBox.critical(dialog, 'Error', 
                               f'Failed to activate tortoise: {str(e)}')
        
    def deactivate_tortoise(self, tortoise):
        """Deactivate a tortoise"""
        reply = QMessageBox.question(
            self, 'Confirm Deactivation',
            f'Are you sure you want to deactivate "{tortoise["name"]}"?\n\n'
            'This will hide the tortoise from care entry screens but preserve all data.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db_manager.deactivate_tortoise(tortoise['id'])
                QMessageBox.information(self, 'Success', 
                                      f'Tortoise "{tortoise["name"]}" deactivated successfully!')
                self.refresh_tortoises()
            except Exception as e:
                QMessageBox.critical(self, 'Error', 
                                   f'Failed to deactivate tortoise: {str(e)}')
    
    def activate_tortoise(self, tortoise):
        """Activate a tortoise"""
        try:
            self.db_manager.activate_tortoise(tortoise['id'])
            QMessageBox.information(self, 'Success', 
                                  f'Tortoise "{tortoise["name"]}" activated successfully!')
            self.refresh_tortoises()
        except Exception as e:
            QMessageBox.critical(self, 'Error', 
                               f'Failed to activate tortoise: {str(e)}')
    
    def go_back(self):
        """Return to settings main screen"""
        self.main_window.show_screen('settings_main')