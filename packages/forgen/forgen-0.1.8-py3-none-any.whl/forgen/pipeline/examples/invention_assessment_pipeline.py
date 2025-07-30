"""
Invention Assessment Pipeline

Comprehensive invention record analysis and assessment workflow.
Multi-path pipeline that processes invention records through parallel analysis tools.
"""

from forgen.pipeline.builder import PipelineBuilder
from forgen.agent.examples.patent_tools import (
    ir_metadata_extractor, ir_innovation_analyzer, ir_prior_art_assessor,
    ir_tech_classifier, ir_assignment_recommender
)

def create_invention_assessment_pipeline():
    """
    Create a comprehensive invention assessment pipeline.
    
    Pipeline Flow:
    1. Extract metadata (ir_metadata_extractor) - Entry point
    2. Parallel analysis phase:
       - Innovation analysis (ir_innovation_analyzer)
       - Prior art assessment (ir_prior_art_assessor)  
       - Technology classification (ir_tech_classifier)
    3. Assignment recommendations (ir_assignment_recommender) - Final consolidation
    """
    
    builder = PipelineBuilder(
        pipeline_name="invention_assessment_pipeline",
        description="Comprehensive invention record analysis and assessment"
    )
    
    # Input schema for the entire pipeline
    pipeline_input_schema = {
        "invention_record_text": str,
        "assessment_goals": list,
        "business_context": dict,
        "timeline_constraints": dict
    }
    
    # Output schema for the entire pipeline
    pipeline_output_schema = {
        "metadata": dict,
        "innovation": dict,
        "prior_art": dict,
        "classification": dict,
        "assignment": dict,
        "comprehensive_assessment": dict,
        "strategic_recommendations": list,
        "risk_analysis": dict
    }
    
    # Set pipeline schemas
    builder.set_input_schema(pipeline_input_schema)
    builder.set_output_schema(pipeline_output_schema)
    
    # Pipeline construction
    
    # Step 1: Extract basic metadata (foundation for all other analyses)
    builder.add_node("metadata_extraction", ir_metadata_extractor)
    
    # Step 2: Parallel analysis phase - all depend on metadata
    builder.add_node("innovation_analysis", ir_innovation_analyzer, depends_on=["metadata_extraction"])
    builder.add_node("prior_art_assessment", ir_prior_art_assessor, depends_on=["metadata_extraction"])
    builder.add_node("technology_classification", ir_tech_classifier, depends_on=["metadata_extraction"])
    
    # Step 3: Assignment recommendation (integrates all previous analyses)
    builder.add_node("assignment_recommendation", ir_assignment_recommender,
                    depends_on=["innovation_analysis", "prior_art_assessment", "technology_classification"])
    
    # Step 4: Comprehensive assessment consolidation
    def assessment_consolidation_function(input_data):
        """Consolidate all assessment components into comprehensive analysis."""
        
        # Extract results from pipeline steps
        metadata = input_data.get("metadata_extraction", {})
        innovation = input_data.get("innovation_analysis", {})
        prior_art = input_data.get("prior_art_assessment", {})
        classification = input_data.get("technology_classification", {})
        assignment = input_data.get("assignment_recommendation", {})
        
        # Calculate comprehensive assessment scores
        patentability_score = calculate_patentability_score(prior_art, innovation)
        commercial_potential = assess_commercial_potential(innovation, classification)
        competitive_landscape = analyze_competitive_position(prior_art, classification)
        
        comprehensive_assessment = {
            "overall_score": (patentability_score + commercial_potential + competitive_landscape) / 3,
            "patentability_assessment": {
                "score": patentability_score,
                "novelty_strength": prior_art.get("novelty_assessment", ""),
                "obviousness_risk": prior_art.get("obviousness_risks", []),
                "patent_likelihood": "High" if patentability_score > 7 else "Medium" if patentability_score > 4 else "Low"
            },
            "commercial_assessment": {
                "score": commercial_potential,
                "market_applications": innovation.get("commercial_applications", []),
                "competitive_advantages": innovation.get("advantages", []),
                "market_readiness": assess_market_readiness(innovation, classification)
            },
            "technical_assessment": {
                "complexity_level": assignment.get("complexity_level", "Medium"),
                "technology_maturity": assess_technology_maturity(classification),
                "implementation_challenges": identify_implementation_challenges(innovation)
            }
        }
        
        # Generate strategic recommendations
        strategic_recommendations = generate_strategic_recommendations(
            metadata, innovation, prior_art, classification, assignment, comprehensive_assessment
        )
        
        # Compile risk analysis
        risk_analysis = {
            "patent_risks": prior_art.get("patent_risks", {}),
            "market_risks": assess_market_risks(innovation, classification),
            "technical_risks": assess_technical_risks(innovation, classification),
            "competitive_risks": assess_competitive_risks(prior_art),
            "overall_risk_level": "Medium"  # Would calculate based on sub-risks
        }
        
        return {
            "metadata": metadata,
            "innovation": innovation,
            "prior_art": prior_art,
            "classification": classification,
            "assignment": assignment,
            "comprehensive_assessment": comprehensive_assessment,
            "strategic_recommendations": strategic_recommendations,
            "risk_analysis": risk_analysis
        }
    
    def calculate_patentability_score(prior_art, innovation):
        """Calculate patentability score based on prior art and innovation analysis."""
        # Simplified scoring logic
        novelty_factors = len(innovation.get("novelty_aspects", []))
        risk_factors = len(prior_art.get("obviousness_risks", []))
        return max(1, min(10, novelty_factors * 2 - risk_factors))
    
    def assess_commercial_potential(innovation, classification):
        """Assess commercial potential based on innovation and classification."""
        applications = len(innovation.get("commercial_applications", []))
        market_size = len(classification.get("industry_sectors", []))
        return min(10, applications + market_size)
    
    def analyze_competitive_position(prior_art, classification):
        """Analyze competitive landscape position."""
        competitive_landscape = prior_art.get("competitive_landscape", "")
        if "strong" in competitive_landscape.lower():
            return 8
        elif "moderate" in competitive_landscape.lower():
            return 6
        else:
            return 4
    
    def assess_market_readiness(innovation, classification):
        """Assess how ready the technology is for market."""
        return "High" if len(innovation.get("commercial_applications", [])) > 3 else "Medium"
    
    def assess_technology_maturity(classification):
        """Assess maturity of the technology field."""
        domains = classification.get("domains", [])
        if any("AI" in domain or "machine learning" in domain for domain in domains):
            return "Emerging"
        else:
            return "Established"
    
    def identify_implementation_challenges(innovation):
        """Identify key implementation challenges."""
        return [
            "Technical complexity",
            "Market adoption",
            "Regulatory approval"
        ]
    
    def assess_market_risks(innovation, classification):
        """Assess market-related risks."""
        return {
            "adoption_risk": "Medium",
            "competition_risk": "High",
            "timing_risk": "Low"
        }
    
    def assess_technical_risks(innovation, classification):
        """Assess technical implementation risks."""
        return {
            "feasibility_risk": "Low",
            "scalability_risk": "Medium",
            "performance_risk": "Low"
        }
    
    def assess_competitive_risks(prior_art):
        """Assess competitive landscape risks."""
        return {
            "patent_blocking_risk": "Medium",
            "freedom_to_operate_risk": "Medium",
            "litigation_risk": "Low"
        }
    
    def generate_strategic_recommendations(metadata, innovation, prior_art, classification, assignment, assessment):
        """Generate strategic recommendations based on all analyses."""
        recommendations = []
        
        # Patent strategy recommendations
        if assessment["patentability_assessment"]["score"] > 7:
            recommendations.append({
                "category": "Patent Strategy",
                "recommendation": "Proceed with patent filing - strong patentability",
                "priority": "High",
                "timeline": "File within 3 months"
            })
        
        # Commercial strategy recommendations
        if assessment["commercial_assessment"]["score"] > 6:
            recommendations.append({
                "category": "Commercial Strategy", 
                "recommendation": "Develop business case for commercialization",
                "priority": "High",
                "timeline": "Initiate within 6 months"
            })
        
        # Technical development recommendations
        recommendations.append({
            "category": "Technical Development",
            "recommendation": "Conduct proof-of-concept validation",
            "priority": "Medium",
            "timeline": "Complete within 4 months"
        })
        
        return recommendations
    
    return {
        "pipeline_name": "invention_assessment_pipeline",
        "description": "Comprehensive invention record analysis and assessment",
        "input_schema": pipeline_input_schema,
        "output_schema": pipeline_output_schema,
        "pipeline_type": "MultiPathPipeline",
        "tools_included": [
            "ir_metadata_extractor", "ir_innovation_analyzer", "ir_prior_art_assessor",
            "ir_tech_classifier", "ir_assignment_recommender"
        ],
        "execution_flow": {
            "phase_1": ["metadata_extraction"],
            "phase_2_parallel": ["innovation_analysis", "prior_art_assessment", "technology_classification"],
            "phase_3": ["assignment_recommendation"],
            "phase_4": ["comprehensive_assessment"]
        },
        "consolidation_function": assessment_consolidation_function
    }

