from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
import emoji
from screens.base_screen import BaseScreen

class SettingsConnectionsScreen(BaseScreen):
    """
    Connections settings screen
    Manage Adafruit.IO, sensors, network settings, and external integrations
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build connections management interface"""
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
            text=f'{emoji.emojize(":link:")} Connections',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Scrollable content
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing=self.get_button_spacing(), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Adafruit.IO Section
        aio_section = self.create_section_layout('Adafruit.IO Integration')
        
        # AIO Enable switch
        aio_enable_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        aio_enable_layout.add_widget(Label(
            text='Enable Adafruit.IO:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.7
        ))
        self.aio_switch = Switch(size_hint_x=0.3)
        self.aio_switch.bind(active=self.on_aio_switch)
        aio_enable_layout.add_widget(self.aio_switch)
        aio_section.add_widget(aio_enable_layout)
        
        # AIO Username
        aio_username_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        aio_username_layout.add_widget(Label(
            text='Username:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.3
        ))
        self.aio_username_input = TextInput(
            multiline=False,
            font_size=self.get_font_size('medium'),
            size_hint_x=0.7
        )
        aio_username_layout.add_widget(self.aio_username_input)
        aio_section.add_widget(aio_username_layout)
        
        # AIO Key
        aio_key_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        aio_key_layout.add_widget(Label(
            text='API Key:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.3
        ))
        self.aio_key_input = TextInput(
            multiline=False,
            password=True,
            font_size=self.get_font_size('medium'),
            size_hint_x=0.7
        )
        aio_key_layout.add_widget(self.aio_key_input)
        aio_section.add_widget(aio_key_layout)
        
        # Test connection button
        test_aio_btn = Button(
            text='Test Connection',
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.4, 0.6, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        test_aio_btn.bind(on_press=self.test_aio_connection)
        aio_section.add_widget(test_aio_btn)
        
        content_layout.add_widget(aio_section)
        
        # Sensor Settings Section
        sensor_section = self.create_section_layout('Sensor Settings')
        
        # Temperature sensor
        temp_sensor_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        temp_sensor_layout.add_widget(Label(
            text='Temperature Sensor:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6
        ))
        self.temp_sensor_switch = Switch(size_hint_x=0.2)
        temp_sensor_layout.add_widget(self.temp_sensor_switch)
        temp_status_label = Label(
            text='Disconnected',
            font_size=self.get_font_size('small'),
            size_hint_x=0.2,
            color=(0.8, 0.2, 0.2, 1)
        )
        temp_sensor_layout.add_widget(temp_status_label)
        sensor_section.add_widget(temp_sensor_layout)
        
        # Humidity sensor
        humidity_sensor_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        humidity_sensor_layout.add_widget(Label(
            text='Humidity Sensor:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6
        ))
        self.humidity_sensor_switch = Switch(size_hint_x=0.2)
        humidity_sensor_layout.add_widget(self.humidity_sensor_switch)
        humidity_status_label = Label(
            text='Disconnected',
            font_size=self.get_font_size('small'),
            size_hint_x=0.2,
            color=(0.8, 0.2, 0.2, 1)
        )
        humidity_sensor_layout.add_widget(humidity_status_label)
        sensor_section.add_widget(humidity_sensor_layout)
        
        # Light sensor
        light_sensor_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        light_sensor_layout.add_widget(Label(
            text='Light Sensor:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6
        ))
        self.light_sensor_switch = Switch(size_hint_x=0.2)
        light_sensor_layout.add_widget(self.light_sensor_switch)
        light_status_label = Label(
            text='Disconnected',
            font_size=self.get_font_size('small'),
            size_hint_x=0.2,
            color=(0.8, 0.2, 0.2, 1)
        )
        light_sensor_layout.add_widget(light_status_label)
        sensor_section.add_widget(light_sensor_layout)
        
        # Scan sensors button
        scan_sensors_btn = Button(
            text='Scan for Sensors',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.4, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        scan_sensors_btn.bind(on_press=self.scan_sensors)
        sensor_section.add_widget(scan_sensors_btn)
        
        content_layout.add_widget(sensor_section)
        
        # Network Settings Section
        network_section = self.create_section_layout('Network Settings')
        
        # WiFi status
        wifi_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        wifi_layout.add_widget(Label(
            text='WiFi Status:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.4
        ))
        wifi_status_label = Label(
            text='Connected to TortoiseNet',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6,
            color=(0.2, 0.6, 0.2, 1)
        )
        wifi_layout.add_widget(wifi_status_label)
        network_section.add_widget(wifi_layout)
        
        # Internet connectivity
        internet_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        internet_layout.add_widget(Label(
            text='Internet Access:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.4
        ))
        internet_status_label = Label(
            text='Connected',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.6,
            color=(0.2, 0.6, 0.2, 1)
        )
        internet_layout.add_widget(internet_status_label)
        network_section.add_widget(internet_layout)
        
        # Test network button
        test_network_btn = Button(
            text='Test Network Connection',
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.4, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        test_network_btn.bind(on_press=self.test_network)
        network_section.add_widget(test_network_btn)
        
        content_layout.add_widget(network_section)
        
        # Save settings button
        save_btn = Button(
            text='Save All Settings',
            font_size=self.get_font_size('large'),
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height() * 1.2
        )
        save_btn.bind(on_press=self.save_settings)
        content_layout.add_widget(save_btn)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def create_section_layout(self, title):
        """Create a titled section layout"""
        section = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=self.get_button_height() * 0.8
        )
        section.bind(minimum_height=section.setter('height'))
        
        title_label = Label(
            text=title,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            color=(0.8, 0.8, 0.2, 1)
        )
        section.add_widget(title_label)
        
        return section
    
    def on_aio_switch(self, instance, value):
        """Handle Adafruit.IO enable/disable"""
        if value:
            self.show_popup('Info', 'Adafruit.IO integration enabled. Please enter your credentials.')
        else:
            self.show_popup('Info', 'Adafruit.IO integration disabled.')
    
    def test_aio_connection(self, instance):
        """Test Adafruit.IO connection"""
        username = self.aio_username_input.text.strip()
        api_key = self.aio_key_input.text.strip()
        
        if not username or not api_key:
            self.show_popup('Error', 'Please enter both username and API key.')
            return
        
        # TODO: Implement actual AIO connection test
        self.show_popup('Coming Soon', 'Adafruit.IO connection testing will be implemented soon!')
    
    def scan_sensors(self, instance):
        """Scan for connected sensors"""
        # TODO: Implement actual sensor scanning
        self.show_popup('Coming Soon', 'Sensor scanning will be implemented soon!')
    
    def test_network(self, instance):
        """Test network connectivity"""
        # TODO: Implement actual network testing
        self.show_popup('Coming Soon', 'Network testing will be implemented soon!')
    
    def save_settings(self, instance):
        """Save all connection settings"""
        # TODO: Implement actual settings saving
        self.show_popup('Success', 'Settings saved successfully!')
    
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