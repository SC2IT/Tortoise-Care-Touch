from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

class SettingsScreen(Screen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.build_ui()
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        back_btn = Button(text='← Back', size_hint_x=0.2, font_size='16sp')
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Settings', font_size='20sp'))
        main_layout.add_widget(header_layout)
        
        # Settings sections
        scroll = ScrollView()
        settings_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        settings_layout.bind(minimum_height=settings_layout.setter('height'))
        
        # User Management Section
        user_section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=300)
        user_section.add_widget(Label(text='User Management', font_size='18sp', size_hint_y=None, height=40, color=(0.2, 0.6, 0.2, 1)))
        
        # Current users list
        self.users_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.users_layout.bind(minimum_height=self.users_layout.setter('height'))
        user_section.add_widget(self.users_layout)
        
        # Add new user
        add_user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.new_user_input = TextInput(
            hint_text='Enter new user name',
            multiline=False,
            font_size='14sp',
            size_hint_x=0.6
        )
        add_user_layout.add_widget(self.new_user_input)
        
        add_user_btn = Button(
            text='Add User',
            size_hint_x=0.4,
            font_size='14sp',
            background_color=(0.2, 0.6, 0.2, 1)
        )
        add_user_btn.bind(on_press=self.add_user)
        add_user_layout.add_widget(add_user_btn)
        
        user_section.add_widget(add_user_layout)
        settings_layout.add_widget(user_section)
        
        # Tortoise Management Section
        tortoise_section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=300)
        tortoise_section.add_widget(Label(text='Tortoise Management', font_size='18sp', size_hint_y=None, height=40, color=(0.6, 0.4, 0.2, 1)))
        
        # Current tortoises list
        self.tortoises_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.tortoises_layout.bind(minimum_height=self.tortoises_layout.setter('height'))
        tortoise_section.add_widget(self.tortoises_layout)
        
        # Add new tortoise button
        add_tortoise_btn = Button(
            text='Add New Tortoise',
            size_hint_y=None,
            height=50,
            font_size='16sp',
            background_color=(0.6, 0.4, 0.2, 1)
        )
        add_tortoise_btn.bind(on_press=self.add_tortoise)
        tortoise_section.add_widget(add_tortoise_btn)
        
        settings_layout.add_widget(tortoise_section)
        
        # Adafruit.IO Section
        aio_section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        aio_section.add_widget(Label(text='Adafruit.IO Settings', font_size='18sp', size_hint_y=None, height=40, color=(0.2, 0.2, 0.6, 1)))
        
        # API Key input
        aio_key_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        aio_key_layout.add_widget(Label(text='API Key:', size_hint_x=0.3))
        self.aio_key_input = TextInput(
            hint_text='Your Adafruit.IO API Key',
            password=True,
            multiline=False,
            font_size='12sp',
            size_hint_x=0.7
        )
        aio_key_layout.add_widget(self.aio_key_input)
        aio_section.add_widget(aio_key_layout)
        
        # Username input
        aio_user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        aio_user_layout.add_widget(Label(text='Username:', size_hint_x=0.3))
        self.aio_user_input = TextInput(
            hint_text='Your Adafruit.IO Username',
            multiline=False,
            font_size='12sp',
            size_hint_x=0.7
        )
        aio_user_layout.add_widget(self.aio_user_input)
        aio_section.add_widget(aio_user_layout)
        
        # Save AIO settings button
        save_aio_btn = Button(
            text='Save Adafruit.IO Settings',
            size_hint_y=None,
            height=50,
            font_size='14sp',
            background_color=(0.2, 0.2, 0.6, 1)
        )
        save_aio_btn.bind(on_press=self.save_aio_settings)
        aio_section.add_widget(save_aio_btn)
        
        settings_layout.add_widget(aio_section)
        
        scroll.add_widget(settings_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.refresh_users()
        self.refresh_tortoises()
        self.load_aio_settings()
    
    def refresh_users(self):
        self.users_layout.clear_widgets()
        users = self.db_manager.get_users()
        
        for user in users:
            user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            user_label = Label(
                text=f"{user['name']} ({user['email'] or 'No email'})",
                font_size='14sp',
                size_hint_x=0.6
            )
            user_layout.add_widget(user_label)
            
            # Task assignment button
            assign_btn = Button(
                text='Assign Tasks',
                size_hint_x=0.25,
                font_size='12sp',
                background_color=(0.4, 0.6, 0.4, 1)
            )
            assign_btn.bind(on_press=lambda x, user_id=user['id'], name=user['name']: self.assign_tasks(user_id, name))
            user_layout.add_widget(assign_btn)
            
            # Delete button (only if not last user)
            if len(users) > 1:
                delete_btn = Button(
                    text='Delete',
                    size_hint_x=0.15,
                    font_size='12sp',
                    background_color=(0.8, 0.2, 0.2, 1)
                )
                delete_btn.bind(on_press=lambda x, user_id=user['id'], name=user['name']: self.delete_user(user_id, name))
                user_layout.add_widget(delete_btn)
            
            self.users_layout.add_widget(user_layout)
    
    def refresh_tortoises(self):
        self.tortoises_layout.clear_widgets()
        tortoises = self.db_manager.get_tortoises()
        
        for tortoise in tortoises:
            tortoise_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            tortoise_info = f"{tortoise['name']} ({tortoise['species']})"
            if tortoise['current_weight']:
                tortoise_info += f" - {tortoise['current_weight']}g"
            
            tortoise_label = Label(
                text=tortoise_info,
                font_size='14sp',
                size_hint_x=0.8
            )
            tortoise_layout.add_widget(tortoise_label)
            
            edit_btn = Button(
                text='Edit',
                size_hint_x=0.2,
                font_size='12sp',
                background_color=(0.6, 0.6, 0.2, 1)
            )
            edit_btn.bind(on_press=lambda x, t_id=tortoise['id']: self.edit_tortoise(t_id))
            tortoise_layout.add_widget(edit_btn)
            
            self.tortoises_layout.add_widget(tortoise_layout)
    
    def load_aio_settings(self):
        aio_key = self.db_manager.get_setting('adafruit_io_key')
        aio_user = self.db_manager.get_setting('adafruit_io_username')
        
        if aio_key:
            self.aio_key_input.text = aio_key
        if aio_user:
            self.aio_user_input.text = aio_user
    
    def add_user(self, instance):
        name = self.new_user_input.text.strip()
        if not name:
            self.show_popup('Error', 'Please enter a user name')
            return
        
        try:
            self.db_manager.add_user(name)
            self.new_user_input.text = ''
            self.refresh_users()
            self.show_popup('Success', f'User "{name}" added successfully!')
        except Exception as e:
            self.show_popup('Error', f'Failed to add user: {str(e)}')
    
    def delete_user(self, user_id, name):
        # Confirmation popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'Are you sure you want to delete user "{name}"?', font_size='16sp'))
        content.add_widget(Label(text='This cannot be undone!', font_size='14sp', color=(0.8, 0.2, 0.2, 1)))
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        confirm_btn = Button(text='Delete', background_color=(0.8, 0.2, 0.2, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.6, 0.6, 0.6, 1))
        
        popup = Popup(
            title='Confirm Delete',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        def do_delete(instance):
            try:
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
                conn.commit()
                popup.dismiss()
                self.refresh_users()
                self.show_popup('Success', f'User "{name}" deleted')
            except Exception as e:
                popup.dismiss()
                self.show_popup('Error', f'Failed to delete user: {str(e)}')
        
        confirm_btn.bind(on_press=do_delete)
        cancel_btn.bind(on_press=popup.dismiss)
        
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup.open()
    
    def assign_tasks(self, user_id, username):
        self.show_task_assignment_popup(user_id, username)
    
    def show_task_assignment_popup(self, user_id, username):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'Assign Tasks to {username}', font_size='18sp', size_hint_y=None, height=40))
        
        # Task type spinner
        task_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        task_layout.add_widget(Label(text='Task Type:', size_hint_x=0.3))
        task_spinner = Spinner(
            text='Select Task Type',
            values=['Daily Feeding', 'Weekly Cleaning', 'Monthly Weight Check', 'Vet Appointment', 'Habitat Check', 'Custom Task'],
            size_hint_x=0.7
        )
        task_layout.add_widget(task_spinner)
        content.add_widget(task_layout)
        
        # Tortoise selection
        tortoise_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        tortoise_layout.add_widget(Label(text='Tortoise:', size_hint_x=0.3))
        tortoise_spinner = Spinner(
            text='Select Tortoise',
            values=[t['name'] for t in self.db_manager.get_tortoises()],
            size_hint_x=0.7
        )
        tortoise_layout.add_widget(tortoise_spinner)
        content.add_widget(tortoise_layout)
        
        # Frequency
        freq_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        freq_layout.add_widget(Label(text='Frequency:', size_hint_x=0.3))
        freq_spinner = Spinner(
            text='Select Frequency',
            values=['Daily', 'Weekly', 'Monthly', 'Once'],
            size_hint_x=0.7
        )
        freq_layout.add_widget(freq_spinner)
        content.add_widget(freq_layout)
        
        # Custom task name (if custom selected)
        task_name_input = TextInput(
            hint_text='Custom task name (if Custom Task selected)',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        content.add_widget(task_name_input)
        
        # Description
        desc_input = TextInput(
            hint_text='Task description or notes',
            multiline=True,
            size_hint_y=None,
            height=80
        )
        content.add_widget(desc_input)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = Button(text='Assign Task', background_color=(0.2, 0.6, 0.2, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.6, 0.6, 0.6, 1))
        
        popup = Popup(
            title='Task Assignment',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        def save_task(instance):
            if task_spinner.text.startswith('Select'):
                self.show_popup('Error', 'Please select a task type')
                return
            
            task_name = task_spinner.text
            if task_spinner.text == 'Custom Task':
                if not task_name_input.text.strip():
                    self.show_popup('Error', 'Please enter a custom task name')
                    return
                task_name = task_name_input.text.strip()
            
            # TODO: Save to database
            popup.dismiss()
            self.show_popup('Success', f'Task "{task_name}" assigned to {username}!')
        
        save_btn.bind(on_press=save_task)
        cancel_btn.bind(on_press=popup.dismiss)
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup.open()
    
    def add_tortoise(self, instance):
        self.show_add_tortoise_popup()
    
    def show_add_tortoise_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Add New Tortoise', font_size='18sp', size_hint_y=None, height=40))
        
        # Name
        name_input = TextInput(hint_text='Tortoise name', multiline=False, size_hint_y=None, height=50)
        content.add_widget(name_input)
        
        # Sex
        sex_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        sex_layout.add_widget(Label(text='Sex:', size_hint_x=0.3))
        sex_spinner = Spinner(
            text='Unknown',
            values=['Unknown', 'Male', 'Female'],
            size_hint_x=0.7
        )
        sex_layout.add_widget(sex_spinner)
        content.add_widget(sex_layout)
        
        # Current weight
        weight_input = TextInput(
            hint_text='Current weight (grams)',
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        content.add_widget(weight_input)
        
        # Notes
        notes_input = TextInput(
            hint_text='Notes (age, acquisition date, etc.)',
            multiline=True,
            size_hint_y=None,
            height=80
        )
        content.add_widget(notes_input)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = Button(text='Add Tortoise', background_color=(0.2, 0.6, 0.2, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.6, 0.6, 0.6, 1))
        
        popup = Popup(
            title='New Tortoise',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        def save_tortoise(instance):
            if not name_input.text.strip():
                self.show_popup('Error', 'Please enter a tortoise name')
                return
            
            try:
                kwargs = {
                    'sex': sex_spinner.text if sex_spinner.text != 'Unknown' else None,
                    'current_weight': float(weight_input.text) if weight_input.text else None,
                    'notes': notes_input.text.strip() if notes_input.text else None
                }
                
                self.db_manager.add_tortoise(name_input.text.strip(), **kwargs)
                popup.dismiss()
                self.refresh_tortoises()
                self.show_popup('Success', f'Tortoise "{name_input.text}" added successfully!')
                
            except ValueError:
                self.show_popup('Error', 'Please enter a valid weight')
            except Exception as e:
                self.show_popup('Error', f'Failed to add tortoise: {str(e)}')
        
        save_btn.bind(on_press=save_tortoise)
        cancel_btn.bind(on_press=popup.dismiss)
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup.open()
    
    def edit_tortoise(self, tortoise_id):
        self.show_popup('Coming Soon', 'Tortoise editing will be implemented soon!')
    
    def save_aio_settings(self, instance):
        try:
            self.db_manager.set_setting('adafruit_io_key', self.aio_key_input.text.strip())
            self.db_manager.set_setting('adafruit_io_username', self.aio_user_input.text.strip())
            self.show_popup('Success', 'Adafruit.IO settings saved!')
        except Exception as e:
            self.show_popup('Error', f'Failed to save settings: {str(e)}')
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, text_size=(400, None), font_size='16sp'))
        
        close_btn = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'