from enum import Enum


class DiscordConversationMessageMode(Enum):
    """
    The speed with which the message will be shown. A
    fast speed means that it will be shown a short
    period of time.
    """
    
    FAST = 'fast'
    NORMAL = 'normal'
    SLOW = 'slow'