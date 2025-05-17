import os
import subprocess
import tempfile
import time
import signal
import sys
import re
from django.utils import timezone
from ..models import ExecutionResult, ProgrammingLanguage
from .error_helper import parse_error_message, detect_missing_libraries

# Maximum execution time in seconds
MAX_EXECUTION_TIME = 10

# Common libraries and packages
COMMON_PYTHON_PACKAGES = [
    'numpy', 'pandas', 'matplotlib', 'scipy', 'tensorflow', 'torch', 
    'sklearn', 'requests', 'bs4', 'django', 'flask', 'pillow',
    'opencv-python', 'seaborn', 'plotly', 'sympy'
]

COMMON_C_HEADERS = ['stdio.h', 'stdlib.h', 'math.h', 'string.h', 'time.h', 
                    'ctype.h', 'assert.h', 'limits.h', 'float.h', 'stdbool.h']

COMMON_CPP_HEADERS = ['iostream', 'vector', 'string', 'algorithm', 'map',
                      'unordered_map', 'set', 'unordered_set', 'queue', 'stack',
                      'deque', 'list', 'cmath', 'cstdlib', 'cstring', 'ctime',
                      'fstream', 'sstream', 'iomanip', 'memory', 'numeric']

def create_temp_file(code, language):
    """Create a temporary file with the given code and language extension"""
    extension = language.extension
    with tempfile.NamedTemporaryFile(suffix=f'.{extension}', delete=False) as temp:
        temp.write(code.encode('utf-8'))
        temp_filename = temp.name
    
    return temp_filename

def create_input_file(user_input):
    """Create a temporary file with the user input"""
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(user_input.encode('utf-8'))
        input_filename = temp.name
    
    return input_filename

def execute_code(execution):
    """Execute code and update execution result"""
    execution.status = 'pending'
    execution.execution_started_at = timezone.now()
    execution.save()
    
    language = execution.language
    code = execution.code_snippet.code if execution.code_snippet else execution.raw_code
    user_input = execution.user_input
    
    # Create a temporary file with the code
    temp_filename = create_temp_file(code, language)
    
    # Create a temporary file with the user input if provided
    input_filename = None
    if user_input:
        input_filename = create_input_file(user_input)
    
    try:
        # Execute the code based on the language
        if language.name.lower() == 'python':
            return _execute_python(execution, temp_filename, input_filename)
        elif language.name.lower() == 'c':
            return _execute_c(execution, temp_filename, input_filename)
        elif language.name.lower() == 'c++':
            return _execute_cpp(execution, temp_filename, input_filename)
        else:
            execution.status = 'error'
            execution.stderr = f"Unsupported language: {language.name}"
            execution.friendly_error = "The selected programming language is not supported yet."
            
    except Exception as e:
        execution.status = 'error'
        execution.stderr = f"Execution failed: {str(e)}"
        execution.friendly_error = "There was an unexpected error running your code."
    
    finally:
        # Clean up the temporary files
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
        if input_filename and os.path.exists(input_filename):
            os.unlink(input_filename)
        
        execution.execution_completed_at = timezone.now()
        execution.save()
    
    return execution

def detect_python_imports(code):
    """Detect Python imports in the code"""
    imports = []
    import_pattern = r'^\s*import\s+(\w+)|^\s*from\s+(\w+)\s+import'
    
    for line in code.split('\n'):
        match = re.search(import_pattern, line)
        if match:
            module = match.group(1) or match.group(2)
            if module and module not in imports:
                imports.append(module)
    
    return imports

