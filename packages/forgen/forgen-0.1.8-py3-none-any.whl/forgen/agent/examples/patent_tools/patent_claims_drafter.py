"""
Patent Claims Drafter Tool

Drafts comprehensive US-style patent claims including independent and 
dependent claims with scope analysis.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def patent_claims_drafting_function(input_data: dict) -> dict:
    """
    Draft patent claims from invention disclosure.
    
    Args:
        input_data: Dictionary containing 'invention_disclosure_text' and optional 'patent_context'
        
    Returns:
        Dictionary with drafted claims
    """
    invention_text = input_data.get('invention_disclosure_text', '')
    patent_context = input_data.get('patent_context', '')
    
    system_prompt = """
    You are an expert patent attorney specializing in claim drafting. Draft comprehensive US-style 
    patent claims that are clear, complete, and properly scoped to protect the invention effectively.
    
    Return a JSON object with the following structure:
    {
        "independent_claims": [
            {
                "claim_number": 1,
                "claim_type": "system/method/apparatus",
                "preamble": "A system for...",
                "body": "comprising: element 1...; element 2...; element 3...",
                "scope_notes": "Scope and strategy notes for this claim"
            }
        ],
        "dependent_claims": [
            {
                "claim_number": 2,
                "depends_on": 1,
                "limitation": "wherein the system further comprises...",
                "rationale": "Why this limitation adds value"
            }
        ],
        "claim_dependencies": {
            "claim_tree": "Visual representation of claim dependencies",
            "independent_count": 3,
            "dependent_count": 15
        },
        "claim_scope_analysis": "Analysis of claim breadth and strength",
        "key_limitations": ["Critical", "limitations", "that", "define", "the", "invention"],
        "alternative_embodiments": [
            {
                "embodiment": "Description of alternative approach",
                "claim_strategy": "How to claim this embodiment"
            }
        ]
    }
    
    Follow proper claim formatting and ensure claims are novel, non-obvious, and adequately supported.
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
        return {"error": f"Failed to draft claims: {str(e)}"}

# Build the tool
def create_patent_claims_drafter():
    """Create and return the Patent Claims Drafter tool."""
    builder = ToolBuilder(
        tool_name="patent_claims_drafter",
        description="Drafts comprehensive US-style patent claims including independent and dependent claims with scope analysis"
    )
    
    # Set schemas
    input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str
    }
    
    output_schema = {
        "independent_claims": list,
        "dependent_claims": list,
        "claim_dependencies": dict,
        "claim_scope_analysis": str,
        "key_limitations": list,
        "alternative_embodiments": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(patent_claims_drafting_function)
    
    return builder.build()

# Create the tool instance
patent_claims_drafter = create_patent_claims_drafter()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_disclosure_text": """
        Invention: Autonomous Drone Delivery System with Dynamic Route Optimization
        
        Technical Field: Unmanned aerial vehicles, logistics, route optimization, autonomous navigation
        
        Key Components:
        1. Autonomous drone with GPS navigation and obstacle avoidance
        2. Central dispatch system with real-time route optimization
        3. Secure package compartment with biometric locks
        4. Weather monitoring and route adjustment algorithms
        5. Landing pad network with automated loading/unloading
        
        Technical Features:
        - Machine learning-based route optimization considering weather, traffic, and no-fly zones
        - Multi-drone coordination to prevent collisions and optimize airspace usage
        - Real-time package tracking with customer notifications
        - Backup landing protocols for emergency situations
        - Integration with existing logistics management systems
        
        Novel Aspects:
        - Dynamic re-routing based on real-time conditions
        - Swarm intelligence for multi-drone operations
        - Predictive maintenance scheduling based on flight data
        - Adaptive payload capacity optimization
        
        Applications:
        - Last-mile delivery for e-commerce
        - Medical supply delivery to remote areas
        - Emergency response and disaster relief
        - Industrial part delivery within facilities
        """,
        "patent_context": ""
    }
    
    result = patent_claims_drafter.execute(test_input)
    print(f"Patent Claims Result: {result}")