from services.gemini_service import GeminiService
from utils.prompt_templates import PromptTemplates
from schemas.request_models import DiseaseRequest
from schemas.response_models import DiseaseResponse
import image2disease
import json

class DiseaseAgent:
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def diagnose(self, request: DiseaseRequest) -> DiseaseResponse:
        """Diagnose plant disease based on symptoms"""
        
        # Format the prompt with the request data
        prompt = PromptTemplates.DISEASE_DIAGNOSIS.format(
            plant_name=request.plant_name,
            disease_description=request.disease_description,
            additional_info=request.additional_info or "None provided"
        )
        
        # Add a system instruction to format the output as JSON
        system_instruction = """
        You are a plant disease expert AI. Provide your diagnosis in JSON format with the following structure:
        {
          "plant_name": "Name of the plant",
          "possible_diseases": ["Disease 1", "Disease 2"],
          "recommendations": ["Recommendation 1", "Recommendation 2"],
          "preventive_measures": ["Measure 1", "Measure 2"],
          "organic_solutions": ["Solution 1", "Solution 2"],
          "chemical_solutions": ["Solution 1", "Solution 2"]
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
            return DiseaseResponse(**response_data)
        except Exception as e:
            # Fallback handling if JSON parsing fails
            return DiseaseResponse(
                plant_name=request.plant_name,
                possible_diseases=["Could not determine based on provided information"],
                recommendations=["Consult a local agricultural extension service"],
                preventive_measures=["Regular inspection of plants"],
                organic_solutions=["Natural pest deterrents"],
                chemical_solutions=["Use appropriate fungicides or pesticides as advised by experts"]
            )
    
    async def diagnose_from_image(self, image_data) -> DiseaseResponse:
        """Diagnose plant disease based on image"""
        
        try:
            # Use the image2disease module to get the raw prediction
            predicted_label = image2disease.analyze_plant_image(image_data)
            
            # Use LLM to extract plant name and disease from the predicted label
            extract_prompt = f"""
            I have a plant disease prediction from an image classifier: "{predicted_label}"
            
            Please extract the plant name and disease name from this label. The format can vary, but typically 
            it's something like "Plant_Disease" or "Plant Disease" or similar patterns.
            
            Return your answer as a JSON object with these fields:
            1. plant_name: The name of the plant (e.g., "Tomato", "Apple")
            2. disease_name: The name of the disease (e.g., "Bacterial Spot", "Rust")
            """
            
            system_instruction = """
            You are a helpful assistant specialized in plant pathology. Extract the plant name and disease name 
            from the given label. Return only a valid JSON object with the requested fields.
            """
            
            # Get the parsed information from Gemini
            extraction_response = await self.gemini_service.generate_content(extract_prompt, system_instruction)
            
            # Parse the JSON response
            try:
                if "```json" in extraction_response:
                    json_str = extraction_response.split("```json")[1].split("```")[0].strip()
                elif "```" in extraction_response:
                    json_str = extraction_response.split("```")[1].strip()
                else:
                    json_str = extraction_response
                
                extracted_data = json.loads(json_str)
                
                # Create a DiseaseRequest object using the extracted information
                request = DiseaseRequest(
                    plant_name=extracted_data.get("plant_name", "Unknown"),
                    disease_description=f"The plant appears to have {extracted_data.get('disease_name', 'an unknown disease')}",
                    additional_info=f"Detected via automated image analysis. Original label: {predicted_label}"
                )
                
                # Use the existing diagnose method to get recommendations
                return await self.diagnose(request)
                
            except Exception as e:
                # If parsing failed, create a simple request with the raw label
                request = DiseaseRequest(
                    plant_name="Unknown",
                    disease_description=f"The plant appears to have a disease. Model prediction: {predicted_label}",
                    additional_info="Failed to parse model prediction into plant and disease names."
                )
                return await self.diagnose(request)
                
        except Exception as e:
            # Fallback handling if image processing fails
            return DiseaseResponse(
                plant_name="Unknown",
                possible_diseases=["Could not determine from image"],
                recommendations=["Upload a clearer image", "Try describing the symptoms manually"],
                preventive_measures=["Regular inspection of plants"],
                organic_solutions=["Natural pest deterrents"],
                chemical_solutions=["Use appropriate fungicides or pesticides as advised by experts"]
            )
