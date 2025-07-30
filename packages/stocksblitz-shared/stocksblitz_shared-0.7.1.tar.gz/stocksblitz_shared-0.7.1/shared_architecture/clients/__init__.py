"""Shared Architecture Service Clients"""

from .service_client import InterServiceClient
from .user_service_client import (
    UserServiceClient, 
    get_user_service_client,
    initialize_user_service_client
)

try:
    from .service_clients import (
        CalendarServiceClient,
        AlertServiceClient,
        MessagingServiceClient,
        check_market_open,
        send_quick_alert,
        send_quick_message,
        safe_check_market_open,
        safe_send_alert,
        safe_send_message
    )
    
    __all__ = [
        "InterServiceClient",
        "UserServiceClient",
        "get_user_service_client",
        "initialize_user_service_client",
        "CalendarServiceClient",
        "AlertServiceClient", 
        "MessagingServiceClient",
        "check_market_open",
        "send_quick_alert",
        "send_quick_message",
        "safe_check_market_open",
        "safe_send_alert",
        "safe_send_message"
    ]
except ImportError:
    __all__ = [
        "InterServiceClient",
        "UserServiceClient",
        "get_user_service_client",
        "initialize_user_service_client"
    ]