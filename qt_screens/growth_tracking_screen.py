"""
Growth Tracking Screen - Photo documentation and measurement tracking system
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QFileDialog,
                              QFrame)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QPixmap
from .base_screen import BaseScreen
from .icon_manager import create_icon_button
import os
import shutil

class AddGrowthRecordDialog(QDialog):
    """Dialog for adding new growth records"""
    
    def __init__(self, parent=None, tortoises=None, users=None):
        super().__init__(parent)
        self.setWindowTitle('Add Growth Record')
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        self.tortoises = tortoises or []
        self.users = users or []
        self.selected_photo_path = None
        
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
        
        # Measurement date
        self.measurement_date = QDateEdit()
        self.measurement_date.setCalendarPopup(True)
        self.measurement_date.setDate(QDate.currentDate())
        self.measurement_date.setStyleSheet("""
            QDateEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        form_layout.addRow('Measurement Date:', self.measurement_date)
        
        layout.addLayout(form_layout)
        
        # Measurements section
        measurements_group = QFrame()
        measurements_group.setFrameStyle(QFrame.Box)
        measurements_group.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 5px; }")
        measurements_layout = QFormLayout(measurements_group)
        
        measurements_label = QLabel("Physical Measurements")
        measurements_label.setStyleSheet("font-weight: bold; color: #4CAF50; margin: 5px;")
        measurements_layout.addRow(measurements_label)
        
        # Weight
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0, 10000)
        self.weight_input.setSuffix(' grams')
        self.weight_input.setDecimals(1)
        self.weight_input.setStyleSheet("""
            QDoubleSpinBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        measurements_layout.addRow('Weight:', self.weight_input)
        
        # Length
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(0, 50)
        self.length_input.setSuffix(' cm')
        self.length_input.setDecimals(1)
        self.length_input.setStyleSheet(self.weight_input.styleSheet())
        measurements_layout.addRow('Length (Carapace):', self.length_input)
        
        # Width
        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(0, 50)
        self.width_input.setSuffix(' cm')
        self.width_input.setDecimals(1)
        self.width_input.setStyleSheet(self.weight_input.styleSheet())
        measurements_layout.addRow('Width (Carapace):', self.width_input)
        
        # Height
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(0, 20)
        self.height_input.setSuffix(' cm')
        self.height_input.setDecimals(1)
        self.height_input.setStyleSheet(self.weight_input.styleSheet())
        measurements_layout.addRow('Height (Shell):', self.height_input)
        
        layout.addWidget(measurements_group)
        
        # Photo section
        photo_group = QFrame()
        photo_group.setFrameStyle(QFrame.Box)
        photo_group.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 5px; }")
        photo_layout = QVBoxLayout(photo_group)
        
        photo_label = QLabel("Photo Documentation")
        photo_label.setStyleSheet("font-weight: bold; color: #2196F3; margin: 5px;")
        photo_layout.addWidget(photo_label)
        
        # Photo selection
        photo_button_layout = QHBoxLayout()
        
        self.select_photo_btn = QPushButton('Select Photo')
        self.select_photo_btn.clicked.connect(self.select_photo)
        self.select_photo_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        photo_button_layout.addWidget(self.select_photo_btn)
        
        self.photo_info_label = QLabel('No photo selected')
        self.photo_info_label.setStyleSheet("font-size: 12px; color: #666; margin-left: 10px;")
        photo_button_layout.addWidget(self.photo_info_label)
        
        photo_button_layout.addStretch()
        photo_layout.addLayout(photo_button_layout)
        
        layout.addWidget(photo_group)
        
        # Notes section
        notes_layout = QVBoxLayout()
        notes_label = QLabel('Notes:')
        notes_label.setStyleSheet("font-weight: bold; margin: 5px 0;")
        notes_layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText('Additional notes about growth, behavior, or observations...')
        self.notes_input.setMaximumHeight(80)
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
        notes_layout.addWidget(self.notes_input)
        
        layout.addLayout(notes_layout)
        
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
        
    def select_photo(self):
        """Open file dialog to select photo"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            'Select Photo',
            '',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)'
        )
        
        if file_path:
            self.selected_photo_path = file_path
            filename = os.path.basename(file_path)
            self.photo_info_label.setText(f'Selected: {filename}')
            self.photo_info_label.setStyleSheet("font-size: 12px; color: #4CAF50; margin-left: 10px; font-weight: bold;")
        
    def get_record_data(self):
        """Get growth record data from form"""
        if self.tortoise_combo.count() == 0:
            QMessageBox.warning(self, 'No Tortoises', 'No tortoises available. Please add a tortoise first.')
            return None
            
        if self.user_combo.count() == 0:
            QMessageBox.warning(self, 'No Users', 'No users available. Please add a user first.')
            return None
        
        # Validate that at least one measurement is provided
        weight = self.weight_input.value() if self.weight_input.value() > 0 else None
        length = self.length_input.value() if self.length_input.value() > 0 else None
        width = self.width_input.value() if self.width_input.value() > 0 else None
        height = self.height_input.value() if self.height_input.value() > 0 else None
        
        if not any([weight, length, width, height]) and not self.selected_photo_path:
            QMessageBox.warning(self, 'No Data', 'Please provide at least one measurement or photo.')
            return None
                
        return {
            'tortoise_id': self.tortoise_combo.currentData(),
            'user_id': self.user_combo.currentData(),
            'measurement_date': self.measurement_date.date().toString(Qt.ISODate),
            'weight': weight,
            'length': length,
            'width': width,
            'height': height,
            'photo_path': self.selected_photo_path,
            'notes': self.notes_input.toPlainText().strip()
        }

