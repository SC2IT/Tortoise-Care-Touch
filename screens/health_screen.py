from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import emoji
from screens.base_screen import BaseScreen

class HealthScreen(BaseScreen):
    """
    Comprehensive health monitoring and care guide system
    Based on The Tortoise Table and veterinary sources
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build health monitoring interface with care guides"""
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
            text='Health & Care',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Emergency alert section
        emergency_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        
        emergency_btn = Button(
            text='EMERGENCY PROTOCOLS',
            font_size=self.get_font_size('medium'),
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_x=0.7
        )
        emergency_btn.bind(on_press=self.show_emergency_protocols)
        emergency_layout.add_widget(emergency_btn)
        
        vet_btn = Button(
            text='CALL VET',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.2, 0.6, 1),
            size_hint_x=0.3
        )
        vet_btn.bind(on_press=self.show_emergency_contacts)
        emergency_layout.add_widget(vet_btn)
        
        main_layout.add_widget(emergency_layout)
        
        # Health monitoring sections
        sections_grid = GridLayout(cols=2, spacing=self.get_button_spacing(), size_hint_y=0.4)
        
        health_sections = [
            {
                'title': f'{emoji.emojize(":green_heart:")} Health Check',
                'subtitle': 'Signs of healthy tortoise',
                'color': (0.2, 0.6, 0.2, 1),
                'action': self.show_health_check_guide
            },
            {
                'title': f'{emoji.emojize(":clipboard:")} Health Records',
                'subtitle': 'Vet visits & observations',
                'color': (0.2, 0.4, 0.6, 1),
                'action': self.show_health_records
            },
            {
                'title': f'{emoji.emojize(":pill:")} Medications',
                'subtitle': 'Track treatments',
                'color': (0.6, 0.4, 0.2, 1),
                'action': self.show_medications
            },
            {
                'title': f'{emoji.emojize(":warning:")} Warning Signs',
                'subtitle': 'Illness & poisoning',
                'color': (0.8, 0.6, 0.2, 1),
                'action': self.show_warning_signs
            }
        ]
        
        for section in health_sections:
            btn_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=self.get_button_height() * 1.5)
            
            main_btn = Button(
                text=section['title'],
                font_size=self.get_font_size('medium'),
                background_color=section['color'],
                size_hint_y=0.7
            )
            main_btn.bind(on_press=lambda x, action=section['action']: action())
            
            subtitle = Label(
                text=section['subtitle'],
                font_size=self.get_font_size('small'),
                size_hint_y=0.3,
                color=(0.7, 0.7, 0.7, 1)
            )
            
            btn_layout.add_widget(main_btn)
            btn_layout.add_widget(subtitle)
            sections_grid.add_widget(btn_layout)
        
        main_layout.add_widget(sections_grid)
        
        # Care guides section
        guides_title = Label(
            text='Care Guides & Resources',
            font_size=self.get_font_size('medium'),
            size_hint_y=0.06,
            color=(0.8, 0.8, 0.2, 1)
        )
        main_layout.add_widget(guides_title)
        
        guides_grid = GridLayout(cols=1, spacing=5, size_hint_y=0.4)
        
        care_guides = [
            {
                'title': f'{emoji.emojize(":turtle:")} Hermann\'s Tortoise Care',
                'subtitle': 'Species-specific care requirements and guidelines',
                'color': (0.4, 0.6, 0.4, 1),
                'action': self.show_hermann_care_guide
            },
            {
                'title': f'{emoji.emojize(":calendar:")} Seasonal Care',
                'subtitle': 'Hibernation, breeding, and seasonal variations',
                'color': (0.4, 0.4, 0.6, 1),
                'action': self.show_seasonal_care_guide
            },
            {
                'title': f'{emoji.emojize(":seedling:")} Plant Safety Guide',
                'subtitle': 'Toxic plants and poisoning prevention',
                'color': (0.6, 0.4, 0.4, 1),
                'action': self.show_plant_safety_guide
            }
        ]
        
        for guide in care_guides:
            guide_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
            
            guide_btn = Button(
                text=f"{guide['title']}\n{guide['subtitle']}",
                font_size=self.get_font_size('small'),
                background_color=guide['color'],
                halign='left'
            )
            guide_btn.bind(on_press=lambda x, action=guide['action']: action())
            guide_layout.add_widget(guide_btn)
            
            guides_grid.add_widget(guide_layout)
        
        main_layout.add_widget(guides_grid)
        
        self.add_widget(main_layout)
    
    def show_emergency_protocols(self, instance=None):
        """Display emergency protocols for poisoning and critical situations"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text=f'{emoji.emojize(":exclamation:")} EMERGENCY PROTOCOLS',
            font_size=self.get_font_size('large'),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            color=(1, 0.3, 0.3, 1)
        )
        content.add_widget(title)
        
        scroll = ScrollView()
        protocol_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        protocol_layout.bind(minimum_height=protocol_layout.setter('height'))
        
        emergency_info = """POISONING EMERGENCY PROTOCOL
