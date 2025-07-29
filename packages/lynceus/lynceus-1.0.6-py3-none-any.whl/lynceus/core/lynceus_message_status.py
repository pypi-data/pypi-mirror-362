"""
This enum is mainly intended to be used by the client project to define
 which messages worth to be shown in UX.
"""

from enum import Enum


class LynceusMessageStatus(Enum):
    """
    Neutral informative message.
    """
    NEUTRAL = 'neutral'

    """
    Positive message leading to score increase.
    """
    POSITIVE = 'positive'

    """
    Positive message leading to score decrease.
    """
    NEGATIVE = 'negative'

    """
    Warning message.
    """
    WARNING = 'warning'

    """
    Error message.
    """
    ERROR = 'error'