class GrowthTrackingScreen(BaseScreen):
    """Growth Tracking Screen"""
    
    def build_ui(self):
        """Build growth tracking UI"""
        # Header
        header = self.create_header('📏 Growth Tracking', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        # Add record button
        add_record_btn = create_icon_button('plus', 'Add Growth Record', (24, 24), self.add_growth_record)
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
        
        # Photo import button
        import_btn = create_icon_button('camera', 'Import Photos', (20, 20), self.import_photos)
        import_btn.setStyleSheet("""
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
        import_btn.setMinimumHeight(50)
        import_btn.setMaximumWidth(180)
        action_layout.addWidget(import_btn)
        
        
        self.main_layout.addLayout(action_layout)
        
        # Filter section
        self.create_filter_section()
        
        # Records list area
        self.create_records_list_area()
        
        # Initialize filter state
        self.current_tortoise_filter = None
        
        # Load initial records (after UI is fully built)
        self.refresh_records()
        
    def create_filter_section(self):
        """Create filter controls"""
        filter_layout = QHBoxLayout()
        
        # Tortoise filter
        filter_label = QLabel('Filter by tortoise:')
        filter_label.setStyleSheet("font-weight: bold; margin-right: 10px;")
        filter_layout.addWidget(filter_label)
        
        self.tortoise_filter_combo = QComboBox()
        self.tortoise_filter_combo.addItem('All Tortoises', None)
        # Connect after initial setup to avoid recursion
        self.tortoise_filter_combo.currentIndexChanged.connect(self.apply_tortoise_filter)
        self.tortoise_filter_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                min-width: 150px;
            }
        """)
        filter_layout.addWidget(self.tortoise_filter_combo)
        
        filter_layout.addStretch()
        
        self.main_layout.addLayout(filter_layout)
        
        # Load tortoise filter options after connecting signal
        self.update_tortoise_filter()
    
    def create_records_list_area(self):
        """Create scrollable growth records list area"""
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
    
    def update_tortoise_filter(self):
        """Update tortoise filter dropdown"""
        # Temporarily disconnect signal to avoid recursion
        self.tortoise_filter_combo.currentIndexChanged.disconnect()
        
        self.tortoise_filter_combo.clear()
        self.tortoise_filter_combo.addItem('All Tortoises', None)
        
        try:
            tortoises = self.db_manager.get_tortoises()
            for tortoise in tortoises:
                self.tortoise_filter_combo.addItem(tortoise['name'], tortoise['id'])
        except Exception:
            pass
        
        # Reconnect signal
        self.tortoise_filter_combo.currentIndexChanged.connect(self.apply_tortoise_filter)
    
    def apply_tortoise_filter(self):
        """Apply tortoise filter"""
        current_data = self.tortoise_filter_combo.currentData()
        self.current_tortoise_filter = current_data
        self.refresh_records()
    
    def refresh_records(self):
        """Refresh the growth records list"""
        # Clear existing records
        for i in reversed(range(self.records_layout.count())):
            child = self.records_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        try:
            # Get records from database (we need to add this method)
            records = self.get_growth_records(self.current_tortoise_filter)
            
            if not records:
                # No records message
                no_records_label = QLabel('No growth records found. Click "Add Growth Record" to get started.')
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
                    record_widget = self.create_growth_record_widget(record)
                    self.records_layout.addWidget(record_widget)
                    
        except Exception as e:
            error_label = QLabel(f'Error loading growth records: {str(e)}')
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
        
        # Update filter options
        self.update_tortoise_filter()
    
    def get_growth_records(self, tortoise_id=None):
        """Get growth records from database"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            if tortoise_id:
                cursor.execute('''
                    SELECT gr.*, t.name as tortoise_name, u.name as user_name
                    FROM growth_records gr
                    JOIN tortoises t ON gr.tortoise_id = t.id
                    JOIN users u ON gr.user_id = u.id
                    WHERE gr.tortoise_id = ?
                    ORDER BY gr.measurement_date DESC
                ''', (tortoise_id,))
            else:
                cursor.execute('''
                    SELECT gr.*, t.name as tortoise_name, u.name as user_name
                    FROM growth_records gr
                    JOIN tortoises t ON gr.tortoise_id = t.id
                    JOIN users u ON gr.user_id = u.id
                    ORDER BY gr.measurement_date DESC
                ''')
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []
    
    def create_growth_record_widget(self, record):
        """Create a widget for displaying growth record information"""
        record_widget = QWidget()
        record_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        layout = QHBoxLayout(record_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Record info
        info_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f"{record['tortoise_name']} - Growth Record")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        date_label = QLabel(record['measurement_date'])
        date_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                font-style: italic;
            }
        """)
        header_layout.addWidget(date_label)
        
        info_layout.addLayout(header_layout)
        
        # User info
        user_label = QLabel(f"Recorded by: {record['user_name']}")
        user_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #777;
                margin-bottom: 10px;
            }
        """)
        info_layout.addWidget(user_label)
        
        # Measurements
        measurements = []
        if record.get('weight'):
            measurements.append(f"Weight: {record['weight']}g")
        if record.get('length'):
            measurements.append(f"Length: {record['length']}cm")
        if record.get('width'):
            measurements.append(f"Width: {record['width']}cm")
        if record.get('height'):
            measurements.append(f"Height: {record['height']}cm")
        
        if measurements:
            measurements_label = QLabel(' • '.join(measurements))
            measurements_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #333;
                    font-weight: bold;
                    margin: 5px 0;
                }
            """)
            info_layout.addWidget(measurements_label)
        
        # Notes
        if record.get('notes'):
            notes_preview = record['notes'][:100] + '...' if len(record['notes']) > 100 else record['notes']
            notes_label = QLabel(f"Notes: {notes_preview}")
            notes_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #555;
                    margin: 5px 0;
                    font-style: italic;
                }
            """)
            notes_label.setWordWrap(True)
            info_layout.addWidget(notes_label)
        
        layout.addLayout(info_layout)
        
        # Photo section
        if record.get('photo_path') and os.path.exists(record['photo_path']):
            photo_layout = QVBoxLayout()
            
            # Photo thumbnail
            photo_label = QLabel()
            pixmap = QPixmap(record['photo_path'])
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                photo_label.setPixmap(scaled_pixmap)
                photo_label.setAlignment(Qt.AlignCenter)
                photo_label.setStyleSheet("""
                    QLabel {
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 2px;
                    }
                """)
                photo_layout.addWidget(photo_label)
                
                # View photo button
                view_btn = QPushButton('View Photo')
                view_btn.clicked.connect(lambda: self.view_photo(record['photo_path']))
                view_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 5px 10px;
                        font-size: 11px;
                        margin-top: 5px;
                    }
                    QPushButton:hover { background-color: #1976D2; }
                """)
                photo_layout.addWidget(view_btn)
            
            layout.addLayout(photo_layout)
        
        # Action buttons
        action_layout = QVBoxLayout()
        
        # Delete button
        delete_btn = QPushButton('Delete')
        delete_btn.clicked.connect(lambda: self.delete_record(record['id']))
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
        action_layout.addWidget(delete_btn)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        return record_widget
    
    def add_growth_record(self):
        """Show add growth record dialog"""
        # Get available tortoises and users
        tortoises = self.db_manager.get_tortoises()
        users = self.db_manager.get_users()
        
        dialog = AddGrowthRecordDialog(self, tortoises, users)
        
        if dialog.exec() == QDialog.Accepted:
            record_data = dialog.get_record_data()
            if record_data:
                try:
                    # Handle photo copying if provided
                    if record_data['photo_path']:
                        photo_path = self.copy_photo(record_data['photo_path'], record_data['tortoise_id'])
                        record_data['photo_path'] = photo_path
                    
                    # Add record to database
                    record_id = self.add_growth_record_to_db(**record_data)
                    
                    # Show success message
                    QMessageBox.information(self, 'Success', 'Growth record added successfully!')
                    
                    # Refresh records list
                    self.refresh_records()
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to add growth record: {str(e)}')
    
    def copy_photo(self, source_path, tortoise_id):
        """Copy photo to growth photos directory"""
        try:
            # Create photos directory if it doesn't exist
            photos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'growth_photos')
            os.makedirs(photos_dir, exist_ok=True)
            
            # Generate unique filename
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tortoise_{tortoise_id}_growth_{timestamp}{os.path.splitext(source_path)[1]}"
            dest_path = os.path.join(photos_dir, filename)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            return dest_path
            
        except Exception as e:
            raise Exception(f"Failed to copy photo: {str(e)}")
    
    def add_growth_record_to_db(self, tortoise_id, user_id, measurement_date, weight=None, 
                              length=None, width=None, height=None, photo_path=None, notes=''):
        """Add growth record to database"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO growth_records (tortoise_id, user_id, measurement_date, weight, length, width, height, photo_path, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tortoise_id, user_id, measurement_date, weight, length, width, height, photo_path, notes))
        conn.commit()
        return cursor.lastrowid
    
    def import_photos(self):
        """Import photos from directory"""
        QMessageBox.information(self, 'Photo Import', 
                              'Bulk photo import feature coming soon!\n\n'
                              'For now, use "Add Growth Record" to add photos individually.')
    
    def view_photo(self, photo_path):
        """View photo in larger dialog"""
        if not os.path.exists(photo_path):
            QMessageBox.warning(self, 'Photo Not Found', 'The photo file could not be found.')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle('Growth Photo')
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Photo display
        photo_label = QLabel()
        pixmap = QPixmap(photo_path)
        if not pixmap.isNull():
            # Scale to reasonable size while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            photo_label.setPixmap(scaled_pixmap)
            photo_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(photo_label)
        
        # Close button
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(dialog.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        layout.addWidget(close_btn)
        
        dialog.resize(650, 650)
        dialog.exec()
    
    def delete_record(self, record_id):
        """Delete growth record with confirmation"""
        reply = QMessageBox.question(self, 'Delete Record', 
                                   'Are you sure you want to delete this growth record?\n\n'
                                   'This action cannot be undone.',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM growth_records WHERE id = ?', (record_id,))
                conn.commit()
                
                QMessageBox.information(self, 'Success', 'Growth record deleted successfully!')
                self.refresh_records()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete record: {str(e)}')
    
    def go_back(self):
        """Return to home screen"""
        self.main_window.show_screen('home')