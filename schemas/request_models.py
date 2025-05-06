from pydantic import BaseModel, Field
from typing import Optional, List

class DiseaseRequest(BaseModel):
    plant_name: str = Field(..., description="Name of the plant with disease")
    disease_description: str = Field(..., description="Description of the observed disease symptoms")
    additional_info: Optional[str] = None

class PlantingPlanRequest(BaseModel):
    location: str = Field(..., description="Location for planting (city or coordinates)")
    season: Optional[str] = None
    plant_types: Optional[List[str]] = None
    garden_size: Optional[str] = None

class WeatherForecastRequest(BaseModel):
    location: str = Field(..., description="Location for weather forecast (city or coordinates)")
    days: Optional[int] = Field(7, description="Number of days for the forecast")
