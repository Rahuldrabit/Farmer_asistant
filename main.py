import sys
import os
# Add the current directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from schemas.request_models import DiseaseRequest, PlantingPlanRequest, WeatherForecastRequest
from schemas.response_models import DiseaseResponse, PlantingPlanResponse, WeatherForecastResponse
from agents.disease_agent import DiseaseAgent
from agents.planting_agent import PlantingAgent
from agents.weather_agent import WeatherAgent
import uvicorn
import traceback
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.translation_service import TranslationService

app = FastAPI(
    title="Plant Care Assistant API",
    description="API for plant disease diagnosis, seasonal planting plans, and weather forecasts for agriculture",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize agents
disease_agent = DiseaseAgent()
planting_agent = PlantingAgent()
weather_agent = WeatherAgent()

# Initialize translation service
translation_service = TranslationService()

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Plant Care Assistant API",
        "endpoints": [
            {
                "path": "/disease/diagnose",
                "method": "POST",
                "description": "Diagnose plant diseases through text description"
            },
            {
                "path": "/disease/image",
                "method": "POST", 
                "description": "Diagnose plant diseases from image uploads"
            },
            {
                "path": "/planting/plan",
                "method": "POST",
                "description": "Get seasonal planting plans"
            },
            {
                "path": "/weather/forecast",
                "method": "POST",
                "description": "Get weather forecasts with agricultural advice"
            }
        ],
        "documentation": "Visit /docs for interactive API documentation"
    }

@app.post("/translate", description="Translate text to Bangla")
async def translate_text(request: dict):
    """Translate text from English to Bangla"""
    try:
        if "text" not in request:
            raise HTTPException(status_code=400, detail="Text field is required")
            
        translated_text = await translation_service.translate_to_bangla(request["text"])
        return {"translated_text": translated_text}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.post("/disease/diagnose", response_model=DiseaseResponse)
async def diagnose_disease(request: DiseaseRequest, translate: bool = False):
    """
    Diagnose plant diseases based on symptoms and provide treatment recommendations
    """
    try:
        result = await disease_agent.diagnose(request)
        if translate:
            # Create a dictionary representation and translate all fields
            result_dict = result.dict()
            translated_dict = await translation_service.translate_dict_to_bangla(result_dict)
            # Convert back to DiseaseResponse
            return DiseaseResponse(**translated_dict)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error diagnosing disease: {str(e)}")

@app.post("/disease/image", response_model=DiseaseResponse)
async def diagnose_disease_from_image(image: UploadFile = File(...), translate: bool = False):
    """
    Diagnose plant diseases by uploading an image of the affected plant
    """
    try:
        # Read the image data
        image_data = await image.read()
        
        # Process the image through disease_agent
        try:
            result = await disease_agent.diagnose_from_image(image_data)
            if translate:
                # Create a dictionary representation and translate all fields
                result_dict = result.dict()
                translated_dict = await translation_service.translate_dict_to_bangla(result_dict)
                # Convert back to DiseaseResponse
                return DiseaseResponse(**translated_dict)
            return result
        except Exception as e:
            print(f"Error in disease_agent.diagnose_from_image: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Disease analysis error: {str(e)}")
            
    except Exception as e:
        print(f"Error processing image upload: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/disease/image")
async def diagnose_disease_from_image_get():
    """Return helpful message when GET is used instead of POST"""
    return {
        "error": "Method Not Allowed: Use POST for this endpoint",
        "message": "This endpoint requires a POST request with an image file upload",
        "example": "Use the /docs interface or send a POST request with an image file in the 'image' field",
        "documentation_url": "/docs#/default/diagnose_disease_from_image_disease_image_post"
    }

@app.post("/planting/plan", response_model=PlantingPlanResponse)
async def create_planting_plan(request: PlantingPlanRequest, translate: bool = False):
    """
    Create a seasonal planting plan based on location, weather, and preferences
    """
    try:
        result = await planting_agent.create_planting_plan(request)
        if translate:
            # Create a dictionary representation and translate all fields
            result_dict = result.dict()
            translated_dict = await translation_service.translate_dict_to_bangla(result_dict)
            # Convert back to PlantingPlanResponse
            return PlantingPlanResponse(**translated_dict)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating planting plan: {str(e)}")

@app.get("/planting/plan")
async def create_planting_plan_get():
    """Return helpful message when GET is used instead of POST"""
    return {
        "error": "Method Not Allowed: Use POST for this endpoint",
        "message": "This endpoint requires a POST request with a JSON body",
        "example": {
            "location": "New York City",
            "season": "Summer",
            "plant_types": ["vegetables", "herbs"],
            "garden_size": "small"
        },
        "documentation_url": "/docs#/default/create_planting_plan_planting_plan_post"
    }

@app.post("/weather/forecast", response_model=WeatherForecastResponse)
async def get_weather_forecast(request: WeatherForecastRequest, translate: bool = False):
    """
    Get weather forecast with agricultural interpretation
    """
    try:
        result = await weather_agent.get_forecast_with_interpretation(request)
        if translate:
            # Create a dictionary representation and translate all fields
            result_dict = result.dict()
            translated_dict = await translation_service.translate_dict_to_bangla(result_dict)
            # Convert back to WeatherForecastResponse
            return WeatherForecastResponse(**translated_dict)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error getting weather forecast: {str(e)}")

@app.get("/weather/forecast")
async def get_weather_forecast_get():
    """Return helpful message when GET is used instead of POST"""
    return {
        "error": "Method Not Allowed: Use POST for this endpoint",
        "message": "This endpoint requires a POST request with a JSON body",
        "example": {
            "location": "New York City",
            "days": 7
        },
        "documentation_url": "/docs#/default/get_weather_forecast_weather_forecast_post"
    }

# Add a route to serve the index.html file
@app.get("/app", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend application"""
    return FileResponse("static/index.html")

# Add a new endpoint to get UI translations
@app.get("/ui-translations")
async def get_ui_translations():
    """Get UI translations for frontend"""
    try:
        translations = await translation_service.get_ui_translations()
        return translations
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error getting translations: {str(e)}")

if __name__ == "__main__":
    # Change from 0.0.0.0 to localhost or 127.0.0.1 for better browser compatibility
    print("Starting server. Access the API at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)