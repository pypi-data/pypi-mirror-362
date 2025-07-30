import ast
import re
import json
from typing import Dict, List, Any
from collections import defaultdict

from forgen.tool.builder import ToolBuilder


def syntax_check(input_data):
    """
    Validates Python code syntax and returns detailed analysis.
    """
    code = input_data.get("code", "")
    language = input_data.get("language", "python")
    
    if language.lower() != "python":
        return {
            "valid": False,
            "errors": [f"Language '{language}' not supported. Only Python is currently supported."],
            "warnings": [],
            "suggestions": []
        }
    
    if not code.strip():
        return {
            "valid": False,
            "errors": ["Empty code provided"],
            "warnings": [],
            "suggestions": ["Provide valid Python code for analysis"]
        }
    
    errors = []
    warnings = []
    suggestions = []
    
    try:
        tree = ast.parse(code)
        
        # Basic syntax checks
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in ['eval', 'exec']:
                warnings.append(f"Line {node.lineno}: Use of '{node.id}' detected - potential security risk")
            
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == '*':
                        warnings.append(f"Line {node.lineno}: Wildcard import '*' not recommended")
        
        # Check for common patterns
        if 'print(' in code and 'def ' in code:
            suggestions.append("Consider using logging instead of print statements in functions")
        
        return {
            "valid": True,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "ast_nodes": len(list(ast.walk(tree)))
        }
        
    except SyntaxError as e:
        errors.append(f"Syntax Error at line {e.lineno}: {e.msg}")
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "suggestions": ["Fix syntax errors before proceeding"]
        }
    except Exception as e:
        errors.append(f"Parsing error: {str(e)}")
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "suggestions": []
        }


def complexity_analysis(input_data):
    """
    Analyzes code complexity using various metrics.
    """
    code = input_data.get("code", "")
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        tree = ast.parse(code)
        
        stats = {
            "lines_of_code": len([line for line in code.split('\n') if line.strip()]),
            "total_lines": len(code.split('\n')),
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "complexity_score": 0,
            "function_details": [],
            "class_details": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stats["functions"] += 1
                func_complexity = calculate_cyclomatic_complexity(node)
                stats["function_details"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "complexity": func_complexity,
                    "args_count": len(node.args.args)
                })
                stats["complexity_score"] += func_complexity
                
            elif isinstance(node, ast.ClassDef):
                stats["classes"] += 1
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                stats["class_details"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods_count": len(methods),
                    "methods": [m.name for m in methods]
                })
                
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                stats["imports"] += 1
        
        # Calculate maintainability index approximation
        if stats["lines_of_code"] > 0:
            maintainability = max(0, 171 - 5.2 * (stats["complexity_score"] / max(1, stats["functions"])) 
                                 - 0.23 * stats["lines_of_code"] - 16.2)
            stats["maintainability_index"] = round(maintainability, 2)
        else:
            stats["maintainability_index"] = 100
        
        return stats
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


def calculate_cyclomatic_complexity(func_node):
    """Calculate cyclomatic complexity for a function."""
    complexity = 1  # Base complexity
    
    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            complexity += 1
    
    return complexity


def dependency_mapper(input_data):
    """
    Maps dependencies and imports in Python code.
    """
    code = input_data.get("code", "")
    include_stdlib = input_data.get("include_stdlib", True)
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    try:
        tree = ast.parse(code)
        
        dependencies = {
            "imports": [],
            "from_imports": [],
            "modules_used": set(),
            "potential_external": [],
            "stdlib_modules": [],
            "dependency_graph": defaultdict(list)
        }
        
        stdlib_modules = {
            'os', 'sys', 'json', 'datetime', 'time', 'random', 'math', 're', 
            'collections', 'itertools', 'functools', 'typing', 'pathlib',
            'urllib', 'http', 'email', 'html', 'xml', 'csv', 'sqlite3',
            'threading', 'multiprocessing', 'subprocess', 'shutil', 'glob',
            'pickle', 'copy', 'base64', 'hashlib', 'hmac', 'secrets'
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    dependencies["imports"].append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    })
                    dependencies["modules_used"].add(module_name)
                    
                    if module_name in stdlib_modules:
                        if include_stdlib:
                            dependencies["stdlib_modules"].append(module_name)
                    else:
                        dependencies["potential_external"].append(module_name)
                        
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split('.')[0]
                    dependencies["from_imports"].append({
                        "module": node.module,
                        "names": [alias.name for alias in node.names],
                        "line": node.lineno
                    })
                    dependencies["modules_used"].add(module_name)
                    
                    if module_name in stdlib_modules:
                        if include_stdlib:
                            dependencies["stdlib_modules"].append(module_name)
                    else:
                        dependencies["potential_external"].append(module_name)
        
        # Convert set to list for JSON serialization
        dependencies["modules_used"] = list(dependencies["modules_used"])
        dependencies["potential_external"] = list(set(dependencies["potential_external"]))
        dependencies["stdlib_modules"] = list(set(dependencies["stdlib_modules"]))
        
        return dependencies
        
    except Exception as e:
        return {"error": f"Dependency analysis failed: {str(e)}"}


