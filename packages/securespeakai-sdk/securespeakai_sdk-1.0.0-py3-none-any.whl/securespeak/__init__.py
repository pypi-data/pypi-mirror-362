"""
SecureSpeak AI Python SDK

Official Python SDK for SecureSpeak AI deepfake detection service.
"""

from .client import SecureSpeakClient, WebSocketClient, SecureSpeakAPIError

__version__ = "1.0.0"
__author__ = "SecureSpeakAI"
__email__ = "nsharma@securespeakai.com"

__all__ = [
    "SecureSpeakClient",
    "WebSocketClient", 
    "SecureSpeakAPIError"
]