def _execute_python(execution, temp_filename, input_filename=None):
    """Execute Python code with optional user input"""
    start_time = time.time()
    
    try:
        # Read the code to check for imports
        with open(temp_filename, 'r') as f:
            code = f.read()
        
        # Detect imports in the code
        imports = detect_python_imports(code)
        
        # Create environment for code execution - this ensures we use the system python
        # with all needed packages installed
        env = os.environ.copy()
        
        # Setup the process with input file if provided
        if input_filename:
            with open(input_filename, 'r') as input_file:
                # Execute the Python code with stdin from the input file
                process = subprocess.Popen(
                    ['python3', temp_filename],
                    stdin=input_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid,
                    env=env
                )
        else:
            # Execute without input
            process = subprocess.Popen(
                ['python3', temp_filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
                env=env
            )
        
        try:
            stdout, stderr = process.communicate(timeout=MAX_EXECUTION_TIME)
            
            execution.stdout = stdout.decode('utf-8')
            execution.stderr = stderr.decode('utf-8')
            
            if process.returncode == 0:
                execution.status = 'success'
            else:
                execution.status = 'error'
                error_message = stderr.decode('utf-8')
                execution.friendly_error = parse_error_message(language='python', error=error_message)
                
                # Check for missing libraries
                missing_libs = detect_missing_libraries('python', code, error_message)
                if missing_libs:
                    execution.friendly_error += f"\n\nMissing Python packages: {', '.join(missing_libs)}"
                    execution.stderr += f"\n\nMissing Python packages: {', '.join(missing_libs)}"
                
        except subprocess.TimeoutExpired:
            # Kill the process if it exceeds the timeout
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.kill()
            process.wait()
            
            execution.status = 'timeout'
            execution.stderr = f"Execution timed out after {MAX_EXECUTION_TIME} seconds"
            execution.friendly_error = f"Your code took too long to run! It exceeded the {MAX_EXECUTION_TIME} second limit."
    
    except Exception as e:
        execution.status = 'error'
        execution.stderr = f"Execution failed: {str(e)}"
        execution.friendly_error = "There was an unexpected error running your Python code."
    
    finally:
        execution.execution_time = time.time() - start_time
        
    return execution

def detect_c_headers(code):
    """Detect C/C++ headers in the code"""
    headers = []
    header_pattern = r'#include\s*[<"]([^>"]+)[>"]'
    
    for match in re.finditer(header_pattern, code):
        header = match.group(1)
        if header not in headers:
            headers.append(header)
    
    return headers

def _execute_c(execution, temp_filename, input_filename=None):
    """Execute C code with optional user input"""
    start_time = time.time()
    compiled_filename = f"{temp_filename}.out"
    
    try:
        # Read the code to check for headers
        with open(temp_filename, 'r') as f:
            code = f.read()
        
        # Detect headers in the code
        headers = detect_c_headers(code)
        
        # Build the compilation command with appropriate flags
        compile_cmd = ['gcc', temp_filename, '-o', compiled_filename]
        
        # Add common libraries that are frequently needed
        compile_cmd.append('-lm')  # Math library
        
        # Check for specific headers and add their libs
        if 'pthread.h' in headers:
            compile_cmd.append('-lpthread')
            
        if any(header in ['time.h', 'sys/time.h'] for header in headers):
            compile_cmd.append('-lrt')
            
        # Run the compilation
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True
        )
        
        if compile_process.returncode != 0:
            execution.status = 'error'
            execution.stderr = compile_process.stderr
            error_message = compile_process.stderr
            execution.friendly_error = parse_error_message(language='c', error=error_message)
            
            # Check for missing libraries
            missing_libs = detect_missing_libraries('c', code, error_message)
            if missing_libs:
                execution.friendly_error += f"\n\nMissing C headers: {', '.join(missing_libs)}"
                execution.stderr += f"\n\nMissing C headers: {', '.join(missing_libs)}"
            
            return execution
        
        # Execute the compiled program with input if provided
        try:
            if input_filename:
                with open(input_filename, 'r') as input_file:
                    process = subprocess.Popen(
                        [compiled_filename],
                        stdin=input_file,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        preexec_fn=os.setsid
                    )
            else:
                process = subprocess.Popen(
                    [compiled_filename],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid
                )
            
            stdout, stderr = process.communicate(timeout=MAX_EXECUTION_TIME)
            
            execution.stdout = stdout.decode('utf-8', errors='replace')
            execution.stderr = stderr.decode('utf-8', errors='replace')
            
            if process.returncode == 0:
                execution.status = 'success'
            else:
                execution.status = 'error'
                error_message = stderr.decode('utf-8', errors='replace')
                execution.friendly_error = parse_error_message(language='c', error=error_message)
                
                # Check for missing libraries
                missing_libs = detect_missing_libraries('c', code, error_message)
                if missing_libs:
                    execution.friendly_error += f"\n\nMissing C headers: {', '.join(missing_libs)}"
                    execution.stderr += f"\n\nMissing C headers: {', '.join(missing_libs)}"
                
        except subprocess.TimeoutExpired:
            # Kill the process if it exceeds the timeout
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.kill()
            process.wait()
            
            execution.status = 'timeout'
            execution.stderr = f"Execution timed out after {MAX_EXECUTION_TIME} seconds"
            execution.friendly_error = f"Your code took too long to run! It exceeded the {MAX_EXECUTION_TIME} second limit."
    
    except Exception as e:
        execution.status = 'error'
        execution.stderr = f"Execution failed: {str(e)}"
        execution.friendly_error = "There was an unexpected error running your C code."
    
    finally:
        execution.execution_time = time.time() - start_time
        
        # Clean up the compiled file
        if os.path.exists(compiled_filename):
            os.unlink(compiled_filename)
    
    return execution

