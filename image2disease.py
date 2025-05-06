# Load model directly
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import os
import io

# Initialize the model on-demand instead of at import time
processor = None
model = None

def get_model():
    global processor, model
    if processor is None or model is None:
        from transformers import AutoImageProcessor, AutoModelForImageClassification
        processor = AutoImageProcessor.from_pretrained("linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")
        model = AutoModelForImageClassification.from_pretrained("linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")
    return processor, model

def analyze_plant_image(image_data):
    """
    Analyze plant disease from image data
    
    Args:
        image_data: BytesIO object or path to image file
        
    Returns:
        str: Raw predicted label from the model
    """
    # Load the model on-demand
    processor, model = get_model()
    
    # Check if image_data is a file path or bytes
    if isinstance(image_data, str) and os.path.exists(image_data):
        image = Image.open(image_data)
    elif isinstance(image_data, bytes) or isinstance(image_data, io.BytesIO):
        image = Image.open(io.BytesIO(image_data) if isinstance(image_data, bytes) else image_data)
    else:
        raise ValueError("Invalid image data format")
    
    # Process the image with the model
    inputs = processor(image, return_tensors="pt")
    
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Get the predicted label
    predicted_label = logits.argmax(-1).item()
    disease_full_name = model.config.id2label[predicted_label]
    
    # Simply return the raw label without parsing
    return disease_full_name

# For testing locally
if __name__ == "__main__":
    test_image_path = "test_image.jpg"  # Replace with an actual test image path
    if os.path.exists(test_image_path):
        result = analyze_plant_image(test_image_path)
        print(f"Predicted label: {result}")