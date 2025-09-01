"""
User Management Screen - Add, edit, and manage user profiles
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, QCheckBox)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class AddUserDialog(QDialog):
    """Dialog for adding new users"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New User')
        self.setMinimumSize(400, 250)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name field (required)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter user name')
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
        
        # Email field (optional)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter email address (optional)')
        self.email_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addRow('Email:', self.email_input)
        
        # Role selector
        self.role_combo = QComboBox()
        self.role_combo.addItems([
            'Caregiver',
            'Primary Owner',
            'Family Member', 
            'Veterinarian',
            'Observer',
            'Administrator'
        ])
        self.role_combo.setCurrentText('Caregiver')  # Default role
        self.role_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #4CAF50;
            }
            QComboBox:hover {
                border-color: #4CAF50;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #ccc;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #4CAF50;
                background-color: white;
                color: black;
            }
        """)
        form_layout.addRow('Role:', self.role_combo)
        
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
        
    def get_user_data(self):
        """Get user data from form"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        
        if not name:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a user name.')
            return None
            
        return {'name': name, 'email': email, 'role': role}

class EditUserDialog(QDialog):
    """Dialog for editing existing users"""
    
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle(f'Edit User: {user_data["name"]}')
        self.setMinimumSize(400, 250)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name field (required)
        self.name_input = QLineEdit()
        self.name_input.setText(user_data.get('name', ''))
        self.name_input.setPlaceholderText('Enter user name')
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
        
        # Email field (optional)
        self.email_input = QLineEdit()
        self.email_input.setText(user_data.get('email', ''))
        self.email_input.setPlaceholderText('Enter email address (optional)')
        self.email_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addRow('Email:', self.email_input)
        
        # Role selector
        self.role_combo = QComboBox()
        self.role_combo.addItems([
            'Caregiver',
            'Primary Owner',
            'Family Member', 
            'Veterinarian',
            'Observer',
            'Administrator'
        ])
        current_role = user_data.get('role', 'Caregiver')
        if current_role in ['Caregiver', 'Primary Owner', 'Family Member', 'Veterinarian', 'Observer', 'Administrator']:
            self.role_combo.setCurrentText(current_role)
        else:
            self.role_combo.setCurrentText('Caregiver')
        self.role_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #4CAF50;
            }
            QComboBox:hover {
                border-color: #4CAF50;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #ccc;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #4CAF50;
                background-color: white;
                color: black;
            }
        """)
        form_layout.addRow('Role:', self.role_combo)
        
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
        
    def get_user_data(self):
        """Get updated user data from form"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        
        if not name:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a user name.')
            return None
            
        return {'name': name, 'email': email, 'role': role}

