import ast
import re
from typing import Dict, List, Any
from datetime import datetime

from forgen.tool.builder import GenToolBuilder


def generate_class(input_data):
    """
    Generates Python class code based on specifications.
    """
    class_name = input_data.get("class_name", "MyClass")
    attributes = input_data.get("attributes", [])
    methods = input_data.get("methods", [])
    parent_class = input_data.get("parent_class", "")
    docstring = input_data.get("docstring", "")
    include_init = input_data.get("include_init", True)
    
    # Start building the class
    inheritance = f"({parent_class})" if parent_class else ""
    class_def = f"class {class_name}{inheritance}:\n"
    
    # Add class docstring
    if docstring:
        class_def += f'    """{docstring}"""\n\n'
    elif not docstring:
        class_def += f'    """A {class_name} class."""\n\n'
    
    # Generate __init__ method if requested
    if include_init and attributes:
        class_def += "    def __init__(self"
        init_params = []
        init_body = []
        
        for attr in attributes:
            if isinstance(attr, dict):
                attr_name = attr.get("name")
                attr_type = attr.get("type", "Any")
                default_value = attr.get("default", None)
                
                if default_value is not None:
                    init_params.append(f"{attr_name}: {attr_type} = {repr(default_value)}")
                else:
                    init_params.append(f"{attr_name}: {attr_type}")
                
                init_body.append(f"        self.{attr_name} = {attr_name}")
            else:
                # Simple string attribute
                init_params.append(f"{attr}")
                init_body.append(f"        self.{attr} = {attr}")
        
        if init_params:
            class_def += ", " + ", ".join(init_params)
        class_def += "):\n"
        
        if init_body:
            class_def += "\n".join(init_body) + "\n"
        else:
            class_def += "        pass\n"
        class_def += "\n"
    
    # Generate other methods
    for method in methods:
        if isinstance(method, dict):
            method_name = method.get("name", "method")
            method_params = method.get("parameters", [])
            method_docstring = method.get("docstring", "")
            return_type = method.get("return_type", "None")
            
            class_def += f"    def {method_name}(self"
            if method_params:
                param_str = ", ".join([f"{p}: {method.get('param_types', {}).get(p, 'Any')}" for p in method_params])
                class_def += f", {param_str}"
            class_def += f") -> {return_type}:\n"
            
            if method_docstring:
                class_def += f'        """{method_docstring}"""\n'
            
            class_def += "        pass\n\n"
        else:
            # Simple method name
            class_def += f"    def {method}(self):\n"
            class_def += "        pass\n\n"
    
    # Add a simple method if no methods specified
    if not methods and include_init:
        class_def += "    def __str__(self):\n"
        class_def += f'        return f"{class_name}({{self.__dict__}})"\n'
    
    return {"generated_code": class_def.rstrip()}


def generate_function(input_data):
    """
    Generates Python function code based on specifications.
    """
    function_name = input_data.get("function_name", "my_function")
    parameters = input_data.get("parameters", [])
    return_type = input_data.get("return_type", "None")
    docstring = input_data.get("docstring", "")
    function_body = input_data.get("body", "pass")
    is_async = input_data.get("async", False)
    decorators = input_data.get("decorators", [])
    
    code = ""
    
    # Add decorators
    for decorator in decorators:
        code += f"@{decorator}\n"
    
    # Function definition
    func_keyword = "async def" if is_async else "def"
    code += f"{func_keyword} {function_name}("
    
    # Add parameters
    if parameters:
        param_strs = []
        for param in parameters:
            if isinstance(param, dict):
                param_name = param.get("name")
                param_type = param.get("type", "Any")
                default_value = param.get("default")
                
                if default_value is not None:
                    param_strs.append(f"{param_name}: {param_type} = {repr(default_value)}")
                else:
                    param_strs.append(f"{param_name}: {param_type}")
            else:
                param_strs.append(str(param))
        
        code += ", ".join(param_strs)
    
    code += f") -> {return_type}:\n"
    
    # Add docstring
    if docstring:
        code += f'    """{docstring}"""\n'
    
    # Add function body
    if function_body and function_body.strip() != "pass":
        # Indent the body properly
        body_lines = function_body.split('\n')
        indented_body = '\n'.join('    ' + line if line.strip() else line for line in body_lines)
        code += indented_body
    else:
        code += "    pass"
    
    return {"generated_code": code}


