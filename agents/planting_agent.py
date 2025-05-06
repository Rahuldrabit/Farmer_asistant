from services.gemini_service import GeminiService
from services.weather_service import WeatherService
from utils.prompt_templates import PromptTemplates
from schemas.request_models import PlantingPlanRequest
from schemas.response_models import PlantingPlanResponse, PlantingRecommendation
import json

class PlantingAgent:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.weather_service = WeatherService()
    
    async def create_planting_plan(self, request: PlantingPlanRequest) -> PlantingPlanResponse:
        """Create a seasonal planting plan"""
        
        # Get current weather conditions
        try:
            weather_data = await self.weather_service.get_weather_forecast(request.location, days=7)
            weather_conditions = self._summarize_weather(weather_data)
        except Exception as e:
            weather_conditions = "Weather data unavailable. Providing general recommendations."
        
        # Format the prompt with the request data
        prompt = PromptTemplates.PLANTING_PLAN.format(
            location=request.location,
            season=request.season or "current season",
            plant_types=", ".join(request.plant_types) if request.plant_types else "all suitable plants",
            garden_size=request.garden_size or "average garden",
            weather_conditions=weather_conditions
        )
        
        # Add a system instruction to format the output as JSON
        system_instruction = """
        You are an expert gardener and agricultural advisor AI. Provide a planting plan in JSON format with the following structure:
        {
          "location": "The location",
          "season": "The current or specified season",
          "recommendations": [
            {
              "plant_name": "Name of the plant",
              "suitable_time": "When to plant",
              "growing_conditions": "Required conditions",
              "care_instructions": "How to care for the plant"
            }
          ],
          "general_advice": "General gardening advice for this location and season"
        }
        """
        
        # Get the response from Gemini
        response_text = await self.gemini_service.generate_content(prompt, system_instruction)
        
        # Extract JSON from the response
        try:
            # Sometimes Gemini might wrap the JSON in markdown code blocks, so let's handle that
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].strip()
            else:
                json_str = response_text
            
            response_data = json.loads(json_str)
            return PlantingPlanResponse(**response_data)
        except Exception as e:
            # Create a fallback response
            return PlantingPlanResponse(
                location=request.location,
                season=request.season or "current season",
                recommendations=[],
                general_advice="Unable to generate specific recommendations. Please try again with more specific information."
            )
    
    def _summarize_weather(self, weather_data):
        """Summarize weather data into a human-readable format"""
        if not weather_data or "list" not in weather_data:
            return "Weather data unavailable"
        
        forecasts = weather_data["list"]
        if not forecasts:
            return "No forecast data available"
        
        # Extract some useful information
        avg_temp = sum(day["main"]["temp"] for day in forecasts) / len(forecasts)
        max_temp = max(day["main"]["temp_max"] for day in forecasts)
        min_temp = min(day["main"]["temp_min"] for day in forecasts)
        
        precipitation_days = sum(1 for day in forecasts if 
                                "rain" in day or 
                                any(weather["main"] in ["Rain", "Snow", "Drizzle"] for weather in day["weather"]))
        
        summary = f"Average temperature: {avg_temp:.1f}°C (Range: {min_temp:.1f}°C to {max_temp:.1f}°C). "
        summary += f"Precipitation expected on {precipitation_days} out of {len(forecasts)} days."
        
        return summary