def _execute_cpp(execution, temp_filename, input_filename=None):
    """Execute C++ code with optional user input"""
    start_time = time.time()
    compiled_filename = f"{temp_filename}.out"
    
    try:
        # Read the code to check for headers
        with open(temp_filename, 'r') as f:
            code = f.read()
        
        # Detect headers in the code
        headers = detect_c_headers(code)
        
        # Build the compilation command with appropriate flags
        compile_cmd = ['g++', temp_filename, '-o', compiled_filename, '-std=c++17']
        
        # Add common libraries that are frequently needed
        compile_cmd.append('-lm')  # Math library
        
        # Check for specific headers and add their libs
        if 'pthread.h' in headers:
            compile_cmd.append('-lpthread')
            
        # Add pthread support by default for C++11 and higher
        compile_cmd.append('-pthread')
            
        if any(header in ['time.h', 'ctime', 'sys/time.h'] for header in headers):
            compile_cmd.append('-lrt')
            
        # Run the compilation
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True
        )
        
        if compile_process.returncode != 0:
            execution.status = 'error'
            execution.stderr = compile_process.stderr
            error_message = compile_process.stderr
            execution.friendly_error = parse_error_message(language='cpp', error=error_message)
            
            # Check for missing libraries
            missing_libs = detect_missing_libraries('cpp', code, error_message)
            if missing_libs:
                execution.friendly_error += f"\n\nMissing C++ headers: {', '.join(missing_libs)}"
                execution.stderr += f"\n\nMissing C++ headers: {', '.join(missing_libs)}"
            
            return execution
        
        # Execute the compiled program
        try:
            if input_filename:
                with open(input_filename, 'r') as input_file:
                    process = subprocess.Popen(
                        [compiled_filename],
                        stdin=input_file,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        preexec_fn=os.setsid
                    )
            else:
                process = subprocess.Popen(
                    [compiled_filename],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid
                )
            
            stdout, stderr = process.communicate(timeout=MAX_EXECUTION_TIME)
            
            execution.stdout = stdout.decode('utf-8', errors='replace')
            execution.stderr = stderr.decode('utf-8', errors='replace')
            
            if process.returncode == 0:
                execution.status = 'success'
            else:
                execution.status = 'error'
                error_message = stderr.decode('utf-8', errors='replace')
                execution.friendly_error = parse_error_message(language='cpp', error=error_message)
                
                # Check for missing libraries
                missing_libs = detect_missing_libraries('cpp', code, error_message)
                if missing_libs:
                    execution.friendly_error += f"\n\nMissing C++ headers: {', '.join(missing_libs)}"
                    execution.stderr += f"\n\nMissing C++ headers: {', '.join(missing_libs)}"
                
        except subprocess.TimeoutExpired:
            # Kill the process if it exceeds the timeout
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.kill()
            process.wait()
            
            execution.status = 'timeout'
            execution.stderr = f"Execution timed out after {MAX_EXECUTION_TIME} seconds"
            execution.friendly_error = f"Your code took too long to run! It exceeded the {MAX_EXECUTION_TIME} second limit."
    
    except Exception as e:
        execution.status = 'error'
        execution.stderr = f"Execution failed: {str(e)}"
        execution.friendly_error = "There was an unexpected error running your C++ code."
    
    finally:
        execution.execution_time = time.time() - start_time
        
        # Clean up the compiled file
        if os.path.exists(compiled_filename):
            os.unlink(compiled_filename)
    
    return execution