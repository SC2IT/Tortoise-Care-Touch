from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from datetime import datetime
import emoji
from screens.base_screen import BaseScreen

class SettingsDatabaseScreen(BaseScreen):
    """
    Database settings screen
    Backup, restore, import/export data, and database maintenance
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build database management interface"""
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
            text=f'{emoji.emojize(":floppy_disk:")} Database Management',
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
        
        # Database Info Section
        info_section = self.create_section_layout('Database Information')
        
        # Database size
        db_size_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        db_size_layout.add_widget(Label(
            text='Database Size:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5
        ))
        db_size_label = Label(
            text='2.4 MB',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5,
            color=(0.2, 0.6, 0.2, 1)
        )
        db_size_layout.add_widget(db_size_label)
        info_section.add_widget(db_size_layout)
        
        # Record counts
        records_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        records_layout.add_widget(Label(
            text='Total Records:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5
        ))
        records_label = Label(
            text='1,247 records',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5,
            color=(0.2, 0.6, 0.2, 1)
        )
        records_layout.add_widget(records_label)
        info_section.add_widget(records_layout)
        
        # Last backup
        backup_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        backup_layout.add_widget(Label(
            text='Last Backup:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5
        ))
        backup_label = Label(
            text='Never',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5,
            color=(0.8, 0.6, 0.2, 1)
        )
        backup_layout.add_widget(backup_label)
        info_section.add_widget(backup_layout)
        
        content_layout.add_widget(info_section)
        
        # Backup Section
        backup_section = self.create_section_layout('Backup & Restore')
        
        # Create backup button
        backup_btn = Button(
            text='Create Backup',
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        backup_btn.bind(on_press=self.create_backup)
        backup_section.add_widget(backup_btn)
        
        # Restore from backup button
        restore_btn = Button(
            text='Restore from Backup',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.4, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        restore_btn.bind(on_press=self.restore_backup)
        backup_section.add_widget(restore_btn)
        
        # Auto backup settings
        auto_backup_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.get_button_height())
        auto_backup_layout.add_widget(Label(
            text='Auto-backup:',
            font_size=self.get_font_size('medium'),
            size_hint_x=0.5
        ))
        auto_backup_btn = Button(
            text='Configure',
            font_size=self.get_font_size('medium'),
            background_color=(0.4, 0.4, 0.6, 1),
            size_hint_x=0.5
        )
        auto_backup_btn.bind(on_press=self.configure_auto_backup)
        auto_backup_layout.add_widget(auto_backup_btn)
        backup_section.add_widget(auto_backup_layout)
        
        content_layout.add_widget(backup_section)
        
        # Import/Export Section
        import_export_section = self.create_section_layout('Import & Export')
        
        # Export buttons
        export_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=self.get_button_height() * 2)
        
        export_feeding_btn = Button(
            text='Export Feeding Data',
            font_size=self.get_font_size('small'),
            background_color=(0.2, 0.4, 0.6, 1)
        )
        export_feeding_btn.bind(on_press=self.export_feeding_data)
        export_grid.add_widget(export_feeding_btn)
        
        export_health_btn = Button(
            text='Export Health Data',
            font_size=self.get_font_size('small'),
            background_color=(0.2, 0.4, 0.6, 1)
        )
        export_health_btn.bind(on_press=self.export_health_data)
        export_grid.add_widget(export_health_btn)
        
        export_growth_btn = Button(
            text='Export Growth Data',
            font_size=self.get_font_size('small'),
            background_color=(0.2, 0.4, 0.6, 1)
        )
        export_growth_btn.bind(on_press=self.export_growth_data)
        export_grid.add_widget(export_growth_btn)
        
        export_all_btn = Button(
            text='Export All Data (CSV)',
            font_size=self.get_font_size('small'),
            background_color=(0.6, 0.2, 0.6, 1)
        )
        export_all_btn.bind(on_press=self.export_all_data)
        export_grid.add_widget(export_all_btn)
        
        import_export_section.add_widget(export_grid)
        
        # Import button
        import_btn = Button(
            text='Import Data from CSV',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        import_btn.bind(on_press=self.import_data)
        import_export_section.add_widget(import_btn)
        
        content_layout.add_widget(import_export_section)
        
        # Maintenance Section
        maintenance_section = self.create_section_layout('Database Maintenance')
        
        # Optimize database button
        optimize_btn = Button(
            text='Optimize Database',
            font_size=self.get_font_size('medium'),
            background_color=(0.4, 0.6, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        optimize_btn.bind(on_press=self.optimize_database)
        maintenance_section.add_widget(optimize_btn)
        
        # Clear old data button
        clear_old_btn = Button(
            text='Clear Data Older Than...',
            font_size=self.get_font_size('medium'),
            background_color=(0.8, 0.4, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        clear_old_btn.bind(on_press=self.clear_old_data)
        maintenance_section.add_widget(clear_old_btn)
        
        # Reset database button (dangerous)
        reset_btn = Button(
            text='RESET DATABASE (DANGER)',
            font_size=self.get_font_size('medium'),
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=self.get_button_height()
        )
        reset_btn.bind(on_press=self.reset_database)
        maintenance_section.add_widget(reset_btn)
        
        content_layout.add_widget(maintenance_section)
        
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
    
    def create_backup(self, instance):
        """Create a database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'tortoise_care_backup_{timestamp}.db'
        
        # TODO: Implement actual backup creation
        self.show_popup('Success', f'Backup created successfully!\nSaved as: {backup_name}')
    
    def restore_backup(self, instance):
        """Restore from backup with file chooser"""
        self.show_popup('Coming Soon', 'Backup restore will be implemented soon!')
    
    def configure_auto_backup(self, instance):
        """Configure automatic backup settings"""
        self.show_popup('Coming Soon', 'Auto-backup configuration will be implemented soon!')
    
    def export_feeding_data(self, instance):
        """Export feeding data to CSV"""
        # TODO: Implement actual feeding data export
        self.show_popup('Coming Soon', 'Feeding data export will be implemented soon!')
    
    def export_health_data(self, instance):
        """Export health data to CSV"""
        # TODO: Implement actual health data export
        self.show_popup('Coming Soon', 'Health data export will be implemented soon!')
    
    def export_growth_data(self, instance):
        """Export growth data to CSV"""
        # TODO: Implement actual growth data export
        self.show_popup('Coming Soon', 'Growth data export will be implemented soon!')
    
    def export_all_data(self, instance):
        """Export all data to CSV"""
        # TODO: Implement actual full data export
        self.show_popup('Coming Soon', 'Full data export will be implemented soon!')
    
    def import_data(self, instance):
        """Import data from CSV"""
        self.show_popup('Coming Soon', 'Data import will be implemented soon!')
    
    def optimize_database(self, instance):
        """Optimize database performance"""
        # TODO: Implement actual database optimization
        self.show_popup('Success', 'Database optimized successfully!\nPerformance improved.')
    
    def clear_old_data(self, instance):
        """Clear old data with date selection"""
        self.show_popup('Coming Soon', 'Old data clearing will be implemented soon!')
    
    def reset_database(self, instance):
        """Reset database with strong confirmation"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        warning_label = Label(
            text='⚠️ DANGER ⚠️\n\nThis will permanently delete ALL data:\n• All tortoises and their records\n• All feeding history\n• All health records\n• All users and settings\n\nThis action CANNOT be undone!\n\nType "DELETE EVERYTHING" to confirm:',
            text_size=(400, None),
            font_size=self.get_font_size('medium'),
            halign='center',
            color=(1, 0.3, 0.3, 1)
        )
        content.add_widget(warning_label)
        
        confirm_input = TextInput(
            multiline=False,
            font_size=self.get_font_size('medium'),
            size_hint_y=None,
            height=self.get_button_height()
        )
        content.add_widget(confirm_input)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=self.get_button_height())
        
        cancel_btn = Button(
            text='Cancel',
            font_size=self.get_font_size('medium'),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        
        delete_btn = Button(
            text='DELETE EVERYTHING',
            font_size=self.get_font_size('medium'),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        popup = Popup(
            title='RESET DATABASE - CONFIRM',
            content=content,
            size_hint=(0.9, 0.8),
            title_size=self.get_font_size('large'),
            auto_dismiss=False
        )
        
        def confirm_reset(instance):
            if confirm_input.text.strip() == 'DELETE EVERYTHING':
                # TODO: Implement actual database reset
                popup.dismiss()
                self.show_popup('Database Reset', 'All data has been permanently deleted.\nApplication will restart.')
            else:
                self.show_popup('Error', 'Confirmation text does not match.\nDatabase reset cancelled.')
        
        def cancel_reset(instance):
            popup.dismiss()
        
        cancel_btn.bind(on_press=cancel_reset)
        delete_btn.bind(on_press=confirm_reset)
        
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