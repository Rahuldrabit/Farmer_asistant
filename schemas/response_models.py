from pydantic import BaseModel
from typing import List, Optional

class DiseaseResponse(BaseModel):
    plant_name: str
    possible_diseases: List[str]
    recommendations: List[str]
    preventive_measures: List[str]
    organic_solutions: Optional[List[str]] = None
    chemical_solutions: Optional[List[str]] = None

class PlantingRecommendation(BaseModel):
    plant_name: str
    suitable_time: str
    growing_conditions: str
    care_instructions: str

class PlantingPlanResponse(BaseModel):
    location: str
    season: str
    recommendations: List[PlantingRecommendation]
    general_advice: str

class WeatherForecast(BaseModel):
    date: str
    temperature_high: float
    temperature_low: float
    precipitation_chance: float
    description: str

class WeatherForecastResponse(BaseModel):
    location: str
    forecasts: List[WeatherForecast]
    planting_advice: str
