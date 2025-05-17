import os
import re
import traceback

# Dictionary of common error patterns and their user-friendly explanations
PYTHON_ERROR_PATTERNS = {
    "ImportError: No module named '(.*)'": "The module '{0}' is not installed or not available.",
    "NameError: name '(.*)' is not defined": "The variable or function '{0}' is used but hasn't been defined yet.",
    "TypeError: (.*) takes (.*) positional argument but (.*) were given": "Function call has the wrong number of arguments: {0}",
    "SyntaxError: invalid syntax": "There's a syntax error in your code. Check for missing parentheses, quotes, or colons.",
    "ZeroDivisionError: division by zero": "You're trying to divide by zero, which is not allowed in mathematics.",
    "IndexError: list index out of range": "You're trying to access an element at an index that doesn't exist in your list.",
    "KeyError: (.*)": "The key '{0}' doesn't exist in the dictionary you're trying to access.",
    "FileNotFoundError: (.*?)$": "The file '{0}' could not be found. Check the path and filename.",
    "IndentationError: (.*)": "There's an issue with the indentation in your code: {0}",
    "ModuleNotFoundError: No module named '(.*)'": "The Python module '{0}' is not installed.",
    "AttributeError: '(.*)' object has no attribute '(.*)'": "The object of type '{0}' doesn't have the attribute or method '{1}'."
}

C_ERROR_PATTERNS = {
    "undefined reference to '(.*)'": "The function '{0}' is being called but hasn't been defined or linked properly.",
    "'(.*)' undeclared": "The variable or function '{0}' is used but hasn't been declared.",
    "expected '(.*)' before '(.*)'": "Syntax error: expected '{0}' before '{1}'.",
    "invalid operands to binary (.*)": "The operation '{0}' cannot be performed on these types.",
    "incompatible implicit declaration of built-in function '(.*)'": "You need to include the proper header file for the function '{0}'."
}

CPP_ERROR_PATTERNS = {
    "undefined reference to '(.*)'": "The function or symbol '{0}' is being called but hasn't been defined or linked properly.",
    "'(.*)' was not declared in this scope": "The variable, function, or class '{0}' is used but hasn't been declared in this scope.",
    "expected '(.*)' before '(.*)'": "Syntax error: expected '{0}' before '{1}'.",
    "no matching function for call to '(.*)'": "There's no version of the function '{0}' that matches the arguments you provided.",
    "invalid operands to binary (.*)": "The operation '{0}' cannot be performed on these types."
}

# Header file suggestions for common errors
HEADER_SUGGESTIONS = {
    "sqrt": "For using sqrt(), you need to include <math.h> for C or <cmath> for C++",
    "printf": "For using printf(), you need to include <stdio.h> for C or <cstdio> for C++",
    "cout": "For using cout, you need to include <iostream> in C++",
    "cin": "For using cin, you need to include <iostream> in C++",
    "malloc": "For using malloc(), you need to include <stdlib.h> for C or <cstdlib> for C++",
    "strlen": "For using strlen(), you need to include <string.h> for C or <cstring> for C++",
    "fopen": "For using file operations like fopen(), you need to include <stdio.h> for C or <cstdio> for C++",
    "std::vector": "For using std::vector, you need to include <vector> in C++",
    "std::string": "For using std::string, you need to include <string> in C++",
    "std::map": "For using std::map, you need to include <map> in C++",
    "rand": "For using rand(), you need to include <stdlib.h> for C or <cstdlib> for C++",
    "time": "For using time(), you need to include <time.h> for C or <ctime> for C++",
    "isalpha": "For using isalpha(), you need to include <ctype.h> for C or <cctype> for C++",
    "numpy": "To use numpy, make sure it's properly imported with 'import numpy as np'",
    "pandas": "To use pandas, make sure it's properly imported with 'import pandas as pd'",
    "matplotlib": "To use matplotlib, make sure it's properly imported with 'import matplotlib.pyplot as plt'"
}

def parse_error_message(language, error):
    """Parse error messages and provide user-friendly explanations"""
    if not error:
        return "An unknown error occurred."
    
    # Choose the appropriate pattern dictionary based on language
    if language.lower() == 'python':
        error_patterns = PYTHON_ERROR_PATTERNS
    elif language.lower() == 'c':
        error_patterns = C_ERROR_PATTERNS
    elif language.lower() == 'cpp':
        error_patterns = CPP_ERROR_PATTERNS
    else:
        return f"Error details: {error}"
    
    # Try to match the error with known patterns
    for pattern, explanation in error_patterns.items():
        match = re.search(pattern, error)
        if match:
            # Format the explanation with captured groups
            groups = match.groups()
            try:
                friendly_error = explanation.format(*groups)
                
                # Add header suggestions if relevant
                for term, suggestion in HEADER_SUGGESTIONS.items():
                    if term in error:
                        friendly_error += f"\n\nTIP: {suggestion}"
                
                return friendly_error
            except Exception:
                # If formatting fails for any reason, return the raw explanation
                return explanation
    
    # If no pattern matches, provide some generic guidance based on keywords
    for term, suggestion in HEADER_SUGGESTIONS.items():
        if term in error:
            return f"Error involving '{term}'. {suggestion}\n\nOriginal error: {error}"
    
    # If no better explanation is found, provide the original error
    lines = error.strip().split('\n')
    if len(lines) > 5:
        # If error is very long, provide a summary
        return f"Error summary: {lines[0]}\n\nPlease check your code for syntax errors or missing libraries."
    else:
        return f"Error details: {error}"

def detect_missing_libraries(language, code, error_message):
    """Detect missing libraries based on code content and error message"""
    missing_libraries = []
    
    if language.lower() == 'python':
        # Common Python imports that might be missing
        imports = {
            'numpy': ['np', 'numpy'],
            'pandas': ['pd', 'pandas'],
            'matplotlib': ['plt', 'matplotlib'],
            'scipy': ['scipy'],
            'tensorflow': ['tf', 'tensorflow'],
            'torch': ['torch'],
            'sklearn': ['sklearn']
        }
        
        # Check if these imports are used in the code but might be missing
        for lib_name, lib_aliases in imports.items():
            for alias in lib_aliases:
                if alias in code and f"No module named '{lib_name}'" in error_message:
                    missing_libraries.append(lib_name)
                    break
    
    elif language.lower() in ['c', 'cpp']:
        # Common C/C++ headers that might be missing
        headers = {
            'math.h': ['sqrt', 'pow', 'sin', 'cos', 'log'],
            'stdio.h': ['printf', 'scanf', 'fopen'],
            'stdlib.h': ['malloc', 'free', 'rand', 'exit'],
            'string.h': ['strlen', 'strcpy', 'strcmp'],
            'iostream': ['cout', 'cin', 'endl'],
            'vector': ['vector'],
            'algorithm': ['sort', 'find', 'max', 'min'],
            'fstream': ['ifstream', 'ofstream']
        }
        
        # If the header is not included but functions from it are used
        for header, functions in headers.items():
            for func in functions:
                if func in code and func in error_message and header not in code:
                    if header not in missing_libraries:
                        missing_libraries.append(header)
    
    return missing_libraries