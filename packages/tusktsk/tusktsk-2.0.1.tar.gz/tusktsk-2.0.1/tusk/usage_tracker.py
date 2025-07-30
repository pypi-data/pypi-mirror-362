"""
TuskLang SDK Usage Tracking Module
Enterprise-grade silent usage tracking for Python SDK
"""

import hashlib
import hmac
import json
import time
import uuid
import threading
import queue
import requests
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque

@dataclass
class UsageEvent:
    """Represents a usage event"""
    timestamp: float
    session_id: str
    event_type: str
    event_data: Dict[str, Any]
    user_id: Optional[str] = None
    license_key_hash: Optional[str] = None

@dataclass
class UsageMetrics:
    """Represents usage metrics"""
    total_events: int
    events_by_type: Dict[str, int]
    unique_users: int
    session_duration: float
    api_calls: int
    errors: int
    last_activity: float

class TuskUsageTracker:
    """Silent usage tracking system for TuskLang Python SDK"""
    
    def __init__(self, api_key: str, endpoint: str = "https://api.tusklang.org/v1/usage"):
        self.api_key = api_key
        self.endpoint = endpoint
        self.session_id = str(uuid.uuid4())
        self.start_time = time.time()
        
        # Event storage
        self.events = deque(maxlen=10000)  # Keep last 10k events
        self.event_queue = queue.Queue()
        self.metrics = UsageMetrics(
            total_events=0,
            events_by_type=defaultdict(int),
            unique_users=0,
            session_duration=0.0,
            api_calls=0,
            errors=0,
            last_activity=time.time()
        )
        
        # User tracking
        self.users = set()
        self.user_sessions = defaultdict(list)
        
        # Configuration
        self.batch_size = 50
        self.flush_interval = 300  # 5 minutes
        self.max_retries = 3
        self.enabled = True
        
        # Threading
        self.lock = threading.RLock()
        self.worker_thread = None
        self.stop_event = threading.Event()
        
        # Start background worker
        self._start_worker()
    
    def _start_worker(self):
        """Start background worker thread"""
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
    
    def _worker_loop(self):
        """Background worker loop for processing events"""
        while not self.stop_event.is_set():
            try:
                # Process events in batches
                batch = []
                while len(batch) < self.batch_size:
                    try:
                        event = self.event_queue.get(timeout=1.0)
                        batch.append(event)
                    except queue.Empty:
                        break
                
                if batch:
                    self._send_batch(batch)
                
                # Sleep for flush interval
                time.sleep(self.flush_interval)
                
            except Exception as e:
                # Log error but continue
                self._log_error(f"Worker loop error: {str(e)}")
    
    def _send_batch(self, events: List[UsageEvent]):
        """Send batch of events to server"""
        try:
            batch_data = {
                "session_id": self.session_id,
                "timestamp": time.time(),
                "events": [asdict(event) for event in events],
                "metrics": asdict(self.metrics)
            }
            
            # Add signature for security
            signature = hmac.new(
                self.api_key.encode(),
                json.dumps(batch_data, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            batch_data["signature"] = signature
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.endpoint,
                json=batch_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self._log_event("batch_sent", {"count": len(events), "status": "success"})
            else:
                self._log_error(f"Failed to send batch: {response.status_code}")
                
        except Exception as e:
            self._log_error(f"Error sending batch: {str(e)}")
    
    def track_event(self, event_type: str, event_data: Dict[str, Any], user_id: Optional[str] = None):
        """Track a usage event"""
        if not self.enabled:
            return
        
        try:
            with self.lock:
                # Create event
                event = UsageEvent(
                    timestamp=time.time(),
                    session_id=self.session_id,
                    event_type=event_type,
                    event_data=event_data,
                    user_id=user_id,
                    license_key_hash=self._hash_license_key()
                )
                
                # Add to storage
                self.events.append(event)
                self.event_queue.put(event)
                
                # Update metrics
                self.metrics.total_events += 1
                self.metrics.events_by_type[event_type] += 1
                self.metrics.last_activity = time.time()
                
                # Track user
                if user_id:
                    self.users.add(user_id)
                    self.user_sessions[user_id].append(event)
                    self.metrics.unique_users = len(self.users)
                
                # Update session duration
                self.metrics.session_duration = time.time() - self.start_time
                
        except Exception as e:
            self._log_error(f"Error tracking event: {str(e)}")
    
    def track_api_call(self, endpoint: str, method: str, status_code: int, duration: float):
        """Track API call"""
        self.track_event("api_call", {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration": duration
        })
        
        with self.lock:
            self.metrics.api_calls += 1
            if status_code >= 400:
                self.metrics.errors += 1
    
    def track_error(self, error_type: str, error_message: str, stack_trace: Optional[str] = None):
        """Track error occurrence"""
        self.track_event("error", {
            "error_type": error_type,
            "error_message": error_message,
            "stack_trace": stack_trace
        })
        
        with self.lock:
            self.metrics.errors += 1
    
    def track_feature_usage(self, feature: str, success: bool, metadata: Optional[Dict[str, Any]] = None):
        """Track feature usage"""
        event_data = {
            "feature": feature,
            "success": success
        }
        if metadata:
            event_data.update(metadata)
        
        self.track_event("feature_usage", event_data)
    
    def track_performance(self, operation: str, duration: float, memory_usage: Optional[float] = None):
        """Track performance metrics"""
        event_data = {
            "operation": operation,
            "duration": duration
        }
        if memory_usage:
            event_data["memory_usage"] = memory_usage
        
        self.track_event("performance", event_data)
    
    def track_security_event(self, event_type: str, severity: str, details: Dict[str, Any]):
        """Track security events"""
        self.track_event("security", {
            "security_type": event_type,
            "severity": severity,
            "details": details
        })
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary"""
        with self.lock:
            return {
                "session_id": self.session_id,
                "start_time": self.start_time,
                "current_time": time.time(),
                "session_duration": self.metrics.session_duration,
                "total_events": self.metrics.total_events,
                "events_by_type": dict(self.metrics.events_by_type),
                "unique_users": self.metrics.unique_users,
                "api_calls": self.metrics.api_calls,
                "errors": self.metrics.errors,
                "last_activity": self.metrics.last_activity,
                "queue_size": self.event_queue.qsize(),
                "enabled": self.enabled
            }
    
    def get_events_by_type(self, event_type: str, limit: int = 100) -> List[UsageEvent]:
        """Get events of specific type"""
        with self.lock:
            events = [event for event in self.events if event.event_type == event_type]
            return events[-limit:]  # Return last N events
    
    def get_user_events(self, user_id: str, limit: int = 100) -> List[UsageEvent]:
        """Get events for specific user"""
        with self.lock:
            return self.user_sessions.get(user_id, [])[-limit:]
    
    def flush_events(self):
        """Manually flush events to server"""
        try:
            batch = []
            while not self.event_queue.empty() and len(batch) < self.batch_size:
                try:
                    event = self.event_queue.get_nowait()
                    batch.append(event)
                except queue.Empty:
                    break
            
            if batch:
                self._send_batch(batch)
                
        except Exception as e:
            self._log_error(f"Error flushing events: {str(e)}")
    
    def set_enabled(self, enabled: bool):
        """Enable or disable usage tracking"""
        self.enabled = enabled
        self.track_event("tracking_toggle", {"enabled": enabled})
    
    def _hash_license_key(self) -> Optional[str]:
        """Hash license key for privacy"""
        # In real implementation, get license key from protection system
        return None
    
    def _log_error(self, message: str):
        """Log error internally"""
        # In production, use proper logging
        print(f"TuskUsageTracker Error: {message}")
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log internal event"""
        # For debugging purposes
        pass
    
    def shutdown(self):
        """Shutdown the usage tracker"""
        self.stop_event.set()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5.0)
        
        # Flush remaining events
        self.flush_events()

# Global usage tracker instance
_usage_tracker_instance: Optional[TuskUsageTracker] = None

def initialize_usage_tracker(api_key: str, endpoint: Optional[str] = None) -> TuskUsageTracker:
    """Initialize global usage tracker instance"""
    global _usage_tracker_instance
    if endpoint:
        _usage_tracker_instance = TuskUsageTracker(api_key, endpoint)
    else:
        _usage_tracker_instance = TuskUsageTracker(api_key)
    return _usage_tracker_instance

def get_usage_tracker() -> TuskUsageTracker:
    """Get global usage tracker instance"""
    if _usage_tracker_instance is None:
        raise RuntimeError("Usage tracker not initialized. Call initialize_usage_tracker() first.")
    return _usage_tracker_instance

# Convenience functions
def track_event(event_type: str, event_data: Dict[str, Any], user_id: Optional[str] = None):
    """Convenience function to track event"""
    try:
        tracker = get_usage_tracker()
        tracker.track_event(event_type, event_data, user_id)
    except Exception:
        pass  # Silently fail if tracker not available

def track_api_call(endpoint: str, method: str, status_code: int, duration: float):
    """Convenience function to track API call"""
    try:
        tracker = get_usage_tracker()
        tracker.track_api_call(endpoint, method, status_code, duration)
    except Exception:
        pass

def track_error(error_type: str, error_message: str, stack_trace: Optional[str] = None):
    """Convenience function to track error"""
    try:
        tracker = get_usage_tracker()
        tracker.track_error(error_type, error_message, stack_trace)
    except Exception:
        pass 