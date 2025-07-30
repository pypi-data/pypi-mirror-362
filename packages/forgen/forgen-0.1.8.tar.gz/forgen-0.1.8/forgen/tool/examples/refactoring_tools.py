import ast
import re
from typing import Dict, List, Any, Tuple
from collections import defaultdict

from forgen.tool.builder import ToolBuilder, GenToolBuilder


def extract_method(input_data):
    """
    Extracts a method from code based on line range or code selection.
    """
    code = input_data.get("code", "")
    start_line = input_data.get("start_line", 1)
    end_line = input_data.get("end_line", 1)
    method_name = input_data.get("method_name", "extracted_method")
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    lines = code.split('\n')
    
    if start_line < 1 or end_line > len(lines) or start_line > end_line:
        return {"error": "Invalid line range"}
    
    # Extract the selected lines (1-indexed)
    selected_lines = lines[start_line-1:end_line]
    
    # Determine indentation
    min_indent = float('inf')
    for line in selected_lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)
    
    if min_indent == float('inf'):
        min_indent = 0
    
    # Remove common indentation
    extracted_code = []
    for line in selected_lines:
        if line.strip():
            extracted_code.append(line[min_indent:])
        else:
            extracted_code.append("")
    
    # Analyze extracted code for variables
    extracted_text = '\n'.join(extracted_code)
    
    # Simple variable analysis (could be improved with AST)
    assigned_vars = set()
    used_vars = set()
    
    for line in extracted_code:
        # Find assignments (simple pattern)
        if '=' in line and not ('==' in line or '!=' in line or '<=' in line or '>=' in line):
            assignment_match = re.search(r'(\w+)\s*=', line)
            if assignment_match:
                assigned_vars.add(assignment_match.group(1))
        
        # Find variable usage (simple pattern)
        for match in re.finditer(r'\b([a-zA-Z_]\w*)\b', line):
            var_name = match.group(1)
            if not var_name.startswith('_') and var_name not in ['def', 'class', 'if', 'else', 'for', 'while', 'try', 'except', 'import', 'from', 'return']:
                used_vars.add(var_name)
    
    # Determine parameters (used but not assigned locally)
    parameters = used_vars - assigned_vars
    
    # Generate the new method
    param_list = ", ".join(sorted(parameters)) if parameters else ""
    if param_list:
        param_list = ", " + param_list
    
    new_method = f"def {method_name}(self{param_list}):\n"
    for line in extracted_code:
        if line.strip():
            new_method += f"    {line}\n"
        else:
            new_method += "\n"
    
    # Generate the method call
    param_args = ", ".join(sorted(parameters)) if parameters else ""
    method_call = f"self.{method_name}({param_args})"
    
    # Replace extracted code with method call
    new_code_lines = lines[:start_line-1] + [' ' * min_indent + method_call] + lines[end_line:]
    new_code = '\n'.join(new_code_lines)
    
    return {
        "extracted_method": new_method,
        "modified_code": new_code,
        "method_call": method_call,
        "parameters": list(parameters)
    }


def rename_variable(input_data):
    """
    Renames a variable throughout the code.
    """
    code = input_data.get("code", "")
    old_name = input_data.get("old_name", "")
    new_name = input_data.get("new_name", "")
    scope = input_data.get("scope", "global")  # "global", "function", "class"
    
    if not code.strip() or not old_name or not new_name:
        return {"error": "Missing required parameters"}
    
    if old_name == new_name:
        return {"error": "Old name and new name are the same"}
    
    try:
        tree = ast.parse(code)
        
        # Simple approach: replace all occurrences
        # For more sophisticated renaming, would need scope analysis
        if scope == "global":
            # Replace all occurrences using word boundaries
            pattern = r'\b' + re.escape(old_name) + r'\b'
            new_code = re.sub(pattern, new_name, code)
            
            # Count replacements
            replacements = len(re.findall(pattern, code))
            
            return {
                "modified_code": new_code,
                "replacements_made": replacements,
                "success": replacements > 0
            }
        else:
            # More complex scope-aware renaming would go here
            return {"error": f"Scope '{scope}' not yet implemented"}
            
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {str(e)}"}
    except Exception as e:
        return {"error": f"Renaming failed: {str(e)}"}


