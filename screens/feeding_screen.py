from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from datetime import datetime

class FeedingScreen(Screen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.current_feeding_items = []
        self.build_ui()
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        back_btn = Button(text='← Back', size_hint_x=0.2, font_size='16sp')
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        
        title = Label(text='Feeding Tracker', font_size='20sp', size_hint_x=0.6)
        header_layout.add_widget(title)
        
        # Quick feed button for emergency/simple logging
        quick_btn = Button(
            text='Quick Feed', 
            size_hint_x=0.2, 
            font_size='16sp',
            background_color=(0.2, 0.6, 0.2, 1)
        )
        quick_btn.bind(on_press=self.quick_feed)
        header_layout.add_widget(quick_btn)
        
        main_layout.add_widget(header_layout)
        
        # Tortoise selection
        tortoise_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        tortoise_layout.add_widget(Label(text='Tortoise:', size_hint_x=0.2, font_size='16sp'))
        
        self.tortoise_spinner = Spinner(
            text='Select Tortoise',
            values=['Loading...'],
            size_hint_x=0.5,
            font_size='16sp'
        )
        tortoise_layout.add_widget(self.tortoise_spinner)
        
        self.user_spinner = Spinner(
            text='Select User',
            values=['Loading...'],
            size_hint_x=0.3,
            font_size='16sp'
        )
        tortoise_layout.add_widget(self.user_spinner)
        
        main_layout.add_widget(tortoise_layout)
        
        # Current feeding session
        session_layout = BoxLayout(orientation='vertical', size_hint_y=0.75, spacing=5)
        
        # Add food item section (portrait layout - 2 rows for better touch)
        add_item_layout = GridLayout(cols=2, rows=2, size_hint_y=0.2, spacing=5)
        
        self.plant_spinner = Spinner(
            text='Select Plant/Supplement',
            values=['Loading...'],
            font_size='14sp'
        )
        add_item_layout.add_widget(self.plant_spinner)
        
        self.weight_input = TextInput(
            hint_text='Weight (g)',
            multiline=False,
            input_filter='float',
            font_size='14sp'
        )
        add_item_layout.add_widget(self.weight_input)
        
        self.item_notes_input = TextInput(
            hint_text='Notes (optional)',
            multiline=False,
            font_size='14sp'
        )
        add_item_layout.add_widget(self.item_notes_input)
        
        add_btn = Button(
            text='Add Item',
            font_size='14sp',
            background_color=(0.2, 0.6, 0.2, 1)
        )
        add_btn.bind(on_press=self.add_feeding_item)
        add_item_layout.add_widget(add_btn)
        
        session_layout.add_widget(add_item_layout)
        
        # Current session items list
        self.items_scroll = ScrollView(size_hint_y=0.5)
        self.items_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.items_layout.bind(minimum_height=self.items_layout.setter('height'))
        self.items_scroll.add_widget(self.items_layout)
        session_layout.add_widget(self.items_scroll)
        
        # Session summary and notes
        summary_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        left_summary = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.total_weight_label = Label(text='Total: 0g', font_size='16sp')
        left_summary.add_widget(self.total_weight_label)
        
        ate_well_layout = BoxLayout(orientation='horizontal')
        ate_well_layout.add_widget(Label(text='Ate well:', font_size='14sp'))
        self.ate_well_checkbox = CheckBox(size_hint_x=0.3)
        ate_well_layout.add_widget(self.ate_well_checkbox)
        left_summary.add_widget(ate_well_layout)
        
        new_food_layout = BoxLayout(orientation='horizontal')
        new_food_layout.add_widget(Label(text='New food:', font_size='14sp'))
        self.new_food_checkbox = CheckBox(size_hint_x=0.3)
        new_food_layout.add_widget(self.new_food_checkbox)
        left_summary.add_widget(new_food_layout)
        
        summary_layout.add_widget(left_summary)
        
        self.session_notes_input = TextInput(
            hint_text='Session notes (behavior, new foods tried, etc.)',
            multiline=True,
            size_hint_x=0.7,
            font_size='14sp'
        )
        summary_layout.add_widget(self.session_notes_input)
        
        session_layout.add_widget(summary_layout)
        
        # Save session button
        save_btn = Button(
            text='Save Feeding Session',
            size_hint_y=0.1,
            font_size='18sp',
            background_color=(0.2, 0.6, 0.2, 1)
        )
        save_btn.bind(on_press=self.save_feeding_session)
        session_layout.add_widget(save_btn)
        
        main_layout.add_widget(session_layout)
        
        # Recent feedings button
        recent_btn = Button(
            text='View Recent Feedings',
            size_hint_y=0.07,
            font_size='16sp',
            background_color=(0.6, 0.6, 0.2, 1)
        )
        recent_btn.bind(on_press=self.show_recent_feedings)
        main_layout.add_widget(recent_btn)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.load_tortoises()
        self.load_users()
        self.load_plants()
    
    def load_tortoises(self):
        tortoises = self.db_manager.get_tortoises()
        tortoise_names = [t['name'] for t in tortoises]
        if tortoise_names:
            self.tortoise_spinner.values = tortoise_names
            self.tortoise_spinner.text = tortoise_names[0] if tortoise_names else 'No tortoises found'
        else:
            self.tortoise_spinner.values = ['No tortoises found']
            self.tortoise_spinner.text = 'No tortoises found'
    
    def load_users(self):
        users = self.db_manager.get_users()
        user_names = [u['name'] for u in users]
        if user_names:
            self.user_spinner.values = user_names
            self.user_spinner.text = user_names[0] if user_names else 'No users found'
        else:
            self.user_spinner.values = ['No users found']
            self.user_spinner.text = 'No users found'
    
    def load_plants(self):
        plants = self.db_manager.get_plants()
        plant_options = []
        
        # Add safe plants first
        safe_plants = [p['name'] for p in plants if p['safety_level'] == 'safe']
        plant_options.extend([f"🟢 {name}" for name in safe_plants])
        
        # Add caution plants
        caution_plants = [p['name'] for p in plants if p['safety_level'] == 'caution']
        plant_options.extend([f"🟡 {name}" for name in caution_plants])
        
        # Add common supplements
        supplements = ['Calcium Powder', 'Vitamin D3', 'Multivitamin', 'Cuttlebone']
        plant_options.extend([f"💊 {supp}" for supp in supplements])
        
        if plant_options:
            self.plant_spinner.values = plant_options
            self.plant_spinner.text = 'Select Plant/Supplement'
        else:
            self.plant_spinner.values = ['No plants found']
            self.plant_spinner.text = 'No plants found'
    
    def add_feeding_item(self, instance):
        if not self.plant_spinner.text or self.plant_spinner.text.startswith('Select') or self.plant_spinner.text.startswith('No'):
            self.show_popup('Error', 'Please select a plant or supplement')
            return
        
        if not self.weight_input.text:
            self.show_popup('Error', 'Please enter a weight')
            return
        
        try:
            weight = float(self.weight_input.text)
        except ValueError:
            self.show_popup('Error', 'Please enter a valid weight')
            return
        
        # Create item record
        item = {
            'plant': self.plant_spinner.text,
            'weight': weight,
            'notes': self.item_notes_input.text
        }
        
        self.current_feeding_items.append(item)
        self.update_items_display()
        self.update_total_weight()
        
        # Clear inputs
        self.weight_input.text = ''
        self.item_notes_input.text = ''
        self.plant_spinner.text = 'Select Plant/Supplement'
    
    def update_items_display(self):
        self.items_layout.clear_widgets()
        
        for i, item in enumerate(self.current_feeding_items):
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            
            # Item info
            info_text = f"{item['plant']} - {item['weight']}g"
            if item['notes']:
                info_text += f" ({item['notes']})"
            
            item_label = Label(
                text=info_text,
                size_hint_x=0.8,
                font_size='14sp',
                text_size=(None, None)
            )
            item_layout.add_widget(item_label)
            
            # Remove button
            remove_btn = Button(
                text='Remove',
                size_hint_x=0.2,
                font_size='12sp',
                background_color=(0.8, 0.2, 0.2, 1)
            )
            remove_btn.bind(on_press=lambda x, index=i: self.remove_item(index))
            item_layout.add_widget(remove_btn)
            
            self.items_layout.add_widget(item_layout)
    
    def remove_item(self, index):
        if 0 <= index < len(self.current_feeding_items):
            del self.current_feeding_items[index]
            self.update_items_display()
            self.update_total_weight()
    
    def update_total_weight(self):
        total = sum(item['weight'] for item in self.current_feeding_items)
        self.total_weight_label.text = f'Total: {total:.1f}g'
    
    def save_feeding_session(self, instance):
        if not self.current_feeding_items:
            self.show_popup('Error', 'Please add at least one feeding item')
            return
        
        if self.tortoise_spinner.text.startswith('Select') or self.tortoise_spinner.text.startswith('No'):
            self.show_popup('Error', 'Please select a tortoise')
            return
        
        if self.user_spinner.text.startswith('Select') or self.user_spinner.text.startswith('No'):
            self.show_popup('Error', 'Please select a user')
            return
        
        # TODO: Implement actual database saving
        # This is a placeholder for the database operations
        
        total_weight = sum(item['weight'] for item in self.current_feeding_items)
        
        success_msg = f"Feeding session saved!\n\n"
        success_msg += f"Tortoise: {self.tortoise_spinner.text}\n"
        success_msg += f"Fed by: {self.user_spinner.text}\n"
        success_msg += f"Total weight: {total_weight:.1f}g\n"
        success_msg += f"Items: {len(self.current_feeding_items)}\n"
        success_msg += f"Ate well: {'Yes' if self.ate_well_checkbox.active else 'No'}\n"
        success_msg += f"New food tried: {'Yes' if self.new_food_checkbox.active else 'No'}"
        
        self.show_popup('Success', success_msg)
        
        # Clear the session
        self.current_feeding_items = []
        self.update_items_display()
        self.update_total_weight()
        self.session_notes_input.text = ''
        self.ate_well_checkbox.active = False
        self.new_food_checkbox.active = False
    
    def quick_feed(self, instance):
        # Simple quick feeding popup for emergency situations
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text='Quick Feed Entry', font_size='18sp'))
        content.add_widget(Label(text='Tortoise:'))
        
        quick_tortoise = Spinner(values=self.tortoise_spinner.values, text=self.tortoise_spinner.text)
        content.add_widget(quick_tortoise)
        
        content.add_widget(Label(text='Approximate weight (g):'))
        quick_weight = TextInput(multiline=False, input_filter='float')
        content.add_widget(quick_weight)
        
        content.add_widget(Label(text='Quick notes:'))
        quick_notes = TextInput(multiline=True, height=100)
        content.add_widget(quick_notes)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = Button(text='Save', background_color=(0.2, 0.6, 0.2, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.6, 0.2, 0.2, 1))
        
        popup = Popup(
            title='Quick Feed',
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=False
        )
        
        def save_quick_feed(instance):
            # TODO: Save to database
            popup.dismiss()
            self.show_popup('Success', 'Quick feed entry saved!')
        
        def cancel_quick_feed(instance):
            popup.dismiss()
        
        save_btn.bind(on_press=save_quick_feed)
        cancel_btn.bind(on_press=cancel_quick_feed)
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup.open()
    
    def show_recent_feedings(self, instance):
        # TODO: Implement recent feedings view
        self.show_popup('Coming Soon', 'Recent feedings view will be implemented soon!')
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, text_size=(300, None), font_size='16sp'))
        
        close_btn = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'