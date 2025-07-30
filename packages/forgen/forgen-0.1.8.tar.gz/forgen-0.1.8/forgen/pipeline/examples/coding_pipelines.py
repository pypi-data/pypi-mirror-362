from forgen.pipeline.builder import SerialPipelineBuilder, MultiPathPipelineBuilder
from forgen.pipeline.item import PipelineItem
from forgen.tool.examples.code_analysis_tools import (
    syntax_checker_tool, complexity_analyzer_tool, dependency_mapper_tool, security_scanner_tool
)
from forgen.tool.examples.code_generation_tools import (
    class_generator_tool, function_generator_tool, test_generator_tool
)
from forgen.tool.examples.refactoring_tools import (
    extract_method_tool, rename_variable_tool, optimize_imports_tool
)
from forgen.tool.examples.documentation_tools import (
    docstring_generator_tool, api_extractor_tool, markdown_docs_generator_tool
)


def create_code_quality_pipeline():
    """
    Creates a pipeline for comprehensive code quality analysis.
    """
    builder = SerialPipelineBuilder("CodeQualityPipeline")
    
    # Set global schemas
    builder.set_input_schema({"code": str, "language": str})
    builder.set_global_output_schema({
        "syntax_analysis": dict,
        "complexity_analysis": dict, 
        "dependency_analysis": dict,
        "security_analysis": dict,
        "quality_score": float,
        "recommendations": list
    })
    
    builder.set_description("Comprehensive code quality analysis pipeline")
    
    # Add nodes to the pipeline
    builder.add_node(syntax_checker_tool)
    builder.add_node(complexity_analyzer_tool)
    builder.add_node(dependency_mapper_tool)
    builder.add_node(security_scanner_tool)
    
    # Add final aggregation node
    def aggregate_quality_metrics(input_data):
        """Aggregates all quality metrics into a final score and recommendations."""
        
        syntax_valid = input_data.get("valid", False)
        complexity = input_data.get("complexity_score", 0)
        maintainability = input_data.get("maintainability_index", 100)
        security_issues = len(input_data.get("high_risk", []))
        
        # Calculate quality score (0-100)
        quality_score = 100
        
        if not syntax_valid:
            quality_score = 0
        else:
            # Deduct points for complexity (assuming avg complexity should be < 10)
            if complexity > 10:
                quality_score -= min(30, (complexity - 10) * 2)
            
            # Factor in maintainability
            quality_score = quality_score * (maintainability / 100)
            
            # Deduct for security issues
            quality_score -= security_issues * 10
            
            quality_score = max(0, quality_score)
        
        recommendations = []
        if not syntax_valid:
            recommendations.append("Fix syntax errors before proceeding")
        if complexity > 10:
            recommendations.append("Consider breaking down complex functions")
        if maintainability < 70:
            recommendations.append("Improve code maintainability")
        if security_issues > 0:
            recommendations.append("Address security vulnerabilities")
        
        return {
            "syntax_analysis": input_data,
            "complexity_analysis": input_data,
            "dependency_analysis": input_data,
            "security_analysis": input_data,
            "quality_score": round(quality_score, 2),
            "recommendations": recommendations
        }
    
    builder.create_and_add_node(
        operative_fn=aggregate_quality_metrics,
        is_generative_node=False
    )
    
    return builder.build()


def create_code_generation_pipeline():
    """
    Creates a pipeline for generating complete code modules with tests and documentation.
    """
    builder = MultiPathPipelineBuilder()
    builder.set_name("CodeGenerationPipeline")
    builder.set_description("Generates classes, functions, tests, and documentation")
    
    # Create pipeline items
    class_gen_item = PipelineItem(
        item_id="class_generator",
        module=class_generator_tool,
        input_data={}
    )
    
    test_gen_item = PipelineItem(
        item_id="test_generator", 
        module=test_generator_tool,
        input_data={}
    )
    
    docs_gen_item = PipelineItem(
        item_id="docs_generator",
        module=docstring_generator_tool,
        input_data={}
    )
    
    # Add items to pipeline
    builder.add_item(class_gen_item)
    builder.add_item(test_gen_item)
    builder.add_item(docs_gen_item)
    
    # Set up dependencies - class generation feeds into both test and docs generation
    builder.add_engine_tuple("class_generator", "test_generator")
    builder.add_engine_tuple("class_generator", "docs_generator")
    
    return builder.build()


