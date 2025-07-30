"""
Filing Management Pipeline

Patent filing preparation and compliance management workflow.
Sequential pipeline for comprehensive filing preparation and compliance checking.
"""

from forgen.pipeline.builder import PipelineBuilder
from forgen.agent.examples.patent_tools import (
    filing_checklist_generator, ads_form_generator, 
    ids_form_generator, ids_compliance_checker
)

def create_filing_management_pipeline():
    """
    Create a comprehensive filing management pipeline.
    
    Pipeline Flow:
    1. Generate filing checklist (filing_checklist_generator)
    2. Generate ADS form (ads_form_generator)
    3. Generate IDS form (ids_form_generator)
    4. Check IDS compliance (ids_compliance_checker)
    5. Consolidate filing package with compliance verification
    """
    
    builder = PipelineBuilder(
        pipeline_name="filing_management_pipeline",
        description="Patent filing preparation and compliance management"
    )
    
    # Input schema for the entire pipeline
    pipeline_input_schema = {
        "application_info": str,
        "prior_art_references": str,
        "prosecution_history": dict,
        "entity_status": str,
        "filing_preferences": dict
    }
    
    # Output schema for the entire pipeline
    pipeline_output_schema = {
        "checklist": dict,
        "ads_form": dict,
        "ids_form": dict,
        "compliance": dict,
        "filing_package": dict,
        "cost_estimate": dict,
        "timeline": dict,
        "risk_assessment": dict
    }
    
    # Set pipeline schemas
    builder.set_input_schema(pipeline_input_schema)
    builder.set_output_schema(pipeline_output_schema)
    
    # Sequential pipeline construction
    
    # Step 1: Generate comprehensive filing checklist
    builder.add_node("checklist_generation", filing_checklist_generator)
    
    # Step 2: Generate Application Data Sheet
    builder.add_node("ads_generation", ads_form_generator, depends_on=["checklist_generation"])
    
    # Step 3: Generate Information Disclosure Statement  
    builder.add_node("ids_generation", ids_form_generator, depends_on=["checklist_generation"])
    
    # Step 4: Check IDS compliance and timing
    builder.add_node("compliance_check", ids_compliance_checker, depends_on=["ids_generation"])
    
    # Step 5: Package consolidation and final verification
    def filing_package_consolidation_function(input_data):
        """Consolidate all filing components into complete package with verification."""
        
        # Extract results from pipeline steps
        checklist = input_data.get("checklist_generation", {})
        ads_form = input_data.get("ads_generation", {})
        ids_form = input_data.get("ids_generation", {})
        compliance = input_data.get("compliance_check", {})
        
        # Create comprehensive filing package
        filing_package = {
            "required_documents": compile_required_documents(checklist, ads_form, ids_form),
            "forms": {
                "ads": ads_form,
                "ids": ids_form,
                "additional_forms": identify_additional_forms(checklist)
            },
            "supporting_documents": {
                "specification": {"status": "ready", "pages": estimate_page_count(checklist)},
                "claims": {"status": "ready", "count": estimate_claim_count(checklist)},
                "drawings": {"status": "ready", "figures": estimate_figure_count(checklist)},
                "abstract": {"status": "ready", "word_count": 150}
            },
            "compliance_status": assess_package_compliance(checklist, ads_form, ids_form, compliance)
        }
        
        # Calculate comprehensive cost estimate
        cost_estimate = calculate_filing_costs(checklist, ids_form, compliance)
        
        # Generate filing timeline
        timeline = generate_filing_timeline(checklist, compliance)
        
        # Assess overall risks
        risk_assessment = assess_filing_risks(checklist, compliance, filing_package)
        
        return {
            "checklist": checklist,
            "ads_form": ads_form,
            "ids_form": ids_form,
            "compliance": compliance,
            "filing_package": filing_package,
            "cost_estimate": cost_estimate,
            "timeline": timeline,
            "risk_assessment": risk_assessment
        }
    
    def compile_required_documents(checklist, ads_form, ids_form):
        """Compile list of all required documents for filing."""
        required_docs = []
        
        # From checklist
        if checklist.get("required_documents"):
            required_docs.extend([doc["document"] for doc in checklist["required_documents"]])
        
        # Add forms
        if ads_form:
            required_docs.append("Application Data Sheet (ADS)")
        if ids_form:
            required_docs.append("Information Disclosure Statement (IDS)")
        
        return list(set(required_docs))  # Remove duplicates
    
    def identify_additional_forms(checklist):
        """Identify any additional forms that may be needed."""
        additional_forms = []
        
        # Check for common additional forms based on checklist
        if checklist.get("foreign_filing_info"):
            additional_forms.append("Foreign Filing License Request")
        
        return additional_forms
    
    def estimate_page_count(checklist):
        """Estimate specification page count."""
        return 25  # Default estimate
    
    def estimate_claim_count(checklist):
        """Estimate total claim count."""
        return 20  # Default estimate
    
    def estimate_figure_count(checklist):
        """Estimate drawing figure count."""
        return 6  # Default estimate
    
    def assess_package_compliance(checklist, ads_form, ids_form, compliance):
        """Assess overall package compliance status."""
        compliance_issues = []
        
        # Check ADS compliance
        if not ads_form or not ads_form.get("inventor_info"):
            compliance_issues.append("ADS form incomplete - missing inventor information")
        
        # Check IDS compliance
        if compliance.get("compliance_status") != "Compliant":
            compliance_issues.append(f"IDS compliance issue: {compliance.get('compliance_status')}")
        
        # Check timing compliance
        if compliance.get("timing_analysis", {}).get("days_remaining", 0) < 7:
            compliance_issues.append("Approaching IDS filing deadline")
        
        return {
            "overall_status": "Compliant" if not compliance_issues else "Issues Found",
            "issues": compliance_issues,
            "recommendations": generate_compliance_recommendations(compliance_issues)
        }
    
    def generate_compliance_recommendations(issues):
        """Generate recommendations to address compliance issues."""
        recommendations = []
        
        for issue in issues:
            if "ADS" in issue:
                recommendations.append("Complete all required inventor information in ADS form")
            elif "IDS" in issue:
                recommendations.append("Address IDS compliance issues before filing")
            elif "deadline" in issue:
                recommendations.append("Prioritize IDS filing to meet deadline")
        
        return recommendations
    
    def calculate_filing_costs(checklist, ids_form, compliance):
        """Calculate comprehensive filing cost estimate."""
        entity_status = checklist.get("entity_status", "large").lower()
        
        # Base fees (2024 USPTO fees)
        base_fees = {
            "large": {"basic": 1600, "search": 700, "examination": 800},
            "small": {"basic": 800, "search": 350, "examination": 400}, 
            "micro": {"basic": 400, "search": 175, "examination": 200}
        }
        
        fees = base_fees.get(entity_status, base_fees["large"])
        total_cost = sum(fees.values())
        
        # Add excess claim fees if applicable
        claim_count = estimate_claim_count(checklist)
        if claim_count > 20:
            excess_claims = claim_count - 20
            excess_fee = 400 if entity_status == "large" else 200 if entity_status == "small" else 100
            total_cost += excess_claims * excess_fee
        
        # Add IDS fees if required
        if compliance.get("fee_requirements", {}).get("current_fee", 0) > 0:
            total_cost += compliance["fee_requirements"]["current_fee"]
        
        return {
            "base_fees": fees,
            "excess_claim_fees": (claim_count - 20) * (400 if entity_status == "large" else 200) if claim_count > 20 else 0,
            "ids_fees": compliance.get("fee_requirements", {}).get("current_fee", 0),
            "total_government_fees": total_cost,
            "attorney_fees_estimate": total_cost * 2,  # Rough estimate
            "total_estimated_cost": total_cost * 3
        }
    
    def generate_filing_timeline(checklist, compliance):
        """Generate filing timeline with key milestones."""
        timeline = {
            "immediate_actions": [
                {"action": "Finalize specification", "deadline": "3 days"},
                {"action": "Complete ADS form", "deadline": "2 days"},
                {"action": "Prepare filing package", "deadline": "5 days"}
            ],
            "filing_milestones": [
                {"milestone": "Application filing", "target_date": "Within 1 week"},
                {"milestone": "IDS filing", "deadline": compliance.get("timing_analysis", {}).get("next_deadline", "TBD")},
                {"milestone": "Publication", "estimated_date": "18 months from filing"}
            ],
            "critical_deadlines": extract_critical_deadlines(checklist, compliance)
        }
        
        return timeline
    
    def extract_critical_deadlines(checklist, compliance):
        """Extract critical deadlines from analysis."""
        deadlines = []
        
        # IDS deadlines
        if compliance.get("timing_analysis", {}).get("next_deadline"):
            deadlines.append({
                "type": "IDS Filing",
                "date": compliance["timing_analysis"]["next_deadline"],
                "importance": "High"
            })
        
        # Foreign filing deadlines
        timing_reqs = checklist.get("timing_requirements", {})
        if timing_reqs.get("foreign_filing_deadline"):
            deadlines.append({
                "type": "Foreign Filing",
                "date": timing_reqs["foreign_filing_deadline"], 
                "importance": "High"
            })
        
        return deadlines
    
    def assess_filing_risks(checklist, compliance, filing_package):
        """Assess risks associated with the filing."""
        risks = []
        
        # Compliance risks
        if filing_package["compliance_status"]["overall_status"] != "Compliant":
            risks.append({
                "risk": "Compliance Issues",
                "level": "High",
                "impact": "Filing delays or rejections",
                "mitigation": "Address all compliance issues before filing"
            })
        
        # Timing risks
        if compliance.get("timing_analysis", {}).get("days_remaining", 30) < 14:
            risks.append({
                "risk": "Tight IDS Deadline",
                "level": "Medium",
                "impact": "Higher fees or late filing penalties",
                "mitigation": "Prioritize IDS preparation and filing"
            })
        
        # Cost risks
        cost_estimate = calculate_filing_costs(checklist, {}, compliance)
        if cost_estimate["total_estimated_cost"] > 20000:
            risks.append({
                "risk": "High Filing Costs",
                "level": "Medium", 
                "impact": "Budget constraints",
                "mitigation": "Review entity status qualification and claim count"
            })
        
        return {
            "overall_risk_level": "High" if any(r["level"] == "High" for r in risks) else "Medium",
            "risk_factors": risks,
            "risk_mitigation_plan": [r["mitigation"] for r in risks]
        }
    
    return {
        "pipeline_name": "filing_management_pipeline",
        "description": "Patent filing preparation and compliance management",
        "input_schema": pipeline_input_schema,
        "output_schema": pipeline_output_schema,
        "pipeline_type": "SerialPipeline",
        "tools_included": [
            "filing_checklist_generator", "ads_form_generator",
            "ids_form_generator", "ids_compliance_checker"
        ],
        "execution_flow": {
            "step_1": "checklist_generation",
            "step_2": "ads_generation (depends on step_1)",
            "step_3": "ids_generation (depends on step_1)",
            "step_4": "compliance_check (depends on step_3)",
            "step_5": "package_consolidation (final assembly)"
        },
        "consolidation_function": filing_package_consolidation_function
    }

# Create the pipeline specification
filing_management_pipeline = create_filing_management_pipeline()

if __name__ == "__main__":
    # Test pipeline structure
    print(f"Pipeline Structure: {filing_management_pipeline}")
    
    # Example usage
    test_input = {
        "application_info": "Patent application information...",
        "prior_art_references": "List of prior art references...",
        "prosecution_history": {"filing_date": "2024-01-15"},
        "entity_status": "small",
        "filing_preferences": {"expedited": False, "foreign_filing": True}
    }
    
    print(f"Pipeline would process: {list(test_input.keys())}")
    
    # Simulate pipeline execution
    if "consolidation_function" in filing_management_pipeline:
        test_pipeline_data = {
            "checklist_generation": {"required_documents": [], "entity_status": "small"},
            "ads_generation": {"inventor_info": [{"name": "Test Inventor"}]},
            "ids_generation": {"total_references": 10},
            "compliance_check": {"compliance_status": "Compliant", "timing_analysis": {"days_remaining": 30}}
        }
        
        result = filing_management_pipeline["consolidation_function"](test_pipeline_data)
        print(f"Filing package result keys: {list(result.keys())}")
        print(f"Total estimated cost: ${result['cost_estimate']['total_estimated_cost']:,}")