class SettingsUsersScreen(BaseScreen):
    """User Management Screen"""
    
    def build_ui(self):
        """Build user management UI"""
        # Header
        header = self.create_header('👥 User Management', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        # Add user button
        add_user_btn = create_icon_button('plus', 'Add New User', (24, 24), self.add_user)
        add_user_btn.setStyleSheet("""
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
        add_user_btn.setMinimumHeight(50)
        action_layout.addWidget(add_user_btn)
        
        # Refresh button
        refresh_btn = create_icon_button('activity', 'Refresh', (20, 20), self.refresh_users)
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
        
        # Show inactive users checkbox
        self.show_inactive_checkbox = QCheckBox('Show inactive users')
        self.show_inactive_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #666;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #4CAF50;
            }
        """)
        self.show_inactive_checkbox.toggled.connect(self.refresh_users)
        action_layout.addWidget(self.show_inactive_checkbox)
        
        self.main_layout.addLayout(action_layout)
        
        # Users list area
        self.create_users_list_area()
        
        # Load users
        self.refresh_users()
        
    def create_users_list_area(self):
        """Create scrollable users list area"""
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
        
        # Container widget for users
        self.users_container = QWidget()
        self.users_layout = QVBoxLayout(self.users_container)
        self.users_layout.setSpacing(10)
        self.users_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.users_container)
        self.main_layout.addWidget(self.scroll_area)
        
    def refresh_users(self):
        """Refresh the users list"""
        # Clear existing users
        for i in reversed(range(self.users_layout.count())):
            child = self.users_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get users from database
        try:
            include_inactive = self.show_inactive_checkbox.isChecked()
            users = self.db_manager.get_users(include_inactive)
            
            if not users:
                # No users message
                no_users_label = QLabel('No users found. Click "Add New User" to get started.')
                no_users_label.setAlignment(Qt.AlignCenter)
                no_users_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #666;
                        padding: 40px;
                        background-color: #f5f5f5;
                        border-radius: 8px;
                        border: 2px dashed #ccc;
                    }
                """)
                self.users_layout.addWidget(no_users_label)
            else:
                # Display users
                for user in users:
                    user_widget = self.create_user_widget(user)
                    self.users_layout.addWidget(user_widget)
                    
        except Exception as e:
            error_label = QLabel(f'Error loading users: {str(e)}')
            error_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    background-color: #ffebee;
                    border-radius: 5px;
                }
            """)
            self.users_layout.addWidget(error_label)
        
        # Add stretch to push content to top
        self.users_layout.addStretch()
        
    def create_user_widget(self, user):
        """Create a widget for displaying user information"""
        user_widget = QWidget()
        user_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        layout = QHBoxLayout(user_widget)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # User info
        info_layout = QVBoxLayout()
        
        # Name
        name_label = QLabel(user['name'])
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
            }
        """)
        info_layout.addWidget(name_label)
        
        # Role and email in one line
        details_text = []
        if user.get('role'):
            details_text.append(f"Role: {user['role']}")
        if user.get('email'):
            details_text.append(f"Email: {user['email']}")
            
        if details_text:
            details_label = QLabel(" | ".join(details_text))
            details_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #666;
                }
            """)
            info_layout.addWidget(details_label)
        
        # Created date
        if user.get('created_at'):
            created_label = QLabel(f"Created: {user['created_at']}")
            created_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #999;
                }
            """)
            info_layout.addWidget(created_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Action buttons
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(5)
        
        # Edit button
        edit_btn = create_icon_button('edit', 'Edit', (16, 16), 
                                     lambda user_data=user: self.edit_user(user_data))
        edit_btn.setMaximumHeight(30)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        actions_layout.addWidget(edit_btn)
        
        # Activate/Deactivate button
        is_active = user.get('is_active', 1)
        if is_active:
            deactivate_btn = create_icon_button('x', 'Deactivate', (16, 16),
                                               lambda user_data=user: self.deactivate_user(user_data))
            deactivate_btn.setMaximumHeight(30)
            deactivate_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                    text-align: left;
                    padding-left: 8px;
                }
                QPushButton:hover { background-color: #F57C00; }
                QPushButton:pressed { background-color: #E65100; }
            """)
            actions_layout.addWidget(deactivate_btn)
        else:
            activate_btn = create_icon_button('check', 'Activate', (16, 16),
                                             lambda user_data=user: self.activate_user(user_data))
            activate_btn.setMaximumHeight(30)
            activate_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                    text-align: left;
                    padding-left: 8px;
                }
                QPushButton:hover { background-color: #45a049; }
                QPushButton:pressed { background-color: #3d8b40; }
            """)
            actions_layout.addWidget(activate_btn)
        
        layout.addLayout(actions_layout)
        
        # Status indicator
        status_label = QLabel('Active' if is_active else 'Inactive')
        status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 12px;
                color: white;
                background-color: #4CAF50;
            }
        """ if is_active else """
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
        
        return user_widget
        
    def add_user(self):
        """Show add user dialog"""
        dialog = AddUserDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            user_data = dialog.get_user_data()
            if user_data:
                try:
                    # Add user to database
                    user_id = self.db_manager.add_user(
                        user_data['name'], 
                        user_data['email'], 
                        user_data['role']
                    )
                    
                    # Show success message
                    QMessageBox.information(self, 'Success', 
                                          f'User "{user_data["name"]}" with role "{user_data["role"]}" added successfully!')
                    
                    # Refresh users list
                    self.refresh_users()
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to add user: {str(e)}')
    
    def edit_user(self, user_data):
        """Show edit user dialog"""
        dialog = EditUserDialog(user_data, self)
        
        if dialog.exec() == QDialog.Accepted:
            updated_data = dialog.get_user_data()
            if updated_data:
                try:
                    # Update user in database
                    success = self.db_manager.update_user(
                        user_data['id'],
                        updated_data['name'],
                        updated_data['email'],
                        updated_data['role']
                    )
                    
                    if success:
                        # Show success message
                        QMessageBox.information(self, 'Success', 
                                              f'User "{updated_data["name"]}" updated successfully!')
                        
                        # Refresh users list
                        self.refresh_users()
                    else:
                        QMessageBox.warning(self, 'Warning', 'No changes were made.')
                    
                except Exception as e:
                    QMessageBox.critical(self, 'Error', 
                                       f'Failed to update user: {str(e)}')
    
    def deactivate_user(self, user_data):
        """Deactivate a user after confirmation"""
        reply = QMessageBox.question(
            self, 'Confirm Deactivation', 
            f'Are you sure you want to deactivate user "{user_data["name"]}"?\n\n'
            'The user will no longer be able to access the system, but their data will be preserved.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.db_manager.deactivate_user(user_data['id'])
                if success:
                    QMessageBox.information(self, 'Success', 
                                          f'User "{user_data["name"]}" has been deactivated.')
                    self.refresh_users()
                else:
                    QMessageBox.warning(self, 'Warning', 'Failed to deactivate user.')
                    
            except Exception as e:
                QMessageBox.critical(self, 'Error', 
                                   f'Failed to deactivate user: {str(e)}')
    
    def activate_user(self, user_data):
        """Reactivate a user"""
        try:
            success = self.db_manager.activate_user(user_data['id'])
            if success:
                QMessageBox.information(self, 'Success', 
                                      f'User "{user_data["name"]}" has been reactivated.')
                self.refresh_users()
            else:
                QMessageBox.warning(self, 'Warning', 'Failed to activate user.')
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', 
                               f'Failed to activate user: {str(e)}')
    
    def go_back(self):
        """Return to settings main screen"""
        self.main_window.show_screen('settings_main')