from typing import Dict, List
from notifications import NotificationManager, NotificationCategory, NotificationChannel

class NotificationSettings:
    def __init__(self, userID: str):
        self.userID = userID
        self.notification_manager = NotificationManager(userID)
    
    def display_settings(self):
        print(f"\n=== Notification Settings for User {self.userID} ===")
        preferences = self.notification_manager.get_all_preferences()
        
        for category, preference in preferences.items():
            categoryName = category.value.replace('_', ' ').title()
            enabledStatus = "ENABLED" if self.notification_manager.is_category_enabled(category) else "DISABLED"
            immutableFlag = " (Always On)" if preference.immutable else ""
            
            print(f"\n{categoryName}{immutableFlag}: {enabledStatus}")
            
            for channel, is_enabled in preference.channels.items():
                channelName = channel.value.upper()
                status = "✓" if is_enabled else "✗"
                print(f"  - {channelName}: {status}")
    
    def toggle_channel(self, categoryName: str, channelName: str, enabled: bool = None) -> bool:
        try:
            category = NotificationCategory(categoryName)
            channel = NotificationChannel(channelName)
        except ValueError:
            print(f"Invalid category or channel name")
            return False
        
        if enabled is None:
            currentPref = self.notification_manager.get_category_preferences(category)
            if currentPref:
                enabled = not currentPref.channels.get(channel, False)
        
        success = self.notification_manager.update_channel_preference(category, channel, enabled)
        
        if success:
            action = "enabled" if enabled else "disabled"
            print(f"{channelName.upper()} notifications {action} for {categoryName.replace('_', ' ')}")
        else:
            print(f"Failed to update {categoryName}. Security alerts must have at least one channel enabled.")
        
        return success
    
    def update_category_settings(self, categoryName: str, 
                               push: bool = None, email: bool = None, sms: bool = None) -> bool:
        try:
            category = NotificationCategory(categoryName)
        except ValueError:
            print(f"Invalid category name: {categoryName}")
            return False
        
        currentPrefs = self.notification_manager.get_category_preferences(category)
        if not currentPrefs:
            return False
        
        newChannels = currentPrefs.channels.copy()
        
        if push is not None:
            newChannels[NotificationChannel.PUSH] = push
        if email is not None:
            newChannels[NotificationChannel.EMAIL] = email
        if sms is not None:
            newChannels[NotificationChannel.SMS] = sms
        
        success = self.notification_manager.update_category_channels(category, newChannels)
        
        if success:
            print(f"Updated {categoryName.replace('_', ' ')} notification settings")
        else:
            print(f"Failed to update {categoryName}. Security alerts must have at least one channel enabled.")
        
        return success
    
    def enable_all_channels(self, categoryName: str) -> bool:
        try:
            category = NotificationCategory(categoryName)
        except ValueError:
            return False
        
        channels = {
            NotificationChannel.PUSH: True,
            NotificationChannel.EMAIL: True,
            NotificationChannel.SMS: True
        }
        
        return self.notification_manager.update_category_channels(category, channels)
    
    def disable_all_channels(self, categoryName: str) -> bool:
        try:
            category = NotificationCategory(categoryName)
        except ValueError:
            return False
        
        if category == NotificationCategory.SECURITY_ALERTS:
            print("Cannot disable all channels for security alerts")
            return False
        
        channels = {
            NotificationChannel.PUSH: False,
            NotificationChannel.EMAIL: False,
            NotificationChannel.SMS: False
        }
        
        return self.notification_manager.update_category_channels(category, channels)
    
    def send_test_notification(self, categoryName: str, message: str = "Test notification") -> bool:
        try:
            category = NotificationCategory(categoryName)
        except ValueError:
            return False
        
        return self.notification_manager.send_notification(
            category, 
            message, 
            title="Test Notification"
        )
    
    def get_settings_summary(self) -> Dict:
        return self.notification_manager.get_preferences_summary()
    
    def reset_all_settings(self) -> bool:
        return self.notification_manager.reset_to_defaults()