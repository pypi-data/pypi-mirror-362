import ast
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from forgen.tool.builder import ToolBuilder, GenToolBuilder


def generate_docstring(input_data):
    """
    Generates docstrings for Python functions and classes.
    """
    code = input_data.get("code", "")
    style = input_data.get("style", "google")  # google, numpy, sphinx
    include_types = input_data.get("include_types", True)
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        tree = ast.parse(code)
        
        # Find function or class definitions
        definitions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = generate_function_docstring(node, style, include_types)
                definitions.append({
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": docstring,
                    "has_existing_docstring": bool(ast.get_docstring(node))
                })
            elif isinstance(node, ast.ClassDef):
                docstring = generate_class_docstring(node, style)
                definitions.append({
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": docstring,
                    "has_existing_docstring": bool(ast.get_docstring(node))
                })
        
        # Insert docstrings into code
        modified_code = insert_docstrings(code, definitions)
        
        return {
            "modified_code": modified_code,
            "generated_docstrings": len(definitions),
            "definitions": definitions
        }
        
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {str(e)}"}
    except Exception as e:
        return {"error": f"Docstring generation failed: {str(e)}"}


def generate_function_docstring(func_node, style, include_types):
    """Generate docstring for a function node."""
    
    # Analyze function signature
    args = []
    for arg in func_node.args.args:
        arg_info = {"name": arg.arg}
        if include_types and arg.annotation:
            arg_info["type"] = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else "Any"
        args.append(arg_info)
    
    # Get return type
    return_type = None
    if include_types and func_node.returns:
        return_type = ast.unparse(func_node.returns) if hasattr(ast, 'unparse') else "Any"
    
    # Generate docstring based on style
    if style == "google":
        return generate_google_function_docstring(func_node.name, args, return_type)
    elif style == "numpy":
        return generate_numpy_function_docstring(func_node.name, args, return_type)
    elif style == "sphinx":
        return generate_sphinx_function_docstring(func_node.name, args, return_type)
    else:
        return generate_google_function_docstring(func_node.name, args, return_type)


def generate_google_function_docstring(func_name, args, return_type):
    """Generate Google-style docstring."""
    lines = [f'"""Brief description of {func_name}.']
    
    if len(lines[0]) > 80:
        lines = ['"""Brief description.']
    
    lines.append('')
    lines.append('Longer description if needed.')
    lines.append('')
    
    if args:
        lines.append('Args:')
        for arg in args:
            arg_type = f" ({arg.get('type', 'Any')})" if 'type' in arg else ""
            lines.append(f"    {arg['name']}{arg_type}: Description of {arg['name']}.")
        lines.append('')
    
    if return_type and return_type != "None":
        lines.append('Returns:')
        lines.append(f'    {return_type}: Description of return value.')
        lines.append('')
    
    lines.append('Raises:')
    lines.append('    ValueError: If invalid input is provided.')
    lines.append('"""')
    
    return '\n'.join(lines)


def generate_numpy_function_docstring(func_name, args, return_type):
    """Generate NumPy-style docstring."""
    lines = [f'"""Brief description of {func_name}.']
    lines.append('')
    lines.append('Longer description if needed.')
    lines.append('')
    
    if args:
        lines.append('Parameters')
        lines.append('----------')
        for arg in args:
            arg_type = arg.get('type', 'Any')
            lines.append(f"{arg['name']} : {arg_type}")
            lines.append(f"    Description of {arg['name']}.")
        lines.append('')
    
    if return_type and return_type != "None":
        lines.append('Returns')
        lines.append('-------')
        lines.append(f'{return_type}')
        lines.append('    Description of return value.')
        lines.append('')
    
    lines.append('Raises')
    lines.append('------')
    lines.append('ValueError')
    lines.append('    If invalid input is provided.')
    lines.append('"""')
    
    return '\n'.join(lines)


def generate_sphinx_function_docstring(func_name, args, return_type):
    """Generate Sphinx-style docstring."""
    lines = [f'"""Brief description of {func_name}.']
    lines.append('')
    lines.append('Longer description if needed.')
    lines.append('')
    
    for arg in args:
        arg_type = f" ({arg.get('type', 'Any')})" if 'type' in arg else ""
        lines.append(f":param {arg['name']}{arg_type}: Description of {arg['name']}.")
    
    if return_type and return_type != "None":
        lines.append(f':returns: Description of return value.')
        lines.append(f':rtype: {return_type}')
    
    lines.append(':raises ValueError: If invalid input is provided.')
    lines.append('"""')
    
    return '\n'.join(lines)


