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

class SettingsTortoisesScreen(BaseScreen):
    """
    Tortoise management settings screen
    Add/edit tortoises, manage profiles, view detailed info
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build tortoise management interface"""
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
            text=f'{emoji.emojize(":turtle:")} Tortoise Management',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Add new tortoise section
        add_tortoise_layout = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=10)
        
        add_tortoise_title = Label(
            text='Add New Tortoise',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 0.6
        )
        add_tortoise_layout.add_widget(add_tortoise_title)
        
        # Tortoise input fields
        input_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=self.get_button_height() * 4)
        
        input_grid.add_widget(Label(text='Name:', font_size=self.get_font_size('medium')))
        self.name_input = TextInput(
            multiline=False,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.name_input)
        
        input_grid.add_widget(Label(text='Species:', font_size=self.get_font_size('medium')))
        self.species_spinner = Spinner(
            text='Select Species',
            values=['Hermann\'s Tortoise', 'Russian Tortoise', 'Greek Tortoise', 'Horsfield\'s Tortoise', 'Other'],
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.species_spinner)
        
        input_grid.add_widget(Label(text='Age (years):', font_size=self.get_font_size('medium')))
        self.age_input = TextInput(
            multiline=False,
            input_filter='float',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.age_input)
        
        input_grid.add_widget(Label(text='Weight (g):', font_size=self.get_font_size('medium')))
        self.weight_input = TextInput(
            multiline=False,
            input_filter='float',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.weight_input)
        
        input_grid.add_widget(Label(text='Gender:', font_size=self.get_font_size('medium')))
        self.gender_spinner = Spinner(
            text='Select Gender',
            values=['Male', 'Female', 'Unknown'],
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.gender_spinner)
        
        input_grid.add_widget(Label(text='Notes:', font_size=self.get_font_size('medium')))
        self.notes_input = TextInput(
            multiline=True,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        input_grid.add_widget(self.notes_input)
        
        add_tortoise_layout.add_widget(input_grid)
        
        # Add tortoise button
        add_btn = Button(
            text='Add Tortoise',
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        add_btn.bind(on_press=self.add_tortoise)
        add_tortoise_layout.add_widget(add_btn)
        
        main_layout.add_widget(add_tortoise_layout)
        
        # Existing tortoises list
        tortoises_title = Label(
            text='Current Tortoises',
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 0.6
        )
        main_layout.add_widget(tortoises_title)
        
        # Scrollable tortoises list
        self.tortoises_scroll = ScrollView(size_hint_y=0.5)
        self.tortoises_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.tortoises_layout.bind(minimum_height=self.tortoises_layout.setter('height'))
        self.tortoises_scroll.add_widget(self.tortoises_layout)
        main_layout.add_widget(self.tortoises_scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Load tortoises when screen is entered"""
        self.load_tortoises_list()
    
    def load_tortoises_list(self):
        """Load and display current tortoises"""
        self.tortoises_layout.clear_widgets()
        
        tortoises = self.db_manager.get_tortoises()
        
        if not tortoises:
            no_tortoises_label = Label(
                text='No tortoises found. Add your first tortoise above.',
                font_size=self.get_font_size('medium'),
                size_hint_y=None,
                height=self.get_button_height(),
                color=(0.7, 0.7, 0.7, 1)
            )
            self.tortoises_layout.add_widget(no_tortoises_label)
            return
        
        for tortoise in tortoises:
            tortoise_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=self.get_button_height() * 1.5,
                spacing=10
            )
            
            # Tortoise info
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
            
            name_label = Label(
                text=tortoise['name'],
                font_size=self.get_font_size('medium'),
                size_hint_y=0.4,
                halign='left',
                text_size=(None, None)
            )
            info_layout.add_widget(name_label)
            
            species_label = Label(
                text=f"Species: {tortoise.get('species', 'Unknown')}",
                font_size=self.get_font_size('small'),
                size_hint_y=0.3,
                halign='left',
                color=(0.7, 0.7, 0.7, 1),
                text_size=(None, None)
            )
            info_layout.add_widget(species_label)
            
            age_weight_label = Label(
                text=f"Age: {tortoise.get('age', 'Unknown')} years, Weight: {tortoise.get('weight', 'Unknown')}g",
                font_size=self.get_font_size('small'),
                size_hint_y=0.3,
                halign='left',
                color=(0.7, 0.7, 0.7, 1),
                text_size=(None, None)
            )
            info_layout.add_widget(age_weight_label)
            
            tortoise_layout.add_widget(info_layout)
            
            # Edit button
            edit_btn = Button(
                text='Edit',
                font_size=self.get_font_size('small'),
                size_hint_x=0.15,
                background_color=(0.6, 0.6, 0.2, 1)
            )
            edit_btn.bind(on_press=lambda x, tortoise_id=tortoise['id']: self.edit_tortoise(tortoise_id))
            tortoise_layout.add_widget(edit_btn)
            
            # Delete button
            delete_btn = Button(
                text='Delete',
                font_size=self.get_font_size('small'),
                size_hint_x=0.15,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            delete_btn.bind(on_press=lambda x, tortoise_id=tortoise['id']: self.delete_tortoise(tortoise_id))
            tortoise_layout.add_widget(delete_btn)
            
            self.tortoises_layout.add_widget(tortoise_layout)
    
    def add_tortoise(self, instance):
        """Add a new tortoise"""
        name = self.name_input.text.strip()
        species = self.species_spinner.text
        age = self.age_input.text.strip()
        weight = self.weight_input.text.strip()
        gender = self.gender_spinner.text
        notes = self.notes_input.text.strip()
        
        if not name:
            self.show_popup('Error', 'Please enter a name for the tortoise.')
            return
        
        if species == 'Select Species':
            self.show_popup('Error', 'Please select a species.')
            return
        
        try:
            # Validate age and weight if provided
            if age:
                float(age)
            if weight:
                float(weight)
                
            # TODO: Implement actual database saving
            # For now, show success message
            self.show_popup('Success', f'Tortoise "{name}" added successfully!')
            
            # Clear inputs
            self.name_input.text = ''
            self.species_spinner.text = 'Select Species'
            self.age_input.text = ''
            self.weight_input.text = ''
            self.gender_spinner.text = 'Select Gender'
            self.notes_input.text = ''
            
            # Refresh tortoises list
            self.load_tortoises_list()
            
        except ValueError:
            self.show_popup('Error', 'Please enter valid numbers for age and weight.')
        except Exception as e:
            self.show_popup('Error', f'Failed to add tortoise: {str(e)}')
    
    def edit_tortoise(self, tortoise_id):
        """Edit existing tortoise"""
        self.show_popup('Coming Soon', 'Tortoise editing will be implemented soon!')
    
    def delete_tortoise(self, tortoise_id):
        """Delete tortoise with confirmation"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        msg_label = Label(
            text='Are you sure you want to delete this tortoise?\nThis will also delete all associated feeding and health records!\nThis action cannot be undone.',
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
            size_hint=(0.8, 0.7),
            title_size=self.get_font_size('large')
        )
        
        def confirm_delete(instance):
            # TODO: Implement actual database deletion
            popup.dismiss()
            self.show_popup('Success', 'Tortoise deleted successfully!')
            self.load_tortoises_list()
        
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