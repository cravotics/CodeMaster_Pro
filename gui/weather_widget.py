"""
Weather Widget for CodeMaster Pro

Learning Notes:
- This module demonstrates real-time data display in GUI
- Shows API integration with user interface
- Implements background updates and caching
- Demonstrates weather-based recommendations for developers
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict, Any, Optional
import threading
from datetime import datetime
from apis.weather_api import WeatherAPI
from utils.config import Config

class WeatherWidget:
    """
    Weather display widget with development recommendations.
    
    This class provides:
    1. Current weather conditions display
    2. Weather forecast information
    3. Development recommendations based on weather
    4. Location management and search
    5. Air quality information
    6. Background data updates
    """
    
    def __init__(self, parent: ctk.CTkFrame, weather_api: WeatherAPI, config: Config):
        """Initialize the weather widget."""
        
        self.parent = parent
        self.weather_api = weather_api
        self.config = config
        
        # Current weather data
        self.current_weather = None
        self.forecast_data = None
        
        # Create the interface
        self.setup_layout()
        self.setup_current_weather()
        self.setup_forecast_display()
        self.setup_recommendations()
        self.setup_controls()
        
        # Load initial weather data
        self.load_weather_data()
        
        print("🌤️ Weather widget initialized")
    
    def setup_layout(self) -> None:
        """
        Set up the main layout for the weather widget.
        
        Learning Notes:
        - Grid layout management for complex interfaces
        - Responsive design with proper weight configuration
        - Component organization and visual hierarchy
        """
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Title section
        self.title_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))
        self.title_frame.grid_columnconfigure(1, weight=1)
        
        # Current weather (left side)
        self.current_frame = ctk.CTkFrame(self.main_frame)
        self.current_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 10), pady=5)
        
        # Right side container
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid_rowconfigure(1, weight=1)
        
        # Controls section (top right)
        self.controls_frame = ctk.CTkFrame(self.right_frame)
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 10))
        
        # Recommendations (bottom right)
        self.recommendations_frame = ctk.CTkFrame(self.right_frame)
        self.recommendations_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def setup_current_weather(self) -> None:
        """
        Set up the current weather display.
        
        Learning Notes:
        - Dynamic content display
        - Icon and emoji integration
        - Real-time data presentation
        """
        
        # Title
        weather_title = ctk.CTkLabel(
            self.title_frame,
            text="🌤️ Weather & Development Insights",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        weather_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Last updated indicator
        self.last_updated_label = ctk.CTkLabel(
            self.title_frame,
            text="Loading...",
            font=ctk.CTkFont(size=12)
        )
        self.last_updated_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Current weather title
        current_title = ctk.CTkLabel(
            self.current_frame,
            text="📍 Current Weather",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        current_title.pack(pady=(15, 10))
        
        # Location display
        self.location_label = ctk.CTkLabel(
            self.current_frame,
            text="New York, US",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.location_label.pack(pady=5)
        
        # Temperature display
        self.temperature_label = ctk.CTkLabel(
            self.current_frame,
            text="--°C",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.temperature_label.pack(pady=10)
        
        # Condition display
        self.condition_label = ctk.CTkLabel(
            self.current_frame,
            text="Loading weather...",
            font=ctk.CTkFont(size=14)
        )
        self.condition_label.pack(pady=5)
        
        # Weather details frame
        details_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=20)
        
        # Details grid
        self.feels_like_label = ctk.CTkLabel(details_frame, text="Feels like: --°C")
        self.feels_like_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.humidity_label = ctk.CTkLabel(details_frame, text="Humidity: --%")
        self.humidity_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.wind_label = ctk.CTkLabel(details_frame, text="Wind: -- km/h")
        self.wind_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        self.pressure_label = ctk.CTkLabel(details_frame, text="Pressure: -- hPa")
        self.pressure_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        self.visibility_label = ctk.CTkLabel(details_frame, text="Visibility: -- km")
        self.visibility_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Forecast preview
        self.setup_forecast_preview()
    
    def setup_forecast_preview(self) -> None:
        """Set up a mini forecast display in the current weather section."""
        
        # Forecast title
        forecast_title = ctk.CTkLabel(
            self.current_frame,
            text="📅 5-Day Forecast",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        forecast_title.pack(pady=(20, 10))
        
        # Forecast container
        self.forecast_container = ctk.CTkFrame(self.current_frame)
        self.forecast_container.pack(fill="x", padx=10, pady=(0, 15))
        
        # Forecast items will be added here dynamically
        self.forecast_items = []
    
    def setup_forecast_display(self) -> None:
        """Set up the detailed forecast display."""
        # This will be expanded if needed - for now using preview in current weather
        pass
    
    def setup_recommendations(self) -> None:
        """
        Set up the development recommendations section.
        
        Learning Notes:
        - Dynamic recommendation system
        - Weather-based advice generation
        - Scrollable content display
        """
        
        # Recommendations title
        rec_title = ctk.CTkLabel(
            self.recommendations_frame,
            text="💡 Development Recommendations",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        rec_title.pack(pady=(15, 10))
        
        # Recommendations display
        self.recommendations_text = ctk.CTkTextbox(
            self.recommendations_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.recommendations_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Initial recommendations
        initial_text = """
