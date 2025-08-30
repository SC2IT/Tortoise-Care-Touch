from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class HealthScreen(Screen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        back_btn = Button(text='← Back', size_hint_x=0.3)
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Health Records', font_size='20sp'))
        layout.add_widget(header_layout)
        
        # Placeholder content
        layout.add_widget(Label(text='Health monitoring features coming soon!\n\nWill include:\n• Vet visit records\n• Health observations\n• Medication tracking\n• Online health resources for Hermann\'s tortoises', font_size='16sp'))
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'home'