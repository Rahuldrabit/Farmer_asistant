import asyncio
from config import GEMINI_MODEL
from services.gemini_service import GeminiService
import json

class TranslationService:
    def __init__(self):
        self.gemini_service = GeminiService()
        
        # Common UI elements translation cache
        self.ui_translations = {
            "english": {},
            "bangla": {}
        }
    
    async def translate_to_bangla(self, text):
        """
        Translate text from English to Bangla using Gemini
        
        Args:
            text: Text to translate (string)
            
        Returns:
            str: Translated text in Bangla
        """
        if not text:
            return ""
            
        prompt = f"""
        Translate the following English text to Bangla (Bengali):
        
        ```
        {text}
        ```
        
        Please provide only the translated text without any additional explanations or notes.
        Maintain all formatting like bullet points and paragraphs in the translation.
        """
        
        system_instruction = """
        আপনি একজন পেশাদার ইংরেজি থেকে বাংলা অনুবাদক। 
        প্রদত্ত পাঠ্যকে স্বাভাবিক-শব্দযুক্ত বাংলায় সঠিকভাবে অনুবাদ করুন। 
        অনুবাদে কৃষি ও উদ্ভিদ বিজ্ঞানের পরিভাষা সঠিকভাবে ব্যবহার করুন।
        শুধু অনুবাদ প্রদান করুন, কোনো ব্যাখ্যা বা নোট ছাড়া।
        """
        
        try:
            result = await self.gemini_service.generate_content(prompt, system_instruction)
            # Clean up any markdown formatting that might be returned
            result = result.replace("```", "").strip()
            return result
        except Exception as e:
            print(f"Translation error: {str(e)}")
            # Return original text if translation fails
            return text
    
    async def translate_dict_to_bangla(self, data):
        """
        Recursively translate all string values in a dictionary/list from English to Bangla
        
        Args:
            data: Dictionary or list containing strings to translate
            
        Returns:
            dict/list: With all string values translated to Bangla
        """
        if isinstance(data, str):
            if len(data) > 500:
                # Split long strings into chunks for better translation quality
                chunks = [data[i:i+500] for i in range(0, len(data), 500)]
                translated_chunks = []
                for chunk in chunks:
                    translated_chunks.append(await self.translate_to_bangla(chunk))
                return "".join(translated_chunks)
            else:
                return await self.translate_to_bangla(data)
        elif isinstance(data, list):
            # Translate lists in parallel for efficiency
            tasks = []
            for item in data:
                tasks.append(self.translate_dict_to_bangla(item))
            return await asyncio.gather(*tasks)
        elif isinstance(data, dict):
            # Process dictionaries - translate each value
            result = {}
            # Use asyncio.gather for parallel processing
            keys = list(data.keys())
            tasks = [self.translate_dict_to_bangla(data[key]) for key in keys]
            values = await asyncio.gather(*tasks)
            for i, key in enumerate(keys):
                result[key] = values[i]
            return result
        else:
            # Return non-string/dict/list values as is
            return data
    
    async def get_ui_translations(self):
        """
        Get translations for common UI elements
        
        Returns:
            dict: UI elements translated to Bangla
        """
        # Return from cache if already translated
        if self.ui_translations["bangla"]:
            return self.ui_translations
            
        # Define common UI elements in English
        ui_elements = {
            "Plant Care Assistant": "Plant Care Assistant",
            "Welcome to Plant Care Assistant!": "Welcome to Plant Care Assistant!",
            "Get expert advice on plant diseases, seasonal planting plans, and weather forecasts for your garden.": 
                "Get expert advice on plant diseases, seasonal planting plans, and weather forecasts for your garden.",
            "Plant Disease Diagnosis": "Plant Disease Diagnosis",
            "Text Description": "Text Description",
            "Image Upload": "Image Upload",
            "Plant Name": "Plant Name",
            "Symptoms Description": "Symptoms Description",
            "Additional Information (optional)": "Additional Information (optional)",
            "Get Diagnosis": "Get Diagnosis",
            "Upload Plant Image": "Upload Plant Image",
            "Analyze Image": "Analyze Image",
            "Diagnosis Results": "Diagnosis Results",
            "Seasonal Planting Plan": "Seasonal Planting Plan",
            "Location": "Location",
            "Season (optional)": "Season (optional)",
            "Current Season": "Current Season",
            "Spring": "Spring",
            "Summer": "Summer",
            "Fall": "Fall",
            "Winter": "Winter",
            "Garden Size (optional)": "Garden Size (optional)",
            "Not specified": "Not specified",
            "Small": "Small", 
            "Medium": "Medium",
            "Large": "Large",
            "Plant Types (optional)": "Plant Types (optional)",
            "Get Planting Plan": "Get Planting Plan",
            "Planting Plan": "Planting Plan",
            "Weather Forecast for Agriculture": "Weather Forecast for Agriculture",
            "Days to Forecast": "Days to Forecast",
            "Get Weather Forecast": "Get Weather Forecast",
            "Weather Forecast": "Weather Forecast",
            "Processing your request...": "Processing your request...",
            "Plant": "Plant",
            "Possible Diseases": "Possible Diseases",
            "Recommendations": "Recommendations",
            "Preventive Measures": "Preventive Measures",
            "Organic Solutions": "Organic Solutions",
            "Chemical Solutions": "Chemical Solutions",
            "Planting Time": "Planting Time",
            "Growing Conditions": "Growing Conditions",
            "Care Instructions": "Care Instructions",
            "General Advice": "General Advice",
            "Date": "Date",
            "Temp High": "Temp High",
            "Temp Low": "Temp Low", 
            "Precipitation": "Precipitation",
            "Description": "Description",
            "Planting Advice": "Planting Advice",
            "Recommended Plants": "Recommended Plants",
            "No specific plant recommendations available.": "No specific plant recommendations available.",
            "No forecast data available.": "No forecast data available."
        }
        
        # Translate all UI elements to Bangla
        self.ui_translations["english"] = ui_elements
        
        # Prepare a JSON of all elements for batch translation
        ui_json = json.dumps(ui_elements, ensure_ascii=False)
        
        # Translate the entire JSON at once to maintain consistency
        prompt = f"""
        Translate all the English UI element values in this JSON to Bangla (Bengali).
        Only translate the values, not the keys.
        
        ```json
        {ui_json}
        ```
        
        Return only the translated JSON with the same structure.
        """
        
        system_instruction = """
        আপনি একজন পেশাদার UI অনুবাদক। জেসন ফাইলের সমস্ত UI উপাদান মান সঠিকভাবে বাংলায় অনুবাদ করুন।
        শুধুমাত্র মান অনুবাদ করুন, কী নয়। একটি বৈধ JSON ফরম্যাটে ফেরত দিন।
        """
        
        try:
            result = await self.gemini_service.generate_content(prompt, system_instruction)
            
            # Extract JSON from the response
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].strip()
            else:
                json_str = result
                
            translated_elements = json.loads(json_str)
            self.ui_translations["bangla"] = translated_elements
            
        except Exception as e:
            print(f"UI translation error: {str(e)}")
            # If translation fails, use original English values
            self.ui_translations["bangla"] = ui_elements
            
        return self.ui_translations
