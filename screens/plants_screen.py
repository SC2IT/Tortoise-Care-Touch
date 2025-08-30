from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import emoji
from screens.base_screen import BaseScreen

class PlantsScreen(BaseScreen):
    """
    Comprehensive plant database screen for tortoise-safe plants
    Based on extensive research and tortoise care guidelines
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
        self.current_filter = 'all'
        self.search_text = ''
    
    def build_ui(self):
        """Build plant database interface"""
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
            text=f'{emoji.emojize(":seedling:")} Plant Database',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Search and filter section
        filter_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        
        # Search bar
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.5, spacing=10)
        search_layout.add_widget(Label(
            text='Search:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.2
        ))
        
        self.search_input = TextInput(
            multiline=False,
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6,
            hint_text='Enter plant name...'
        )
        self.search_input.bind(text=self.on_search_text)
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text='Clear',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.2,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        search_btn.bind(on_press=self.clear_search)
        search_layout.add_widget(search_btn)
        
        filter_layout.add_widget(search_layout)
        
        # Filter buttons
        filter_buttons_layout = GridLayout(cols=4, size_hint_y=0.5, spacing=5)
        
        filter_buttons = [
            ('All Plants', 'all', (0.4, 0.4, 0.6, 1)),
            ('Safe Daily', 'safe', (0.2, 0.6, 0.2, 1)),
            ('Caution', 'caution', (0.8, 0.6, 0.2, 1)),
            ('Toxic - Never', 'toxic', (0.8, 0.2, 0.2, 1))
        ]
        
        for text, filter_type, color in filter_buttons:
            btn = Button(
                text=text,
                font_size=self.get_font_size('small'),
                background_color=color
            )
            btn.bind(on_press=lambda x, f=filter_type: self.set_filter(f))
            filter_buttons_layout.add_widget(btn)
        
        filter_layout.add_widget(filter_buttons_layout)
        main_layout.add_widget(filter_layout)
        
        # Plant stats summary
        self.stats_label = Label(
            text='Loading plant database...',
            font_size=self.get_font_size('small'),
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(self.stats_label)
        
        # Scrollable plants list
        self.plants_scroll = ScrollView(size_hint_y=0.7)
        self.plants_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.plants_layout.bind(minimum_height=self.plants_layout.setter('height'))
        self.plants_scroll.add_widget(self.plants_layout)
        main_layout.add_widget(self.plants_scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Load plants when screen is entered"""
        self.load_plants_list()
        self.update_stats()
    
    def on_search_text(self, instance, text):
        """Handle search text changes"""
        self.search_text = text.lower().strip()
        self.load_plants_list()
    
    def clear_search(self, instance):
        """Clear search text"""
        self.search_input.text = ''
        self.search_text = ''
        self.load_plants_list()
    
    def set_filter(self, filter_type):
        """Set plant safety filter"""
        self.current_filter = filter_type
        self.load_plants_list()
        self.update_stats()
    
    def load_plants_list(self):
        """Load and display plants based on current filter and search"""
        self.plants_layout.clear_widgets()
        
        # Get plants from database
        if self.current_filter == 'all':
            plants = self.db_manager.get_plants()
        else:
            plants = self.db_manager.get_plants(safety_level=self.current_filter)
        
        # Filter by search text
        if self.search_text:
            plants = [p for p in plants if 
                     self.search_text in p['name'].lower() or 
                     (p['scientific_name'] and self.search_text in p['scientific_name'].lower())]
        
        if not plants:
            no_plants_label = Label(
                text=f'No plants found for filter: {self.current_filter}' + 
                     (f' and search: "{self.search_text}"' if self.search_text else ''),
                font_size=self.get_font_size('medium'),
                size_hint_y=None,
                height=self.get_button_height(),
                color=(0.7, 0.7, 0.7, 1)
            )
            self.plants_layout.add_widget(no_plants_label)
            return
        
        # Group plants by feeding frequency for better organization
        grouped_plants = {}
        for plant in plants:
            freq = plant.get('feeding_frequency', 'unknown')
            if freq not in grouped_plants:
                grouped_plants[freq] = []
            grouped_plants[freq].append(plant)
        
        # Display plants by groups
        frequency_order = ['daily', '2-3 times per week', 'weekly', 'monthly', 'never', 'unknown']
        frequency_labels = {
            'daily': f'{emoji.emojize(":green_circle:")} Feed Daily',
            '2-3 times per week': f'{emoji.emojize(":yellow_circle:")} Feed Moderately', 
            'weekly': f'{emoji.emojize(":orange_circle:")} Weekly Treats',
            'monthly': f'{emoji.emojize(":red_circle:")} Rare/Caution',
            'never': f'{emoji.emojize(":cross_mark:")} Never Feed - TOXIC',
            'unknown': 'Other'
        }
        
        for freq in frequency_order:
            if freq in grouped_plants and grouped_plants[freq]:
                # Add frequency header
                freq_header = Label(
                    text=frequency_labels.get(freq, freq.title()),
                    font_size=self.get_font_size('medium'),
                    size_hint_y=None,
                    height=self.get_button_height() * 0.8,
                    color=(0.8, 0.8, 0.2, 1)
                )
                self.plants_layout.add_widget(freq_header)
                
                # Add plants in this frequency group
                for plant in sorted(grouped_plants[freq], key=lambda x: x['name']):
                    self.add_plant_item(plant)
    
    def add_plant_item(self, plant):
        """Add a plant item to the list"""
        plant_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=self.get_button_height() * 1.8,
            spacing=10
        )
        
        # Safety indicator
        safety_colors = {
            'safe': (0.2, 0.6, 0.2, 1),
            'caution': (0.8, 0.6, 0.2, 1),
            'toxic': (0.8, 0.2, 0.2, 1)
        }
        
        safety_icons = {
            'safe': ':green_circle:',
            'caution': ':yellow_circle:',
            'toxic': ':cross_mark:'
        }
        
        safety_level = plant.get('safety_level', 'unknown')
        safety_icon = safety_icons.get(safety_level, ':question:')
        
        safety_btn = Button(
            text=emoji.emojize(safety_icon),
            font_size=self.get_font_size('large'),
            size_hint_x=0.1,
            background_color=safety_colors.get(safety_level, (0.5, 0.5, 0.5, 1))
        )
        safety_btn.bind(on_press=lambda x, p=plant: self.show_plant_details(p))
        plant_layout.add_widget(safety_btn)
        
        # Plant info
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.9)
        
        # Plant name
        name_label = Label(
            text=plant['name'],
            font_size=self.get_font_size('medium'),
            size_hint_y=0.4,
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        info_layout.add_widget(name_label)
        
        # Scientific name
        if plant.get('scientific_name'):
            scientific_label = Label(
                text=f"Scientific: {plant['scientific_name']}",
                font_size=self.get_font_size('small'),
                size_hint_y=0.25,
                halign='left',
                color=(0.6, 0.6, 0.6, 1),
                text_size=(None, None)
            )
            info_layout.add_widget(scientific_label)
        
        # Feeding frequency and safety
        freq_safety_text = f"Feeding: {plant.get('feeding_frequency', 'Unknown')} | Safety: {safety_level.title()}"
        freq_safety_label = Label(
            text=freq_safety_text,
            font_size=self.get_font_size('small'),
            size_hint_y=0.25,
            halign='left',
            color=(0.7, 0.7, 0.7, 1),
            text_size=(None, None)
        )
        info_layout.add_widget(freq_safety_label)
        
        # Nutrition notes preview
        if plant.get('nutrition_notes'):
            notes_preview = plant['nutrition_notes'][:60] + ('...' if len(plant['nutrition_notes']) > 60 else '')
            notes_label = Label(
                text=notes_preview,
                font_size=self.get_font_size('small'),
                size_hint_y=0.35,
                halign='left',
                color=(0.5, 0.5, 0.5, 1),
                text_size=(None, None)
            )
            info_layout.add_widget(notes_label)
        
        plant_layout.add_widget(info_layout)
        self.plants_layout.add_widget(plant_layout)
    
    def show_plant_details(self, plant):
        """Show detailed plant information popup"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Plant name and scientific name
        name_text = plant['name']
        if plant.get('scientific_name'):
            name_text += f"\n({plant['scientific_name']})"
        
        name_label = Label(
            text=name_text,
            font_size=self.get_font_size('large'),
            size_hint_y=None,
            height=self.get_button_height() * 1.2,
            halign='center'
        )
        content.add_widget(name_label)
        
        # Safety and feeding info
        safety_level = plant.get('safety_level', 'unknown')
        safety_colors = {
            'safe': '[color=00ff00]SAFE[/color]',
            'caution': '[color=ffaa00]CAUTION[/color]',
            'toxic': '[color=ff0000]TOXIC - NEVER FEED[/color]'
        }
        
        safety_text = f"Safety Level: {safety_colors.get(safety_level, safety_level.upper())}\n"
        safety_text += f"Feeding Frequency: {plant.get('feeding_frequency', 'Unknown')}"
        
        safety_label = Label(
            text=safety_text,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 1.5,
            markup=True,
            halign='center'
        )
        content.add_widget(safety_label)
        
        # Nutrition notes
        if plant.get('nutrition_notes'):
            notes_label = Label(
                text=f"Nutrition & Notes:\n{plant['nutrition_notes']}",
                font_size=self.get_font_size('medium'),
                text_size=(400, None),
                halign='left'
            )
            content.add_widget(notes_label)
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title=f'Plant Information',
            content=content,
            size_hint=(0.9, 0.8),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def update_stats(self):
        """Update plant database statistics"""
        all_plants = self.db_manager.get_plants()
        safe_plants = self.db_manager.get_plants('safe')
        caution_plants = self.db_manager.get_plants('caution') 
        toxic_plants = self.db_manager.get_plants('toxic')
        
        stats_text = f"Total: {len(all_plants)} plants | "
        stats_text += f"Safe: {len(safe_plants)} | "
        stats_text += f"Caution: {len(caution_plants)} | "
        stats_text += f"Toxic: {len(toxic_plants)}"
        
        if hasattr(self, 'stats_label'):
            self.stats_label.text = stats_text
    
    def go_back(self, instance):
        """Return to home screen"""
        self.manager.current = 'home'