"""
Adafruit.IO utility functions for habitat monitoring
"""

import logging
import warnings
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

# Suppress pkg_resources deprecation warning from Adafruit.IO library
# This warning comes from the third-party library (adafruit-io v2.8.0), not our code
# The library uses pkg_resources which is deprecated in setuptools>=81
# TODO: Monitor for updates to adafruit-io library that fix this deprecation
# See: https://github.com/adafruit/Adafruit_IO_Python/issues
warnings.filterwarnings("ignore", message="pkg_resources is deprecated.*")

# Set up logging
logger = logging.getLogger(__name__)

class AdafruitIOConnector:
    """Handles Adafruit.IO connections and data operations"""
    
    def __init__(self, username: str, api_key: str):
        self.username = username
        self.api_key = api_key
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Adafruit.IO client"""
        try:
            from Adafruit_IO import Client
            self.client = Client(self.username, self.api_key)
            logger.info("Adafruit.IO client initialized successfully")
        except ImportError:
            logger.error("Adafruit.IO library not installed")
            raise ImportError("Install with: pip install adafruit-io")
        except Exception as e:
            logger.error(f"Failed to initialize Adafruit.IO client: {e}")
            raise
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test connection to Adafruit.IO
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if not self.client:
                return False, "Client not initialized"
            
            # Try to get feeds list to test connection
            feeds = self.client.feeds()
            return True, f"Connected successfully. Found {len(feeds)} feeds."
            
        except Exception as e:
            error_msg = str(e)
            if 'Unauthorized' in error_msg or '401' in error_msg:
                return False, "Invalid username or API key"
            elif 'Network' in error_msg or 'Connection' in error_msg:
                return False, "Network connection failed"
            else:
                return False, f"Connection error: {error_msg}"
    
    def get_feed_value(self, feed_name: str) -> Tuple[bool, Optional[float], str]:
        """
        Get the latest value from a feed
        
        Args:
            feed_name: Name of the feed
            
        Returns:
            Tuple[bool, Optional[float], str]: (success, value, message)
        """
        try:
            if not self.client:
                return False, None, "Client not initialized"
            
            data = self.client.receive(feed_name)
            value = float(data.value)
            timestamp = data.created_at
            
            return True, value, f"Retrieved at {timestamp}"
            
        except Exception as e:
            error_msg = str(e)
            if 'does not exist' in error_msg.lower() or 'not found' in error_msg.lower():
                return False, None, f"Feed '{feed_name}' not found"
            else:
                return False, None, f"Error reading feed: {error_msg}"
    
    def get_multiple_feeds(self, feed_names: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """
        Get values from multiple feeds
        
        Args:
            feed_names: Dict mapping display names to feed names
            
        Returns:
            Dict with feed data including success status, value, and message
        """
        results = {}
        
        for display_name, feed_name in feed_names.items():
            success, value, message = self.get_feed_value(feed_name)
            results[display_name] = {
                'success': success,
                'value': value,
                'message': message,
                'feed_name': feed_name,
                'timestamp': datetime.now().isoformat()
            }
        
        return results
    
    def create_feed_if_not_exists(self, feed_name: str, description: str = '') -> Tuple[bool, str]:
        """
        Create a feed if it doesn't exist
        
        Args:
            feed_name: Name of the feed to create
            description: Optional description
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if not self.client:
                return False, "Client not initialized"
            
            # Check if feed exists
            try:
                self.client.feeds(feed_name)
                return True, f"Feed '{feed_name}' already exists"
            except:
                # Feed doesn't exist, create it
                feed_data = {'name': feed_name}
                if description:
                    feed_data['description'] = description
                
                self.client.create_feed(feed_data)
                return True, f"Feed '{feed_name}' created successfully"
                
        except Exception as e:
            return False, f"Failed to create feed: {str(e)}"
    
    def send_data(self, feed_name: str, value: float) -> Tuple[bool, str]:
        """
        Send data to a feed
        
        Args:
            feed_name: Name of the feed
            value: Value to send
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if not self.client:
                return False, "Client not initialized"
            
            self.client.send_data(feed_name, value)
            return True, f"Sent {value} to {feed_name}"
            
        except Exception as e:
            return False, f"Failed to send data: {str(e)}"
    
    def get_feed_history(self, feed_name: str, limit: int = 10) -> Tuple[bool, list, str]:
        """
        Get historical data from a feed
        
        Args:
            feed_name: Name of the feed
            limit: Number of recent records to retrieve
            
        Returns:
            Tuple[bool, list, str]: (success, data_list, message)
        """
        try:
            if not self.client:
                return False, [], "Client not initialized"
            
            data = self.client.data(feed_name, limit=limit)
            history = []
            
            for item in data:
                history.append({
                    'value': float(item.value),
                    'timestamp': item.created_at,
                    'feed_id': item.feed_id
                })
            
            return True, history, f"Retrieved {len(history)} records"
            
        except Exception as e:
            return False, [], f"Failed to get history: {str(e)}"

def create_adafruit_connector(db_manager) -> Optional[AdafruitIOConnector]:
    """
    Create Adafruit.IO connector from database settings
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        AdafruitIOConnector instance or None if not configured
    """
    try:
        username = db_manager.get_setting('adafruit_io_username')
        api_key = db_manager.get_setting('adafruit_io_key')
        
        if not username or not api_key:
            logger.warning("Adafruit.IO credentials not configured")
            return None
        
        return AdafruitIOConnector(username, api_key)
        
    except Exception as e:
        logger.error(f"Failed to create Adafruit.IO connector: {e}")
        return None

def get_sensor_thresholds(db_manager) -> Dict[str, Dict[str, float]]:
    """
    Get sensor alert thresholds from database
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        Dict with temperature and humidity thresholds
    """
    try:
        return {
            'temperature': {
                'min': float(db_manager.get_setting('temp_min') or 20),
                'max': float(db_manager.get_setting('temp_max') or 35)
            },
            'humidity': {
                'min': float(db_manager.get_setting('humidity_min') or 60),
                'max': float(db_manager.get_setting('humidity_max') or 80)
            }
        }
    except Exception as e:
        logger.error(f"Failed to get sensor thresholds: {e}")
        return {
            'temperature': {'min': 20.0, 'max': 35.0},
            'humidity': {'min': 60.0, 'max': 80.0}
        }

def check_alert_conditions(value: float, thresholds: Dict[str, float]) -> Tuple[str, str]:
    """
    Check if a sensor value is within acceptable thresholds
    
    Args:
        value: Sensor reading
        thresholds: Dict with 'min' and 'max' keys
        
    Returns:
        Tuple[str, str]: (status, color) where status is 'optimal', 'low', or 'high'
    """
    if value < thresholds['min']:
        return 'low', '#2196F3'  # Blue for low
    elif value > thresholds['max']:
        return 'high', '#f44336'  # Red for high
    else:
        return 'optimal', '#4CAF50'  # Green for optimal