def generate_test_suite(input_data):
    """
    Generates unit test code for given functions or classes.
    """
    target_name = input_data.get("target_name", "MyClass")
    target_type = input_data.get("target_type", "function")  # "function" or "class"
    test_framework = input_data.get("framework", "unittest")  # "unittest" or "pytest"
    methods_to_test = input_data.get("methods", [])
    
    if test_framework == "pytest":
        return generate_pytest_suite(target_name, target_type, methods_to_test)
    else:
        return generate_unittest_suite(target_name, target_type, methods_to_test)


def generate_unittest_suite(target_name, target_type, methods_to_test):
    """Generate unittest-style test suite."""
    test_code = "import unittest\n"
    test_code += f"from your_module import {target_name}\n\n\n"
    
    test_class_name = f"Test{target_name}"
    test_code += f"class {test_class_name}(unittest.TestCase):\n"
    test_code += '    """Test suite for {target_name}."""\n\n'
    
    # Setup method
    if target_type == "class":
        test_code += "    def setUp(self):\n"
        test_code += f'        """Set up test fixtures before each test method."""\n'
        test_code += f"        self.{target_name.lower()} = {target_name}()\n\n"
    
    # Generate test methods
    if methods_to_test:
        for method in methods_to_test:
            method_name = method if isinstance(method, str) else method.get("name", "method")
            test_code += f"    def test_{method_name}(self):\n"
            test_code += f'        """Test {method_name} method."""\n'
            
            if target_type == "class":
                test_code += f"        result = self.{target_name.lower()}.{method_name}()\n"
            else:
                test_code += f"        result = {method_name}()\n"
            
            test_code += "        # Add your assertions here\n"
            test_code += "        self.assertIsNotNone(result)\n\n"
    else:
        # Generate basic test
        test_code += f"    def test_{target_name.lower()}_creation(self):\n"
        test_code += f'        """Test {target_name} creation."""\n'
        
        if target_type == "class":
            test_code += f"        instance = {target_name}()\n"
            test_code += "        self.assertIsInstance(instance, {target_name})\n\n"
        else:
            test_code += f"        result = {target_name}()\n"
            test_code += "        self.assertIsNotNone(result)\n\n"
    
    # Add teardown if needed
    test_code += "    def tearDown(self):\n"
    test_code += '        """Clean up after each test method."""\n'
    test_code += "        pass\n\n"
    
    # Main execution
    test_code += '\nif __name__ == "__main__":\n'
    test_code += "    unittest.main()\n"
    
    return {"generated_code": test_code}


def generate_pytest_suite(target_name, target_type, methods_to_test):
    """Generate pytest-style test suite."""
    test_code = "import pytest\n"
    test_code += f"from your_module import {target_name}\n\n\n"
    
    # Fixture for class testing
    if target_type == "class":
        test_code += "@pytest.fixture\n"
        test_code += f"def {target_name.lower()}_instance():\n"
        test_code += f'    """Create a {target_name} instance for testing."""\n'
        test_code += f"    return {target_name}()\n\n\n"
    
    # Generate test functions
    if methods_to_test:
        for method in methods_to_test:
            method_name = method if isinstance(method, str) else method.get("name", "method")
            
            if target_type == "class":
                test_code += f"def test_{method_name}({target_name.lower()}_instance):\n"
                test_code += f'    """Test {method_name} method."""\n'
                test_code += f"    result = {target_name.lower()}_instance.{method_name}()\n"
            else:
                test_code += f"def test_{method_name}():\n"
                test_code += f'    """Test {method_name} function."""\n'
                test_code += f"    result = {method_name}()\n"
            
            test_code += "    # Add your assertions here\n"
            test_code += "    assert result is not None\n\n\n"
    else:
        # Generate basic test
        if target_type == "class":
            test_code += f"def test_{target_name.lower()}_creation({target_name.lower()}_instance):\n"
            test_code += f'    """Test {target_name} creation."""\n'
            test_code += f"    assert isinstance({target_name.lower()}_instance, {target_name})\n\n"
        else:
            test_code += f"def test_{target_name.lower()}():\n"
            test_code += f'    """Test {target_name} function."""\n'
            test_code += f"    result = {target_name}()\n"
            test_code += "    assert result is not None\n\n"
    
    return {"generated_code": test_code}


