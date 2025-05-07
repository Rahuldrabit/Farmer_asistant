# Plant Care Assistant

A comprehensive agricultural assistant system that provides plant disease diagnosis, seasonal planting recommendations, and weather forecasts tailored for gardeners and farmers.

![Plant Care Assistant](https://via.placeholder.com/800x400?text=Plant+Care+Assistant)

## Features

- **Plant Disease Diagnosis**: 
  - Text-based diagnosis based on symptoms description
  - Image-based disease detection using machine learning
  - Detailed treatment recommendations and preventive measures

- **Seasonal Planting Plans**:
  - Personalized planting recommendations based on location and season
  - Detailed growing conditions and care instructions for each plant
  - Garden size-specific advice

- **Agricultural Weather Forecasts**:
  - Weather predictions with agricultural interpretation
  - Plant-specific advice based on upcoming weather conditions
  - Customizable forecast duration

- **Multi-language Support**:
  - Full English and Bangla interface and responses
  - Real-time translation of AI-generated content

## Technology Stack

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI Services**:
  - Google Gemini API for intelligent responses and translations
  - Hugging Face Transformers for plant disease image classification
- **APIs**:
  - OpenWeatherMap for weather data
  - Async architecture for efficient API rate limiting

## Installation

### Prerequisites

- Python 3.8+
- API Keys:
  - Google Gemini API key
  - OpenWeatherMap API key

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Brac_Hackaton
   ```

2. Create a virtual environment:
   ```
   python -m venv hackaton_env
   # On Windows
   hackaton_env\Scripts\activate
   # On Unix or MacOS
   source hackaton_env/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure API keys:
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   WEATHER_API_KEY=your_weather_api_key_here
   GEMINI_MODEL=gemini-2.0-flash
   GEMINI_RATE_LIMIT=60
   WEATHER_RATE_LIMIT=60
   ```

## Usage

### Running the Application

1. Start the server:
   ```
   python main.py
   or
   python run_app.py
   ```


2. Access the application:
   - Web interface: http://localhost:8000/app
   - API documentation: http://localhost:8000/docs

### Using the Web Interface

1. **Plant Disease Diagnosis**:
   - Provide plant name and symptoms description, or
   - Upload an image of the affected plant

2. **Seasonal Planting Plan**:
   - Enter your location and season
   - Optionally specify garden size and plant types of interest

3. **Weather Forecast**:
   - Enter your location
   - Select the number of forecast days

4. **Language Selection**:
   - Click the language toggle button in the top right corner to switch between English and Bangla

## API Endpoints

### Plant Disease Diagnosis

- **Text-based Diagnosis**:
  - `POST /disease/diagnose`
  - Request body: `{"plant_name": "Tomato", "disease_description": "Yellow leaves with brown spots", "additional_info": "..."}`

- **Image-based Diagnosis**:
  - `POST /disease/image`
  - Form data: `image` (file upload)

### Seasonal Planting Plan

- `POST /planting/plan`
- Request body: `{"location": "Dhaka", "season": "Summer", "garden_size": "Medium", "plant_types": ["vegetables", "herbs"]}`

### Weather Forecast

- `POST /weather/forecast`
- Request body: `{"location": "Dhaka", "days": 7}`

### Translation

Add `?translate=true` query parameter to any endpoint to receive responses in Bangla.

## Architecture

The application follows a modular architecture:

- **Agents**: Handle specific domains (disease, planting, weather)
- **Services**: Provide API integration (Gemini, weather)
- **Schemas**: Define data models for requests/responses
- **Utils**: Provide helper functions and prompt templates
- **Frontend**: Single-page application with direct API calls

## Project Structure

```
f:/Brac_Hackaton/
├── main.py                # FastAPI application entry point
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── README.md              # Project documentation
├── image2disease.py       # Plant disease image classifier
├── static/                # Static files
│   └── index.html         # Web frontend
├── agents/                # Domain-specific agents
│   ├── disease_agent.py
│   ├── planting_agent.py
│   └── weather_agent.py
├── services/              # External service integrations
│   ├── gemini_service.py
│   ├── weather_service.py
│   └── translation_service.py
├── schemas/               # Data models
│   ├── request_models.py
│   └── response_models.py
└── utils/                 # Utilities
    ├── prompt_templates.py
    └── api_utils.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built for BRAC Hackathon
- Plant disease classification model: [linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification](https://huggingface.co/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification)
- Weather data: OpenWeatherMap API
- AI capabilities: Google Gemini API
