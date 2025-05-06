from services.gemini_service import GeminiService
from services.weather_service import WeatherService
from utils.prompt_templates import PromptTemplates
from schemas.request_models import WeatherForecastRequest
from schemas.response_models import WeatherForecastResponse, WeatherForecast
import json
from datetime import datetime

class WeatherAgent:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.weather_service = WeatherService()
    
    async def get_forecast_with_interpretation(self, request: WeatherForecastRequest) -> WeatherForecastResponse:
        """Get weather forecast with agricultural interpretation"""
        
        # Get weather forecast
        try:
            weather_data = await self.weather_service.get_weather_forecast(request.location, days=request.days)
            formatted_forecast = self._format_weather_data(weather_data)
            
            # Generate agricultural interpretation
            prompt = PromptTemplates.WEATHER_INTERPRETATION.format(
                location=request.location,
                weather_data=json.dumps(formatted_forecast, indent=2)
            )
            
            interpretation = await self.gemini_service.generate_content(
                prompt,
                system_instruction="You are an agricultural meteorologist. Provide practical advice for gardeners and farmers based on the weather forecast."
            )
            
            # Create response object
            forecasts = []
            for day_data in formatted_forecast:
                forecasts.append(WeatherForecast(
                    date=day_data["date"],
                    temperature_high=day_data["temperature_high"],
                    temperature_low=day_data["temperature_low"],
                    precipitation_chance=day_data["precipitation_chance"],
                    description=day_data["description"]
                ))
            
            return WeatherForecastResponse(
                location=request.location,
                forecasts=forecasts,
                planting_advice=interpretation
            )
            
        except Exception as e:
            # Return a placeholder response if the weather service fails
            return WeatherForecastResponse(
                location=request.location,
                forecasts=[],
                planting_advice="Weather forecast unavailable. Please try again later."
            )
    
    def _format_weather_data(self, weather_data):
        """Format the raw weather API data into a more usable structure"""
        if not weather_data or "list" not in weather_data:
            return []
        
        formatted_data = []
        for day in weather_data["list"]:
            # OpenWeatherMap provides forecasts in 3-hour intervals
            # We'll simplify by grouping by date
            date_str = datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")
            
            # Find or create the entry for this date
            day_entry = next((item for item in formatted_data if item["date"] == date_str), None)
            if not day_entry:
                day_entry = {
                    "date": date_str,
                    "temperature_high": day["main"]["temp_max"],
                    "temperature_low": day["main"]["temp_min"],
                    "precipitation_chance": day["pop"] if "pop" in day else 0,
                    "description": day["weather"][0]["description"] if "weather" in day and day["weather"] else "No data"
                }
                formatted_data.append(day_entry)
            else:
                # Update the existing entry with extremes
                day_entry["temperature_high"] = max(day_entry["temperature_high"], day["main"]["temp_max"])
                day_entry["temperature_low"] = min(day_entry["temperature_low"], day["main"]["temp_min"])
                day_entry["precipitation_chance"] = max(day_entry["precipitation_chance"], 
                                                       day["pop"] if "pop" in day else 0)
        
        return formatted_data
