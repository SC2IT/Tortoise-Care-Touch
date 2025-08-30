from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import emoji
from screens.base_screen import BaseScreen

class SettingsUsersScreen(BaseScreen):
    """
    User management settings screen
    Add/edit users, assign roles, manage access levels
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build user management interface"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=self.get_button_spacing())
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=self.get_header_height())
        
        back_btn = Button(
            text='← Back',
            size_hint_x=0.25,
            font_size=self.get_font_size('medium'),
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        
        title = Label(
            text=f'{emoji.emojize(":busts_in_silhouette:")} User Management',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Add new user section
        add_user_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10)
        
        add_user_title = Label(
            text='Add New User',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 0.6
        )
        add_user_layout.add_widget(add_user_title)
        
        # User input fields
        input_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=self.get_button_height() * 2.5)
        
        input_grid.add_widget(Label(text='Name:', font_size=self.get_font_size('medium')))
        self.name_input = TextInput(
            multiline=False,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.name_input)
        
        input_grid.add_widget(Label(text='Role:', font_size=self.get_font_size('medium')))
        self.role_spinner = Spinner(
            text='Select Role',
            values=['Primary Caregiver', 'Secondary Caregiver', 'Observer', 'Veterinarian'],
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.role_spinner)
        
        input_grid.add_widget(Label(text='Notes:', font_size=self.get_font_size('medium')))
        self.notes_input = TextInput(
            multiline=True,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.notes_input)
        
        add_user_layout.add_widget(input_grid)
        
        # Add user button
        add_btn = Button(
            text='Add User',
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        add_btn.bind(on_press=self.add_user)
        add_user_layout.add_widget(add_btn)
        
        main_layout.add_widget(add_user_layout)
        
        # Existing users list
        users_title = Label(
            text='Current Users',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 0.6
        )
        main_layout.add_widget(users_title)
        
        # Scrollable users list
        self.users_scroll = ScrollView(size_hint_y=0.6)
        self.users_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.users_layout.bind(minimum_height=self.users_layout.setter('height'))
        self.users_scroll.add_widget(self.users_layout)
        main_layout.add_widget(self.users_scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Load users when screen is entered"""
        self.load_users_list()
    
    def load_users_list(self):
        """Load and display current users"""
        self.users_layout.clear_widgets()
        
        users = self.db_manager.get_users()
        
        if not users:
            no_users_label = Label(
                text='No users found. Add your first user above.',
                font_size=self.get_font_size('medium'),
                size_hint_y=None,
                height=self.get_button_height(),
                color=(0.7, 0.7, 0.7, 1)
            )
            self.users_layout.add_widget(no_users_label)
            return
        
        for user in users:
            user_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=self.get_button_height() * 1.2,
                spacing=10
            )
            
            # User info
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
            
            name_label = Label(
                text=user['name'],
                font_size=self.get_font_size('medium'),
                size_hint_y=0.6,
                halign='left',
                text_size=(None, None)
            )
            info_layout.add_widget(name_label)
            
            role_label = Label(
                text=f"Role: {user.get('role', 'Unknown')}",
                font_size=self.get_font_size('small'),
                size_hint_y=0.4,
                halign='left',
                color=(0.7, 0.7, 0.7, 1),
                text_size=(None, None)
            )
            info_layout.add_widget(role_label)
            
            user_layout.add_widget(info_layout)
            
            # Edit button
            edit_btn = Button(
                text='Edit',
                font_size=self.get_font_size('small'),
                size_hint_x=0.15,
                background_color=(0.6, 0.6, 0.2, 1)
            )
            edit_btn.bind(on_press=lambda x, user_id=user['id']: self.edit_user(user_id))
            user_layout.add_widget(edit_btn)
            
            # Delete button
            delete_btn = Button(
                text='Delete',
                font_size=self.get_font_size('small'),
                size_hint_x=0.15,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            delete_btn.bind(on_press=lambda x, user_id=user['id']: self.delete_user(user_id))
            user_layout.add_widget(delete_btn)
            
            self.users_layout.add_widget(user_layout)
    
    def add_user(self, instance):
        """Add a new user"""
        name = self.name_input.text.strip()
        role = self.role_spinner.text
        notes = self.notes_input.text.strip()
        
        if not name:
            self.show_popup('Error', 'Please enter a name for the user.')
            return
        
        if role == 'Select Role':
            self.show_popup('Error', 'Please select a role for the user.')
            return
        
        try:
            # TODO: Implement actual database saving
            # For now, show success message
            self.show_popup('Success', f'User "{name}" added successfully!')
            
            # Clear inputs
            self.name_input.text = ''
            self.role_spinner.text = 'Select Role'
            self.notes_input.text = ''
            
            # Refresh users list
            self.load_users_list()
            
        except Exception as e:
            self.show_popup('Error', f'Failed to add user: {str(e)}')
    
    def edit_user(self, user_id):
        """Edit existing user"""
        self.show_popup('Coming Soon', 'User editing will be implemented soon!')
    
    def delete_user(self, user_id):
        """Delete user with confirmation"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        msg_label = Label(
            text='Are you sure you want to delete this user?\nThis action cannot be undone.',
            text_size=(400, None),
            font_size=self.get_font_size('medium'),
            halign='center'
        )
        content.add_widget(msg_label)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=self.get_button_height())
        
        cancel_btn = Button(
            text='Cancel',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        
        delete_btn = Button(
            text='Delete',
            font_size=self.get_font_size('medium'),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        popup = Popup(
            title='Confirm Delete',
            content=content,
            size_hint=(0.8, 0.6),
            title_size=self.get_font_size('large')
        )
        
        def confirm_delete(instance):
            # TODO: Implement actual database deletion
            popup.dismiss()
            self.show_popup('Success', 'User deleted successfully!')
            self.load_users_list()
        
        def cancel_delete(instance):
            popup.dismiss()
        
        cancel_btn.bind(on_press=cancel_delete)
        delete_btn.bind(on_press=confirm_delete)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(delete_btn)
        content.add_widget(button_layout)
        
        popup.open()
    
    def show_popup(self, title, message):
        """Show information popup"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        msg_label = Label(
            text=message,
            text_size=(400, None),
            font_size=self.get_font_size('medium'),
            halign='center'
        )
        content.add_widget(msg_label)
        
        close_btn = Button(
            text='OK',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.6),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        """Return to main settings screen"""
        self.manager.current = 'settings_main'