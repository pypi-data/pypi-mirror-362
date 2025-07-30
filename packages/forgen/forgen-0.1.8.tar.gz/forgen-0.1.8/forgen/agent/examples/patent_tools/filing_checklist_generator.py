"""
Filing Checklist Generator Tool

Generates comprehensive filing checklists with required documents, 
fees, and compliance requirements.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def filing_checklist_generation_function(input_data: dict) -> dict:
    """
    Generate comprehensive filing checklist.
    
    Args:
        input_data: Dictionary containing 'application_info' and optional 'app_status'
        
    Returns:
        Dictionary with filing checklist
    """
    application_info = input_data.get('application_info', '')
    app_status = input_data.get('app_status', {})
    
    system_prompt = """
    You are an expert patent prosecutor specializing in USPTO filing procedures. Generate a comprehensive 
    filing checklist that covers all required documents, fees, and compliance requirements for the 
    patent application filing.
    
    Return a JSON object with the following structure:
    {
        "required_documents": [
            {
                "document": "Application Data Sheet (ADS)",
                "status": "Required/Optional",
                "description": "What this document contains",
                "deadline": "Filing deadline if applicable",
                "notes": "Special considerations"
            }
        ],
        "optional_documents": [
            {
                "document": "Information Disclosure Statement (IDS)",
                "benefit": "Why this might be beneficial",
                "timing": "When to file",
                "considerations": "Things to consider"
            }
        ],
        "fees": {
            "basic_filing_fee": {
                "large_entity": 1600,
                "small_entity": 800,
                "micro_entity": 400,
                "description": "Basic filing fee for utility application"
            },
            "search_fee": {
                "large_entity": 700,
                "small_entity": 350,
                "micro_entity": 175,
                "description": "Search fee"
            },
            "examination_fee": {
                "large_entity": 800,
                "small_entity": 400,
                "micro_entity": 200,
                "description": "Examination fee"
            },
            "additional_fees": [
                {
                    "fee_type": "Excess claims fee",
                    "condition": "More than 20 total claims or 3 independent claims",
                    "amount": "Variable based on excess count"
                }
            ]
        },
        "formal_requirements": [
            {
                "requirement": "Proper format and margins",
                "specification": "1.5 or double spacing, 1-inch margins",
                "compliance_check": "Verify formatting before filing"
            }
        ],
        "disclosure_requirements": [
            {
                "requirement": "Best mode requirement",
                "description": "Must disclose best mode known to inventor",
                "compliance": "Ensure specification includes best mode"
            }
        ],
        "timing_requirements": {
            "filing_deadline": "Based on priority claims",
            "ids_deadline": "3 months from filing or before first OA",
            "foreign_filing_deadline": "12 months from priority date",
            "critical_dates": [
                {
                    "date": "YYYY-MM-DD",
                    "description": "What happens on this date",
                    "action_required": "What needs to be done"
                }
            ]
        },
        "compliance_checks": [
            {
                "check": "Unity of invention",
                "description": "All claims relate to single inventive concept",
                "verification": "Review claims for unity"
            }
        ]
    }
    
    Provide practical, actionable guidance for successful patent application filing.
    """
    
    user_content = f"Application Information:\n\n{application_info}"
    if app_status:
        user_content += f"\n\nApplication Status Data:\n{app_status}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to generate filing checklist: {str(e)}"}

# Build the tool
def create_filing_checklist_generator():
    """Create and return the Filing Checklist Generator tool."""
    builder = ToolBuilder(
        tool_name="filing_checklist_generator",
        description="Generates comprehensive filing checklists with required documents, fees, and compliance requirements"
    )
    
    # Set schemas
    input_schema = {
        "application_info": str,
        "app_status": dict
    }
    
    output_schema = {
        "required_documents": list,
        "optional_documents": list,
        "fees": dict,
        "formal_requirements": list,
        "disclosure_requirements": list,
        "timing_requirements": dict,
        "compliance_checks": list
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(filing_checklist_generation_function)
    
    return builder.build()

# Create the tool instance
filing_checklist_generator = create_filing_checklist_generator()

if __name__ == "__main__":
    # Test example
    test_input = {
        "application_info": """
        Patent Application Filing Information:
        
        Application Type: Non-provisional utility application
        Title: "Quantum-Enhanced Cryptographic Security System"
        
        Inventor: Dr. Alex Quantum (US Citizen)
        Applicant: CryptoTech Solutions LLC (Small Entity)
        
        Priority Claim: US Provisional 63/789123, filed January 15, 2024
        Filing Target: July 15, 2024 (within 12 months of provisional)
        
        Claims Summary:
        - 25 total claims (5 excess claims)
        - 4 independent claims (1 excess independent claim)
        - Claims cover system, method, and computer program product
        
        Specification: 45 pages including detailed description and drawings
        Drawings: 8 figures showing system architecture and flow diagrams
        
        Foreign Filing Plans:
        - Europe (EPO filing planned)
        - Japan (direct national filing)
        - Canada (direct filing)
        
        Prior Art Considerations:
        - Preliminary search conducted
        - 15 relevant prior art references identified
        - IDS filing planned within 3 months
        
        Special Considerations:
        - Complex technical subject matter requiring detailed description
        - Software and hardware components both claimed
        - Security-related invention with potential export control considerations
        """,
        "app_status": {
            "entity_status": "small",
            "expedited_examination": False,
            "track_one": False
        }
    }
    
    result = filing_checklist_generator.execute(test_input)
    print(f"Filing Checklist Result: {result}")