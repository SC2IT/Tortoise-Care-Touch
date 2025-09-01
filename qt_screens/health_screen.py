"""
Health monitoring and care guide screen
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QPushButton, QLabel, QMessageBox, QScrollArea, QTextEdit)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class HealthScreen(BaseScreen):
    """Comprehensive health monitoring and care guide system"""
    
    def build_ui(self):
        """Build health screen UI"""
        # Header with back button
        header = self.create_header('🩺 Health & Care', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Emergency section
        self.create_emergency_section()
        
        # Health monitoring sections
        self.create_health_sections()
        
        # Care guides section
        self.create_care_guides_section()
        
    def create_emergency_section(self):
        """Create emergency alert section"""
        emergency_layout = QHBoxLayout()
        
        # Emergency protocols button with icon
        emergency_btn = create_icon_button('emergency', 'EMERGENCY PROTOCOLS', (28, 28), 
                                         self.show_emergency_protocols)
        emergency_btn.setMinimumHeight(60)
        emergency_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #d32f2f; }
            QPushButton:pressed { background-color: #b71c1c; }
        """)
        
        # Vet contact button with icon
        vet_btn = create_icon_button('phone', 'CALL VET', (24, 24), 
                                   self.show_emergency_contacts)
        vet_btn.setMinimumHeight(60)
        vet_btn.setMaximumWidth(200)
        vet_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #616161; }
            QPushButton:pressed { background-color: #424242; }
        """)
        
        emergency_layout.addWidget(emergency_btn, 2)
        emergency_layout.addWidget(vet_btn, 1)
        
        self.main_layout.addLayout(emergency_layout)
        
    def create_health_sections(self):
        """Create health monitoring section buttons"""
        health_layout = QGridLayout()
        health_layout.setSpacing(10)
        
        health_sections = [
            ('💚 Health Check', 'Signs of healthy tortoise', self.show_health_check_guide, 'primary'),
            ('📋 Health Records', 'Vet visits & observations', self.show_health_records, 'secondary'),
            ('💊 Medications', 'Track treatments', self.show_medications, 'warning'),
            ('⚠️ Warning Signs', 'Illness & poisoning', self.show_warning_signs, 'danger')
        ]
        
        row, col = 0, 0
        for title, subtitle, callback, style in health_sections:
            # Button container
            container_layout = QVBoxLayout()
            
            # Main button
            button = self.create_button(title, callback, style)
            button.setMinimumHeight(70)
            
            font = button.font()
            font.setPointSize(14)
            button.setFont(font)
            
            container_layout.addWidget(button)
            
            # Subtitle
            subtitle_label = QLabel(subtitle)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setStyleSheet("color: #666; font-size: 11px; margin: 2px;")
            container_layout.addWidget(subtitle_label)
            
            # Add to grid
            from PySide6.QtWidgets import QWidget
            container_widget = QWidget()
            container_widget.setLayout(container_layout)
            health_layout.addWidget(container_widget, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
                
        self.main_layout.addLayout(health_layout)
        
    def create_care_guides_section(self):
        """Create care guides section"""
        # Section title
        guides_title = self.create_title_label('Care Guides & Resources', 'medium')
        guides_title.setStyleSheet("color: #FF9800; margin: 10px 5px 5px 5px;")
        self.main_layout.addWidget(guides_title)
        
        # Care guide buttons
        care_guides = [
            ('🐢 Hermann\'s Tortoise Care', 'Species-specific care requirements', 
             self.show_hermann_care_guide, 'primary'),
            ('📅 Seasonal Care', 'Hibernation, breeding, seasonal variations', 
             self.show_seasonal_care_guide, 'secondary'),
            ('🌿 Plant Safety Guide', 'Toxic plants and poisoning prevention', 
             self.show_plant_safety_guide, 'warning')
        ]
        
        for title, subtitle, callback, style in care_guides:
            # Container for button and subtitle
            guide_layout = QVBoxLayout()
            
            # Main button
            button = self.create_button(title, callback, style)
            button.setMinimumHeight(50)
            
            font = button.font()
            font.setPointSize(13)
            button.setFont(font)
            
            guide_layout.addWidget(button)
            
            # Subtitle
            subtitle_label = QLabel(subtitle)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setStyleSheet("color: #666; font-size: 10px; margin: 2px;")
            subtitle_label.setWordWrap(True)
            guide_layout.addWidget(subtitle_label)
            
            self.main_layout.addLayout(guide_layout)
            
    def show_emergency_protocols(self):
        """Display emergency protocols"""
        self.show_info_dialog('🚨 EMERGENCY PROTOCOLS', 
                             self.get_emergency_protocols_text())
        
    def show_emergency_contacts(self):
        """Show emergency veterinary contacts"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Emergency Contacts')
        msg.setText('Emergency veterinary contact management will be implemented in Settings → Connections.\n\n'
                   'For now, keep your exotic vet contact information readily available.')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
    def show_health_check_guide(self):
        """Display healthy tortoise signs guide"""
        self.show_info_dialog('💚 Signs of a Healthy Tortoise', 
                             self.get_health_check_text())
        
    def show_health_records(self):
        """Navigate to health records management screen"""
        self.main_window.show_screen('health_records')
        
    def show_medications(self):
        """Show medication tracking"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Medications')
        msg.setText('Medication tracking system will be implemented soon!\n\n'
                   'Features will include:\n'
                   '• Dosage scheduling\n'
                   '• Treatment compliance\n'
                   '• Medication reminders\n'
                   '• Side effect monitoring')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
    def show_warning_signs(self):
        """Display illness warning signs"""
        self.show_info_dialog('⚠️ Warning Signs & Illness', 
                             self.get_warning_signs_text())
        
    def show_hermann_care_guide(self):
        """Show Hermann's tortoise specific care guide"""
        self.show_info_dialog('🐢 Hermann\'s Tortoise Care Guide', 
                             self.get_hermann_care_text())
        
    def show_seasonal_care_guide(self):
        """Show seasonal care guide"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Seasonal Care')
        msg.setText('Seasonal care guide will be implemented soon!\n\n'
                   'Will include:\n'
                   '• Hibernation protocols\n'
                   '• Breeding season care\n'
                   '• Summer heat management\n'
                   '• Spring emergence procedures')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
    def show_plant_safety_guide(self):
        """Show plant safety guide"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Plant Safety')
        msg.setText('Advanced plant safety features are available in the Plant Database!\n\n'
                   '• Comprehensive toxic plant list\n'
                   '• Safety classifications\n'
                   '• Feeding guidelines\n'
                   '• Emergency poisoning protocols\n\n'
                   'Access via: Home → Plant Database')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
    def show_info_dialog(self, title, content):
        """Show scrollable information dialog"""
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        
        # Create scrollable text area
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        text_edit.setMinimumSize(600, 400)
        text_edit.setStyleSheet("font-size: 16px; line-height: 1.5; padding: 10px;")
        
        # Replace the default text with our custom widget
        dialog.layout().addWidget(text_edit, 1, 1)
        
        # Style for touch interface
        dialog.setStyleSheet("""
            QMessageBox {
                min-width: 650px;
                min-height: 450px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 40px;
                font-size: 12px;
            }
        """)
        
        dialog.exec()
        
    def get_emergency_protocols_text(self):
        """Get emergency protocols text"""
        return """POISONING EMERGENCY PROTOCOL
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
        
    def get_health_check_text(self):
        """Get health check guide text"""
        return """COMPREHENSIVE HEALTH INDICATORS
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
• Consult exotic vet for any concerns"""
        
    def get_warning_signs_text(self):
        """Get warning signs text"""
        return """ILLNESS WARNING SIGNS
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

IMPORTANT: Any sudden change in normal behavior or appearance warrants veterinary consultation."""
        
    def get_hermann_care_text(self):
        """Get Hermann's tortoise care text"""
        return """HERMANN'S TORTOISE CARE GUIDE
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

VETERINARY CARE:
• Annual wellness exams recommended
• Find ARAV-certified exotic veterinarian
• Regular parasite screening
• Pre-hibernation health checks essential"""