def create_refactoring_pipeline():
    """
    Creates a pipeline for systematic code refactoring.
    """
    builder = SerialPipelineBuilder("RefactoringPipeline")
    
    builder.set_input_schema({"code": str, "refactoring_operations": list})
    builder.set_global_output_schema({
        "refactored_code": str,
        "operations_performed": list,
        "improvements": dict
    })
    
    builder.set_description("Systematic code refactoring pipeline")
    
    # Add refactoring tools in sequence
    builder.add_node(optimize_imports_tool)
    builder.add_node(rename_variable_tool) 
    builder.add_node(extract_method_tool)
    
    # Add final consolidation node
    def consolidate_refactoring(input_data):
        """Consolidates refactoring results and provides summary."""
        return {
            "refactored_code": input_data.get("modified_code", ""),
            "operations_performed": [
                "optimize_imports",
                "rename_variables", 
                "extract_methods"
            ],
            "improvements": {
                "imports_optimized": True,
                "variables_renamed": input_data.get("replacements_made", 0),
                "methods_extracted": 1 if input_data.get("success", False) else 0
            }
        }
    
    builder.create_and_add_node(
        operative_fn=consolidate_refactoring,
        is_generative_node=False
    )
    
    return builder.build()


def create_documentation_pipeline():
    """
    Creates a pipeline for comprehensive code documentation.
    """
    builder = SerialPipelineBuilder("DocumentationPipeline")
    
    builder.set_input_schema({"code": str, "project_name": str})
    builder.set_global_output_schema({
        "documented_code": str,
        "api_documentation": str,
        "markdown_docs": str
    })
    
    builder.set_description("Comprehensive code documentation pipeline")
    
    # Sequential documentation generation
    builder.add_node(docstring_generator_tool)
    builder.add_node(api_extractor_tool) 
    builder.add_node(markdown_docs_generator_tool)
    
    return builder.build()


def create_code_review_pipeline():
    """
    Creates a comprehensive code review pipeline combining multiple analysis tools.
    """
    builder = MultiPathPipelineBuilder()
    builder.set_name("CodeReviewPipeline")
    builder.set_description("Comprehensive automated code review")
    
    # Create parallel analysis items
    syntax_item = PipelineItem(
        item_id="syntax_check",
        module=syntax_checker_tool,
        input_data={}
    )
    
    complexity_item = PipelineItem(
        item_id="complexity_check", 
        module=complexity_analyzer_tool,
        input_data={}
    )
    
    security_item = PipelineItem(
        item_id="security_check",
        module=security_scanner_tool,
        input_data={}
    )
    
    dependency_item = PipelineItem(
        item_id="dependency_check",
        module=dependency_mapper_tool,
        input_data={}
    )
    
    # Create aggregation function for review results
    def aggregate_review_results(input_data):
        """Aggregates all code review results into a comprehensive report."""
        
        review_report = {
            "overall_status": "PASS",
            "critical_issues": [],
            "warnings": [],
            "suggestions": [],
            "metrics": {},
            "dependencies": {}
        }
        
        # Process syntax results
        if not input_data.get("valid", True):
            review_report["overall_status"] = "FAIL"
            review_report["critical_issues"].extend(input_data.get("errors", []))
        
        review_report["warnings"].extend(input_data.get("warnings", []))
        review_report["suggestions"].extend(input_data.get("suggestions", []))
        
        # Process complexity results  
        complexity_score = input_data.get("complexity_score", 0)
        maintainability = input_data.get("maintainability_index", 100)
        
        review_report["metrics"] = {
            "complexity_score": complexity_score,
            "maintainability_index": maintainability,
            "lines_of_code": input_data.get("lines_of_code", 0),
            "functions": input_data.get("functions", 0),
            "classes": input_data.get("classes", 0)
        }
        
        if complexity_score > 15:
            review_report["warnings"].append("High complexity detected - consider refactoring")
        
        if maintainability < 60:
            review_report["warnings"].append("Low maintainability index - code may be hard to maintain")
        
        # Process security results
        high_risk = input_data.get("high_risk", [])
        medium_risk = input_data.get("medium_risk", [])
        
        if high_risk:
            review_report["overall_status"] = "FAIL"
            review_report["critical_issues"].extend(high_risk)
        
        review_report["warnings"].extend(medium_risk)
        
        # Process dependencies
        review_report["dependencies"] = {
            "external_packages": input_data.get("potential_external", []),
            "stdlib_usage": input_data.get("stdlib_modules", []),
            "total_imports": len(input_data.get("imports", []))
        }
        
        return review_report
    
    # Create aggregation item
    aggregation_item = PipelineItem(
        item_id="review_aggregator",
        module=None,  # Will use a simple function
        input_data={}
    )
    
    # Add all items
    builder.add_item(syntax_item)
    builder.add_item(complexity_item)
    builder.add_item(security_item)
    builder.add_item(dependency_item)
    builder.add_item(aggregation_item)
    
    # Set up parallel execution feeding into aggregation
    builder.add_engine_tuple("syntax_check", "review_aggregator")
    builder.add_engine_tuple("complexity_check", "review_aggregator")
    builder.add_engine_tuple("security_check", "review_aggregator")
    builder.add_engine_tuple("dependency_check", "review_aggregator")
    
    return builder.build()


