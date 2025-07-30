"""
Draft Specification Mapper Tool

Generates detailed specification outlines from invention disclosures 
with section-by-section guidance.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def draft_spec_mapping_function(input_data: dict) -> dict:
    """
    Generate specification outline from invention disclosure.
    
    Args:
        input_data: Dictionary containing 'invention_disclosure_text' and optional 'patent_context'
        
    Returns:
        Dictionary with specification outline
    """
    invention_text = input_data.get('invention_disclosure_text', '')
    patent_context = input_data.get('patent_context', '')
    
    system_prompt = """
    You are an expert patent attorney specializing in patent application drafting. Generate a comprehensive 
    specification outline from the invention disclosure that follows USPTO guidelines and best practices.
    
    Return a JSON object with the following structure:
    {
        "title": "Concise, descriptive patent title",
        "field_of_invention": "Brief description of the technical field",
        "background": {
            "problem_statement": "Technical problem being addressed",
            "limitations_of_prior_art": "What prior art fails to solve",
            "industry_context": "Relevant industry background"
        },
        "summary": "Brief summary of the invention and its advantages",
        "drawing_descriptions": [
            {
                "figure_number": "Fig. 1",
                "description": "Brief description of what the figure shows"
            }
        ],
        "detailed_description_outline": {
            "overview": "High-level description approach",
            "preferred_embodiment": "Main embodiment description plan",
            "alternative_embodiments": ["Other", "embodiments", "to", "describe"],
            "operation_description": "How the invention operates",
            "implementation_details": "Technical implementation specifics"
        },
        "claims_outline": {
            "independent_claims": ["Scope", "of", "main", "independent", "claims"],
            "dependent_claims_strategy": "Approach for dependent claims",
            "claim_scope_considerations": "Factors affecting claim breadth"
        },
        "abstract": "Technical abstract (150 words max)",
        "drawings_needed": ["List", "of", "drawings", "required"]
    }
    
    Focus on creating a roadmap for comprehensive patent application drafting.
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
        return {"error": f"Failed to generate specification outline: {str(e)}"}

# Build the tool
def create_draft_spec_mapper():
    """Create and return the Draft Specification Mapper tool."""
    builder = ToolBuilder(
        tool_name="draft_spec_mapper",
        description="Generates detailed specification outlines from invention disclosures with section-by-section guidance"
    )
    
    # Set schemas
    input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str
    }
    
    output_schema = {
        "title": str,
        "field_of_invention": str,
        "background": dict,
        "summary": str,
        "drawing_descriptions": list,
        "detailed_description_outline": dict,
        "claims_outline": dict,
        "abstract": str,
        "drawings_needed": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(draft_spec_mapping_function)
    
    return builder.build()

# Create the tool instance
draft_spec_mapper = create_draft_spec_mapper()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_disclosure_text": """
        Invention: Smart Home Energy Management System
        
        Problem: Current home energy systems lack intelligent coordination between 
        renewable energy generation, battery storage, and appliance usage, leading 
        to inefficient energy utilization and higher costs.
        
        Solution: An AI-powered energy management system that optimizes energy flow 
        in real-time based on weather forecasts, electricity pricing, usage patterns, 
        and grid demand signals.
        
        Key Components:
        - Central processing unit with machine learning algorithms
        - Smart inverters for solar panel integration
        - Battery management system with predictive charging
        - IoT-enabled appliance controllers
        - Weather and pricing data integration APIs
        - Mobile app for user control and monitoring
        
        Technical Features:
        - Real-time load balancing algorithms
        - Predictive energy demand modeling
        - Dynamic pricing optimization
        - Grid interaction protocols
        - Backup power management during outages
        
        Benefits:
        - 30% reduction in electricity costs
        - Improved grid stability
        - Maximized renewable energy utilization
        - Enhanced home energy independence
        """,
        "patent_context": ""
    }
    
    result = draft_spec_mapper.execute(test_input)
    print(f"Specification Outline Result: {result}")