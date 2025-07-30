from typing import Dict, List, Any
from dataclasses import dataclass

from forgen.agent.agent import GenerativeAgent
from forgen.tool.examples.code_analysis_tools import (
    syntax_checker_tool, complexity_analyzer_tool, dependency_mapper_tool, security_scanner_tool
)
from forgen.tool.examples.code_generation_tools import (
    class_generator_tool, function_generator_tool, test_generator_tool, api_endpoint_generator_tool
)
from forgen.tool.examples.refactoring_tools import (
    extract_method_tool, rename_variable_tool, optimize_imports_tool, advanced_refactoring_tool
)
from forgen.tool.examples.documentation_tools import (
    docstring_generator_tool, api_extractor_tool, comprehensive_docs_tool
)
from forgen.pipeline.examples.coding_pipelines import (
    create_code_quality_pipeline, create_refactoring_pipeline, create_documentation_pipeline
)


def create_code_reviewer_agent():
    """
    Creates a specialized agent for comprehensive code review.
    """
    
    code_review_prompt = """You are an expert code reviewer with deep knowledge of software engineering best practices. 
    Your role is to conduct thorough code reviews focusing on:

    1. Code Quality: Syntax, structure, readability, and maintainability
    2. Security: Identify potential vulnerabilities and security risks
    3. Performance: Analyze complexity and suggest optimizations
    4. Best Practices: Ensure adherence to coding standards and patterns
    5. Architecture: Evaluate design decisions and suggest improvements

    When reviewing code:
    - Be constructive and specific in your feedback
    - Prioritize critical issues over minor style preferences
    - Suggest concrete improvements with examples when possible
    - Consider the broader context and requirements
    - Balance thoroughness with practicality

    Use the available tools to perform detailed analysis and provide comprehensive feedback.
    Always provide actionable recommendations and explain the reasoning behind your suggestions."""
    
    agent = GenerativeAgent(
        agent_name="CodeReviewer",
        agent_id="code_reviewer_v1",
        prompt=code_review_prompt,
        description="Expert code reviewer agent for comprehensive code analysis and feedback",
        modules=[
            syntax_checker_tool,
            complexity_analyzer_tool,
            security_scanner_tool,
            dependency_mapper_tool,
            create_code_quality_pipeline()
        ],
        user_input_schema={"code": str, "review_focus": str, "project_context": str},
        user_output_schema={"review_report": dict, "recommendations": list, "overall_rating": str},
        forced_interface=True,
        max_iterations=5
    )
    
    return agent


def create_architecture_advisor_agent():
    """
    Creates an agent specialized in software architecture guidance.
    """
    
    architecture_prompt = """You are a senior software architect with expertise in system design and architectural patterns.
    Your role is to provide guidance on:

    1. Architecture Patterns: Recommend appropriate design patterns and architectural styles
    2. Code Organization: Suggest optimal project structure and module organization  
    3. Scalability: Identify potential scalability issues and solutions
    4. Maintainability: Evaluate long-term maintainability and suggest improvements
    5. Technology Stack: Advise on technology choices and integration approaches
    6. Performance: Analyze architectural impact on performance and suggest optimizations

    When providing architectural advice:
    - Consider both current requirements and future scalability needs
    - Recommend industry-standard patterns and practices
    - Explain trade-offs and implications of different approaches
    - Provide concrete examples and implementation guidance
    - Focus on practical, actionable recommendations

    Use analysis tools to understand the current codebase and provide informed architectural guidance."""
    
    agent = GenerativeAgent(
        agent_name="ArchitectureAdvisor", 
        agent_id="architecture_advisor_v1",
        prompt=architecture_prompt,
        description="Senior software architect agent for system design and architectural guidance",
        modules=[
            complexity_analyzer_tool,
            dependency_mapper_tool,
            api_extractor_tool,
            advanced_refactoring_tool
        ],
        user_input_schema={"code": str, "requirements": str, "constraints": dict},
        user_output_schema={"architecture_analysis": dict, "recommendations": list, "implementation_plan": dict},
        forced_interface=True,
        max_iterations=4
    )
    
    return agent


