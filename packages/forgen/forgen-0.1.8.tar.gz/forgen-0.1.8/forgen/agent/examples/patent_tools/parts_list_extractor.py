"""
Parts List Extractor Tool

Extracts and organizes parts lists with reference numerals 
from invention disclosures.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def parts_list_extraction_function(input_data: dict) -> dict:
    """
    Extract and organize parts list from invention disclosure.
    
    Args:
        input_data: Dictionary containing 'invention_disclosure_text' and optional 'patent_context'
        
    Returns:
        Dictionary with organized parts list
    """
    invention_text = input_data.get('invention_disclosure_text', '')
    patent_context = input_data.get('patent_context', '')
    
    system_prompt = """
    You are an expert patent attorney specializing in detailed description drafting. Extract and organize 
    all components, parts, and elements from the invention disclosure into a structured parts list with 
    appropriate reference numerals.
    
    Return a JSON object with the following structure:
    {
        "components": [
            {
                "name": "Component name",
                "reference_numeral": 10,
                "description": "Brief description of the component",
                "function": "What this component does",
                "location": "Where it's located in the system"
            }
        ],
        "reference_numerals": {
            "10": "First major component",
            "12": "Sub-component of 10",
            "14": "Another sub-component",
            "20": "Second major component"
        },
        "component_hierarchy": {
            "main_system": {
                "reference": "1",
                "sub_components": ["10", "20", "30"]
            },
            "sub_assemblies": [
                {
                    "parent": "10",
                    "children": ["12", "14", "16"]
                }
            ]
        },
        "descriptions": {
            "detailed_descriptions": {
                "10": "Detailed description for component 10",
                "12": "Detailed description for component 12"
            }
        },
        "relationships": [
            {
                "component_1": "10",
                "component_2": "12", 
                "relationship": "12 is mounted on 10",
                "connection_type": "mechanical/electrical/optical"
            }
        ],
        "drawing_references": {
            "Figure_1": ["10", "12", "14"],
            "Figure_2": ["20", "22", "24"]
        }
    }
    
    Use standard patent drafting conventions for reference numerals (even numbers, hierarchical numbering).
    """
    
    user_content = f"Invention Disclosure:\n\n{invention_text}"
    if patent_context:
        user_content += f"\n\nRelated Patent Context:\n{patent_context}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to extract parts list: {str(e)}"}

# Build the tool
def create_parts_list_extractor():
    """Create and return the Parts List Extractor tool."""
    builder = ToolBuilder(
        tool_name="parts_list_extractor",
        description="Extracts and organizes parts lists with reference numerals from invention disclosures"
    )
    
    # Set schemas
    input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str
    }
    
    output_schema = {
        "components": list,
        "reference_numerals": dict,
        "component_hierarchy": dict,
        "descriptions": dict,
        "relationships": list,
        "drawing_references": dict
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(parts_list_extraction_function)
    
    return builder.build()

# Create the tool instance
parts_list_extractor = create_parts_list_extractor()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_disclosure_text": """
        Invention: Modular Solar Panel Cleaning Robot System
        
        System Overview: An autonomous robotic system for cleaning solar panels that consists 
        of a mobile cleaning unit, a control station, and a water supply system.
        
        Main Components:
        
        1. Mobile Cleaning Unit:
        - Wheeled chassis with all-terrain capabilities
        - Rotating brush assembly with variable speed motor
        - Water spray nozzles with adjustable pressure
        - Onboard sensors (proximity, dust detection, panel edge detection)
        - Battery pack with solar charging capability
        - Wireless communication module
        
        2. Control Station:
        - Central processing unit with scheduling software
        - Weather monitoring sensors (wind, rain, temperature)
        - Communication hub for robot coordination
        - Data storage and analysis system
        - User interface display panel
        - Power supply and backup battery
        
        3. Water Supply System:
        - Water reservoir tank with level sensors
        - Pressure pump with variable flow control
        - Filtration system with replaceable filters
        - Distribution manifold with multiple outlets
        - Drainage collection system
        - Water recycling unit
        
        Operation: The mobile cleaning unit travels along predetermined paths on the solar 
        panel array, using sensors to detect dirt accumulation and automatically adjusting 
        cleaning intensity. The control station coordinates multiple cleaning units and 
        schedules cleaning operations based on weather conditions and panel performance data.
        """,
        "patent_context": ""
    }
    
    result = parts_list_extractor.execute(test_input)
    print(f"Parts List Extraction Result: {result}")