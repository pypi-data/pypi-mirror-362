"""
IDS Form Generator Tool

Generates Information Disclosure Statement (IDS) forms from prior art references 
with compliance checking.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ids_form_generation_function(input_data: dict) -> dict:
    """
    Generate IDS form from prior art references.
    
    Args:
        input_data: Dictionary containing 'prior_art_references' and optional 'prosecution_history'
        
    Returns:
        Dictionary with IDS form data
    """
    prior_art_text = input_data.get('prior_art_references', '')
    prosecution_history = input_data.get('prosecution_history', {})
    
    system_prompt = """
    You are an expert patent prosecutor specializing in Information Disclosure Statement (IDS) preparation. 
    Generate a properly formatted IDS form from the provided prior art references according to USPTO guidelines.
    
    Return a JSON object with the following structure:
    {
        "us_patents": [
            {
                "patent_number": "US123456789",
                "issue_date": "YYYY-MM-DD",
                "patentee_name": "Inventor Name",
                "relevance": "Brief explanation of relevance"
            }
        ],
        "us_applications": [
            {
                "application_number": "16/123456",
                "filing_date": "YYYY-MM-DD",
                "applicant_name": "Applicant Name",
                "status": "Published/Pending",
                "relevance": "Brief explanation of relevance"
            }
        ],
        "foreign_patents": [
            {
                "country_code": "EP",
                "patent_number": "EP1234567",
                "issue_date": "YYYY-MM-DD",
                "patentee_name": "Inventor Name",
                "relevance": "Brief explanation of relevance"
            }
        ],
        "non_patent_literature": [
            {
                "title": "Article/Document Title",
                "author": "Author Name",
                "publication": "Journal/Source Name",
                "date": "YYYY-MM-DD",
                "pages": "Page numbers if applicable",
                "relevance": "Brief explanation of relevance"
            }
        ],
        "form_metadata": {
            "total_references": 25,
            "filing_deadline": "Calculated deadline based on prosecution status",
            "fee_required": true,
            "statement_required": true
        },
        "examiner_citations": [
            "References cited by examiner that should be included"
        ],
        "applicant_citations": [
            "References known to applicant that should be disclosed"
        ],
        "compliance_check": {
            "duty_of_disclosure_met": true,
            "timing_compliant": true,
            "format_compliant": true,
            "warnings": ["Any warnings or issues"],
            "recommendations": ["Recommendations for filing"]
        }
    }
    
    Ensure all references are properly categorized and formatted according to USPTO requirements.
    """
    
    user_content = f"Prior Art References:\n\n{prior_art_text}"
    if prosecution_history:
        user_content += f"\n\nProsecution History:\n{prosecution_history}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to generate IDS form: {str(e)}"}

# Build the tool
def create_ids_form_generator():
    """Create and return the IDS Form Generator tool."""
    builder = ToolBuilder(
        tool_name="ids_form_generator",
        description="Generates Information Disclosure Statement (IDS) forms from prior art references with compliance checking"
    )
    
    # Set schemas
    input_schema = {
        "prior_art_references": str,
        "prosecution_history": dict
    }
    
    output_schema = {
        "us_patents": list,
        "us_applications": list,
        "foreign_patents": list,
        "non_patent_literature": list,
        "form_metadata": dict,
        "examiner_citations": list,
        "applicant_citations": list,
        "compliance_check": dict
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ids_form_generation_function)
    
    return builder.build()

# Create the tool instance
ids_form_generator = create_ids_form_generator()

if __name__ == "__main__":
    # Test example
    test_input = {
        "prior_art_references": """
        US Patent References:
        1. US10,123,456 - "Autonomous Vehicle Navigation System" by Smith et al., issued January 15, 2020
        2. US9,876,543 - "Machine Learning for Route Optimization" by Johnson, issued March 22, 2018
        
        Foreign Patent References:
        1. EP3456789A1 - "Intelligent Transportation System" by Mueller et al., published June 10, 2019
        2. JP2019-123456 - "Vehicle Communication Network" by Tanaka, published July 5, 2019
        
        Non-Patent Literature:
        1. "Deep Learning for Autonomous Driving" by Chen, L. et al., IEEE Transactions on Intelligent Transportation Systems, Vol. 21, No. 4, April 2020, pp. 1234-1245
        2. "Survey of Path Planning Algorithms for Autonomous Vehicles" by Rodriguez, M., Journal of Robotics, Vol. 15, 2019, pp. 67-89
        3. Technical Report: "5G Networks for Connected Vehicles" by AutoTech Consortium, December 2019
        
        Additional References from Preliminary Search:
        - US8,765,432 - "Vehicle-to-Vehicle Communication Protocol" 
        - WO2020/123456 - "Predictive Maintenance for Autonomous Vehicles"
        - Academic paper: "Safety Considerations in Autonomous Vehicle Design"
        """,
        "prosecution_history": {
            "filing_date": "2021-03-15",
            "publication_date": "2021-09-16", 
            "first_office_action": "2022-01-20",
            "current_status": "Pending examination"
        }
    }
    
    result = ids_form_generator.execute(test_input)
    print(f"IDS Form Generation Result: {result}")