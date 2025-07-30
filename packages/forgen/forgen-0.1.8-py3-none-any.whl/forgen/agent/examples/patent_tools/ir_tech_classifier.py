"""
Invention Record Technology Classifier Tool

Classifies inventions by technology field using CPC/IPC codes and technical domains.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ir_technology_classification_function(input_data: dict) -> dict:
    """
    Classify invention by technology field and patent classifications.
    
    Args:
        input_data: Dictionary containing 'invention_record_text'
        
    Returns:
        Dictionary with technology classification
    """
    invention_text = input_data.get('invention_record_text', '')
    
    system_prompt = """
    You are an expert patent classifier with deep knowledge of CPC (Cooperative Patent Classification) 
    and IPC (International Patent Classification) systems. Classify the invention into appropriate 
    technology categories.
    
    Return a JSON object with the following structure:
    {
        "cpc_classifications": [
            {
                "code": "H04L9/08",
                "description": "Cryptographic mechanisms or processes",
                "confidence": "High/Medium/Low"
            }
        ],
        "ipc_classifications": [
            {
                "code": "H04L9/08",
                "description": "Cryptographic mechanisms or processes",
                "confidence": "High/Medium/Low"
            }
        ],
        "domains": ["Primary", "technology", "domains"],
        "application_areas": ["Specific", "application", "areas"],
        "technical_disciplines": ["Engineering", "disciplines", "involved"],
        "industry_sectors": ["Industry", "sectors", "that", "would", "use", "this"],
        "patent_classes": ["USPTO", "patent", "classes", "if", "applicable"]
    }
    
    Provide the most relevant classifications with confidence levels. Include both primary and secondary classifications where appropriate.
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
        return {"error": f"Failed to classify technology: {str(e)}"}

# Build the tool
def create_ir_tech_classifier():
    """Create and return the IR Technology Classifier tool."""
    builder = ToolBuilder(
        tool_name="ir_tech_classifier",
        description="Classifies inventions by technology field using CPC/IPC codes and technical domains"
    )
    
    # Set schemas
    input_schema = {"invention_record_text": str}
    
    output_schema = {
        "cpc_classifications": list,
        "ipc_classifications": list,
        "domains": list,
        "application_areas": list,
        "technical_disciplines": list,
        "industry_sectors": list,
        "patent_classes": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ir_technology_classification_function)
    
    return builder.build()

# Create the tool instance
ir_tech_classifier = create_ir_tech_classifier()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_record_text": """
        Title: AI-Powered Medical Diagnostic Imaging System
        
        Technical Field: Artificial intelligence, medical imaging, computer vision, machine learning
        
        Description: An advanced medical diagnostic system that uses deep learning neural networks 
        to analyze radiological images (X-rays, CT scans, MRIs) and automatically detect anomalies 
        such as tumors, fractures, and other pathological conditions.
        
        Key Components:
        - Convolutional neural network architecture optimized for medical imaging
        - Real-time image preprocessing and enhancement algorithms
        - Multi-modal imaging fusion capabilities
        - Confidence scoring and uncertainty quantification
        - Integration with hospital PACS (Picture Archiving and Communication Systems)
        - Automated report generation with natural language processing
        
        Applications:
        - Radiology departments in hospitals
        - Emergency room diagnostic support
        - Telemedicine and remote diagnostics
        - Medical screening programs
        - Research institutions
        """
    }
    
    result = ir_tech_classifier.execute(test_input)
    print(f"Technology Classification Result: {result}")