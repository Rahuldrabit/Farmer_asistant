import httpx
import asyncio
import time
from typing import Dict, Any
from config import WEATHER_API_KEY, WEATHER_RATE_LIMIT

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = WEATHER_API_KEY
        self.request_times = []
        self.lock = asyncio.Lock()
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting for the weather API"""
        async with self.lock:
            current_time = time.time()
            # Remove timestamps older than a minute
            self.request_times = [t for t in self.request_times if current_time - t < 60]
            
            if len(self.request_times) >= WEATHER_RATE_LIMIT:
                oldest_request = self.request_times[0]
                sleep_time = 60 - (current_time - oldest_request)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self.request_times.append(time.time())
    
    async def get_weather_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """Get weather forecast for a location"""
        await self._enforce_rate_limit()
        
        async with httpx.AsyncClient() as client:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric",
                "cnt": min(days, 7)  # OpenWeatherMap free tier limits to 7 days
            }
            
            response = await client.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            
            return response.json()