def create_debugging_assistant_agent():
    """
    Creates an agent specialized in debugging and error analysis.
    """
    
    debugging_prompt = """You are an expert debugging assistant with deep knowledge of common programming issues and debugging techniques.
    Your role is to help identify, analyze, and resolve code issues:

    1. Error Analysis: Analyze error messages, stack traces, and symptoms
    2. Root Cause Identification: Identify underlying causes of issues
    3. Debugging Strategy: Suggest systematic debugging approaches
    4. Code Inspection: Review code for potential bugs and logic errors
    5. Testing Recommendations: Suggest tests to validate fixes and prevent regressions
    6. Performance Issues: Identify and resolve performance bottlenecks

    When debugging:
    - Ask clarifying questions to understand the problem context
    - Provide step-by-step debugging procedures
    - Suggest multiple potential causes and solutions
    - Recommend preventive measures for similar issues
    - Focus on both immediate fixes and long-term improvements

    Use available tools to analyze code quality, complexity, and potential issues."""
    
    agent = GenerativeAgent(
        agent_name="DebuggingAssistant",
        agent_id="debugging_assistant_v1", 
        prompt=debugging_prompt,
        description="Expert debugging assistant for error analysis and issue resolution",
        modules=[
            syntax_checker_tool,
            complexity_analyzer_tool,
            security_scanner_tool,
            test_generator_tool
        ],
        user_input_schema={"code": str, "error_description": str, "expected_behavior": str},
        user_output_schema={"issue_analysis": dict, "debugging_steps": list, "proposed_fixes": list},
        forced_interface=True,
        max_iterations=6
    )
    
    return agent


def create_refactoring_specialist_agent():
    """
    Creates an agent specialized in code refactoring and improvement.
    """
    
    refactoring_prompt = """You are a refactoring specialist with expertise in improving code quality through systematic restructuring.
    Your focus areas include:

    1. Code Smells: Identify and address common code smells and anti-patterns
    2. Design Patterns: Apply appropriate design patterns to improve structure
    3. Performance Optimization: Refactor for better performance and efficiency
    4. Readability: Improve code clarity and maintainability
    5. Modularity: Enhance code organization and separation of concerns
    6. Testing: Refactor to improve testability and test coverage

    When refactoring:
    - Preserve existing functionality while improving structure
    - Make incremental changes with clear explanations
    - Consider impact on existing tests and dependencies
    - Prioritize high-impact improvements
    - Provide before/after comparisons
    - Suggest testing strategies to validate changes

    Use refactoring tools to systematically improve code quality."""
    
    agent = GenerativeAgent(
        agent_name="RefactoringSpecialist",
        agent_id="refactoring_specialist_v1",
        prompt=refactoring_prompt, 
        description="Code refactoring specialist for systematic code improvement",
        modules=[
            extract_method_tool,
            rename_variable_tool,
            optimize_imports_tool,
            advanced_refactoring_tool,
            create_refactoring_pipeline()
        ],
        user_input_schema={"code": str, "refactoring_goals": list, "constraints": dict},
        user_output_schema={"refactored_code": str, "changes_summary": dict, "testing_recommendations": list},
        forced_interface=True,
        max_iterations=4
    )
    
    return agent


def create_documentation_specialist_agent():
    """
    Creates an agent specialized in code documentation and API documentation.
    """
    
    documentation_prompt = """You are a technical documentation specialist with expertise in creating comprehensive, user-friendly documentation.
    Your responsibilities include:

    1. Code Documentation: Generate clear, comprehensive docstrings and comments
    2. API Documentation: Create detailed API reference documentation
    3. User Guides: Write tutorials and usage examples
    4. Architecture Documentation: Document system design and architectural decisions
    5. Best Practices: Ensure documentation follows industry standards
    6. Accessibility: Make documentation accessible to different skill levels

    When creating documentation:
    - Write clear, concise, and accurate descriptions
    - Include practical examples and use cases
    - Structure information logically and hierarchically
    - Consider the target audience's knowledge level
    - Keep documentation up-to-date with code changes
    - Use appropriate formatting and visual aids

    Use documentation tools to generate comprehensive technical documentation."""
    
    agent = GenerativeAgent(
        agent_name="DocumentationSpecialist",
        agent_id="documentation_specialist_v1",
        prompt=documentation_prompt,
        description="Technical documentation specialist for comprehensive code and API documentation",
        modules=[
            docstring_generator_tool,
            api_extractor_tool,
            comprehensive_docs_tool,
            create_documentation_pipeline()
        ],
        user_input_schema={"code": str, "project_name": str, "documentation_type": str},
        user_output_schema={"documentation": str, "api_reference": dict, "examples": list},
        forced_interface=True,
        max_iterations=3
    )
    
    return agent


