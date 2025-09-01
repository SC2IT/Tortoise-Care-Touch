"""
Care Reminders Screen - Task scheduling and notification system for daily tortoise care
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QDateTimeEdit, QSpinBox, QTextEdit, QCheckBox, QFrame)
from PySide6.QtCore import Qt, QDateTime, QDate, QTimer
from PySide6.QtGui import QFont
from .base_screen import BaseScreen
from .icon_manager import create_icon_button
import datetime

class AddReminderDialog(QDialog):
    """Dialog for adding new care reminders"""
    
    def __init__(self, parent=None, tortoises=None, users=None):
        super().__init__(parent)
        self.setWindowTitle('Add Care Reminder')
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        self.tortoises = tortoises or []
        self.users = users or []
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Title field
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('e.g., Daily Feeding, Weekly Cleaning, Monthly Health Check')
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
        self.description_input.setPlaceholderText('Detailed description of the care task...')
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
        
        # Tortoise assignment
        self.tortoise_combo = QComboBox()
        self.tortoise_combo.addItem('All Tortoises', None)
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
        form_layout.addRow('Tortoise:', self.tortoise_combo)
        
        # User assignment
        self.user_combo = QComboBox()
        self.user_combo.addItem('Any User', None)
        for user in self.users:
            self.user_combo.addItem(user['name'], user['id'])
        self.user_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        form_layout.addRow('Assigned To:', self.user_combo)
        
        # Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(['low', 'medium', 'high'])
        self.priority_combo.setCurrentText('medium')
        self.priority_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        form_layout.addRow('Priority:', self.priority_combo)
        
        layout.addLayout(form_layout)
        
        # Frequency settings
        frequency_group = QFrame()
        frequency_group.setFrameStyle(QFrame.Box)
        frequency_group.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 5px; }")
        frequency_layout = QFormLayout(frequency_group)
        
        frequency_label = QLabel("Frequency & Scheduling")
        frequency_label.setStyleSheet("font-weight: bold; color: #FF9800; margin: 5px;")
        frequency_layout.addRow(frequency_label)
        
        # Reminder type
        self.reminder_type_combo = QComboBox()
        self.reminder_type_combo.addItems(['daily', 'weekly', 'monthly', 'yearly', 'once'])
        self.reminder_type_combo.currentTextChanged.connect(self.update_frequency_options)
        self.reminder_type_combo.setStyleSheet(self.tortoise_combo.styleSheet())
        frequency_layout.addRow('Frequency Type:', self.reminder_type_combo)
        
        # Frequency days (for custom intervals)
        self.frequency_days_input = QSpinBox()
        self.frequency_days_input.setRange(1, 365)
        self.frequency_days_input.setValue(1)
        self.frequency_days_input.setSuffix(' days')
        self.frequency_days_input.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        self.frequency_days_label = QLabel('Every:')
        frequency_layout.addRow(self.frequency_days_label, self.frequency_days_input)
        
        # Next due date
        self.next_due_input = QDateTimeEdit()
        self.next_due_input.setCalendarPopup(True)
        self.next_due_input.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.next_due_input.setStyleSheet("""
            QDateTimeEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        frequency_layout.addRow('Next Due:', self.next_due_input)
        
        layout.addWidget(frequency_group)
        
        # Set initial frequency options
        self.update_frequency_options()
        
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
        
    def update_frequency_options(self):
        """Update frequency options based on reminder type"""
        reminder_type = self.reminder_type_combo.currentText()
        
        if reminder_type == 'daily':
            self.frequency_days_input.setValue(1)
            self.frequency_days_label.setVisible(False)
            self.frequency_days_input.setVisible(False)
        elif reminder_type == 'weekly':
            self.frequency_days_input.setValue(7)
            self.frequency_days_label.setVisible(False)
            self.frequency_days_input.setVisible(False)
        elif reminder_type == 'monthly':
            self.frequency_days_input.setValue(30)
            self.frequency_days_label.setVisible(False)
            self.frequency_days_input.setVisible(False)
        elif reminder_type == 'yearly':
            self.frequency_days_input.setValue(365)
            self.frequency_days_label.setVisible(False)
            self.frequency_days_input.setVisible(False)
        elif reminder_type == 'once':
            self.frequency_days_input.setValue(0)
            self.frequency_days_label.setVisible(False)
            self.frequency_days_input.setVisible(False)
        else:  # custom
            self.frequency_days_label.setVisible(True)
            self.frequency_days_input.setVisible(True)
    
    def get_reminder_data(self):
        """Get reminder data from form"""
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a title for the reminder.')
            return None
        
        # Get frequency days based on type
        reminder_type = self.reminder_type_combo.currentText()
        if reminder_type == 'daily':
            frequency_days = 1
        elif reminder_type == 'weekly':
            frequency_days = 7
        elif reminder_type == 'monthly':
            frequency_days = 30
        elif reminder_type == 'yearly':
            frequency_days = 365
        elif reminder_type == 'once':
            frequency_days = 0
        else:
            frequency_days = self.frequency_days_input.value()
        
        return {
            'title': title,
            'description': self.description_input.toPlainText().strip(),
            'assigned_user_id': self.user_combo.currentData(),
            'tortoise_id': self.tortoise_combo.currentData(),
            'reminder_type': reminder_type,
            'frequency_days': frequency_days,
            'next_due_date': self.next_due_input.dateTime().toString(Qt.ISODate),
            'priority': self.priority_combo.currentText()
        }

