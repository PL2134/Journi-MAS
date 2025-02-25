from typing import Any, Optional
from smolagents.tools import Tool
import datetime
import random
import os
import requests

class GetWeatherForecastTool(Tool):
    name = "get_weather_forecast"
    description = "Gets the weather forecast for a travel destination."
    inputs = {
        'destination': {'type': 'string', 'description': 'City or location name'},
        'days': {'type': 'integer', 'description': 'Number of days to forecast (default: 3)'}
    }
    output_type = "string"

    def __init__(self, api_key=None):
        super().__init__()
        # You can set an API key for a real weather service like OpenWeatherMap
        self.api_key = api_key or os.environ.get("WEATHER_API_KEY")
        
        # Weather conditions for demo/fallback
        self.weather_conditions = [
            "Sunny", "Partly Cloudy", "Cloudy", "Light Rain", 
            "Heavy Rain", "Thunderstorms", "Windy", "Foggy", "Snow", "Clear"
        ]

    def forward(self, destination: str, days: int = 3) -> str:
        try:
            # Try to use a real weather API if the API key is available
            if self.api_key:
                try:
                    url = f"http://api.openweathermap.org/data/2.5/forecast?q={destination}&appid={self.api_key}&units=metric"
                    response = requests.get(url)
                    data = response.json()
                    
                    if response.status_code != 200:
                        # Fall back to demo method if API call fails
                        return self._generate_demo_forecast(destination, days)
                    
                    # Process and format forecast data
                    forecast_text = f"🌦️ Weather forecast for {destination}:\n\n"
                    
                    # Group forecasts by day
                    forecasts_by_day = {}
                    for item in data['list'][:days * 8]:  # API returns data in 3-hour intervals
                        date = item['dt_txt'].split(' ')[0]
                        if date not in forecasts_by_day:
                            forecasts_by_day[date] = []
                        forecasts_by_day[date].append(item)
                    
                    # Format each day's forecast
                    for date, items in list(forecasts_by_day.items())[:days]:
                        day_name = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                        temps = [item['main']['temp'] for item in items]
                        avg_temp = sum(temps) / len(temps)
                        conditions = [item['weather'][0]['main'] for item in items]
                        most_common = max(set(conditions), key=conditions.count)
                        
                        precipitation = any('Rain' in item['weather'][0]['main'] or 'Snow' in item['weather'][0]['main'] for item in items)
                        precipitation_chance = "60%" if precipitation else "0%"
                        
                        forecast_text += f"• {day_name}, {date}: {most_common}, {min(temps):.1f}°C to {max(temps):.1f}°C"
                        if precipitation:
                            forecast_text += f", {precipitation_chance} chance of precipitation"
                        forecast_text += "\n"
                    
                    # Add packing recommendations
                    forecast_text += self._generate_packing_tips(forecasts_by_day)
                    
                    return forecast_text
                
                except Exception:
                    # Fall back to demo method if any error occurs
                    return self._generate_demo_forecast(destination, days)
            
            # If no API key is available, use the demo method
            return self._generate_demo_forecast(destination, days)
        
        except Exception as e:
            return f"Error retrieving weather data for {destination}: {str(e)}"
    
    def _generate_demo_forecast(self, destination: str, days: int) -> str:
        # Create a deterministic but seemingly random forecast based on destination name
        seed = sum(ord(c) for c in destination)
        random.seed(seed)
        
        # Generate forecast data
        forecast_text = f"🌦️ Weather forecast for {destination}:\n\n"
        
        today = datetime.datetime.now()
        temp_base = random.randint(10, 25)  # Base temperature varies by destination
        
        for i in range(days):
            day = today + datetime.timedelta(days=i)
            day_name = day.strftime("%A")
            date = day.strftime("%b %d")
            
            # "Random" but deterministic weather for the demo
            condition = self.weather_conditions[random.randint(0, len(self.weather_conditions)-1)]
            temp_high = temp_base + random.randint(0, 10)  # Celsius
            temp_low = temp_high - random.randint(5, 15)
            precipitation = random.randint(0, 100) if "Rain" in condition or "Snow" in condition or "Thunder" in condition else 0
            
            forecast_text += f"• {day_name}, {date}: {condition}, {temp_low}°C to {temp_high}°C"
            if precipitation > 0:
                forecast_text += f", {precipitation}% chance of precipitation"
            forecast_text += "\n"
        
        # Add packing recommendations
        cold_days = sum(1 for i in range(days) if temp_base + 5 < 15)
        rainy_days = sum(1 for i in range(days) if "Rain" in self.weather_conditions[random.randint(0, len(self.weather_conditions)-1)])
        hot_days = sum(1 for i in range(days) if temp_base + 5 > 25)
        
        forecast_text += "\n🧳 Packing tips: "
        if cold_days > days/2:
            forecast_text += "Bring warm layers and a jacket. "
        elif cold_days > 0:
            forecast_text += "Pack a light jacket for cooler periods. "
        
        if rainy_days > 0:
            forecast_text += "Don't forget an umbrella or rain gear. "
        
        if hot_days > days/2:
            forecast_text += "Bring sunscreen, sunglasses, and light clothing. "
        
        return forecast_text
    
    def _generate_packing_tips(self, forecasts_by_day):
        # Extract temperature ranges across all days
        all_temps = []
        has_rain = False
        has_snow = False
        
        for day_items in forecasts_by_day.values():
            for item in day_items:
                all_temps.append(item['main']['temp'])
                if 'Rain' in item['weather'][0]['main']:
                    has_rain = True
                if 'Snow' in item['weather'][0]['main']:
                    has_snow = True
        
        min_temp = min(all_temps) if all_temps else 0
        max_temp = max(all_temps) if all_temps else 30
        
        # Generate packing tips based on conditions
        tips = "\n🧳 Packing tips: "
        
        if min_temp < 5:
            tips += "Bring a heavy winter coat, gloves, and hat. "
        elif min_temp < 15:
            tips += "Pack a warm jacket and layers. "
        elif min_temp < 20:
            tips += "Bring a light jacket for evenings. "
        
        if max_temp > 25:
            tips += "Pack light, breathable clothing for warm days. "
        
        if has_rain:
            tips += "Don't forget an umbrella and waterproof footwear. "
        
        if has_snow:
            tips += "Bring waterproof boots and warm socks. "
        
        if max_temp > 22:
            tips += "Sunscreen and sunglasses are recommended. "
        
        return tips
