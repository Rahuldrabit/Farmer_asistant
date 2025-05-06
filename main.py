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

@app.post("/disease/diagnose", response_model=DiseaseResponse)
async def diagnose_disease(request: DiseaseRequest):
    """
    Diagnose plant diseases based on symptoms and provide treatment recommendations
    """
    try:
        return await disease_agent.diagnose(request)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error diagnosing disease: {str(e)}")

@app.post("/disease/image", response_model=DiseaseResponse)
async def diagnose_disease_from_image(image: UploadFile = File(...)):
    """
    Diagnose plant diseases by uploading an image of the affected plant
    """
    try:
        # Read the image data
        image_data = await image.read()
        
        # Process the image through disease_agent
        try:
            return await disease_agent.diagnose_from_image(image_data)
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
async def create_planting_plan(request: PlantingPlanRequest):
    """
    Create a seasonal planting plan based on location, weather, and preferences
    """
    try:
        return await planting_agent.create_planting_plan(request)
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
async def get_weather_forecast(request: WeatherForecastRequest):
    """
    Get weather forecast with agricultural interpretation
    """
    try:
        return await weather_agent.get_forecast_with_interpretation(request)
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

if __name__ == "__main__":
    # Change from 0.0.0.0 to localhost or 127.0.0.1 for better browser compatibility
    print("Starting server. Access the API at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)