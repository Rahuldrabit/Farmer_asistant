import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# API Rate Limits
GEMINI_RATE_LIMIT = int(os.getenv("GEMINI_RATE_LIMIT", "60"))  # requests per minute
WEATHER_RATE_LIMIT = int(os.getenv("WEATHER_RATE_LIMIT", "60"))  # requests per minute

# Model settings
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
