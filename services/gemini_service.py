import google.generativeai as genai
import asyncio
import time
from typing import Dict, Any, Optional
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_RATE_LIMIT

class GeminiService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.request_times = []
        self.lock = asyncio.Lock()
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting for the Gemini API"""
        async with self.lock:
            current_time = time.time()
            # Remove timestamps older than a minute
            self.request_times = [t for t in self.request_times if current_time - t < 60]
            
            if len(self.request_times) >= GEMINI_RATE_LIMIT:
                oldest_request = self.request_times[0]
                sleep_time = 60 - (current_time - oldest_request)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self.request_times.append(time.time())
    
    async def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate content from Gemini API with rate limiting"""
        await self._enforce_rate_limit()
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        try:
            if system_instruction:
                response = await self.model.generate_content_async(
                    system_instruction + "\n\n" + prompt,
                    generation_config=generation_config
                )
            else:
                response = await self.model.generate_content_async(
                    prompt, 
                    generation_config=generation_config
                )
            
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            raise e
