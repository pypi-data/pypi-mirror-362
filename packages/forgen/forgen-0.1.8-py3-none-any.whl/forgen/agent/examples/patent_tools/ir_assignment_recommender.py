"""
Invention Record Assignment Recommender Tool

Suggests suitable agent/attorney assignments based on invention complexity 
and expertise requirements.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ir_assignment_recommendation_function(input_data: dict) -> dict:
    """
    Recommend attorney assignment based on invention characteristics.
    
    Args:
        input_data: Dictionary containing 'invention_record_text'
        
    Returns:
        Dictionary with assignment recommendations
    """
    invention_text = input_data.get('invention_record_text', '')
    
    system_prompt = """
    You are an expert patent law firm manager with deep knowledge of attorney specializations 
    and case assignment optimization. Analyze the invention record to recommend appropriate 
    attorney assignments and resource allocation.
    
    Return a JSON object with the following structure:
    {
        "attorney_recommendations": [
            {
                "specialization": "Required attorney specialization",
                "experience_level": "Senior/Mid/Junior",
                "specific_skills": ["Required", "specific", "skills"],
                "rationale": "Why this specialization is needed"
            }
        ],
        "expertise_requirements": ["Key", "areas", "of", "expertise", "needed"],
        "complexity_level": "High/Medium/Low",
        "estimated_hours": 120,
        "priority_level": "Urgent/High/Normal/Low",
        "special_considerations": ["Any", "special", "factors", "to", "consider"],
        "timeline_recommendations": {
            "initial_review": "1-2 weeks",
            "prior_art_search": "2-3 weeks", 
            "drafting": "4-6 weeks",
            "filing": "8-10 weeks"
        },
        "budget_considerations": {
            "estimated_cost_range": "$15,000 - $25,000",
            "cost_factors": ["Factors", "affecting", "cost"],
            "cost_optimization_tips": ["Ways", "to", "optimize", "costs"]
        }
    }
    
    Consider technical complexity, legal challenges, commercial importance, and timeline requirements.
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
        return {"error": f"Failed to generate assignment recommendations: {str(e)}"}

# Build the tool
def create_ir_assignment_recommender():
    """Create and return the IR Assignment Recommender tool."""
    builder = ToolBuilder(
        tool_name="ir_assignment_recommender",
        description="Suggests suitable agent/attorney assignments based on invention complexity and expertise requirements"
    )
    
    # Set schemas
    input_schema = {"invention_record_text": str}
    
    output_schema = {
        "attorney_recommendations": list,
        "expertise_requirements": list,
        "complexity_level": str,
        "estimated_hours": int,
        "priority_level": str,
        "special_considerations": list,
        "timeline_recommendations": dict,
        "budget_considerations": dict
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ir_assignment_recommendation_function)
    
    return builder.build()

# Create the tool instance
ir_assignment_recommender = create_ir_assignment_recommender()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_record_text": """
        Title: Blockchain-Based Supply Chain Verification System
        
        Inventors: Dr. Elena Vasquez (Cryptography), James Park (Supply Chain), Sarah Kim (Software Engineering)
        
        Technology Field: Blockchain, distributed ledger technology, supply chain management, cryptography
        
        Complexity: High - involves multiple technical domains, regulatory compliance, international standards
        
        Description: A comprehensive blockchain-based system for verifying the authenticity and traceability 
        of products throughout complex global supply chains. The system uses smart contracts, IoT sensors, 
        and cryptographic proofs to create immutable records of product journey from manufacture to consumer.
        
        Key Technical Challenges:
        - Multi-party consensus protocols
        - Integration with existing ERP systems
        - Scalability for global supply chains
        - Privacy-preserving verification
        - Regulatory compliance across jurisdictions
        
        Commercial Importance: High - targeting Fortune 500 companies in pharmaceutical, food, and luxury goods industries
        
        Timeline: Urgent - need to file before upcoming industry conference announcement
        
        Competitive Landscape: Several major tech companies working on similar solutions
        
        Regulatory Considerations: FDA regulations for pharmaceuticals, GDPR for data privacy, various international trade regulations
        """
    }
    
    result = ir_assignment_recommender.execute(test_input)
    print(f"Assignment Recommendation Result: {result}")