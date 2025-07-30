"""Shared client libraries for Calendar, Alerts, and Messaging services"""
import asyncio
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime


class ServiceClient:
    """Base class for service clients"""
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request"""
        try:
            response = await self.client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error: {e}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make POST request"""
        try:
            response = await self.client.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error: {e}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")


class CalendarServiceClient(ServiceClient):
    """Client for Calendar Service"""
    
    def __init__(self, base_url: str = "http://stocksblitz-calendar-service:8011"):
        super().__init__(base_url)
    
    async def health_check(self) -> Dict:
        """Check service health"""
        return await self.get("/health")
    
    async def is_market_open(self, exchange: str = "NSE") -> bool:
        """Check if market is currently open"""
        try:
            response = await self.get(f"/api/v1/market-status", params={"exchange": exchange})
            return response.get("is_open", False)
        except:
            # Fallback - assume market is open during business hours
            current_hour = datetime.now().hour
            return 9 <= current_hour <= 15
    
    async def get_trading_hours(self, exchange: str = "NSE") -> Dict:
        """Get trading hours for exchange"""
        try:
            return await self.get(f"/api/v1/trading-hours", params={"exchange": exchange})
        except:
            return {
                "exchange": exchange,
                "open_time": "09:15",
                "close_time": "15:30",
                "is_open": True
            }
    
    async def get_market_holidays(self, year: int = None) -> List[Dict]:
        """Get market holidays"""
        if year is None:
            year = datetime.now().year
        try:
            return await self.get(f"/api/v1/holidays", params={"year": year})
        except:
            return []
    
    async def create_event(self, event_data: Dict) -> Dict:
        """Create a calendar event"""
        return await self.post("/api/v1/events", event_data)
    
    async def schedule_for_next_session(self, callback_data: Dict) -> Dict:
        """Schedule something for the next trading session"""
        event_data = {
            "event_type": "SCHEDULED_CALLBACK",
            "callback_data": callback_data,
            "schedule_time": "next_market_open"
        }
        return await self.create_event(event_data)


