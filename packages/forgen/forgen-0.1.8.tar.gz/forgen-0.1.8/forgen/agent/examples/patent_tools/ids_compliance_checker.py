"""
IDS Compliance Checker Tool

Verifies IDS timing compliance and filing requirements with risk assessment.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ids_compliance_checking_function(input_data: dict) -> dict:
    """
    Check IDS filing compliance and timing requirements.
    
    Args:
        input_data: Dictionary containing 'ids_info' and optional 'prosecution_timeline'
        
    Returns:
        Dictionary with compliance analysis
    """
    ids_info = input_data.get('ids_info', '')
    prosecution_timeline = input_data.get('prosecution_timeline', {})
    
    system_prompt = """
    You are an expert patent prosecutor specializing in IDS compliance and USPTO procedures. Analyze the 
    IDS information and prosecution timeline to verify compliance with timing requirements and provide 
    risk assessment.
    
    Return a JSON object with the following structure:
    {
        "filing_windows": {
            "window_1": {
                "period": "Within 3 months of filing date",
                "deadline": "YYYY-MM-DD",
                "fee_required": false,
                "statement_required": false,
                "status": "Open/Closed/Applicable"
            },
            "window_2": {
                "period": "Before first Office Action or 3 months (whichever is later)",
                "deadline": "YYYY-MM-DD", 
                "fee_required": false,
                "statement_required": false,
                "status": "Open/Closed/Applicable"
            },
            "window_3": {
                "period": "Within 3 months of first Office Action",
                "deadline": "YYYY-MM-DD",
                "fee_required": true,
                "statement_required": true,
                "status": "Open/Closed/Applicable"
            }
        },
        "compliance_status": "Compliant/Non-compliant/At Risk",
        "timing_analysis": {
            "current_window": "Which window applies now",
            "days_remaining": 45,
            "next_deadline": "YYYY-MM-DD",
            "escalation_risk": "Risk of moving to more expensive window"
        },
        "fee_requirements": {
            "current_fee": 180,
            "entity_type": "Large/Small/Micro",
            "fee_escalation": {
                "next_window_fee": 800,
                "increase_amount": 620
            }
        },
        "statement_requirements": [
            {
                "requirement": "37 CFR 1.97(e) statement",
                "required": true,
                "description": "Statement explaining late filing"
            }
        ],
        "recommendations": [
            {
                "action": "File IDS immediately",
                "priority": "High/Medium/Low",
                "rationale": "Why this action is recommended",
                "deadline": "YYYY-MM-DD"
            }
        ],
        "risk_assessment": {
            "overall_risk": "Low/Medium/High",
            "specific_risks": [
                {
                    "risk": "Late filing penalty",
                    "likelihood": "Low/Medium/High",
                    "impact": "Description of impact",
                    "mitigation": "How to mitigate this risk"
                }
            ],
            "worst_case_scenario": "What happens if IDS is not filed properly"
        }
    }
    
    Provide practical guidance for maintaining IDS compliance and minimizing risks.
    """
    
    user_content = f"IDS Information:\n\n{ids_info}"
    if prosecution_timeline:
        user_content += f"\n\nProsecution Timeline:\n{prosecution_timeline}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to check IDS compliance: {str(e)}"}

# Build the tool
def create_ids_compliance_checker():
    """Create and return the IDS Compliance Checker tool."""
    builder = ToolBuilder(
        tool_name="ids_compliance_checker",
        description="Verifies IDS timing compliance and filing requirements with risk assessment"
    )
    
    # Set schemas
    input_schema = {
        "ids_info": str,
        "prosecution_timeline": dict
    }
    
    output_schema = {
        "filing_windows": dict,
        "compliance_status": str,
        "timing_analysis": dict,
        "fee_requirements": dict,
        "statement_requirements": list,
        "recommendations": list,
        "risk_assessment": dict
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ids_compliance_checking_function)
    
    return builder.build()

# Create the tool instance
ids_compliance_checker = create_ids_compliance_checker()

if __name__ == "__main__":
    # Test example
    test_input = {
        "ids_info": """
        IDS Filing Information:
        
        Application Number: 17/123456
        Filing Date: March 15, 2023
        Entity Status: Small Entity
        
        Current Status: First Office Action received January 20, 2024
        Response Due: April 20, 2024
        
        Prior Art to be Disclosed:
        - 12 US patents discovered during prosecution
        - 3 foreign patent documents
        - 5 non-patent literature references
        - 2 examiner-cited references from related applications
        
        Previous IDS Filings:
        - Initial IDS filed June 10, 2023 (within first 3 months)
        - No subsequent IDS filings
        
        Current Date: February 15, 2024
        
        Circumstances:
        - New prior art discovered during claim analysis for OA response
        - Some references were known at filing but inadvertently omitted
        - Client wants to ensure compliance with duty of disclosure
        - Budget considerations for fees
        
        Questions:
        - What are the filing options and deadlines?
        - What fees and statements are required?
        - What are the risks of delay?
        """,
        "prosecution_timeline": {
            "filing_date": "2023-03-15",
            "first_oa_date": "2024-01-20", 
            "response_due": "2024-04-20",
            "current_date": "2024-02-15"
        }
    }
    
    result = ids_compliance_checker.execute(test_input)
    print(f"IDS Compliance Check Result: {result}")