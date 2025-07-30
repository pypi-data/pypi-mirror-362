"""
Invention Record Metadata Extractor Tool

Extracts structured metadata from invention records including title, inventors, 
filing info, and technical classifications.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ir_metadata_extraction_function(input_data: dict) -> dict:
    """
    Extract structured metadata from invention record text.
    
    Args:
        input_data: Dictionary containing 'invention_record_text'
        
    Returns:
        Dictionary with extracted metadata
    """
    invention_text = input_data.get('invention_record_text', '')
    
    system_prompt = """
    You are an expert patent attorney and IP analyst. Extract structured metadata from the provided invention record.
    
    Return a JSON object with the following structure:
    {
        "title": "Clear, descriptive invention title",
        "inventors": ["List", "of", "inventor", "names"],
        "filing_dates": {
            "priority_date": "YYYY-MM-DD or null",
            "filing_date": "YYYY-MM-DD or null",
            "target_filing_date": "YYYY-MM-DD or null"
        },
        "technology_field": "Primary technology domain",
        "abstract": "Brief technical summary (150-250 words)",
        "key_features": ["List", "of", "key", "technical", "features"],
        "related_applications": ["List", "of", "related", "application", "numbers"],
        "assignee": "Company or entity name",
        "attorney_docket": "Docket number if available"
    }
    
    If information is not available, use null for strings and empty arrays for lists.
    """
    
    user_content = f"Invention Record Text:\n\n{invention_text}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to extract metadata: {str(e)}"}

# Build the tool
def create_ir_metadata_extractor():
    """Create and return the IR Metadata Extractor tool."""
    builder = ToolBuilder(
        tool_name="ir_metadata_extractor",
        description="Extracts structured metadata from invention records including title, inventors, filing info, and technical classifications"
    )
    
    # Set schemas
    input_schema = {"invention_record_text": str}
    
    output_schema = {
        "title": str,
        "inventors": list,
        "filing_dates": dict,
        "technology_field": str,
        "abstract": str,
        "key_features": list,
        "related_applications": list,
        "assignee": str,
        "attorney_docket": str
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ir_metadata_extraction_function)
    
    return builder.build()

# Create the tool instance
ir_metadata_extractor = create_ir_metadata_extractor()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_record_text": """
        Title: Autonomous Vehicle Navigation System with Machine Learning
        
        Inventors: Dr. Sarah Chen, Michael Rodriguez, Jennifer Liu
        
        Technology Field: Autonomous vehicles, machine learning, computer vision
        
        Abstract: This invention relates to an improved navigation system for autonomous vehicles that uses machine learning algorithms to predict and adapt to traffic patterns. The system incorporates real-time sensor data from cameras, lidar, and radar to make intelligent routing decisions.
        
        Assignee: TechDrive Innovations LLC
        Attorney Docket: TD-2024-001
        
        Description: The autonomous vehicle navigation system includes multiple components working together to provide enhanced navigation capabilities...
        """
    }
    
    result = ir_metadata_extractor.execute(test_input)
    print(f"Metadata Extraction Result: {result}")