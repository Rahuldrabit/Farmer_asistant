class PromptTemplates:
    DISEASE_DIAGNOSIS = """
    As a plant disease expert, analyze the following information:
    
    Plant: {plant_name}
    Symptoms: {disease_description}
    Additional Information: {additional_info}
    
    Provide a detailed analysis including:
    1. Possible diseases affecting the plant
    2. Recommendations for treatment
    3. Preventive measures
    4. Organic solutions
    5. Chemical solutions (if necessary)
    
    Format your response in a clear, structured manner.
    """
    
    PLANTING_PLAN = """
    As a gardening and agricultural expert, provide a seasonal planting plan for:
    
    Location: {location}
    Season: {season}
    Plant Types of Interest: {plant_types}
    Garden Size: {garden_size}
    Current Weather Conditions: {weather_conditions}
    
    Include in your response:
    1. Best plants to grow in this season at this location
    2. Optimal planting times
    3. Growing conditions and requirements for each plant
    4. Care instructions
    5. General gardening advice for this location and season
    
    Format your response in a clear, structured manner.
    """
    
    WEATHER_INTERPRETATION = """
    As an agricultural meteorologist, interpret the following weather forecast for:
    
    Location: {location}
    Forecast Data: {weather_data}
    
    Provide:
    1. Analysis of the weather conditions
    2. How these conditions might impact plant growth and health
    3. Recommendations for gardening and agricultural activities
    4. Precautions to take given the forecast
    
    Format your response in a clear, structured manner.
    """
