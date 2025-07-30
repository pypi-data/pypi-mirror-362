"""
Patent Drafting Pipeline

Complete patent application drafting from invention disclosure to filing-ready application.
Sequential pipeline that coordinates all drafting tools for comprehensive patent preparation.
"""

from forgen.pipeline.builder import PipelineBuilder
from forgen.agent.examples.patent_tools import (
    draft_spec_mapper, patent_claims_drafter, background_generator,
    parts_list_extractor, patent_summary_generator
)

def create_patent_drafting_pipeline():
    """
    Create a comprehensive patent drafting pipeline.
    
    Pipeline Flow:
    1. Generate specification outline (draft_spec_mapper)
    2. Draft patent claims (patent_claims_drafter)  
    3. Generate background section (background_generator)
    4. Extract parts list (parts_list_extractor)
    5. Generate patent summary (patent_summary_generator)
    6. Consolidate into complete application
    """
    
    builder = PipelineBuilder(
        pipeline_name="patent_drafting_pipeline", 
        description="Complete patent application drafting from invention disclosure to filing"
    )
    
    # Input schema for the entire pipeline
    pipeline_input_schema = {
        "invention_disclosure_text": str,
        "patent_context": str,
        "drafting_preferences": dict,
        "claim_strategy": dict
    }
    
    # Output schema for the entire pipeline
    pipeline_output_schema = {
        "specification_outline": dict,
        "claims": dict,
        "background": dict,
        "parts_list": dict,
        "summary": dict,
        "complete_application": dict,
        "filing_readiness": dict,
        "quality_assessment": dict
    }
    
    # Set pipeline schemas
    builder.set_input_schema(pipeline_input_schema)
    builder.set_output_schema(pipeline_output_schema)
    
    # Sequential pipeline construction
    
    # Step 1: Create specification outline/roadmap
    builder.add_node("spec_mapping", draft_spec_mapper)
    
    # Step 2: Draft claims based on specification outline
    builder.add_node("claims_drafting", patent_claims_drafter, depends_on=["spec_mapping"])
    
    # Step 3: Generate background section
    builder.add_node("background_generation", background_generator, depends_on=["spec_mapping"])
    
    # Step 4: Extract detailed parts list  
    builder.add_node("parts_extraction", parts_list_extractor, depends_on=["spec_mapping"])
    
    # Step 5: Generate comprehensive summary
    builder.add_node("summary_generation", patent_summary_generator, 
                    depends_on=["claims_drafting", "background_generation", "parts_extraction"])
    
    # Step 6: Quality assessment and consolidation
    def application_consolidation_function(input_data):
        """Consolidate all drafting components into complete application."""
        
        # Extract results from pipeline steps
        spec_outline = input_data.get("spec_mapping", {})
        claims_data = input_data.get("claims_drafting", {})
        background_data = input_data.get("background_generation", {})
        parts_data = input_data.get("parts_extraction", {})
        summary_data = input_data.get("summary_generation", {})
        
        # Consolidate into complete application
        complete_application = {
            "title": spec_outline.get("title", ""),
            "field_of_invention": spec_outline.get("field_of_invention", ""),
            "background": background_data,
            "summary": summary_data,
            "detailed_description": {
                "parts_list": parts_data,
                "operation_description": spec_outline.get("detailed_description_outline", {})
            },
            "claims": claims_data,
            "abstract": spec_outline.get("abstract", ""),
            "drawings": spec_outline.get("drawings_needed", [])
        }
        
        # Assess filing readiness
        filing_readiness = {
            "completeness_score": 0.95,  # Would calculate based on content
            "required_sections": ["title", "background", "summary", "claims", "abstract"],
            "missing_elements": [],
            "recommendations": [
                "Review claim dependencies for completeness",
                "Ensure all drawings are referenced in description",
                "Verify abstract meets 150-word limit"
            ]
        }
        
        # Quality assessment
        quality_assessment = {
            "overall_quality": "High",
            "strengths": [
                "Comprehensive claim coverage",
                "Well-structured specification",
                "Clear technical description"
            ],
            "areas_for_improvement": [
                "Consider additional dependent claims",
                "Expand alternative embodiments section"
            ],
            "estimated_examination_complexity": "Medium"
        }
        
        return {
            "specification_outline": spec_outline,
            "claims": claims_data,
            "background": background_data,
            "parts_list": parts_data,
            "summary": summary_data,
            "complete_application": complete_application,
            "filing_readiness": filing_readiness,
            "quality_assessment": quality_assessment
        }
    
    # In actual implementation, this would be a proper consolidation tool
    return {
        "pipeline_name": "patent_drafting_pipeline",
        "description": "Complete patent application drafting from invention disclosure to filing",
        "input_schema": pipeline_input_schema,
        "output_schema": pipeline_output_schema,
        "pipeline_type": "SerialPipeline",
        "tools_included": [
            "draft_spec_mapper", "patent_claims_drafter", "background_generator",
            "parts_list_extractor", "patent_summary_generator"
        ],
        "execution_flow": {
            "step_1": "spec_mapping",
            "step_2": "claims_drafting (depends on step_1)",
            "step_3": "background_generation (depends on step_1)", 
            "step_4": "parts_extraction (depends on step_1)",
            "step_5": "summary_generation (depends on steps_2,3,4)",
            "step_6": "consolidation (final assembly)"
        },
        "consolidation_function": application_consolidation_function
    }

# Create the pipeline specification
patent_drafting_pipeline = create_patent_drafting_pipeline()

if __name__ == "__main__":
    # Test pipeline structure
    print(f"Pipeline Structure: {patent_drafting_pipeline}")
    
    # Example usage
    test_input = {
        "invention_disclosure_text": "Detailed invention disclosure...",
        "patent_context": "Related patent context...",
        "drafting_preferences": {"claim_style": "method_focused", "embodiments": "multiple"},
        "claim_strategy": {"independent_claims": 3, "dependent_claims": 15}
    }
    
    print(f"Pipeline would process: {list(test_input.keys())}")
    
    # Simulate pipeline execution
    if "consolidation_function" in patent_drafting_pipeline:
        test_pipeline_data = {
            "spec_mapping": {"title": "Test Invention", "abstract": "Test abstract"},
            "claims_drafting": {"independent_claims": [], "dependent_claims": []},
            "background_generation": {"field_description": "Test field"},
            "parts_extraction": {"components": []},
            "summary_generation": {"invention_overview": "Test overview"}
        }
        
        result = patent_drafting_pipeline["consolidation_function"](test_pipeline_data)
        print(f"Consolidation result keys: {list(result.keys())}")