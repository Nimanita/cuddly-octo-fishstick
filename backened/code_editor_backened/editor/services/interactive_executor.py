
import os
import uuid
import asyncio
import sys
import subprocess

#--------------------------------------------------------------------------
# Configuration: Use a dedicated directory for code files.
#--------------------------------------------------------------------------
DEFAULT_CODE_EXEC_DIR = os.path.join(os.getcwd(), "code_exec_files")
CODE_EXEC_DIR = os.environ.get("CODE_EXEC_DIR", DEFAULT_CODE_EXEC_DIR)
os.makedirs(CODE_EXEC_DIR, exist_ok=True)

#--------------------------------------------------------------------------
# Create a temporary (but persistent) code file in CODE_EXEC_DIR.
#--------------------------------------------------------------------------
def create_temp_file(content, extension):
    """
    Writes code content to a file in CODE_EXEC_DIR and returns its absolute path.
    Uses a unique filename based on uuid.
    """
    # Generate a unique filename
    filename = f"code_{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(CODE_EXEC_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path

#--------------------------------------------------------------------------
# Start an interactive Python process for direct execution
#--------------------------------------------------------------------------
async def start_interactive_python(source_filepath):
    """
    Launches a Python subprocess for direct code execution without Docker.
    Creates a wrapper that overrides input() so that prompts are flushed.
    Returns an asyncio subprocess.Process for the Python interpreter.
    """
    filename = os.path.basename(source_filepath)
    
    # Create a Python wrapper that flushes prompt output immediately
    wrapper_content = f"""
import sys, os 
# Read the original code
with open('{source_filepath}', 'r') as f:
    code = f.read()
exec_globals = {{"__name__": "__main__"}}
def custom_input(prompt=''):
    sys.stdout.write("PROMPT:" + prompt + "\\n")
    sys.stdout.flush()
    return sys.stdin.readline().rstrip("\\n")
exec_globals['input'] = custom_input
try:
    exec(code, exec_globals)
except Exception as e:
    print(f"Error: {{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
"""
    # Save the wrapper in our persistent directory
    wrapper_filepath = create_temp_file(wrapper_content, "py")
    
    # Run Python directly (no Docker)
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-u", wrapper_filepath,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return process

#--------------------------------------------------------------------------
# Main function to start interactive execution (API remains compatible)
#--------------------------------------------------------------------------
async def start_interactive_docker(language, source_filepath, mount_dir):
    """
    Compatible API that now directly executes Python code without Docker.
    For non-Python languages, returns a helpful error message.
    """
    if language.lower() != "python":
        raise Exception(f"Sorry, only Python is supported in this environment. {language} requires Docker which is not available on this hosting plan.")
    
    return await start_interactive_python(source_filepath)

# For compatibility with old code
async def compile_source(language, source_filepath, mount_dir):
    """Stub for compatibility"""
    return (False, "Compilation requires Docker which is not available on this hosting plan.", None)

def get_clean_env():
    """Stub for compatibility"""
    return os.environ.copy()