def optimize_imports(input_data):
    """
    Optimizes import statements by removing unused imports and organizing them.
    """
    code = input_data.get("code", "")
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        tree = ast.parse(code)
        
        # Find all imports
        imports = []
        import_lines = {}
        used_names = set()
        
        # Collect import statements and their line numbers
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.asname if alias.asname else alias.name
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "name": import_name,
                        "line": node.lineno
                    })
                    import_lines[node.lineno] = f"import {alias.name}"
                    if alias.asname:
                        import_lines[node.lineno] += f" as {alias.asname}"
                        
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    import_name = alias.asname if alias.asname else alias.name
                    imports.append({
                        "type": "from_import",
                        "module": module,
                        "name": import_name,
                        "imported": alias.name,
                        "line": node.lineno
                    })
                    if node.lineno not in import_lines:
                        import_lines[node.lineno] = f"from {module} import "
                    
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
        
        # Determine which imports are used
        used_imports = []
        unused_imports = []
        
        for imp in imports:
            if imp["name"] in used_names:
                used_imports.append(imp)
            else:
                unused_imports.append(imp)
        
        # Organize imports
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        stdlib_modules = {
            'os', 'sys', 'json', 'datetime', 'time', 'random', 'math', 're', 
            'collections', 'itertools', 'functools', 'typing', 'pathlib',
            'urllib', 'http', 'email', 'html', 'xml', 'csv', 'sqlite3',
            'threading', 'multiprocessing', 'subprocess', 'shutil', 'glob',
            'pickle', 'copy', 'base64', 'hashlib', 'hmac', 'secrets', 'ast'
        }
        
        for imp in used_imports:
            module_root = imp["module"].split('.')[0]
            if module_root in stdlib_modules:
                stdlib_imports.append(imp)
            elif imp["module"].startswith('.') or not imp["module"]:
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        # Generate organized import block
        organized_imports = []
        
        # Standard library imports
        if stdlib_imports:
            for imp in sorted(stdlib_imports, key=lambda x: x["module"]):
                if imp["type"] == "import":
                    organized_imports.append(f"import {imp['module']}")
                else:
                    organized_imports.append(f"from {imp['module']} import {imp['imported']}")
            organized_imports.append("")
        
        # Third-party imports
        if third_party_imports:
            for imp in sorted(third_party_imports, key=lambda x: x["module"]):
                if imp["type"] == "import":
                    organized_imports.append(f"import {imp['module']}")
                else:
                    organized_imports.append(f"from {imp['module']} import {imp['imported']}")
            organized_imports.append("")
        
        # Local imports
        if local_imports:
            for imp in sorted(local_imports, key=lambda x: x["module"]):
                if imp["type"] == "import":
                    organized_imports.append(f"import {imp['module']}")
                else:
                    organized_imports.append(f"from {imp['module']} import {imp['imported']}")
            organized_imports.append("")
        
        # Remove original import lines and add optimized imports
        lines = code.split('\n')
        non_import_lines = []
        
        for i, line in enumerate(lines, 1):
            if i not in import_lines and not line.strip().startswith(('import ', 'from ')):
                non_import_lines.append(line)
        
        # Combine organized imports with non-import code
        optimized_code = '\n'.join(organized_imports) + '\n'.join(non_import_lines)
        
        return {
            "optimized_code": optimized_code,
            "unused_imports": [f"{imp['module']}.{imp['name']}" for imp in unused_imports],
            "organized_imports": organized_imports[:-1] if organized_imports else [],
            "imports_removed": len(unused_imports)
        }
        
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {str(e)}"}
    except Exception as e:
        return {"error": f"Import optimization failed: {str(e)}"}


def inline_variable(input_data):
    """
    Inlines a variable by replacing all usages with its assigned value.
    """
    code = input_data.get("code", "")
    variable_name = input_data.get("variable_name", "")
    
    if not code.strip() or not variable_name:
        return {"error": "Missing required parameters"}
    
    try:
        lines = code.split('\n')
        assignment_line = None
        assignment_value = None
        
        # Find the assignment
        for i, line in enumerate(lines):
            # Simple pattern matching for assignment
            pattern = rf'\s*{re.escape(variable_name)}\s*=\s*(.+)'
            match = re.match(pattern, line.strip())
            if match:
                assignment_line = i
                assignment_value = match.group(1)
                break
        
        if assignment_line is None:
            return {"error": f"Variable '{variable_name}' assignment not found"}
        
        # Replace usages with the value
        modified_lines = []
        replacements = 0
        
        for i, line in enumerate(lines):
            if i == assignment_line:
                # Skip the assignment line
                continue
            
            # Replace variable usage with value
            pattern = r'\b' + re.escape(variable_name) + r'\b'
            new_line, count = re.subn(pattern, assignment_value, line)
            replacements += count
            modified_lines.append(new_line)
        
        modified_code = '\n'.join(modified_lines)
        
        return {
            "modified_code": modified_code,
            "inlined_value": assignment_value,
            "replacements_made": replacements,
            "success": replacements > 0
        }
        
    except Exception as e:
        return {"error": f"Inlining failed: {str(e)}"}