def generate_api_endpoint(input_data):
    """
    Generates FastAPI or Flask endpoint code.
    """
    framework = input_data.get("framework", "fastapi")
    endpoint_name = input_data.get("endpoint_name", "my_endpoint")
    http_method = input_data.get("method", "GET").upper()
    path = input_data.get("path", f"/{endpoint_name}")
    request_model = input_data.get("request_model", "")
    response_model = input_data.get("response_model", "")
    description = input_data.get("description", "")
    
    if framework.lower() == "fastapi":
        return generate_fastapi_endpoint(endpoint_name, http_method, path, request_model, response_model, description)
    else:
        return generate_flask_endpoint(endpoint_name, http_method, path, description)


def generate_fastapi_endpoint(endpoint_name, method, path, request_model, response_model, description):
    """Generate FastAPI endpoint."""
    code = "from fastapi import APIRouter, HTTPException\n"
    code += "from pydantic import BaseModel\n"
    code += "from typing import Optional\n\n"
    
    # Add models if specified
    if request_model:
        code += f"class {request_model}(BaseModel):\n"
        code += "    # Add your request fields here\n"
        code += "    pass\n\n"
    
    if response_model:
        code += f"class {response_model}(BaseModel):\n"
        code += "    # Add your response fields here\n"
        code += "    pass\n\n"
    
    code += "router = APIRouter()\n\n"
    
    # Generate endpoint
    decorator_args = [f'"{path}"']
    if response_model:
        decorator_args.append(f"response_model={response_model}")
    
    code += f'@router.{method.lower()}({", ".join(decorator_args)})\n'
    
    # Function signature
    params = []
    if request_model and method in ["POST", "PUT", "PATCH"]:
        params.append(f"request: {request_model}")
    
    code += f"async def {endpoint_name}({', '.join(params)}):\n"
    
    if description:
        code += f'    """{description}"""\n'
    
    code += "    try:\n"
    code += "        # Add your endpoint logic here\n"
    
    if method == "GET":
        code += '        return {"message": "Success"}\n'
    elif method in ["POST", "PUT", "PATCH"]:
        if request_model:
            code += "        # Process the request data\n"
            code += "        processed_data = request.dict()\n"
            code += "        return processed_data\n"
        else:
            code += '        return {"message": "Success"}\n'
    elif method == "DELETE":
        code += '        return {"message": "Deleted successfully"}\n'
    
    code += "    except Exception as e:\n"
    code += '        raise HTTPException(status_code=500, detail=str(e))\n'
    
    return {"generated_code": code}


def generate_flask_endpoint(endpoint_name, method, path, description):
    """Generate Flask endpoint."""
    code = "from flask import Flask, request, jsonify\n\n"
    code += "app = Flask(__name__)\n\n"
    
    methods_list = f"['{method}']" if method != "GET" else "['GET']"
    code += f"@app.route('{path}', methods={methods_list})\n"
    code += f"def {endpoint_name}():\n"
    
    if description:
        code += f'    """{description}"""\n'
    
    code += "    try:\n"
    
    if method in ["POST", "PUT", "PATCH"]:
        code += "        data = request.get_json()\n"
        code += "        # Process the request data\n"
        code += "        return jsonify(data)\n"
    elif method == "DELETE":
        code += '        return jsonify({"message": "Deleted successfully"})\n'
    else:
        code += '        return jsonify({"message": "Success"})\n'
    
    code += "    except Exception as e:\n"
    code += "        return jsonify({'error': str(e)}), 500\n"
    
    return {"generated_code": code}