# Import QLineEdit at the top
from PySide6.QtWidgets import QLineEdit

class CareRemindersScreen(BaseScreen):
    """Care Reminders Management Screen"""
    
    def build_ui(self):
        """Build care reminders UI"""
        # Header
        header = self.create_header('⏰ Care Reminders', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        # Add reminder button
        add_reminder_btn = create_icon_button('plus', 'Add Reminder', (24, 24), self.add_reminder)
        add_reminder_btn.setStyleSheet("""
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
        add_reminder_btn.setMinimumHeight(50)
        action_layout.addWidget(add_reminder_btn)
        
        # Quick task buttons
        self.create_quick_task_buttons(action_layout)
        
        
        self.main_layout.addLayout(action_layout)
        
        # Filter tabs
        self.create_filter_tabs()
        
        # Reminders list area
        self.create_reminders_list_area()
        
        # Setup auto-refresh timer
        self.setup_refresh_timer()
        
        # Load initial reminders
        self.current_filter = 'due'
        self.refresh_reminders()
    
    def create_quick_task_buttons(self, parent_layout):
        """Create quick task creation buttons"""
        quick_tasks = [
            ('🍽️', 'Daily Feed', self.add_daily_feeding),
            ('🧽', 'Weekly Clean', self.add_weekly_cleaning),
            ('⚖️', 'Monthly Weigh', self.add_monthly_weighing)
        ]
        
        for icon, text, callback in quick_tasks:
            btn = QPushButton(f'{icon} {text}')
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #1976D2; }
                QPushButton:pressed { background-color: #1565C0; }
            """)
            btn.setMinimumHeight(50)
            btn.setMaximumWidth(140)
            parent_layout.addWidget(btn)
    
    def create_filter_tabs(self):
        """Create filter tabs for different reminder views"""
        filter_layout = QHBoxLayout()
        
        # Filter buttons
        self.filter_due_btn = QPushButton('Due Today')
        self.filter_overdue_btn = QPushButton('Overdue')
        self.filter_upcoming_btn = QPushButton('Upcoming')
        self.filter_all_btn = QPushButton('All Active')
        self.filter_completed_btn = QPushButton('Completed')
        
        filter_buttons = [self.filter_due_btn, self.filter_overdue_btn, 
                         self.filter_upcoming_btn, self.filter_all_btn, self.filter_completed_btn]
        
        for btn in filter_buttons:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #757575;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #616161; }
                QPushButton:pressed { background-color: #424242; }
                QPushButton:checked { 
                    background-color: #4CAF50; 
                }
            """)
            btn.setCheckable(True)
            filter_layout.addWidget(btn)
            
        # Set default filter
        self.filter_due_btn.setChecked(True)
        
        # Connect filter buttons
        self.filter_due_btn.clicked.connect(lambda: self.apply_filter('due'))
        self.filter_overdue_btn.clicked.connect(lambda: self.apply_filter('overdue'))
        self.filter_upcoming_btn.clicked.connect(lambda: self.apply_filter('upcoming'))
        self.filter_all_btn.clicked.connect(lambda: self.apply_filter('all'))
        self.filter_completed_btn.clicked.connect(lambda: self.apply_filter('completed'))
        
        filter_layout.addStretch()
        self.main_layout.addLayout(filter_layout)
    
    def create_reminders_list_area(self):
        """Create scrollable reminders list area"""
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
        
        # Container widget for reminders
        self.reminders_container = QWidget()
        self.reminders_layout = QVBoxLayout(self.reminders_container)
        self.reminders_layout.setSpacing(10)
        self.reminders_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.reminders_container)
        self.main_layout.addWidget(self.scroll_area)
    
    def setup_refresh_timer(self):
        """Setup automatic refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_reminders)
        self.refresh_timer.start(60000)  # Refresh every minute
    
    def apply_filter(self, filter_type):
        """Apply reminder filter"""
        # Update button states
        filter_buttons = [self.filter_due_btn, self.filter_overdue_btn, 
                         self.filter_upcoming_btn, self.filter_all_btn, self.filter_completed_btn]
        for btn in filter_buttons:
            btn.setChecked(False)
            
        if filter_type == 'due':
            self.filter_due_btn.setChecked(True)
        elif filter_type == 'overdue':
            self.filter_overdue_btn.setChecked(True)
        elif filter_type == 'upcoming':
            self.filter_upcoming_btn.setChecked(True)
        elif filter_type == 'all':
            self.filter_all_btn.setChecked(True)
        elif filter_type == 'completed':
            self.filter_completed_btn.setChecked(True)
            
        self.current_filter = filter_type
        self.refresh_reminders()
    
    def refresh_reminders(self):
        """Refresh the reminders list"""
        # Clear existing reminders
        for i in reversed(range(self.reminders_layout.count())):
            child = self.reminders_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        try:
            # Get reminders based on current filter
            reminders = self.get_filtered_reminders(self.current_filter)
            
            if not reminders:
                # No reminders message
                no_reminders_label = QLabel(f'No {self.current_filter} reminders found.')
                no_reminders_label.setAlignment(Qt.AlignCenter)
                no_reminders_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #666;
                        padding: 40px;
                        background-color: #f5f5f5;
                        border-radius: 8px;
                        border: 2px dashed #ccc;
                    }
                """)
                self.reminders_layout.addWidget(no_reminders_label)
            else:
                # Display reminders
                for reminder in reminders:
                    reminder_widget = self.create_reminder_widget(reminder)
                    self.reminders_layout.addWidget(reminder_widget)
                    
        except Exception as e:
            error_label = QLabel(f'Error loading reminders: {str(e)}')
            error_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    background-color: #ffebee;
                    border-radius: 5px;
                }
            """)
            self.reminders_layout.addWidget(error_label)
        
        # Add stretch to push content to top
        self.reminders_layout.addStretch()
    
    def get_filtered_reminders(self, filter_type):
        """Get filtered reminders from database"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            now = datetime.datetime.now()
            today = now.date()
            
            base_query = '''
                SELECT cr.*, t.name as tortoise_name, u.name as user_name
                FROM care_reminders cr
                LEFT JOIN tortoises t ON cr.tortoise_id = t.id
                LEFT JOIN users u ON cr.assigned_user_id = u.id
                WHERE cr.is_active = 1
            '''
            
            if filter_type == 'due':
                cursor.execute(base_query + ' AND DATE(cr.next_due_date) <= DATE(?) ORDER BY cr.next_due_date ASC', (today,))
            elif filter_type == 'overdue':
                cursor.execute(base_query + ' AND DATE(cr.next_due_date) < DATE(?) ORDER BY cr.next_due_date ASC', (today,))
            elif filter_type == 'upcoming':
                cursor.execute(base_query + ' AND DATE(cr.next_due_date) > DATE(?) ORDER BY cr.next_due_date ASC', (today,))
            elif filter_type == 'completed':
                cursor.execute('''
                    SELECT cr.*, t.name as tortoise_name, u.name as user_name
                    FROM care_reminders cr
                    LEFT JOIN tortoises t ON cr.tortoise_id = t.id
                    LEFT JOIN users u ON cr.assigned_user_id = u.id
                    WHERE cr.last_completed IS NOT NULL
                    ORDER BY cr.last_completed DESC LIMIT 20
                ''')
            else:  # all
                cursor.execute(base_query + ' ORDER BY cr.next_due_date ASC')
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception:
            return []
    
    def create_reminder_widget(self, reminder):
        """Create a widget for displaying reminder information"""
        reminder_widget = QWidget()
        
        # Determine color based on status
        now = datetime.datetime.now().date()
        try:
            due_date = datetime.datetime.fromisoformat(reminder['next_due_date']).date()
            if due_date < now:
                bg_color = '#ffebee'  # Light red for overdue
                border_color = '#f44336'
            elif due_date == now:
                bg_color = '#fff3e0'  # Light orange for due today
                border_color = '#ff9800'
            else:
                bg_color = '#f5f5f5'  # Light gray for upcoming
                border_color = '#757575'
        except:
            bg_color = '#f5f5f5'
            border_color = '#757575'
        
        # Priority color override
        if reminder['priority'] == 'high':
            border_color = '#f44336'
        elif reminder['priority'] == 'low':
            border_color = '#4caf50'
        
        reminder_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout(reminder_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header layout
        header_layout = QHBoxLayout()
        
        # Title and info
        title_layout = QVBoxLayout()
        
        title_label = QLabel(reminder['title'])
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
            }
        """)
        title_layout.addWidget(title_label)
        
        # Details
        details = []
        if reminder.get('tortoise_name'):
            details.append(f"Tortoise: {reminder['tortoise_name']}")
        else:
            details.append("All Tortoises")
        
        if reminder.get('user_name'):
            details.append(f"Assigned to: {reminder['user_name']}")
        else:
            details.append("Any User")
        
        details.append(f"Type: {reminder['reminder_type'].title()}")
        
        details_label = QLabel(' • '.join(details))
        details_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                font-style: italic;
            }
        """)
        title_layout.addWidget(details_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Due date and priority
        status_layout = QVBoxLayout()
        
        # Due date
        due_date_label = QLabel(f"Due: {reminder['next_due_date'][:10]}")
        due_date_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #333;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(due_date_label)
        
        # Priority
        priority_label = QLabel(reminder['priority'].title())
        priority_color = {
            'high': '#f44336',
            'medium': '#ff9800',
            'low': '#4caf50'
        }.get(reminder['priority'], '#757575')
        
        priority_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 10px;
                color: white;
                background-color: {priority_color};
            }}
        """)
        status_layout.addWidget(priority_label)
        
        header_layout.addLayout(status_layout)
        layout.addLayout(header_layout)
        
        # Description
        if reminder.get('description'):
            desc_label = QLabel(reminder['description'])
            desc_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #555;
                    margin: 10px 0;
                }
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        # Complete button
        complete_btn = QPushButton('Mark Complete')
        complete_btn.clicked.connect(lambda: self.complete_reminder(reminder['id']))
        complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        button_layout.addWidget(complete_btn)
        
        # Edit button
        edit_btn = QPushButton('Edit')
        edit_btn.clicked.connect(lambda: self.edit_reminder(reminder['id']))
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
        button_layout.addWidget(edit_btn)
        
        # Deactivate button
        deactivate_btn = QPushButton('Deactivate')
        deactivate_btn.clicked.connect(lambda: self.deactivate_reminder(reminder['id']))
        deactivate_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        button_layout.addWidget(deactivate_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return reminder_widget
    
    def add_reminder(self):
        """Show add reminder dialog"""
        tortoises = self.db_manager.get_tortoises()
        users = self.db_manager.get_users()
        
        dialog = AddReminderDialog(self, tortoises, users)
        
        if dialog.exec() == QDialog.Accepted:
            reminder_data = dialog.get_reminder_data()
            if reminder_data:
                try:
                    self.add_reminder_to_db(**reminder_data)
                    QMessageBox.information(self, 'Success', 'Care reminder added successfully!')
                    self.refresh_reminders()
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to add reminder: {str(e)}')
    
    def add_reminder_to_db(self, title, description, assigned_user_id, tortoise_id, 
                          reminder_type, frequency_days, next_due_date, priority):
        """Add reminder to database"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO care_reminders (title, description, assigned_user_id, tortoise_id, 
                                      reminder_type, frequency_days, next_due_date, priority) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, assigned_user_id, tortoise_id, reminder_type, 
              frequency_days, next_due_date, priority))
        conn.commit()
        return cursor.lastrowid
    
    def add_daily_feeding(self):
        """Add quick daily feeding reminder"""
        try:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
            self.add_reminder_to_db(
                title="Daily Feeding",
                description="Provide fresh food and check water supply",
                assigned_user_id=None,
                tortoise_id=None,
                reminder_type="daily",
                frequency_days=1,
                next_due_date=tomorrow.isoformat(),
                priority="medium"
            )
            QMessageBox.information(self, 'Success', 'Daily feeding reminder added!')
            self.refresh_reminders()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add reminder: {str(e)}')
    
    def add_weekly_cleaning(self):
        """Add quick weekly cleaning reminder"""
        try:
            next_week = (datetime.datetime.now() + datetime.timedelta(days=7)).replace(hour=10, minute=0, second=0, microsecond=0)
            self.add_reminder_to_db(
                title="Weekly Habitat Cleaning",
                description="Clean habitat, replace substrate, sanitize water dish",
                assigned_user_id=None,
                tortoise_id=None,
                reminder_type="weekly",
                frequency_days=7,
                next_due_date=next_week.isoformat(),
                priority="medium"
            )
            QMessageBox.information(self, 'Success', 'Weekly cleaning reminder added!')
            self.refresh_reminders()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add reminder: {str(e)}')
    
    def add_monthly_weighing(self):
        """Add quick monthly weighing reminder"""
        try:
            next_month = (datetime.datetime.now() + datetime.timedelta(days=30)).replace(hour=9, minute=0, second=0, microsecond=0)
            self.add_reminder_to_db(
                title="Monthly Weight Check",
                description="Weigh tortoise and record growth measurements",
                assigned_user_id=None,
                tortoise_id=None,
                reminder_type="monthly",
                frequency_days=30,
                next_due_date=next_month.isoformat(),
                priority="high"
            )
            QMessageBox.information(self, 'Success', 'Monthly weighing reminder added!')
            self.refresh_reminders()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add reminder: {str(e)}')
    
    def complete_reminder(self, reminder_id):
        """Mark reminder as complete and schedule next occurrence"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # Get reminder details
            cursor.execute('SELECT * FROM care_reminders WHERE id = ?', (reminder_id,))
            reminder = dict(cursor.fetchone())
            
            # Update last completed
            now = datetime.datetime.now()
            cursor.execute('UPDATE care_reminders SET last_completed = ? WHERE id = ?', 
                          (now.isoformat(), reminder_id))
            
            # Calculate next due date if recurring
            if reminder['reminder_type'] != 'once' and reminder['frequency_days'] > 0:
                current_due = datetime.datetime.fromisoformat(reminder['next_due_date'])
                next_due = current_due + datetime.timedelta(days=reminder['frequency_days'])
                cursor.execute('UPDATE care_reminders SET next_due_date = ? WHERE id = ?', 
                              (next_due.isoformat(), reminder_id))
            else:
                # Deactivate one-time reminders
                cursor.execute('UPDATE care_reminders SET is_active = 0 WHERE id = ?', (reminder_id,))
            
            conn.commit()
            QMessageBox.information(self, 'Success', 'Reminder marked as complete!')
            self.refresh_reminders()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to complete reminder: {str(e)}')
    
    def edit_reminder(self, reminder_id):
        """Edit reminder (simplified for now)"""
        QMessageBox.information(self, 'Coming Soon', 
                               'Reminder editing will be implemented in the next update!')
    
    def deactivate_reminder(self, reminder_id):
        """Deactivate reminder with confirmation"""
        reply = QMessageBox.question(self, 'Deactivate Reminder', 
                                   'Are you sure you want to deactivate this reminder?\n\n'
                                   'It will no longer appear in your active reminders.',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE care_reminders SET is_active = 0 WHERE id = ?', (reminder_id,))
                conn.commit()
                
                QMessageBox.information(self, 'Success', 'Reminder deactivated successfully!')
                self.refresh_reminders()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to deactivate reminder: {str(e)}')
    
    def closeEvent(self, event):
        """Clean up when screen closes"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()
    
    def go_back(self):
        """Return to home screen"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        self.main_window.show_screen('home')