def convert_to_list_comprehension(input_data):
    """
    Converts simple for loops to list comprehensions where applicable.
    """
    code = input_data.get("code", "")
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        # Simple pattern matching for basic for loop to list comprehension
        # Pattern: for item in iterable: result.append(expression)
        
        lines = code.split('\n')
        modified_lines = []
        i = 0
        conversions_made = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for for loop pattern
            for_match = re.match(r'(\s*)for\s+(\w+)\s+in\s+(.+):', line)
            if for_match and i + 1 < len(lines):
                indent = for_match.group(1)
                var_name = for_match.group(2)
                iterable = for_match.group(3)
                next_line = lines[i + 1].strip()
                
                # Check if next line is an append operation
                append_match = re.match(rf'(\w+)\.append\((.+)\)', next_line)
                if append_match:
                    list_name = append_match.group(1)
                    expression = append_match.group(2)
                    
                    # Convert to list comprehension
                    comprehension = f"{indent}{list_name} = [{expression} for {var_name} in {iterable}]"
                    modified_lines.append(comprehension)
                    conversions_made += 1
                    i += 2  # Skip both lines
                    continue
            
            modified_lines.append(lines[i])
            i += 1
        
        modified_code = '\n'.join(modified_lines)
        
        return {
            "modified_code": modified_code,
            "conversions_made": conversions_made,
            "success": conversions_made > 0
        }
        
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}


# Build the refactoring tools
extract_method_tool = ToolBuilder(
    name="ExtractMethod",
    tool_fn=extract_method,
    input_schema={"code": str, "start_line": int, "end_line": int, "method_name": str},
    output_schema={"extracted_method": str, "modified_code": str, "method_call": str, "parameters": list},
    description="Extracts a method from code by analyzing line ranges and automatically determining parameters"
).build()

rename_variable_tool = ToolBuilder(
    name="RenameVariable",
    tool_fn=rename_variable,
    input_schema={"code": str, "old_name": str, "new_name": str, "scope": str},
    output_schema={"modified_code": str, "replacements_made": int, "success": bool},
    description="Renames variables throughout code with scope awareness and conflict detection"
).build()

optimize_imports_tool = ToolBuilder(
    name="OptimizeImports",
    tool_fn=optimize_imports,
    input_schema={"code": str},
    output_schema={"optimized_code": str, "unused_imports": list, "organized_imports": list, "imports_removed": int},
    description="Organizes and optimizes import statements by removing unused imports and following PEP 8 organization"
).build()

inline_variable_tool = ToolBuilder(
    name="InlineVariable",
    tool_fn=inline_variable,
    input_schema={"code": str, "variable_name": str},
    output_schema={"modified_code": str, "inlined_value": str, "replacements_made": int, "success": bool},
    description="Inlines a variable by replacing all usages with its assigned value and removing the assignment"
).build()

convert_to_comprehension_tool = ToolBuilder(
    name="ConvertToComprehension",
    tool_fn=convert_to_list_comprehension,
    input_schema={"code": str},
    output_schema={"modified_code": str, "conversions_made": int, "success": bool},
    description="Converts simple for loops with append operations to more Pythonic list comprehensions"
).build()

# Advanced refactoring tool using LLM
advanced_refactoring_tool = GenToolBuilder(
    name="AdvancedRefactoring",
    input_schema={
        "code": str,
        "refactoring_type": str,
        "target_element": str,
        "parameters": dict
    },
    output_schema={"refactored_code": str, "changes_made": list, "explanation": str},
    system_prompt="""You are an expert code refactoring assistant. You can perform various refactoring operations including:
- Extract class
- Move method
- Replace conditional with polymorphism
- Replace magic numbers with constants
- Split large functions
- Improve naming conventions
- Apply design patterns

Always ensure the refactored code maintains the same functionality while improving readability, maintainability, and following best practices.""",
    user_prompt_template="""Perform the following refactoring:
Code to refactor:
{code}

Refactoring type: {refactoring_type}
Target element: {target_element}
Additional parameters: {parameters}

Provide the refactored code along with an explanation of the changes made and why they improve the code quality.""",
    description="Advanced refactoring tool powered by LLM for complex refactoring operations and code quality improvements"
).build()