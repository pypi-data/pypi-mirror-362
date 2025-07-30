"""
ADS Form Generator Tool

Generates Application Data Sheet (ADS) forms from application metadata 
with all required sections.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ads_form_generation_function(input_data: dict) -> dict:
    """
    Generate ADS form from application metadata.
    
    Args:
        input_data: Dictionary containing 'application_metadata' and optional 'app_metadata'
        
    Returns:
        Dictionary with ADS form data
    """
    application_metadata = input_data.get('application_metadata', '')
    app_metadata = input_data.get('app_metadata', {})
    
    system_prompt = """
    You are an expert patent prosecutor specializing in Application Data Sheet (ADS) preparation. 
    Generate a properly formatted ADS form from the provided application metadata according to USPTO guidelines.
    
    Return a JSON object with the following structure:
    {
        "application_info": {
            "title": "Full title of the invention",
            "application_type": "Nonprovisional/Provisional/Continuation/etc.",
            "subject_matter": "Utility/Design/Plant",
            "filing_date": "YYYY-MM-DD",
            "confirmation_number": "Confirmation number if available"
        },
        "inventor_info": [
            {
                "name": {
                    "family_name": "Last Name",
                    "given_name": "First Name",
                    "middle_name": "Middle Name"
                },
                "residence": {
                    "city": "City",
                    "state": "State",
                    "country": "Country Code"
                },
                "citizenship": "Country Code",
                "inventor_authority": true
            }
        ],
        "applicant_info": {
            "name": "Applicant Name (if different from inventor)",
            "type": "Person/Corporation/Government",
            "address": {
                "street": "Street Address",
                "city": "City",
                "state": "State",
                "postal_code": "ZIP/Postal Code",
                "country": "Country Code"
            }
        },
        "correspondence_info": {
            "address": {
                "name": "Correspondence Name",
                "street": "Street Address", 
                "city": "City",
                "state": "State",
                "postal_code": "ZIP Code",
                "country": "Country Code"
            },
            "email": "email@domain.com",
            "phone": "Phone Number"
        },
        "representative_info": {
            "attorney_registration_number": "12345",
            "name": "Attorney Name",
            "firm_name": "Law Firm Name",
            "phone": "Phone Number",
            "email": "attorney@lawfirm.com"
        },
        "priority_claims": [
            {
                "country": "Country Code",
                "application_number": "Application Number",
                "filing_date": "YYYY-MM-DD",
                "priority_type": "Domestic/Foreign"
            }
        ],
        "foreign_filing_info": {
            "foreign_priority": true,
            "pct_filing": false,
            "foreign_filing_license": "Required/Not Required"
        },
        "publication_info": {
            "early_publication": false,
            "nonpublication_request": false,
            "publication_date": "YYYY-MM-DD or null"
        }
    }
    
    Ensure all required fields are completed and format follows USPTO ADS requirements.
    """
    
    user_content = f"Application Metadata:\n\n{application_metadata}"
    if app_metadata:
        user_content += f"\n\nAdditional Application Data:\n{app_metadata}"
    
    try:
        response = get_chat_json(
            message_history=[],
            system_content=system_prompt,
            user_content=user_content,
            json_response=True
        )
        return response
    except Exception as e:
        return {"error": f"Failed to generate ADS form: {str(e)}"}

# Build the tool
def create_ads_form_generator():
    """Create and return the ADS Form Generator tool."""
    builder = ToolBuilder(
        tool_name="ads_form_generator",
        description="Generates Application Data Sheet (ADS) forms from application metadata with all required sections"
    )
    
    # Set schemas
    input_schema = {
        "application_metadata": str,
        "app_metadata": dict
    }
    
    output_schema = {
        "application_info": dict,
        "inventor_info": list,
        "applicant_info": dict,
        "correspondence_info": dict,
        "representative_info": dict,
        "priority_claims": list,
        "foreign_filing_info": dict,
        "publication_info": dict
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ads_form_generation_function)
    
    return builder.build()

# Create the tool instance
ads_form_generator = create_ads_form_generator()

if __name__ == "__main__":
    # Test example
    test_input = {
        "application_metadata": """
        Patent Application Information:
        
        Title: "Artificial Intelligence-Powered Medical Diagnostic System with Real-Time Analysis"
        
        Inventors:
        1. Dr. Sarah Chen - US Citizen, residing in San Francisco, CA, USA
        2. Michael Rodriguez - US Citizen, residing in Boston, MA, USA  
        3. Dr. Priya Patel - Indian Citizen, residing in Bangalore, India
        
        Applicant: MedTech Innovations Inc. (Delaware Corporation)
        Address: 123 Innovation Drive, San Francisco, CA 94105, USA
        
        Attorney Information:
        Law Firm: Patterson & Associates Patent Law
        Attorney: Jennifer Patterson (Registration No. 45678)
        Address: 456 Legal Street, San Francisco, CA 94102
        Phone: (415) 555-0123
        Email: jpatterson@patersonlaw.com
        
        Correspondence Address: Same as attorney address
        
        Application Type: Non-provisional utility application
        Filing Date: March 15, 2024
        
        Priority Claims:
        - US Provisional Application No. 63/456789, filed September 15, 2023
        
        Foreign Filing: Planning to file in Europe (EPO) and Japan within 12 months
        
        Publication: Standard publication requested (18 months from priority date)
        
        Subject Matter: Utility patent for medical device technology
        """,
        "app_metadata": {
            "confirmation_number": "8765",
            "entity_status": "Large Entity",
            "expedited_examination": False
        }
    }
    
    result = ads_form_generator.execute(test_input)
    print(f"ADS Form Generation Result: {result}")