# Build the generation tools using GenToolBuilder for LLM-powered generation
class_generator_tool = GenToolBuilder(
    name="ClassGenerator",
    input_schema={
        "class_name": str, 
        "attributes": list, 
        "methods": list, 
        "parent_class": str,
        "docstring": str,
        "include_init": bool
    },
    output_schema={"generated_code": str},
    system_prompt="""You are a Python class code generator. Generate clean, well-structured Python classes based on the provided specifications. Follow Python best practices and PEP 8 style guidelines. Include proper type hints, docstrings, and error handling where appropriate.""",
    user_prompt_template="""Generate a Python class with the following specifications:
Class name: {class_name}
Attributes: {attributes}
Methods: {methods}
Parent class: {parent_class}
Docstring: {docstring}
Include __init__: {include_init}

Provide the complete class code with proper indentation, type hints, and docstrings.""",
    description="Generates Python class code based on specifications including attributes, methods, and inheritance"
).build()

function_generator_tool = GenToolBuilder(
    name="FunctionGenerator", 
    input_schema={
        "function_name": str,
        "parameters": list,
        "return_type": str,
        "docstring": str,
        "body": str,
        "async": bool,
        "decorators": list
    },
    output_schema={"generated_code": str},
    system_prompt="""You are a Python function code generator. Generate clean, well-structured Python functions based on the provided specifications. Follow Python best practices and include proper type hints, docstrings, and error handling.""",
    user_prompt_template="""Generate a Python function with the following specifications:
Function name: {function_name}
Parameters: {parameters}
Return type: {return_type}
Docstring: {docstring}
Function body: {body}
Async: {async}
Decorators: {decorators}

Provide the complete function code with proper type hints and documentation.""",
    description="Generates Python function code with parameters, type hints, docstrings, and decorators"
).build()

test_generator_tool = GenToolBuilder(
    name="TestGenerator",
    input_schema={
        "target_name": str,
        "target_type": str,
        "framework": str,
        "methods": list
    },
    output_schema={"generated_code": str},
    system_prompt="""You are a test code generator. Generate comprehensive unit tests for Python code using either unittest or pytest frameworks. Create thorough test cases with proper setup, assertions, and edge case handling.""",
    user_prompt_template="""Generate unit tests for the following:
Target: {target_name}
Type: {target_type}
Framework: {framework}
Methods to test: {methods}

Create comprehensive test cases with proper setup, teardown, and meaningful assertions. Include edge cases and error conditions.""",
    description="Generates comprehensive unit test suites using unittest or pytest frameworks"
).build()

api_endpoint_generator_tool = GenToolBuilder(
    name="APIEndpointGenerator",
    input_schema={
        "framework": str,
        "endpoint_name": str,
        "method": str,
        "path": str,
        "request_model": str,
        "response_model": str,
        "description": str
    },
    output_schema={"generated_code": str},
    system_prompt="""You are an API endpoint code generator. Generate clean, production-ready API endpoints for FastAPI or Flask frameworks. Include proper error handling, input validation, and documentation.""",
    user_prompt_template="""Generate an API endpoint with the following specifications:
Framework: {framework}
Endpoint name: {endpoint_name}
HTTP method: {method}
Path: {path}
Request model: {request_model}
Response model: {response_model}
Description: {description}

Provide complete endpoint code with proper error handling, validation, and documentation.""",
    description="Generates API endpoint code for FastAPI or Flask frameworks with proper error handling"
).build()