(Source: The Tortoise Table - tortoisetable.org.uk)

IMMEDIATE ACTIONS:
1. SEEK VETERINARY HELP IMMEDIATELY
2. Bring suspected poison source to vet
3. Do NOT attempt self-diagnosis
4. Note time of exposure and symptoms

ACUTE POISONING SYMPTOMS:
• Respiratory distress
• Excess salivation
• Choking or difficulty swallowing
• Vomiting (rare in tortoises)
• Tremors or convulsions
• Paralysis or inability to move

CUMULATIVE POISONING SYMPTOMS:
• Progressive muscular weakness
• Inability to walk normally
• Gastrointestinal upset/diarrhea
• Loss of appetite
• Lethargy or unresponsiveness

PREVENTION MEASURES:
• Never use pesticides, herbicides, or fertilizers in tortoise areas
• Keep slug/snail bait completely inaccessible
• Thoroughly wash all store-bought vegetation
• Carefully inspect all wild-collected plants
• Maintain toxic plant database awareness

WARNING: Do not attempt to treat poisoning yourself. Only qualified exotic veterinarians should handle poisoning cases.

Emergency Vet Contacts: [Configure in Settings → Connections]"""
        
        protocol_label = Label(
            text=emergency_info,
            font_size=self.get_font_size('small'),
            text_size=(500, None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        protocol_label.bind(texture_size=protocol_label.setter('size'))
        protocol_layout.add_widget(protocol_label)
        
        scroll.add_widget(protocol_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Emergency Protocols',
            content=content,
            size_hint=(0.95, 0.9),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_emergency_contacts(self, instance=None):
        """Show emergency veterinary contacts"""
        self.show_popup('Emergency Contacts', 'Emergency veterinary contact management will be implemented in Settings → Connections.\n\nFor now, keep your exotic vet contact information readily available.')
    
    def show_health_check_guide(self, instance=None):
        """Display comprehensive healthy tortoise signs guide"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text=f'{emoji.emojize(":green_heart:")} Signs of a Healthy Tortoise',
            font_size=self.get_font_size('large'),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            color=(0.2, 0.8, 0.2, 1)
        )
        content.add_widget(title)
        
        scroll = ScrollView()
        health_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        health_layout.bind(minimum_height=health_layout.setter('height'))
        
        health_info = """COMPREHENSIVE HEALTH INDICATORS
(Source: The Tortoise Table - tortoisetable.org.uk)

PHYSICAL CONDITION:
✓ Shell (Carapace):
  • Smooth and firm to touch
  • No obvious bumps, soft spots, or injuries
  • Visible growth rings between scute plates
  • Feels solid when lifted

✓ Eyes:
  • Clear and bright
  • No discharge or weeping
  • Minimal third eyelid visibility
  • Alert and responsive

✓ Respiratory System:
  • Clear, dry nostrils
  • No discharge or bubbling
  • No wheezing or labored breathing
  • Mouth breathing is abnormal

✓ Oral Health:
  • Pink, moist tongue
  • Strong bite reflex
  • Properly sized beak with slight top overbite
  • No lesions or growths

✓ Skin & External:
  • No visible injuries or wounds
  • No external parasites (ticks/mites)
  • Normal skin shedding around neck area
  • Good muscle tone

BEHAVIORAL INDICATORS:
✓ Activity & Movement:
  • Active and mobile when appropriate
  • Walks with plastron clear of ground
  • Good muscle tone and coordination
  • Able to right itself if turned over

✓ Waste Production:
  • Firm, well-formed feces
  • Clear to slightly cloudy urine
  • Urates: watery to soft toothpaste consistency
  • Regular elimination pattern

✓ Appetite & Behavior:
  • Good appetite for appropriate foods
  • Alert and responsive to environment
  • Normal basking and hiding behaviors
  • Appropriate seasonal activity patterns

MONITORING RECOMMENDATIONS:
• Perform weekly visual health checks
• Weigh monthly (same time of day)
• Document any changes in behavior
• Maintain health record logs
• Consult exotic vet for any concerns

Remember: Early detection of health issues significantly improves treatment outcomes."""
        
        health_label = Label(
            text=health_info,
            font_size=self.get_font_size('small'),
            text_size=(500, None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        health_label.bind(texture_size=health_label.setter('size'))
        health_layout.add_widget(health_label)
        
        scroll.add_widget(health_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Healthy Tortoise Guide',
            content=content,
            size_hint=(0.95, 0.9),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_health_records(self, instance=None):
        """Show health records management"""
        self.show_popup('Health Records', 'Health records management system will be implemented soon!\n\nFeatures will include:\n• Vet visit tracking\n• Daily health observations\n• Photo documentation\n• Medication schedules')
    
    def show_medications(self, instance=None):
        """Show medication tracking"""
        self.show_popup('Medications', 'Medication tracking system will be implemented soon!\n\nFeatures will include:\n• Dosage scheduling\n• Treatment compliance\n• Medication reminders\n• Side effect monitoring')
    
    def show_warning_signs(self, instance=None):
        """Display illness warning signs and symptoms"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text=f'{emoji.emojize(":warning:")} Warning Signs & Illness',
            font_size=self.get_font_size('large'),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            color=(1, 0.6, 0.2, 1)
        )
        content.add_widget(title)
        
        scroll = ScrollView()
        warning_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        warning_layout.bind(minimum_height=warning_layout.setter('height'))
        
        warning_info = """ILLNESS WARNING SIGNS
(Sources: The Tortoise Table, Tortoise Trust, ARAV)

IMMEDIATE VETERINARY ATTENTION REQUIRED:
🚨 Respiratory Issues:
  • Wheezing, gasping, or mouth breathing
  • Nasal discharge (clear or colored)
  • Stretching neck upward while breathing

🚨 Severe Lethargy:
  • Unresponsive to stimuli
  • Unable to lift head normally
  • Collapse or inability to support body weight

🚨 Traumatic Injuries:
  • Shell cracks or damage
  • Deep wounds or bleeding
  • Suspected broken bones

🚨 Eye Problems:
  • Swollen, closed, or sunken eyes
  • Thick discharge or pus
  • Cloudiness or color changes

MONITOR CLOSELY - VET CONSULTATION ADVISED:
⚠️ Appetite Changes:
  • Complete loss of appetite (>3 days)
  • Difficulty eating or swallowing
  • Selective eating (avoiding hard foods)

⚠️ Shell Abnormalities:
  • Soft spots or flexibility
  • Pyramiding (raised scutes)
  • Discoloration or lesions

⚠️ Behavioral Changes:
  • Excessive hiding or lack of basking
  • Circling or disorientation
  • Aggressive or unusual behavior

⚠️ Digestive Issues:
  • Diarrhea or very liquid waste
  • No waste production (>5 days)
  • Blood in waste

COMMON CONDITIONS:
• Respiratory Infections (RI)
• Shell Rot (bacterial/fungal)
• Metabolic Bone Disease (MBD)
• Parasites (internal/external)
• Kidney disease
• Egg binding (females)

IMPORTANT: Any sudden change in normal behavior or appearance warrants veterinary consultation. Early intervention significantly improves treatment success rates.

Emergency Protocols: See Emergency button for poisoning procedures."""
        
        warning_label = Label(
            text=warning_info,
            font_size=self.get_font_size('small'),
            text_size=(500, None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        warning_label.bind(texture_size=warning_label.setter('size'))
        warning_layout.add_widget(warning_label)
        
        scroll.add_widget(warning_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Warning Signs Guide',
            content=content,
            size_hint=(0.95, 0.9),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_hermann_care_guide(self, instance=None):
        """Show Hermann's tortoise specific care guide"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text=f'{emoji.emojize(":turtle:")} Hermann\'s Tortoise Care Guide',
            font_size=self.get_font_size('large'),
            size_hint_y=None,
            height=self.get_button_height() * 0.8,
            color=(0.4, 0.6, 0.4, 1)
        )
        content.add_widget(title)
        
        scroll = ScrollView()
        care_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        care_layout.bind(minimum_height=care_layout.setter('height'))
        
        care_info = """HERMANN'S TORTOISE CARE GUIDE
(Sources: Tortoise Trust, World Chelonian Trust, ARAV)

SPECIES OVERVIEW:
Scientific Name: Testudo hermanni
Subspecies: T. h. hermanni (Western), T. h. boettgeri (Eastern)
Lifespan: 80-120+ years
Adult Size: 6-10 inches (depending on subspecies)

HABITAT REQUIREMENTS:
🏠 Housing:
  • Minimum 8x4 feet for adult (larger preferred)
  • Outdoor housing ideal in suitable climates
  • Substrate: Topsoil/sand mix, cypress mulch
  • Hiding areas and shelter from elements

🌡️ Temperature:
  • Basking spot: 95-100°F (35-38°C)
  • Cool side: 70-75°F (21-24°C)
  • Nighttime: 60-70°F (16-21°C)
  • UVB lighting: 10-12% UVB, 12-14 hours daily

💧 Humidity:
  • 50-70% relative humidity
  • Shallow water dish for drinking/soaking
  • Humid hide area for younger tortoises

DIETARY REQUIREMENTS:
🥬 Primary Diet (90%):
  • Weeds: Dandelion, plantain, clover, mallow
  • Grasses: Timothy, meadow grass, various native grasses
  • Wild plants: Chickweed, sow thistle, bramble leaves

🍓 Supplements (10%):
  • Fruits: Occasional strawberries, apple, melon
  • Vegetables: Limited amounts of safe varieties
  • Flowers: Hibiscus, rose petals, nasturtiums

⚠️ AVOID:
  • High protein foods (beans, meat)
  • High oxalate plants (spinach, rhubarb)
  • Toxic plants (see Plant Database)
  • Processed human foods

HEALTH MONITORING:
📊 Regular Checks:
  • Weekly visual health assessment
  • Monthly weight monitoring
  • Shell condition inspection
  • Appetite and waste monitoring

💊 Calcium & D3:
  • Dust food 2-3x weekly with calcium
  • Calcium with D3 once weekly (indoor tortoises)
  • Cuttlebone available continuously

SEASONAL CARE:
❄️ Hibernation (Brumation):
  • Natural process for adults (2+ years)
  • 6-20 weeks depending on age/health
  • Pre-hibernation health check essential
  • Controlled temperature: 39-45°F (4-7°C)

🌱 Spring Emergence:
  • Gradual warming and light increase
  • Fresh water and easy-to-digest foods
  • Health assessment upon awakening

☀️ Summer Care:
  • Adequate shade and water access
  • Monitor for overheating
  • Peak feeding and growth period

🍂 Fall Preparation:
  • Health assessment before hibernation
  • Gradual reduction in feeding
  • Weight and parasite checks

BREEDING CONSIDERATIONS:
• Sexual maturity: 10-20 years
• Breeding season: Spring after hibernation
• Egg laying: 2-5 eggs, 2-3 clutches per year
• Incubation: 90-120 days at 88-90°F

SPECIAL NOTES:
• Hermann's tortoises are excellent climbers
• Require varied terrain and obstacles
• Social animals - can be housed together with care
• Long-term commitment species

VETERINARY CARE:
• Annual wellness exams recommended
• Find ARAV-certified exotic veterinarian
• Regular parasite screening
• Pre-hibernation health checks essential"""
        
        care_label = Label(
            text=care_info,
            font_size=self.get_font_size('small'),
            text_size=(500, None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        care_label.bind(texture_size=care_label.setter('size'))
        care_layout.add_widget(care_label)
        
        scroll.add_widget(care_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Hermann's Tortoise Care",
            content=content,
            size_hint=(0.95, 0.9),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_seasonal_care_guide(self, instance=None):
        """Show seasonal care variations guide"""
        self.show_popup('Seasonal Care', 'Seasonal care guide will be implemented soon!\n\nWill include:\n• Hibernation protocols\n• Breeding season care\n• Summer heat management\n• Spring emergence procedures')
    
    def show_plant_safety_guide(self, instance=None):
        """Show plant safety and poisoning prevention"""
        self.show_popup('Plant Safety', 'Advanced plant safety features are available in the Plant Database!\n\n• Comprehensive toxic plant list\n• Safety classifications\n• Feeding guidelines\n• Emergency poisoning protocols\n\nAccess via: Home → Plant Database')
    
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
        """Return to home screen"""
        self.manager.current = 'home'