# Create the pipeline specification
invention_assessment_pipeline = create_invention_assessment_pipeline()

if __name__ == "__main__":
    # Test pipeline structure
    print(f"Pipeline Structure: {invention_assessment_pipeline}")
    
    # Example usage
    test_input = {
        "invention_record_text": "Detailed invention record...",
        "assessment_goals": ["patentability", "commercial_potential", "competitive_analysis"],
        "business_context": {"industry": "technology", "timeline": "urgent"},
        "timeline_constraints": {"filing_deadline": "2024-06-01"}
    }
    
    print(f"Pipeline would process: {list(test_input.keys())}")
    
    # Simulate pipeline execution
    if "consolidation_function" in invention_assessment_pipeline:
        test_pipeline_data = {
            "metadata_extraction": {"title": "Test Invention"},
            "innovation_analysis": {"novelty_aspects": ["aspect1", "aspect2"], "commercial_applications": ["app1", "app2"]},
            "prior_art_assessment": {"obviousness_risks": [], "competitive_landscape": "moderate competition"},
            "technology_classification": {"domains": ["AI"], "industry_sectors": ["healthcare"]},
            "assignment_recommendation": {"complexity_level": "High"}
        }
        
        result = invention_assessment_pipeline["consolidation_function"](test_pipeline_data)
        print(f"Assessment result keys: {list(result.keys())}")
        print(f"Overall score: {result['comprehensive_assessment']['overall_score']}")