"""
Patent Summary Generator Tool

Generates comprehensive patent application summaries with technical 
solutions and embodiments.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def patent_summary_generation_function(input_data: dict) -> dict:
    """
    Generate patent application summary from invention disclosure.
    
    Args:
        input_data: Dictionary containing 'invention_disclosure_text' and optional 'patent_context'
        
    Returns:
        Dictionary with patent summary
    """
    invention_text = input_data.get('invention_disclosure_text', '')
    patent_context = input_data.get('patent_context', '')
    
    system_prompt = """
    You are an expert patent attorney specializing in summary sections. Generate a comprehensive 
    patent application summary that clearly explains the invention, its technical solution, 
    and its various embodiments in a way that supports the claims.
    
    Return a JSON object with the following structure:
    {
        "invention_overview": "High-level overview of what the invention is and does",
        "technical_solution": "Detailed explanation of how the invention solves the technical problem",
        "key_advantages": [
            "Primary advantage 1 with specific benefits",
            "Primary advantage 2 with specific benefits"
        ],
        "preferred_embodiments": [
            {
                "embodiment": "Main embodiment description",
                "key_features": ["Feature 1", "Feature 2"],
                "operation": "How this embodiment operates"
            }
        ],
        "alternative_embodiments": [
            {
                "embodiment": "Alternative approach description", 
                "differences": "How it differs from preferred embodiment",
                "advantages": "Specific advantages of this approach"
            }
        ],
        "applications": [
            {
                "application": "Specific use case or application",
                "benefits": "Benefits in this application context",
                "market": "Target market or industry"
            }
        ],
        "technical_effects": [
            "Specific technical effect 1",
            "Specific technical effect 2"
        ],
        "scope_of_protection": "Description of the scope of protection sought"
    }
    
    Ensure the summary is comprehensive yet concise, and supports the broadest reasonable claim scope.
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
        return {"error": f"Failed to generate patent summary: {str(e)}"}

# Build the tool
def create_patent_summary_generator():
    """Create and return the Patent Summary Generator tool."""
    builder = ToolBuilder(
        tool_name="patent_summary_generator",
        description="Generates comprehensive patent application summaries with technical solutions and embodiments"
    )
    
    # Set schemas
    input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str
    }
    
    output_schema = {
        "invention_overview": str,
        "technical_solution": str,
        "key_advantages": list,
        "preferred_embodiments": list,
        "alternative_embodiments": list,
        "applications": list,
        "technical_effects": list,
        "scope_of_protection": str
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(patent_summary_generation_function)
    
    return builder.build()

# Create the tool instance
patent_summary_generator = create_patent_summary_generator()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_disclosure_text": """
        Invention: Smart Wearable Health Monitoring System with Predictive Analytics
        
        Technical Problem: Current wearable health devices provide basic monitoring but lack 
        predictive capabilities and personalized health insights. They cannot predict health 
        issues before they become serious or provide actionable recommendations.
        
        Technical Solution: A comprehensive wearable health monitoring system that combines 
        multiple biometric sensors with AI-powered predictive analytics to provide early 
        warning of potential health issues and personalized health recommendations.
        
        Key Components:
        1. Multi-sensor wearable device with:
           - Continuous heart rate and ECG monitoring
           - Blood oxygen saturation measurement
           - Body temperature tracking
           - Sleep pattern analysis
           - Activity and motion detection
           
        2. AI Analytics Engine:
           - Machine learning models for pattern recognition
           - Predictive algorithms for health risk assessment
           - Personalized baseline establishment
           - Anomaly detection systems
           
        3. Health Management Platform:
           - Mobile app with user interface
           - Healthcare provider dashboard
           - Emergency alert system
           - Data sharing and privacy controls
        
        Novel Features:
        - Predictive health modeling using personal baseline data
        - Integration with electronic health records
        - Real-time risk assessment and alerts
        - Personalized health recommendations
        - Long-term trend analysis and reporting
        
        Applications:
        - Chronic disease management (diabetes, heart disease)
        - Elderly care and remote monitoring
        - Fitness and wellness optimization
        - Clinical research and drug trials
        - Preventive healthcare programs
        
        Benefits:
        - Early detection of health issues before symptoms appear
        - Reduced healthcare costs through prevention
        - Improved quality of life for users
        - Better health outcomes through personalized care
        - Reduced burden on healthcare systems
        """,
        "patent_context": ""
    }
    
    result = patent_summary_generator.execute(test_input)
    print(f"Patent Summary Result: {result}")