def security_scanner(input_data):
    """
    Scans Python code for potential security issues.
    """
    code = input_data.get("code", "")
    
    if not code.strip():
        return {"error": "Empty code provided"}
    
    security_issues = {
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
        "recommendations": []
    }
    
    lines = code.split('\n')
    
    # High-risk patterns
    high_risk_patterns = [
        (r'eval\s*\(', "Use of eval() - arbitrary code execution risk"),
        (r'exec\s*\(', "Use of exec() - arbitrary code execution risk"),
        (r'subprocess\.call\s*\(.*shell\s*=\s*True', "subprocess with shell=True - command injection risk"),
        (r'os\.system\s*\(', "Use of os.system() - command injection risk"),
        (r'pickle\.loads?\s*\(', "Use of pickle - arbitrary code execution when loading untrusted data")
    ]
    
    # Medium-risk patterns
    medium_risk_patterns = [
        (r'open\s*\([^)]*[\'"]w[\'"]', "File writing detected - ensure proper permissions"),
        (r'requests\.(get|post|put|delete)\s*\(.*verify\s*=\s*False', "SSL verification disabled"),
        (r'random\.random\s*\(', "Use of random module - not cryptographically secure"),
        (r'input\s*\(', "Use of input() - potential for unexpected user input")
    ]
    
    # Low-risk patterns
    low_risk_patterns = [
        (r'print\s*\(.*password|secret|key.*\)', "Potential sensitive data in print statements"),
        (r'#.*TODO|FIXME|HACK', "Code contains TODO/FIXME comments"),
        (r'assert\s+', "Use of assert statements - disabled in optimized mode")
    ]
    
    for i, line in enumerate(lines, 1):
        for pattern, message in high_risk_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                security_issues["high_risk"].append(f"Line {i}: {message}")
        
        for pattern, message in medium_risk_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                security_issues["medium_risk"].append(f"Line {i}: {message}")
        
        for pattern, message in low_risk_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                security_issues["low_risk"].append(f"Line {i}: {message}")
    
    # Add general recommendations
    if not any(security_issues.values()):
        security_issues["recommendations"].append("No obvious security issues detected")
    else:
        security_issues["recommendations"].extend([
            "Review flagged code sections carefully",
            "Consider using static analysis tools like bandit",
            "Implement input validation and sanitization",
            "Use parameterized queries for database operations",
            "Keep dependencies updated"
        ])
    
    return security_issues


# Build the tools
syntax_checker_tool = ToolBuilder(
    name="SyntaxChecker",
    tool_fn=syntax_check,
    input_schema={"code": str, "language": str},
    output_schema={"valid": bool, "errors": list, "warnings": list, "suggestions": list},
    description="Validates Python code syntax and provides detailed analysis with errors, warnings, and suggestions"
).build()

complexity_analyzer_tool = ToolBuilder(
    name="ComplexityAnalyzer", 
    tool_fn=complexity_analysis,
    input_schema={"code": str},
    output_schema={"lines_of_code": int, "functions": int, "classes": int, "complexity_score": int, "maintainability_index": float},
    description="Analyzes code complexity using cyclomatic complexity, lines of code, and maintainability metrics"
).build()

dependency_mapper_tool = ToolBuilder(
    name="DependencyMapper",
    tool_fn=dependency_mapper,
    input_schema={"code": str, "include_stdlib": bool},
    output_schema={"imports": list, "from_imports": list, "modules_used": list, "potential_external": list},
    description="Maps and analyzes code dependencies including imports, stdlib usage, and external packages"
).build()

security_scanner_tool = ToolBuilder(
    name="SecurityScanner",
    tool_fn=security_scanner,
    input_schema={"code": str},
    output_schema={"high_risk": list, "medium_risk": list, "low_risk": list, "recommendations": list},
    description="Scans Python code for potential security vulnerabilities and provides risk assessment"
).build()