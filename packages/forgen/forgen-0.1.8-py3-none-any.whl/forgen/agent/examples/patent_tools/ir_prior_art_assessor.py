"""
Invention Record Prior Art Assessor Tool

Identifies prior art references and assesses patentability risks from invention records.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ir_prior_art_assessment_function(input_data: dict) -> dict:
    """
    Assess prior art landscape and patentability risks for invention.
    
    Args:
        input_data: Dictionary containing 'invention_record_text'
        
    Returns:
        Dictionary with prior art assessment
    """
    invention_text = input_data.get('invention_record_text', '')
    
    system_prompt = """
    You are an expert patent examiner and prior art specialist. Analyze the invention record to identify potential prior art references and assess patentability risks.
    
    Return a JSON object with the following structure:
    {
        "prior_art_references": [
            {
                "reference": "Description or citation",
                "relevance": "How it relates to the invention",
                "impact": "High/Medium/Low"
            }
        ],
        "patent_risks": {
            "novelty_risk": "High/Medium/Low",
            "obviousness_risk": "High/Medium/Low",
            "anticipation_risk": "High/Medium/Low",
            "overall_patentability": "High/Medium/Low"
        },
        "novelty_assessment": "Analysis of what appears novel about the invention",
        "obviousness_risks": ["Specific", "obviousness", "concerns"],
        "freedom_to_operate": "Assessment of potential infringement risks",
        "competitive_landscape": "Overview of competitors and existing solutions",
        "search_recommendations": ["Suggested", "search", "strategies", "and", "databases"]
    }
    
    Be thorough but realistic in risk assessment. Consider both technical and legal aspects.
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
        return {"error": f"Failed to assess prior art: {str(e)}"}

# Build the tool
def create_ir_prior_art_assessor():
    """Create and return the IR Prior Art Assessor tool."""
    builder = ToolBuilder(
        tool_name="ir_prior_art_assessor",
        description="Identifies prior art references and assesses patentability risks from invention records"
    )
    
    # Set schemas
    input_schema = {"invention_record_text": str}
    
    output_schema = {
        "prior_art_references": list,
        "patent_risks": dict,
        "novelty_assessment": str,
        "obviousness_risks": list,
        "freedom_to_operate": str,
        "competitive_landscape": str,
        "search_recommendations": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ir_prior_art_assessment_function)
    
    return builder.build()

# Create the tool instance
ir_prior_art_assessor = create_ir_prior_art_assessor()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_record_text": """
        Title: Quantum Cryptography Key Distribution System
        
        Technical Field: Quantum computing, cryptography, secure communications
        
        Description: A quantum key distribution system that uses entangled photon pairs 
        to establish secure cryptographic keys between remote parties. The system includes 
        quantum state generators, fiber optic transmission channels, and quantum state 
        detectors with error correction algorithms.
        
        Key Features:
        - Entangled photon pair generation using parametric down-conversion
        - Automatic quantum channel alignment
        - Real-time eavesdropping detection
        - Error correction protocols for noisy channels
        - Integration with classical communication networks
        
        Background: Traditional cryptographic systems rely on computational complexity 
        for security, which may be vulnerable to quantum computers. Quantum key distribution 
        offers information-theoretic security guaranteed by quantum mechanics.
        """
    }
    
    result = ir_prior_art_assessor.execute(test_input)
    print(f"Prior Art Assessment Result: {result}")