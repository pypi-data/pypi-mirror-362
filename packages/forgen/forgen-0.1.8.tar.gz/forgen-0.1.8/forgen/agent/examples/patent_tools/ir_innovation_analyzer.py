"""
Invention Record Innovation Analyzer Tool

Analyzes invention records to extract innovation summaries, technical problems, 
and commercial applications.
"""

from forgen.tool.builder import ToolBuilder
from forgen.llm.openai_interface.interface import get_chat_json

def ir_innovation_analysis_function(input_data: dict) -> dict:
    """
    Analyze invention record to extract innovation insights.
    
    Args:
        input_data: Dictionary containing 'invention_record_text'
        
    Returns:
        Dictionary with innovation analysis
    """
    invention_text = input_data.get('invention_record_text', '')
    
    system_prompt = """
    You are an expert innovation analyst and patent strategist. Analyze the provided invention record to extract key innovation insights.
    
    Return a JSON object with the following structure:
    {
        "innovation_summary": "Concise summary of the core innovation (100-200 words)",
        "technical_problem": "Primary technical problem being solved",
        "solution_approach": "How the invention solves the technical problem",
        "advantages": ["List", "of", "key", "technical", "advantages"],
        "novelty_aspects": ["Unique", "features", "that", "distinguish", "from", "prior", "art"],
        "commercial_applications": ["Potential", "commercial", "use", "cases"],
        "differentiation": "What makes this invention unique in the market"
    }
    
    Focus on technical merit, commercial viability, and competitive advantages.
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
        return {"error": f"Failed to analyze innovation: {str(e)}"}

# Build the tool
def create_ir_innovation_analyzer():
    """Create and return the IR Innovation Analyzer tool."""
    builder = ToolBuilder(
        tool_name="ir_innovation_analyzer",
        description="Analyzes invention records to extract innovation summaries, technical problems, and commercial applications"
    )
    
    # Set schemas
    input_schema = {"invention_record_text": str}
    
    output_schema = {
        "innovation_summary": str,
        "technical_problem": str,
        "solution_approach": str,
        "advantages": list,
        "novelty_aspects": list,
        "commercial_applications": list,
        "differentiation": str
    }
    
    builder.set_input_schema(input_schema)
    builder.set_output_schema(output_schema)
    builder.set_operative_function(ir_innovation_analysis_function)
    
    return builder.build()

# Create the tool instance
ir_innovation_analyzer = create_ir_innovation_analyzer()

if __name__ == "__main__":
    # Test example
    test_input = {
        "invention_record_text": """
        Title: Smart Battery Management System with Predictive Analytics
        
        Technical Problem: Current electric vehicle batteries suffer from unpredictable degradation, 
        leading to reduced range and unexpected failures. Existing battery management systems are 
        reactive rather than predictive.
        
        Solution: Our invention provides a smart battery management system that uses machine learning 
        to predict battery cell degradation patterns. The system continuously monitors voltage, 
        temperature, and current flow to build predictive models for each individual cell.
        
        Key Features:
        - Real-time cell-level monitoring
        - Predictive degradation modeling
        - Adaptive charging algorithms
        - Thermal management optimization
        
        Benefits:
        - 25% increase in battery lifespan
        - 15% improvement in energy efficiency
        - Early warning system for battery maintenance
        - Reduced warranty claims
        """
    }
    
    result = ir_innovation_analyzer.execute(test_input)
    print(f"Innovation Analysis Result: {result}")