def generate_class_docstring(class_node, style):
    """Generate docstring for a class node."""
    
    # Find methods
    methods = [node.name for node in class_node.body if isinstance(node, ast.FunctionDef)]
    
    if style == "google":
        lines = [f'"""Brief description of {class_node.name} class.']
        lines.append('')
        lines.append('Longer description of the class purpose and usage.')
        lines.append('')
        lines.append('Attributes:')
        lines.append('    attribute_name (type): Description of attribute.')
        lines.append('')
        if methods:
            lines.append('Methods:')
            for method in methods[:3]:  # Show first 3 methods
                lines.append(f'    {method}(): Description of {method}.')
        lines.append('"""')
    else:
        # Use Google style as default
        return generate_class_docstring(class_node, "google")
    
    return '\n'.join(lines)


def insert_docstrings(code, definitions):
    """Insert generated docstrings into code."""
    lines = code.split('\n')
    offset = 0
    
    for defn in definitions:
        if defn["has_existing_docstring"]:
            continue  # Skip if already has docstring
        
        # Find the line after the definition
        target_line = defn["line"] + offset
        
        # Insert docstring with proper indentation
        if target_line < len(lines):
            # Find indentation of the definition line
            def_line = lines[target_line - 1]
            indent = len(def_line) - len(def_line.lstrip())
            
            # Add docstring with proper indentation
            docstring_lines = defn["docstring"].split('\n')
            indented_docstring = []
            for i, doc_line in enumerate(docstring_lines):
                if i == 0:
                    indented_docstring.append(' ' * (indent + 4) + doc_line)
                else:
                    indented_docstring.append(' ' * (indent + 4) + doc_line if doc_line.strip() else doc_line)
            
            # Insert after the definition line
            for i, doc_line in enumerate(indented_docstring):
                lines.insert(target_line + i, doc_line)
            
            offset += len(indented_docstring)
    
    return '\n'.join(lines)


def extract_api_info(input_data):
    """
    Extracts API information from Python code for documentation.
    """
    code = input_data.get("code", "")
    include_private = input_data.get("include_private", False)
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        tree = ast.parse(code)
        
        api_info = {
            "modules": [],
            "classes": [],
            "functions": [],
            "constants": [],
            "imports": []
        }
        
        # Extract top-level elements
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if not include_private and node.name.startswith('_'):
                    continue
                    
                func_info = extract_function_info(node)
                api_info["functions"].append(func_info)
                
            elif isinstance(node, ast.ClassDef):
                if not include_private and node.name.startswith('_'):
                    continue
                    
                class_info = extract_class_info(node, include_private)
                api_info["classes"].append(class_info)
                
            elif isinstance(node, ast.Assign):
                # Extract constants (uppercase variables)
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        api_info["constants"].append({
                            "name": target.id,
                            "line": node.lineno,
                            "value": ast.unparse(node.value) if hasattr(ast, 'unparse') else "..."
                        })
                        
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = extract_import_info(node)
                api_info["imports"].append(import_info)
        
        return api_info
        
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {str(e)}"}
    except Exception as e:
        return {"error": f"API extraction failed: {str(e)}"}


def extract_function_info(func_node):
    """Extract information about a function."""
    return {
        "name": func_node.name,
        "line": func_node.lineno,
        "docstring": ast.get_docstring(func_node),
        "parameters": [arg.arg for arg in func_node.args.args],
        "is_async": isinstance(func_node, ast.AsyncFunctionDef),
        "decorators": [ast.unparse(dec) if hasattr(ast, 'unparse') else "..." for dec in func_node.decorator_list]
    }


def extract_class_info(class_node, include_private):
    """Extract information about a class."""
    methods = []
    attributes = []
    
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            if not include_private and node.name.startswith('_') and node.name != '__init__':
                continue
            methods.append(extract_function_info(node))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    attributes.append(target.id)
    
    return {
        "name": class_node.name,
        "line": class_node.lineno,
        "docstring": ast.get_docstring(class_node),
        "methods": methods,
        "attributes": attributes,
        "bases": [ast.unparse(base) if hasattr(ast, 'unparse') else "..." for base in class_node.bases]
    }


def extract_import_info(import_node):
    """Extract information about imports."""
    if isinstance(import_node, ast.Import):
        return {
            "type": "import",
            "modules": [alias.name for alias in import_node.names],
            "line": import_node.lineno
        }
    else:  # ImportFrom
        return {
            "type": "from_import",
            "module": import_node.module,
            "names": [alias.name for alias in import_node.names],
            "line": import_node.lineno
        }


