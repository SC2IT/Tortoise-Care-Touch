"""
Health Records Management Screen - Track vet visits, observations, treatments
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QDateEdit, QTextEdit, QCheckBox, QFrame)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class AddHealthRecordDialog(QDialog):
    """Dialog for adding new health records"""
    
    def __init__(self, parent=None, tortoises=None, users=None):
        super().__init__(parent)
        self.setWindowTitle('Add Health Record')
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        self.tortoises = tortoises or []
        self.users = users or []
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Tortoise selection
        self.tortoise_combo = QComboBox()
        for tortoise in self.tortoises:
            self.tortoise_combo.addItem(tortoise['name'], tortoise['id'])
        self.tortoise_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        form_layout.addRow('Tortoise *:', self.tortoise_combo)
        
        # User selection
        self.user_combo = QComboBox()
        for user in self.users:
            self.user_combo.addItem(user['name'], user['id'])
        self.user_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        form_layout.addRow('Recorded by *:', self.user_combo)
        
        # Record type
        self.record_type_combo = QComboBox()
        self.record_type_combo.addItems([
            'observation', 'vet_visit', 'medication', 'injury', 'behavior'
        ])
        self.record_type_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        form_layout.addRow('Record Type *:', self.record_type_combo)
        
        # Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(['low', 'medium', 'high', 'urgent'])
        self.priority_combo.setCurrentText('medium')
        self.priority_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        form_layout.addRow('Priority:', self.priority_combo)
        
        # Title field
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Brief description of the record')
        self.title_input.setStyleSheet("""
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
        form_layout.addRow('Title *:', self.title_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Detailed description of the observation, symptoms, or treatment')
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
        form_layout.addRow('Description:', self.description_input)
        
        layout.addLayout(form_layout)
        
        # Veterinary section
        vet_group = QFrame()
        vet_group.setFrameStyle(QFrame.Box)
        vet_group.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 5px; }")
        vet_layout = QFormLayout(vet_group)
        
        vet_label = QLabel("Veterinary Information (if applicable)")
        vet_label.setStyleSheet("font-weight: bold; color: #2196F3; margin: 5px;")
        vet_layout.addRow(vet_label)
        
        # Vet name
        self.vet_name_input = QLineEdit()
        self.vet_name_input.setPlaceholderText('Veterinarian name')
        self.vet_name_input.setStyleSheet(self.title_input.styleSheet())
        vet_layout.addRow('Veterinarian:', self.vet_name_input)
        
        # Diagnosis
        self.diagnosis_input = QLineEdit()
        self.diagnosis_input.setPlaceholderText('Diagnosis or assessment')
        self.diagnosis_input.setStyleSheet(self.title_input.styleSheet())
        vet_layout.addRow('Diagnosis:', self.diagnosis_input)
        
        # Treatment
        self.treatment_input = QTextEdit()
        self.treatment_input.setPlaceholderText('Treatment plan or recommendations')
        self.treatment_input.setMaximumHeight(60)
        self.treatment_input.setStyleSheet(self.description_input.styleSheet())
        vet_layout.addRow('Treatment:', self.treatment_input)
        
        # Medication
        self.medication_input = QLineEdit()
        self.medication_input.setPlaceholderText('Prescribed medications and dosages')
        self.medication_input.setStyleSheet(self.title_input.styleSheet())
        vet_layout.addRow('Medication:', self.medication_input)
        
        # Follow-up date
        self.follow_up_date = QDateEdit()
        self.follow_up_date.setCalendarPopup(True)
        self.follow_up_date.setDate(QDate.currentDate().addDays(7))
        self.follow_up_date.setSpecialValueText("Not scheduled")
        self.follow_up_date.setStyleSheet("""
            QDateEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        vet_layout.addRow('Follow-up Date:', self.follow_up_date)
        
        layout.addWidget(vet_group)
        
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
        
    def get_record_data(self):
        """Get health record data from form"""
        if not self.title_input.text().strip():
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a title for the health record.')
            return None
            
        if self.tortoise_combo.count() == 0:
            QMessageBox.warning(self, 'No Tortoises', 'No tortoises available. Please add a tortoise first.')
            return None
            
        if self.user_combo.count() == 0:
            QMessageBox.warning(self, 'No Users', 'No users available. Please add a user first.')
            return None
        
        # Get follow-up date (None if not set)
        follow_up_date = None
        if not self.follow_up_date.specialValueText():
            follow_up_date = self.follow_up_date.date().toString(Qt.ISODate)
                
        return {
            'tortoise_id': self.tortoise_combo.currentData(),
            'user_id': self.user_combo.currentData(),
            'record_type': self.record_type_combo.currentText(),
            'title': self.title_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'vet_name': self.vet_name_input.text().strip(),
            'diagnosis': self.diagnosis_input.text().strip(),
            'treatment': self.treatment_input.toPlainText().strip(),
            'medication': self.medication_input.text().strip(),
            'follow_up_date': follow_up_date,
            'priority': self.priority_combo.currentText()
        }

class HealthRecordsScreen(BaseScreen):
    """Health Records Management Screen"""
    
    def build_ui(self):
        """Build health records management UI"""
        # Header
        header = self.create_header('📋 Health Records', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        # Add record button
        add_record_btn = create_icon_button('plus', 'Add Health Record', (24, 24), self.add_health_record)
        add_record_btn.setStyleSheet("""
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
        add_record_btn.setMinimumHeight(50)
        action_layout.addWidget(add_record_btn)
        
        # Filter buttons
        filter_layout = QHBoxLayout()
        
        self.filter_all_btn = QPushButton('All Records')
        self.filter_urgent_btn = QPushButton('Urgent')
        self.filter_unresolved_btn = QPushButton('Unresolved')
        self.filter_recent_btn = QPushButton('Recent')
        
        filter_buttons = [self.filter_all_btn, self.filter_urgent_btn, 
                         self.filter_unresolved_btn, self.filter_recent_btn]
        
        for btn in filter_buttons:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #1976D2; }
                QPushButton:pressed { background-color: #1565C0; }
                QPushButton:checked { background-color: #1565C0; }
            """)
            btn.setCheckable(True)
            filter_layout.addWidget(btn)
            
        # Set default filter
        self.filter_all_btn.setChecked(True)
        
        # Connect filter buttons
        self.filter_all_btn.clicked.connect(lambda: self.apply_filter('all'))
        self.filter_urgent_btn.clicked.connect(lambda: self.apply_filter('urgent'))
        self.filter_unresolved_btn.clicked.connect(lambda: self.apply_filter('unresolved'))
        self.filter_recent_btn.clicked.connect(lambda: self.apply_filter('recent'))
        
        action_layout.addLayout(filter_layout)
        
        
        self.main_layout.addLayout(action_layout)
        
        # Records list area
        self.create_records_list_area()
        
        # Load initial records
        self.current_filter = 'all'
        self.refresh_records()
        
    def create_records_list_area(self):
        """Create scrollable records list area"""
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
        
        # Container widget for records
        self.records_container = QWidget()
        self.records_layout = QVBoxLayout(self.records_container)
        self.records_layout.setSpacing(10)
        self.records_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.records_container)
        self.main_layout.addWidget(self.scroll_area)
        
    def apply_filter(self, filter_type):
        """Apply record filter"""
        # Update button states
        filter_buttons = [self.filter_all_btn, self.filter_urgent_btn, 
                         self.filter_unresolved_btn, self.filter_recent_btn]
        for btn in filter_buttons:
            btn.setChecked(False)
            
        if filter_type == 'all':
            self.filter_all_btn.setChecked(True)
        elif filter_type == 'urgent':
            self.filter_urgent_btn.setChecked(True)
        elif filter_type == 'unresolved':
            self.filter_unresolved_btn.setChecked(True)
        elif filter_type == 'recent':
            self.filter_recent_btn.setChecked(True)
            
        self.current_filter = filter_type
        self.refresh_records()
        
    def refresh_records(self):
        """Refresh the health records list"""
        # Clear existing records
        for i in reversed(range(self.records_layout.count())):
            child = self.records_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        try:
            # Get records based on current filter
            if self.current_filter == 'urgent':
                records = self.db_manager.get_health_records(resolved=False)
                records = [r for r in records if r['priority'] == 'urgent']
            elif self.current_filter == 'unresolved':
                records = self.db_manager.get_health_records(resolved=False)
            elif self.current_filter == 'recent':
                records = self.db_manager.get_health_records()
                # Filter to last 30 days (simplified client-side filtering)
                from datetime import datetime, timedelta
                cutoff = datetime.now() - timedelta(days=30)
                records = [r for r in records if datetime.fromisoformat(r['record_date'].replace('Z', '+00:00')) > cutoff]
            else:  # all
                records = self.db_manager.get_health_records()
            
            if not records:
                # No records message
                no_records_label = QLabel(f'No {self.current_filter} health records found.')
                no_records_label.setAlignment(Qt.AlignCenter)
                no_records_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #666;
                        padding: 40px;
                        background-color: #f5f5f5;
                        border-radius: 8px;
                        border: 2px dashed #ccc;
                    }
                """)
                self.records_layout.addWidget(no_records_label)
            else:
                # Display records
                for record in records:
                    record_widget = self.create_health_record_widget(record)
                    self.records_layout.addWidget(record_widget)
                    
        except Exception as e:
            error_label = QLabel(f'Error loading health records: {str(e)}')
            error_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    background-color: #ffebee;
                    border-radius: 5px;
                }
            """)
            self.records_layout.addWidget(error_label)
        
        # Add stretch to push content to top
        self.records_layout.addStretch()
        
    def create_health_record_widget(self, record):
        """Create a widget for displaying health record information"""
        record_widget = QWidget()
        
        # Set background color based on priority
        priority_colors = {
            'urgent': '#ffebee',  # Light red
            'high': '#fff3e0',    # Light orange
            'medium': '#f5f5f5',  # Light gray
            'low': '#e8f5e8'      # Light green
        }
        
        bg_color = priority_colors.get(record['priority'], '#f5f5f5')
        border_color = {
            'urgent': '#f44336',
            'high': '#ff9800',
            'medium': '#757575',
            'low': '#4caf50'
        }.get(record['priority'], '#757575')
        
        record_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout(record_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header layout
        header_layout = QHBoxLayout()
        
        # Title and basic info
        title_layout = QVBoxLayout()
        
        title_label = QLabel(record['title'])
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
            }
        """)
        title_layout.addWidget(title_label)
        
        # Record info
        info_text = f"{record['tortoise_name']} • {record['record_type'].title()} • {record['user_name']}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                font-style: italic;
            }
        """)
        title_layout.addWidget(info_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Priority and status
        status_layout = QVBoxLayout()
        
        priority_label = QLabel(record['priority'].title())
        priority_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 10px;
                color: white;
                background-color: {border_color};
            }}
        """)
        status_layout.addWidget(priority_label)
        
        resolved_label = QLabel('Resolved' if record['resolved'] else 'Active')
        resolved_color = '#4CAF50' if record['resolved'] else '#FF9800'
        resolved_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 10px;
                color: white;
                background-color: {resolved_color};
            }}
        """)
        status_layout.addWidget(resolved_label)
        
        header_layout.addLayout(status_layout)
        
        layout.addLayout(header_layout)
        
        # Date
        date_label = QLabel(f"Date: {record['record_date'][:10]}")
        date_label.setStyleSheet("font-size: 12px; color: #666; margin: 5px 0;")
        layout.addWidget(date_label)
        
        # Description
        if record['description']:
            desc_preview = record['description'][:150] + '...' if len(record['description']) > 150 else record['description']
            desc_label = QLabel(f"Description: {desc_preview}")
            desc_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #333;
                    margin: 5px 0;
                }
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Vet info if applicable
        if record['vet_name'] or record['diagnosis']:
            vet_text = []
            if record['vet_name']:
                vet_text.append(f"Vet: {record['vet_name']}")
            if record['diagnosis']:
                vet_text.append(f"Diagnosis: {record['diagnosis']}")
            
            vet_label = QLabel(' • '.join(vet_text))
            vet_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #2196F3;
                    font-weight: bold;
                    margin: 5px 0;
                }
            """)
            layout.addWidget(vet_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        # Mark resolved/unresolved button
        resolve_text = 'Mark Unresolved' if record['resolved'] else 'Mark Resolved'
        resolve_btn = QPushButton(resolve_text)
        resolve_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        resolve_btn.clicked.connect(lambda: self.toggle_resolved(record['id'], not record['resolved']))
        button_layout.addWidget(resolve_btn)
        
        # Edit button
        edit_btn = QPushButton('Edit')
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        edit_btn.clicked.connect(lambda: self.edit_record(record['id']))
        button_layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton('Delete')
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        delete_btn.clicked.connect(lambda: self.delete_record(record['id'], record['title']))
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return record_widget
    
    def add_health_record(self):
        """Show add health record dialog"""
        # Get available tortoises and users
        tortoises = self.db_manager.get_tortoises()
        users = self.db_manager.get_users()
        
        dialog = AddHealthRecordDialog(self, tortoises, users)
        
        if dialog.exec() == QDialog.Accepted:
            record_data = dialog.get_record_data()
            if record_data:
                try:
                    # Add record to database
                    record_id = self.db_manager.add_health_record(**record_data)
                    
                    # Show success message
                    QMessageBox.information(self, 'Success', 
                                          f'Health record "{record_data["title"]}" added successfully!')
                    
                    # Refresh records list
                    self.refresh_records()
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to add health record: {str(e)}')
    
    def toggle_resolved(self, record_id, resolved):
        """Toggle record resolved status"""
        try:
            self.db_manager.update_health_record(record_id, resolved=resolved)
            self.refresh_records()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update record: {str(e)}')
    
    def edit_record(self, record_id):
        """Edit health record (simplified for now)"""
        QMessageBox.information(self, 'Coming Soon', 
                               'Health record editing will be implemented in the next update!')
    
    def delete_record(self, record_id, title):
        """Delete health record with confirmation"""
        reply = QMessageBox.question(self, 'Delete Record', 
                                   f'Are you sure you want to delete the health record:\n\n"{title}"?\n\n'
                                   'This action cannot be undone.',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.db_manager.delete_health_record(record_id)
                QMessageBox.information(self, 'Success', 'Health record deleted successfully!')
                self.refresh_records()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete record: {str(e)}')
    
    def go_back(self):
        """Return to health screen"""
        self.main_window.show_screen('health')