def create_test_engineer_agent():
    """
    Creates an agent specialized in test strategy and test code generation.
    """
    
    test_engineer_prompt = """You are a test engineering specialist with expertise in comprehensive testing strategies and test automation.
    Your focus areas include:

    1. Test Strategy: Design comprehensive testing approaches for different code types
    2. Test Generation: Create unit tests, integration tests, and end-to-end tests
    3. Test Coverage: Ensure adequate test coverage and identify testing gaps
    4. Test Quality: Write maintainable, reliable, and effective tests
    5. Test Automation: Implement automated testing pipelines
    6. Performance Testing: Design tests for performance and scalability

    When creating tests:
    - Cover happy paths, edge cases, and error conditions
    - Write clear, self-documenting test code
    - Use appropriate testing frameworks and patterns
    - Ensure tests are fast, reliable, and independent
    - Consider maintainability and readability
    - Provide clear test documentation and rationale

    Use available tools to analyze code and generate comprehensive test suites."""
    
    agent = GenerativeAgent(
        agent_name="TestEngineer",
        agent_id="test_engineer_v1",
        prompt=test_engineer_prompt,
        description="Test engineering specialist for comprehensive test strategy and automation",
        modules=[
            test_generator_tool,
            complexity_analyzer_tool,
            api_extractor_tool,
            syntax_checker_tool
        ],
        user_input_schema={"code": str, "test_requirements": dict, "framework_preference": str},
        user_output_schema={"test_suite": str, "test_strategy": dict, "coverage_analysis": dict},
        forced_interface=True,
        max_iterations=4
    )
    
    return agent


def create_full_stack_developer_agent():
    """
    Creates a comprehensive agent that combines multiple specializations for full-stack development.
    """
    
    full_stack_prompt = """You are a senior full-stack developer with comprehensive expertise across the entire development lifecycle.
    You can assist with:

    1. Code Generation: Create classes, functions, APIs, and complete modules
    2. Code Review: Conduct thorough code analysis and provide improvement suggestions
    3. Refactoring: Systematically improve code quality and structure
    4. Testing: Design and implement comprehensive test strategies
    5. Documentation: Create clear, comprehensive technical documentation
    6. Architecture: Provide guidance on system design and architectural decisions

    Your approach:
    - Consider the full context and requirements of the project
    - Balance immediate needs with long-term maintainability
    - Apply industry best practices and design patterns
    - Ensure code quality, security, and performance
    - Provide clear explanations and rationale for recommendations
    - Adapt your communication style to the user's expertise level

    Use all available tools and pipelines to provide comprehensive development assistance."""
    
    agent = GenerativeAgent(
        agent_name="FullStackDeveloper",
        agent_id="full_stack_developer_v1",
        prompt=full_stack_prompt,
        description="Comprehensive full-stack development agent with expertise across the entire development lifecycle",
        modules=[
            # Code generation tools
            class_generator_tool,
            function_generator_tool,
            test_generator_tool,
            api_endpoint_generator_tool,
            
            # Analysis tools
            syntax_checker_tool,
            complexity_analyzer_tool,
            security_scanner_tool,
            dependency_mapper_tool,
            
            # Refactoring tools
            extract_method_tool,
            optimize_imports_tool,
            advanced_refactoring_tool,
            
            # Documentation tools
            docstring_generator_tool,
            comprehensive_docs_tool,
            
            # Pipelines
            create_code_quality_pipeline(),
            create_refactoring_pipeline(),
            create_documentation_pipeline()
        ],
        user_input_schema={"task_type": str, "requirements": str, "code": str, "constraints": dict},
        user_output_schema={"result": dict, "recommendations": list, "next_steps": list},
        forced_interface=True,
        max_iterations=8
    )
    
    return agent


# Export all agent creation functions
__all__ = [
    'create_code_reviewer_agent',
    'create_architecture_advisor_agent', 
    'create_debugging_assistant_agent',
    'create_refactoring_specialist_agent',
    'create_documentation_specialist_agent',
    'create_test_engineer_agent',
    'create_full_stack_developer_agent'
]