def generate_markdown_docs(input_data):
    """
    Generates markdown documentation from API information.
    """
    api_info = input_data.get("api_info", {})
    title = input_data.get("title", "API Documentation")
    
    if not api_info:
        return {"error": "No API information provided"}
    
    markdown = f"# {title}\n\n"
    markdown += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Table of Contents
    markdown += "## Table of Contents\n\n"
    if api_info.get("classes"):
        markdown += "- [Classes](#classes)\n"
    if api_info.get("functions"):
        markdown += "- [Functions](#functions)\n"
    if api_info.get("constants"):
        markdown += "- [Constants](#constants)\n"
    markdown += "\n"
    
    # Classes
    if api_info.get("classes"):
        markdown += "## Classes\n\n"
        for cls in api_info["classes"]:
            markdown += f"### {cls['name']}\n\n"
            if cls.get("docstring"):
                markdown += f"{cls['docstring']}\n\n"
            
            if cls.get("bases"):
                markdown += f"**Inheritance:** {', '.join(cls['bases'])}\n\n"
            
            if cls.get("methods"):
                markdown += "**Methods:**\n\n"
                for method in cls["methods"]:
                    markdown += f"- `{method['name']}({', '.join(method['parameters'])})`"
                    if method.get("docstring"):
                        # Get first line of docstring
                        first_line = method["docstring"].split('\n')[0]
                        markdown += f": {first_line}"
                    markdown += "\n"
                markdown += "\n"
    
    # Functions
    if api_info.get("functions"):
        markdown += "## Functions\n\n"
        for func in api_info["functions"]:
            markdown += f"### {func['name']}\n\n"
            markdown += f"```python\n{func['name']}({', '.join(func['parameters'])})\n```\n\n"
            
            if func.get("docstring"):
                markdown += f"{func['docstring']}\n\n"
            
            if func.get("decorators"):
                markdown += f"**Decorators:** {', '.join(func['decorators'])}\n\n"
    
    # Constants
    if api_info.get("constants"):
        markdown += "## Constants\n\n"
        for const in api_info["constants"]:
            markdown += f"- `{const['name']}`: {const.get('value', 'Value not available')}\n"
        markdown += "\n"
    
    return {"markdown_docs": markdown}


# Build the documentation tools
docstring_generator_tool = GenToolBuilder(
    name="DocstringGenerator",
    input_schema={
        "code": str,
        "style": str,
        "include_types": bool
    },
    output_schema={"modified_code": str, "generated_docstrings": int, "definitions": list},
    system_prompt="""You are a documentation expert. Generate high-quality docstrings for Python functions and classes following the specified style guide (Google, NumPy, or Sphinx). Include comprehensive parameter descriptions, return value documentation, and exception information.""",
    user_prompt_template="""Generate docstrings for the following Python code:

Code:
{code}

Style: {style}
Include type hints: {include_types}

Add appropriate docstrings following the {style} style guide. Include parameter descriptions, return values, and potential exceptions.""",
    description="Generates comprehensive docstrings for Python functions and classes following various style guides"
).build()

api_extractor_tool = ToolBuilder(
    name="APIExtractor",
    tool_fn=extract_api_info,
    input_schema={"code": str, "include_private": bool},
    output_schema={"modules": list, "classes": list, "functions": list, "constants": list, "imports": list},
    description="Extracts comprehensive API information from Python code including classes, functions, and constants"
).build()

markdown_docs_generator_tool = ToolBuilder(
    name="MarkdownDocsGenerator",
    tool_fn=generate_markdown_docs,
    input_schema={"api_info": dict, "title": str},
    output_schema={"markdown_docs": str},
    description="Generates well-formatted markdown documentation from extracted API information"
).build()

comprehensive_docs_tool = GenToolBuilder(
    name="ComprehensiveDocsGenerator",
    input_schema={
        "code": str,
        "project_name": str,
        "description": str,
        "include_examples": bool
    },
    output_schema={"documentation": str, "sections": list, "examples": list},
    system_prompt="""You are a technical documentation specialist. Create comprehensive, user-friendly documentation for Python code including:
- Clear overview and purpose
- Installation/usage instructions
- API reference with examples
- Code samples and tutorials
- Best practices and common patterns""",
    user_prompt_template="""Create comprehensive documentation for this Python project:

Project: {project_name}
Description: {description}
Include examples: {include_examples}

Code to document:
{code}

Generate complete documentation including overview, API reference, usage examples, and best practices.""",
    description="Creates comprehensive project documentation with examples, tutorials, and best practices"
).build()