def create_full_development_pipeline():
    """
    Creates a complete development pipeline: generation -> quality check -> documentation.
    """
    builder = SerialPipelineBuilder("FullDevelopmentPipeline")
    
    builder.set_input_schema({
        "specification": str,
        "project_name": str,
        "generate_tests": bool
    })
    
    builder.set_global_output_schema({
        "generated_code": str,
        "quality_report": dict,
        "documentation": str,
        "tests": str,
        "final_status": str
    })
    
    builder.set_description("Complete development pipeline from specification to documented code")
    
    # Code generation phase
    def generate_from_spec(input_data):
        """Generate code based on specification."""
        spec = input_data.get("specification", "")
        project_name = input_data.get("project_name", "MyProject")
        
        # This would typically use an LLM to generate code from specification
        # For now, return a simple template
        generated_code = f'''
class {project_name}:
    """
    {spec}
    """
    
    def __init__(self):
        self.name = "{project_name}"
    
    def execute(self):
        """Main execution method."""
        return f"Executing {{self.name}}"
'''
        
        return {
            "code": generated_code,
            "language": "python"
        }
    
    builder.create_and_add_node(
        operative_fn=generate_from_spec,
        is_generative_node=False
    )
    
    # Quality analysis phase
    builder.add_node(syntax_checker_tool)
    builder.add_node(complexity_analyzer_tool)
    builder.add_node(security_scanner_tool)
    
    # Documentation phase
    builder.add_node(docstring_generator_tool)
    
    # Final consolidation
    def finalize_development(input_data):
        """Finalize the development pipeline output."""
        
        syntax_valid = input_data.get("valid", False)
        quality_score = 100 if syntax_valid else 0
        
        if input_data.get("complexity_score", 0) > 10:
            quality_score -= 20
            
        if input_data.get("high_risk", []):
            quality_score -= 30
        
        final_status = "SUCCESS" if quality_score >= 70 else "NEEDS_REVIEW"
        
        return {
            "generated_code": input_data.get("modified_code", ""),
            "quality_report": {
                "syntax_valid": syntax_valid,
                "quality_score": quality_score,
                "complexity": input_data.get("complexity_score", 0),
                "security_issues": len(input_data.get("high_risk", []))
            },
            "documentation": "Generated with docstrings",
            "tests": "Test generation would go here",
            "final_status": final_status
        }
    
    builder.create_and_add_node(
        operative_fn=finalize_development,
        is_generative_node=False
    )
    
    return builder.build()


# Export the pipeline creation functions
__all__ = [
    'create_code_quality_pipeline',
    'create_code_generation_pipeline', 
    'create_refactoring_pipeline',
    'create_documentation_pipeline',
    'create_code_review_pipeline',
    'create_full_development_pipeline'
]