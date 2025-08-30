from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
import emoji
from screens.base_screen import BaseScreen

class AboutScreen(BaseScreen):
    """
    About screen with sources, attributions, and application information
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build about page interface"""
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
            text=f'{emoji.emojize(":information:")} About',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Scrollable content
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, padding=[0, 10])
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Application Information
        app_info = self.create_info_section(
            "Tortoise Care Touch v0.1.6-alpha",
            """A comprehensive care management application for Hermann's tortoises and other Mediterranean species.

Designed specifically for Raspberry Pi 4 with Pi Touch Display 2 (720x1280 resolution).

Features:
• Feeding tracking with comprehensive plant database
• Health monitoring and veterinary records
• Growth tracking with photo integration
• Habitat monitoring via Adafruit.IO
• Multi-user care management system
• Care reminders and task scheduling

This application is open source and available on GitHub.
Repository: github.com/SC2IT/Tortoise-Care-Touch"""
        )
        content_layout.add_widget(app_info)
        
        # Plant Database & Health Sources
        plant_sources = self.create_info_section(
            "Plant Database & Health Sources",
            """PLANT DATABASE SOURCES (60+ plants):
• The Tortoise Table (thetortoisetable.org.uk)
  - Comprehensive tortoise plant safety database
  - Scientific plant classifications and safety levels
  - Poisoning symptoms and emergency protocols

• Tortoise Trust (tortoisetrust.org)
  - Expert veterinary guidance on tortoise nutrition
  - Plant safety research and feeding recommendations
  - Species-specific dietary guidelines

• World Chelonian Trust
  - Mediterranean tortoise nutrition research
  - Habitat and dietary requirements

HEALTH MONITORING SOURCES:
• The Tortoise Table - Signs of Healthy Tortoise Guide
  - Physical health indicators (shell, eyes, respiratory)
  - Behavioral indicators (activity, waste, appetite)
  - Health monitoring recommendations

• The Tortoise Table - Poisoning Information
  - Acute and cumulative poisoning symptoms
  - Emergency protocols and prevention measures
  - Veterinary intervention guidelines

SCIENTIFIC & VETERINARY REFERENCES:
• Association of Reptilian and Amphibian Veterinarians (ARAV)
• European Association of Zoo and Wildlife Veterinarians
• Journal of Herpetological Medicine and Surgery
• Veterinary Clinics: Exotic Animal Practice
• Applied Animal Behaviour Science (reptile nutrition)

HERMANN'S TORTOISE SPECIFIC CARE:
• Tortoise Trust species care sheets
• World Chelonian Trust husbandry guidelines
• ARAV-certified exotic veterinary protocols

SAFETY CLASSIFICATIONS:
Plants: SAFE (daily), CAUTION (sparingly), TOXIC (never)
Health: Emergency protocols based on veterinary standards
All recommendations follow established tortoise care protocols."""
        )
        content_layout.add_widget(plant_sources)
        
        # Technical Acknowledgments
        tech_info = self.create_info_section(
            "Technical Framework & Libraries",
            """CORE FRAMEWORK:
• Python 3.11+ - Primary development language
• Kivy 2.3.0 - Cross-platform GUI framework optimized for touch interfaces
• SQLite3 - Local database for offline data storage

UI & DISPLAY:
• KivyMD 1.2.0 - Material Design components for Kivy
• Emoji 2.2.0+ - Unicode emoji rendering support
• Dynamic orientation detection for landscape/portrait modes

HARDWARE INTEGRATION:
• Raspberry Pi 4 optimization
• Pi Touch Display 2 (720x1280) touch interface
• Adafruit.IO integration for sensor monitoring
• GPIO sensor support for temperature/humidity monitoring

IMAGE PROCESSING:
• Pillow 10.0.0+ - Image processing for photo import
• Camera integration for growth tracking photos

NETWORKING:
• Requests 2.31.0+ - HTTP client for web integrations
• Python-dateutil 2.8.2+ - Date/time handling utilities

DEVELOPMENT TOOLS:
• Git version control
• GitHub repository hosting
• Raspberry Pi OS compatibility testing"""
        )
        content_layout.add_widget(tech_info)
        
        # Disclaimers and Legal
        disclaimer = self.create_info_section(
            "Disclaimer & Veterinary Advice",
            """IMPORTANT VETERINARY DISCLAIMER:
This application is designed as a care management tool and information resource. It is NOT a substitute for professional veterinary care.

ALWAYS consult with a qualified exotic animal veterinarian for:
• Health concerns or unusual behavior
• Dietary questions for sick or recovering tortoises
• Species-specific care requirements
• Emergency medical situations

PLANT SAFETY:
While our plant database is compiled from authoritative sources, individual tortoises may have different sensitivities. Always:
• Introduce new foods gradually
• Monitor your tortoise's response to new plants
• Consult your veterinarian if unsure about any plant
• Never feed plants you cannot positively identify

DATA ACCURACY:
Plant safety information is current as of the application release date. Veterinary knowledge evolves, and new research may update feeding recommendations.

LIABILITY:
The developers and contributors are not responsible for any adverse effects from using this application. Users assume full responsibility for their tortoise's care and feeding decisions."""
        )
        content_layout.add_widget(disclaimer)
        
        # Credits and Attribution
        credits = self.create_info_section(
            "Development & Attribution",
            """DEVELOPMENT:
• Primary Developer: Claude (Anthropic AI Assistant)
• Project Coordination: User-guided development
• Testing Environment: Raspberry Pi 4 with Pi Touch Display 2

SPECIAL THANKS:
• The Tortoise Table team for their comprehensive plant database
• The Tortoise Trust for decades of reptile care research
• Raspberry Pi Foundation for accessible computing hardware
• Kivy development team for excellent touch interface framework
• The Python community for robust libraries and tools

INSPIRATION:
This project was created to provide Hermann's tortoise owners with a comprehensive, offline-capable care management system. The goal is to improve tortoise welfare through better record keeping, informed feeding decisions, and proactive health monitoring.

FUTURE DEVELOPMENT:
This is an active project with planned features including:
• Integration with veterinary practice management systems
• Photo-based plant identification
• Community sharing of care data (anonymized)
• Integration with tortoise rescue organizations

For updates, feature requests, or contributions, visit:
github.com/SC2IT/Tortoise-Care-Touch"""
        )
        content_layout.add_widget(credits)
        
        # License Information
        license_info = self.create_info_section(
            "License & Open Source",
            """LICENSE:
This project is released under the MIT License.

You are free to:
• Use the software for any purpose
• Modify the source code
• Distribute copies
• Create derivative works

The only requirement is to include the original license notice in any distribution.

CONTRIBUTING:
We welcome contributions from the tortoise care community:
• Bug reports and feature requests
• Plant database additions (with proper citations)
• Translation to other languages
• Platform compatibility improvements

PRIVACY:
• All data is stored locally on your device
• No personal information is transmitted to external servers
• Optional Adafruit.IO integration only sends habitat sensor data
• No tracking or analytics are implemented

OPEN SOURCE COMMITMENT:
The complete source code is available on GitHub under an open source license. This ensures transparency, allows community contributions, and prevents vendor lock-in for this critical animal care application."""
        )
        content_layout.add_widget(license_info)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def create_info_section(self, title, content):
        """Create a titled information section"""
        section = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            spacing=10,
            height=self.get_button_height() * 0.8  # Base height, will expand with content
        )
        
        # Section title
        title_label = Label(
            text=title,
            font_size=self.get_font_size('medium'),
            color=(0.8, 0.8, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            halign='left',
            text_size=(None, None)
        )
        section.add_widget(title_label)
        
        # Section content
        content_label = Label(
            text=content,
            font_size=self.get_font_size('small'),
            color=(0.9, 0.9, 0.9, 1),
            text_size=(700, None),  # Fixed width for text wrapping
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        # Calculate height based on text content
        content_label.bind(texture_size=content_label.setter('size'))
        content_label.bind(size=lambda *x: setattr(section, 'height', 
                          title_label.height + content_label.height + 20))
        
        section.add_widget(content_label)
        
        return section
    
    def go_back(self, instance):
        """Return to home screen"""
        self.manager.current = 'home'