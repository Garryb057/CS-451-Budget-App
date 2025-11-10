from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class NotificationChannel(Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"

class NotificationCategory(Enum):
    SECURITY_ALERTS = "security_alerts"
    TRANSACTION_ALERTS = "transaction_alerts"
    MARKETING = "marketing"
    STATEMENTS = "statements"

@dataclass
class NotificationPreferences:
    category: NotificationCategory
    channels: Dict[NotificationChannel, bool]
    immutable: bool = False

class NotificationManager:
    def __init__(self, userID: str):
        self.userID = userID
        self.preferences = self.initialize_default_preferences()
    
    def initialize_default_preferences(self) -> Dict[NotificationCategory, NotificationPreferences]:
        return {
            NotificationCategory.SECURITY_ALERTS: NotificationPreferences(
                category=NotificationCategory.SECURITY_ALERTS,
                channels={
                    NotificationChannel.PUSH: True,
                    NotificationChannel.EMAIL: True,
                    NotificationChannel.SMS: True
                },
                immutable=True
            ),
            NotificationCategory.TRANSACTION_ALERTS: NotificationPreferences(
                category=NotificationCategory.TRANSACTION_ALERTS,
                channels={
                    NotificationChannel.PUSH: True,
                    NotificationChannel.EMAIL: True,
                    NotificationChannel.SMS: False
                }
            ),
            NotificationCategory.MARKETING: NotificationPreferences(
                category=NotificationCategory.MARKETING,
                channels={
                    NotificationChannel.PUSH: False,
                    NotificationChannel.EMAIL: True,
                    NotificationChannel.SMS: False
                }
            ),
            NotificationCategory.STATEMENTS: NotificationPreferences(
                category=NotificationCategory.STATEMENTS,
                channels={
                    NotificationChannel.PUSH: False,
                    NotificationChannel.EMAIL: True,
                    NotificationChannel.SMS: False
                }
            )
        }
    
    def update_channel_preference(self, category: NotificationCategory, channel: NotificationChannel, enabled: bool) -> bool:
        if category not in self.preferences:
            return False
        
        preference = self.preferences[category]
        
        if preference.immutable:
            currentEnabledChannels = [ch for ch, enabled in preference.channels.items() if enabled]
            if len(currentEnabledChannels) == 1 and currentEnabledChannels[0] == channel and not enabled:
                return False
        
        preference.channels[channel] = enabled
        self.save_preferences()
        return True
    
    def update_category_channels(self, category: NotificationCategory, channels: Dict[NotificationChannel, bool]) -> bool:
        if category not in self.preferences:
            return False
        
        preference = self.preferences[category]
        
        if preference.immutable:
            if not any(channels.values()):
                return False
        
        preference.channels = channels.copy()
        self.save_preferences()
        return True
    
    def get_category_preferences(self, category: NotificationCategory) -> Optional[NotificationPreferences]:
        return self.preferences.get(category)
    
    def get_all_preferences(self) -> Dict[NotificationCategory, NotificationPreferences]:
        return self.preferences.copy()
    
    def is_category_enabled(self, category: NotificationCategory) -> bool:
        if category not in self.preferences:
            return False
        return any(self.preferences[category].channels.values())
    
    def get_enabled_channels(self, category: NotificationCategory) -> List[NotificationChannel]:
        if category not in self.preferences:
            return []
        return [channel for channel, enabled in self.preferences[category].channels.items() if enabled]
    
    #Future Implementation: save to database
    def save_preferences(self) -> bool:
        print(f"Notification preferences saved for user {self.user_id}")
        return True
    
    def send_notification(self, category: NotificationCategory, message: str, 
                        title: Optional[str] = None) -> bool:
        if not self.is_category_enabled(category):
            print(f"Category {category.value} is disabled, notification not sent: {message}")
            return False
        
        enabledChannels = self.get_enabled_channels(category)
        if not enabledChannels:
            return False
        
        print(f"Sending {category.value} notification: {title or ''} - {message}")
        for channel in enabledChannels:
            self.send_via_channel(channel, category, message, title)
        
        return True
    
    def send_via_channel(self, channel: NotificationChannel, category: NotificationCategory,
                         message: str, title: Optional[str] = None):
        channelName = channel.value.upper()
        categoryName = category.value.replace('_', ' ').title()
        
        if title:
            print(f"[{channelName}] {categoryName}: {title} - {message}")
        else:
            print(f"[{channelName}] {categoryName}: {message}")
    
    def reset_to_defaults(self) -> bool:
        self.preferences = self.initialize_default_preferences()
        self.save_preferences()
        print("Notification preferences reset to defaults")
        return True
    
    def get_preferences_summary(self) -> Dict:
        summary = {}
        for category, preference in self.preferences.items():
            summary[category.value] = {
                'enabled': self.is_category_enabled(category),
                'channels': {
                    channel.value: enabled 
                    for channel, enabled in preference.channels.items()
                },
                'immutable': preference.immutable
            }
        return summary