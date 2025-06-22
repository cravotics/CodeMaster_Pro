"""
Weather API Integration for CodeMaster Pro

Learning Notes:
- This module demonstrates HTTP API integration in Python
- Shows asynchronous programming with requests
- Implements caching for API efficiency
- Demonstrates data parsing and error handling
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from utils.config import Config

class WeatherAPI:
    """
    Weather API integration for development environment enhancement.
    
    This class provides:
    1. Real-time weather data fetching
    2. Location-based weather services
    3. Weather-based development recommendations
    4. API response caching for efficiency
    5. Error handling and fallback mechanisms
    """
    
    def __init__(self, config: Config):
        """Initialize weather API with configuration."""
        
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # API configuration
        self.api_key = config.get_api_key('weather')
        self.base_url = config.get('api_endpoints', {}).get('weather', 
                                 'https://api.openweathermap.org/data/2.5')
        
        # Cache configuration
        self.cache_duration = timedelta(minutes=30)  # Cache for 30 minutes
        self.cache = {}
        
        # Default location
        self.default_location = config.get('weather_location', 'New York')
        
        print(f"🌤️ Weather API initialized - Default location: {self.default_location}")
    
    def get_current_weather(self, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather data for a location.
        
        Learning Notes:
        - HTTP GET requests with parameters
        - JSON response parsing
        - Error handling for network operations
        - Data transformation and formatting
        """
        
        location = location or self.default_location
        
        # Check cache first
        cache_key = f"current_{location}"
        if self._is_cached_valid(cache_key):
            self.logger.debug(f"Returning cached weather data for {location}")
            return self.cache[cache_key]['data']
        
        if not self.api_key:
            return self._get_fallback_weather(location)
        
        try:
            # Build API request URL
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'  # Celsius temperature
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Transform to our format
            weather_data = self._transform_current_weather(data)
            
            # Cache the result
            self._cache_data(cache_key, weather_data)
            
            self.logger.info(f"Weather data fetched for {location}")
            return weather_data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Weather API request failed: {e}")
            return self._get_fallback_weather(location)
        except Exception as e:
            self.logger.error(f"Weather data processing failed: {e}")
            return self._get_fallback_weather(location)
    
    def get_forecast(self, location: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for multiple days.
        
        Learning Notes:
        - Extended API requests with multiple parameters
        - List processing and data aggregation
        - Time-based data handling
        """
        
        location = location or self.default_location
        
        # Check cache
        cache_key = f"forecast_{location}_{days}"
        if self._is_cached_valid(cache_key):
            return self.cache[cache_key]['data']
        
        if not self.api_key:
            return self._get_fallback_forecast(location, days)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast_data = self._transform_forecast(data, days)
            
            self._cache_data(cache_key, forecast_data)
            
            return forecast_data
            
        except Exception as e:
            self.logger.error(f"Forecast API request failed: {e}")
            return self._get_fallback_forecast(location, days)
    
    def get_development_recommendations(self, weather_data: Dict[str, Any]) -> List[str]:
        """
        Generate development recommendations based on weather.
        
        Learning Notes:
        - Business logic implementation
        - Conditional processing based on data
        - User experience enhancement features
        """
        
        recommendations = []
        
        try:
            temperature = weather_data.get('temperature', 20)
            condition = weather_data.get('condition', '').lower()
            humidity = weather_data.get('humidity', 50)
            
            # Temperature-based recommendations
            if temperature < 10:
                recommendations.append("🔥 Cold weather detected! Perfect time for hot coffee and intense coding sessions.")
                recommendations.append("💡 Consider working on performance optimizations - your mind is sharp in cold weather!")
            elif temperature > 30:
                recommendations.append("🌞 Hot weather! Stay hydrated and consider shorter coding sessions.")
                recommendations.append("🏖️ Maybe it's time to work on that mobile app for beach activities?")
            else:
                recommendations.append("🌤️ Perfect weather for productive coding! Great conditions for focused work.")
            
            # Weather condition recommendations
            if 'rain' in condition:
                recommendations.append("🌧️ Rainy day perfect for indoor coding! Great time for documentation and refactoring.")
                recommendations.append("☔ Consider working on your backup and sync systems while it's raining outside.")
            elif 'snow' in condition:
                recommendations.append("❄️ Snowy weather! Perfect time for algorithm challenges and deep learning.")
            elif 'clear' in condition or 'sun' in condition:
                recommendations.append("☀️ Sunny day! Great for pair programming or outdoor coding sessions.")
                recommendations.append("🌅 Consider working on UI/UX - bright weather inspires creative design!")
            
            # Humidity recommendations
            if humidity > 80:
                recommendations.append("💨 High humidity detected! Make sure your equipment stays cool.")
            elif humidity < 30:
                recommendations.append("🌵 Low humidity! Stay hydrated and protect your electronics from static.")
            
            # Time-based recommendations
            current_hour = datetime.now().hour
            if 6 <= current_hour <= 10:
                recommendations.append("🌅 Morning hours! Best time for complex problem-solving and architecture design.")
            elif 14 <= current_hour <= 17:
                recommendations.append("☕ Afternoon productivity! Great time for testing and debugging.")
            elif 18 <= current_hour <= 22:
                recommendations.append("🌙 Evening coding! Perfect for creative projects and experimentation.")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            recommendations.append("🤖 Unable to generate weather-based recommendations, but coding is always a good idea!")
        
        return recommendations
    
    def _transform_current_weather(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform API response to our internal format."""
        
        return {
            'location': api_data.get('name', 'Unknown'),
            'country': api_data.get('sys', {}).get('country', ''),
            'temperature': round(api_data.get('main', {}).get('temp', 0), 1),
            'feels_like': round(api_data.get('main', {}).get('feels_like', 0), 1),
            'humidity': api_data.get('main', {}).get('humidity', 0),
            'pressure': api_data.get('main', {}).get('pressure', 0),
            'condition': api_data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': api_data.get('weather', [{}])[0].get('description', ''),
            'icon': api_data.get('weather', [{}])[0].get('icon', ''),
            'wind_speed': api_data.get('wind', {}).get('speed', 0),
            'wind_direction': api_data.get('wind', {}).get('deg', 0),
            'visibility': api_data.get('visibility', 0) / 1000,  # Convert to km
            'uv_index': api_data.get('uvi', 0),
            'last_updated': datetime.now().isoformat()
        }
    
    def _transform_forecast(self, api_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Transform forecast API response to our internal format."""
        
        forecasts = []
        daily_data = {}
        
        for item in api_data.get('list', []):
            date_str = item['dt_txt'].split(' ')[0]
            
            if date_str not in daily_data:
                daily_data[date_str] = {
                    'date': date_str,
                    'temperatures': [],
                    'conditions': [],
                    'humidity': [],
                    'descriptions': []
                }
            
            daily_data[date_str]['temperatures'].append(item['main']['temp'])
            daily_data[date_str]['conditions'].append(item['weather'][0]['main'])
            daily_data[date_str]['humidity'].append(item['main']['humidity'])
            daily_data[date_str]['descriptions'].append(item['weather'][0]['description'])
        
        # Process daily summaries
        for date_str, data in list(daily_data.items())[:days]:
            forecasts.append({
                'date': date_str,
                'min_temp': round(min(data['temperatures']), 1),
                'max_temp': round(max(data['temperatures']), 1),
                'avg_temp': round(sum(data['temperatures']) / len(data['temperatures']), 1),
                'condition': max(set(data['conditions']), key=data['conditions'].count),
                'avg_humidity': round(sum(data['humidity']) / len(data['humidity']), 1),
                'description': max(set(data['descriptions']), key=data['descriptions'].count)
            })
        
        return {
            'location': api_data.get('city', {}).get('name', 'Unknown'),
            'forecasts': forecasts,
            'last_updated': datetime.now().isoformat()
        }
    
    def _is_cached_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key]['timestamp']
        return datetime.now() - cached_time < self.cache_duration
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache data with timestamp."""
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def _get_fallback_weather(self, location: str) -> Dict[str, Any]:
        """Return fallback weather data when API is unavailable."""
        
        return {
            'location': location,
            'country': '',
            'temperature': 20.0,
            'feels_like': 20.0,
            'humidity': 50,
            'pressure': 1013,
            'condition': 'Unknown',
            'description': 'Weather data unavailable',
            'icon': '01d',
            'wind_speed': 0,
            'wind_direction': 0,
            'visibility': 10,
            'uv_index': 0,
            'last_updated': datetime.now().isoformat(),
            'fallback': True
        }
    
    def _get_fallback_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Return fallback forecast data when API is unavailable."""
        
        forecasts = []
        base_date = datetime.now()
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            forecasts.append({
                'date': date.strftime('%Y-%m-%d'),
                'min_temp': 15.0,
                'max_temp': 25.0,
                'avg_temp': 20.0,
                'condition': 'Unknown',
                'avg_humidity': 50,
                'description': 'Weather data unavailable'
            })
        
        return {
            'location': location,
            'forecasts': forecasts,
            'last_updated': datetime.now().isoformat(),
            'fallback': True
        }
    
    def search_locations(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for locations by name.
        
        Learning Notes:
        - Geographic API integration
        - Search functionality implementation
        - Data filtering and formatting
        """
        
        if not self.api_key:
            return [{'name': query, 'country': '', 'state': ''}]
        
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': query,
                'limit': 5,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            locations = response.json()
            
            return [
                {
                    'name': loc.get('name', ''),
                    'country': loc.get('country', ''),
                    'state': loc.get('state', ''),
                    'lat': loc.get('lat', 0),
                    'lon': loc.get('lon', 0)
                }
                for loc in locations
            ]
            
        except Exception as e:
            self.logger.error(f"Location search failed: {e}")
            return [{'name': query, 'country': '', 'state': ''}]
    
    def get_air_quality(self, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Get air quality data for a location.
        
        Learning Notes:
        - Extended API functionality
        - Health and environment data integration
        - Complex data structures handling
        """
        
        location = location or self.default_location
        
        if not self.api_key:
            return {'aqi': 3, 'description': 'Moderate', 'components': {}}
        
        try:
            # First get coordinates for the location
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                'q': location,
                'limit': 1,
                'appid': self.api_key
            }
            
            geo_response = requests.get(geo_url, params=geo_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data:
                raise Exception("Location not found")
            
            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
            
            # Get air quality data
            aq_url = f"{self.base_url}/air_pollution"
            aq_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            aq_response = requests.get(aq_url, params=aq_params, timeout=10)
            aq_response.raise_for_status()
            aq_data = aq_response.json()
            
            # Transform air quality data
            aqi_levels = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
            current_aq = aq_data['list'][0]
            
            return {
                'aqi': current_aq['main']['aqi'],
                'description': aqi_levels[current_aq['main']['aqi'] - 1],
                'components': current_aq['components'],
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Air quality request failed: {e}")
            return {
                'aqi': 3,
                'description': 'Moderate',
                'components': {},
                'last_updated': datetime.now().isoformat(),
                'fallback': True
            } 