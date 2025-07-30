"""
Background Section Generator Tool

Generates patent background sections with prior art discussion 
and technical problem identification.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def background_generation_function(input_data: dict) -> dict:
    """
    Generate background section for patent application.
    
    Args:
        input_data: Dictionary containing 'invention_disclosure_text' and optional 'patent_context'
        
    Returns:
        Dictionary with background section content
    """
    invention_text = input_data.get('invention_disclosure_text', '')
    patent_context = input_data.get('patent_context', '')
    
    system_prompt = """
    You are an expert patent attorney specializing in background section drafting. Generate a comprehensive 
    background section that establishes the technical field, discusses relevant prior art, and clearly 
    articulates the problems solved by the invention.
    
    Return a JSON object with the following structure:
    {
        "field_description": "Clear description of the technical field and its importance",
        "prior_art_discussion": "Discussion of relevant prior art technologies and approaches",
        "technical_problems": [
            {
                "problem": "Specific technical problem",
                "impact": "Why this problem is significant",
                "prior_art_limitations": "How existing solutions fail to address this"
            }
        ],
        "limitations_of_prior_art": [
            "Specific limitation 1 of existing approaches",
            "Specific limitation 2 of existing approaches"
        ],
        "industry_context": "Broader industry context and market needs",
        "regulatory_considerations": [
            "Relevant regulations or standards that apply"
        ],
        "safety_considerations": [
            "Safety issues that existing solutions don't adequately address"
        ],
        "economic_factors": [
            "Economic drivers that make this invention valuable"
        ]
    }
    
    Ensure the background clearly motivates the need for the invention without disparaging prior art inappropriately.
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
        return {"error": f"Failed to generate background section: {str(e)}"}

# Build the tool
def create_background_generator():
    """Create and return the Background Generator tool."""
    builder = ToolBuilder(
        tool_name="background_generator",
        description="Generates patent background sections with prior art discussion and technical problem identification"
    )
    
    # Set schemas
    input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str
    }
    
    output_schema = {
        "field_description": str,
        "prior_art_discussion": str,
        "technical_problems": list,
        "limitations_of_prior_art": list,
        "industry_context": str,
        "regulatory_considerations": list,
        "safety_considerations": list,
        "economic_factors": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(background_generation_function)
    
    return builder.build()

# Create the tool instance
background_generator = create_background_generator()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_disclosure_text": """
        Invention: Biodegradable Food Packaging with Active Antimicrobial Properties
        
        Technical Field: Food packaging, biodegradable materials, antimicrobial coatings, food safety
        
        Problem: Traditional plastic food packaging creates environmental waste and lacks active 
        antimicrobial properties. Current biodegradable alternatives often have poor barrier 
        properties and don't actively prevent bacterial growth.
        
        Solution: A novel biodegradable packaging material made from plant-based polymers 
        infused with natural antimicrobial compounds that actively inhibit bacterial and 
        fungal growth while maintaining food freshness.
        
        Key Features:
        - Biodegradable polymer matrix from agricultural waste
        - Embedded antimicrobial agents from plant extracts
        - Oxygen and moisture barrier properties equivalent to plastic
        - Active release of antimicrobial compounds over time
        - Compostable within 90 days in industrial composting facilities
        
        Current Packaging Problems:
        - Plastic pollution and microplastics in food chain
        - Limited shelf life due to microbial contamination
        - High food waste from spoilage
        - Lack of sustainable packaging options
        - Regulatory pressure to reduce plastic use
        
        Industry Context:
        - $300B global food packaging market
        - Increasing consumer demand for sustainable packaging
        - Stringent food safety regulations
        - Extended supply chains requiring longer preservation
        """,
        "patent_context": ""
    }
    
    result = background_generator.execute(test_input)
    print(f"Background Section Result: {result}")