class AlertServiceClient(ServiceClient):
    """Client for Alert Service"""
    
    def __init__(self, base_url: str = "http://stocksblitz-alert-service:8010"):
        super().__init__(base_url)
    
    async def health_check(self) -> Dict:
        """Check service health"""
        return await self.get("/health")
    
    async def send_alert(self, 
                        user_id: str, 
                        alert_type: str, 
                        message: str, 
                        priority: str = "medium",
                        channels: List[str] = None) -> Dict:
        """Send an alert"""
        if channels is None:
            channels = ["ui"]
        
        alert_data = {
            "user_id": user_id,
            "alert_type": alert_type,
            "message": message,
            "priority": priority,
            "channels": channels
        }
        return await self.post("/api/v1/alerts/send", alert_data)
    
    async def trigger_alert(self, alert_data: Dict) -> Dict:
        """Trigger an alert with custom data"""
        return await self.post("/api/v1/alerts/trigger", alert_data)
    
    async def get_alerts(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get alerts for user"""
        params = {"user_id": user_id} if user_id else None
        return await self.get("/api/v1/alerts", params)
    
    async def send_trade_alert(self, user_id: str, order_id: str, status: str) -> Dict:
        """Send trade-specific alert"""
        return await self.send_alert(
            user_id=user_id,
            alert_type="TRADE_EXECUTION",
            message=f"Order {order_id} {status}",
            priority="high",
            channels=["ui", "email"]
        )
    
    async def send_signal_alert(self, user_id: str, symbol: str, signal_type: str, value: float) -> Dict:
        """Send signal-specific alert"""
        return await self.send_alert(
            user_id=user_id,
            alert_type="SIGNAL_ALERT",
            message=f"Signal {signal_type} for {symbol}: {value}",
            priority="medium",
            channels=["ui"]
        )
    
    async def send_system_alert(self, message: str, priority: str = "low") -> Dict:
        """Send system-wide alert"""
        return await self.send_alert(
            user_id="system",
            alert_type="SYSTEM_STATUS",
            message=message,
            priority=priority,
            channels=["ui", "email"]
        )


class MessagingServiceClient(ServiceClient):
    """Client for Messaging Service"""
    
    def __init__(self, base_url: str = "http://stocksblitz-messaging-service:8012"):
        super().__init__(base_url)
    
    async def health_check(self) -> Dict:
        """Check service health"""
        return await self.get("/health")
    
    async def send_message(self, 
                          recipient: str, 
                          message: str, 
                          message_type: str = "notification",
                          delivery_method: str = "async") -> Dict:
        """Send a message"""
        message_data = {
            "recipient": recipient,
            "message": message,
            "message_type": message_type,
            "delivery_method": delivery_method
        }
        return await self.post("/api/v1/messages/send", message_data)
    
    async def send_template_message(self, 
                                   recipient: str, 
                                   template: str, 
                                   variables: Dict,
                                   priority: str = "normal") -> Dict:
        """Send a templated message"""
        message_data = {
            "recipient": recipient,
            "template": template,
            "variables": variables,
            "priority": priority
        }
        return await self.post("/api/v1/messages/template", message_data)
    
    async def send_user_notification(self, user_id: str, message: str) -> Dict:
        """Send user notification"""
        return await self.send_message(
            recipient=user_id,
            message=message,
            message_type="USER_NOTIFICATION",
            delivery_method="async"
        )
    
    async def send_welcome_message(self, user_id: str, username: str) -> Dict:
        """Send welcome message to new user"""
        return await self.send_template_message(
            recipient=user_id,
            template="welcome_new_user",
            variables={"username": username},
            priority="high"
        )
    
    async def send_trade_confirmation(self, user_id: str, trade_details: Dict) -> Dict:
        """Send trade confirmation message"""
        return await self.send_template_message(
            recipient=user_id,
            template="trade_confirmation",
            variables=trade_details,
            priority="high"
        )


# Convenience functions for quick integration
async def check_market_open(exchange: str = "NSE") -> bool:
    """Quick check if market is open"""
    async with CalendarServiceClient() as client:
        return await client.is_market_open(exchange)

async def send_quick_alert(user_id: str, message: str, priority: str = "medium") -> Dict:
    """Send a quick alert"""
    async with AlertServiceClient() as client:
        return await client.send_alert(user_id, "QUICK_ALERT", message, priority)

async def send_quick_message(user_id: str, message: str) -> Dict:
    """Send a quick message"""
    async with MessagingServiceClient() as client:
        return await client.send_user_notification(user_id, message)


# Circuit breaker pattern for resilience
class CircuitBreaker:
    """Simple circuit breaker for service calls"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection"""
        if self.state == "OPEN":
            if datetime.now().timestamp() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now().timestamp()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            
            raise e


# Global circuit breakers for each service
calendar_breaker = CircuitBreaker()
alert_breaker = CircuitBreaker()
messaging_breaker = CircuitBreaker()


async def safe_check_market_open(exchange: str = "NSE") -> bool:
    """Market check with circuit breaker"""
    try:
        async with CalendarServiceClient() as client:
            return await calendar_breaker.call(client.is_market_open, exchange)
    except:
        # Fallback logic
        current_hour = datetime.now().hour
        return 9 <= current_hour <= 15


async def safe_send_alert(user_id: str, message: str, priority: str = "medium") -> Dict:
    """Send alert with circuit breaker"""
    try:
        async with AlertServiceClient() as client:
            return await alert_breaker.call(client.send_alert, user_id, "ALERT", message, priority)
    except:
        # Fallback - log locally
        print(f"ALERT FALLBACK: {user_id} - {message}")
        return {"status": "fallback", "logged": True}


async def safe_send_message(user_id: str, message: str) -> Dict:
    """Send message with circuit breaker"""
    try:
        async with MessagingServiceClient() as client:
            return await messaging_breaker.call(client.send_user_notification, user_id, message)
    except:
        # Fallback - log locally
        print(f"MESSAGE FALLBACK: {user_id} - {message}")
        return {"status": "fallback", "logged": True}