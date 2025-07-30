"""
SIP Client Library - A professional Python SIP client with voice support
"""

from .client import SIPClient
from .models.account import SIPAccount
from .models.call import CallInfo
from .models.enums import CallState, RegistrationState
from .audio.devices import AudioDevice

__version__ = "1.0.0"
__author__ = "SIP Client Library"
__email__ = "support@sipclient.com"

__all__ = [
    "SIPClient",
    "SIPAccount", 
    "CallInfo",
    "CallState",
    "RegistrationState",
    "AudioDevice",
] 