🤖 Weather-Based Development Tips:

Loading personalized recommendations based on current weather conditions...

These recommendations help you optimize your development environment and productivity based on weather patterns and conditions.

Categories include:
• Productivity optimization
• Environment setup
• Break scheduling
• Project planning
• Health and comfort tips
        """
        self.recommendations_text.insert("1.0", initial_text)
        self.recommendations_text.configure(state="disabled")
    
    def setup_controls(self) -> None:
        """
        Set up weather controls and settings.
        
        Learning Notes:
        - User interaction controls
        - Location management
        - Settings integration
        """
        
        # Controls title
        controls_title = ctk.CTkLabel(
            self.controls_frame,
            text="🎛️ Weather Controls",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        controls_title.pack(pady=(15, 10))
        
        # Location input
        location_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        location_frame.pack(fill="x", padx=15, pady=10)
        
        location_label = ctk.CTkLabel(location_frame, text="Location:")
        location_label.pack(anchor="w", pady=(0, 5))
        
        self.location_entry = ctk.CTkEntry(
            location_frame,
            placeholder_text="Enter city name...",
            width=200
        )
        self.location_entry.pack(fill="x", pady=(0, 5))
        
        # Location buttons
        button_frame = ctk.CTkFrame(location_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        self.update_location_btn = ctk.CTkButton(
            button_frame,
            text="Update Location",
            width=120,
            command=self.update_location
        )
        self.update_location_btn.pack(side="left", padx=(0, 5))
        
        self.refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            width=80,
            command=self.refresh_weather
        )
        self.refresh_btn.pack(side="left")
        
        # Weather settings
        settings_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        settings_frame.pack(fill="x", padx=15, pady=10)
        
        settings_label = ctk.CTkLabel(settings_frame, text="Settings:")
        settings_label.pack(anchor="w", pady=(0, 5))
        
        # Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_cb = ctk.CTkCheckBox(
            settings_frame,
            text="Auto-refresh (30 min)",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        auto_refresh_cb.pack(anchor="w", pady=2)
        
        # Notifications toggle
        self.notifications_var = tk.BooleanVar(value=False)
        notifications_cb = ctk.CTkCheckBox(
            settings_frame,
            text="Weather notifications",
            variable=self.notifications_var
        )
        notifications_cb.pack(anchor="w", pady=2)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.controls_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)
    
    def load_weather_data(self) -> None:
        """
        Load weather data in background thread.
        
        Learning Notes:
        - Background threading for non-blocking operations
        - API data fetching and processing
        - UI updates from background threads
        """
        
        def fetch_weather():
            try:
                self.update_status("Loading weather data...")
                
                # Get current location from config or entry
                location = self.location_entry.get().strip() or self.config.get('weather_location', 'New York')
                
                # Fetch current weather
                self.current_weather = self.weather_api.get_current_weather(location)
                
                # Fetch forecast
                self.forecast_data = self.weather_api.get_forecast(location, 5)
                
                # Update UI on main thread
                self.parent.after(0, self.update_weather_display)
                
            except Exception as e:
                self.parent.after(0, lambda: self.update_status(f"Error: {str(e)}"))
        
        # Start background thread
        threading.Thread(target=fetch_weather, daemon=True).start()
    
    def update_weather_display(self) -> None:
        """Update the weather display with current data."""
        
        if not self.current_weather:
            return
        
        try:
            # Update location
            location = self.current_weather.get('location', 'Unknown')
            country = self.current_weather.get('country', '')
            if country:
                location += f", {country}"
            self.location_label.configure(text=location)
            
            # Update temperature
            temp = self.current_weather.get('temperature', 0)
            self.temperature_label.configure(text=f"{temp}°C")
            
            # Update condition
            condition = self.current_weather.get('description', 'Unknown').title()
            self.condition_label.configure(text=condition)
            
            # Update details
            feels_like = self.current_weather.get('feels_like', 0)
            humidity = self.current_weather.get('humidity', 0)
            wind_speed = self.current_weather.get('wind_speed', 0)
            pressure = self.current_weather.get('pressure', 0)
            visibility = self.current_weather.get('visibility', 0)
            
            self.feels_like_label.configure(text=f"Feels like: {feels_like}°C")
            self.humidity_label.configure(text=f"Humidity: {humidity}%")
            self.wind_label.configure(text=f"Wind: {wind_speed} km/h")
            self.pressure_label.configure(text=f"Pressure: {pressure} hPa")
            self.visibility_label.configure(text=f"Visibility: {visibility} km")
            
            # Update forecast
            self.update_forecast_display()
            
            # Update recommendations
            self.update_recommendations()
            
            # Update timestamp
            self.last_updated_label.configure(text=f"Updated: {datetime.now().strftime('%H:%M')}")
            
            self.update_status("Weather data updated successfully")
            
        except Exception as e:
            self.update_status(f"Display error: {str(e)}")
    
    def update_forecast_display(self) -> None:
        """Update the forecast preview."""
        
        # Clear existing forecast items
        for item in self.forecast_items:
            item.destroy()
        self.forecast_items.clear()
        
        if not self.forecast_data or 'forecasts' not in self.forecast_data:
            return
        
        forecasts = self.forecast_data['forecasts'][:5]  # Show 5 days
        
        for i, forecast in enumerate(forecasts):
            # Create forecast item frame
            item_frame = ctk.CTkFrame(self.forecast_container)
            item_frame.grid(row=0, column=i, padx=2, pady=5, sticky="ew")
            
            # Configure grid weight
            self.forecast_container.grid_columnconfigure(i, weight=1)
            
            # Date
            date_str = forecast.get('date', '')
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    day_name = date_obj.strftime('%a')
                except:
                    day_name = date_str[:3]
            else:
                day_name = f"Day {i+1}"
            
            date_label = ctk.CTkLabel(item_frame, text=day_name, font=ctk.CTkFont(size=10, weight="bold"))
            date_label.pack(pady=2)
            
            # Temperature range
            min_temp = forecast.get('min_temp', 0)
            max_temp = forecast.get('max_temp', 0)
            temp_label = ctk.CTkLabel(item_frame, text=f"{max_temp}°/{min_temp}°", font=ctk.CTkFont(size=10))
            temp_label.pack(pady=2)
            
            # Condition
            condition = forecast.get('condition', '').replace(' ', '\n')
            if len(condition) > 8:
                condition = condition[:8] + "..."
            condition_label = ctk.CTkLabel(item_frame, text=condition, font=ctk.CTkFont(size=9))
            condition_label.pack(pady=2)
            
            self.forecast_items.append(item_frame)
    
    def update_recommendations(self) -> None:
        """Update development recommendations based on weather."""
        
        if not self.current_weather:
            return
        
        recommendations = self.weather_api.get_development_recommendations(self.current_weather)
        
        # Format recommendations
        rec_text = "🌤️ Personalized Development Recommendations:\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            rec_text += f"{i}. {rec}\n\n"
        
        # Add general tips
        rec_text += "\n" + "="*50 + "\n"
        rec_text += "🧠 General Productivity Tips:\n\n"
        rec_text += "• Take regular breaks every 25-30 minutes\n"
        rec_text += "• Adjust your screen brightness based on ambient light\n"
        rec_text += "• Stay hydrated - aim for 8 glasses of water daily\n"
        rec_text += "• Use the weather as inspiration for your projects\n"
        rec_text += "• Plan outdoor activities during nice weather breaks\n"
        
        # Update display
        self.recommendations_text.configure(state="normal")
        self.recommendations_text.delete("1.0", "end")
        self.recommendations_text.insert("1.0", rec_text)
        self.recommendations_text.configure(state="disabled")
    
    def update_location(self) -> None:
        """Update weather location."""
        
        new_location = self.location_entry.get().strip()
        if not new_location:
            self.update_status("Please enter a location")
            return
        
        # Save to config
        self.config.set('weather_location', new_location)
        self.config.save()
        
        # Reload weather data
        self.load_weather_data()
    
    def refresh_weather(self) -> None:
        """Manually refresh weather data."""
        self.load_weather_data()
    
    def toggle_auto_refresh(self) -> None:
        """Toggle auto-refresh functionality."""
        if self.auto_refresh_var.get():
            self.start_auto_refresh()
            self.update_status("Auto-refresh enabled")
        else:
            self.update_status("Auto-refresh disabled")
    
    def start_auto_refresh(self) -> None:
        """Start auto-refresh timer."""
        if self.auto_refresh_var.get():
            # Schedule next refresh in 30 minutes
            self.parent.after(30 * 60 * 1000, self.auto_refresh_callback)
    
    def auto_refresh_callback(self) -> None:
        """Auto-refresh callback."""
        if self.auto_refresh_var.get():
            self.refresh_weather()
            self.start_auto_refresh()  # Schedule next refresh
    
    def update_status(self, message: str) -> None:
        """Update status message."""
        self.status_label.configure(text=message)
        print(f"Weather Widget: {message}")
        
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text="Ready")) 