"""
Tortoise Management Screen - Add, edit, and manage tortoise profiles
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QDateEdit, QTextEdit)
from PySide6.QtCore import Qt, QDate
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
        
    def get_tortoise_data(self):
        """Get tortoise data from form"""
        name = self.name_input.text().strip()
        species = self.species_input.text().strip()
        subspecies = self.subspecies_combo.currentText()
        sex = self.sex_combo.currentText()
        birth_date = self.birth_date.date().toString(Qt.ISODate)
        acquisition_date = self.acquisition_date.date().toString(Qt.ISODate)
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
        
        # Refresh button
        refresh_btn = create_icon_button('activity', 'Refresh', (20, 20), self.refresh_tortoises)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        refresh_btn.setMinimumHeight(50)
        refresh_btn.setMaximumWidth(120)
        action_layout.addWidget(refresh_btn)
        
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
        
        layout = QHBoxLayout(tortoise_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
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
        
        # Birth date
        if tortoise.get('birth_date'):
            birth_label = QLabel('Born:')
            birth_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold;")
            birth_value = QLabel(tortoise['birth_date'])
            birth_value.setStyleSheet("font-size: 12px; color: #333;")
            details_layout.addWidget(birth_label, row, 0)
            details_layout.addWidget(birth_value, row, 1)
            row += 1
        
        info_layout.addLayout(details_layout)
        
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
    
    def go_back(self):
        """Return to settings main screen"""
        self.main_window.show_screen('settings_main')