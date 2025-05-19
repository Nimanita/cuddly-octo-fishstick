import os
import uuid
import asyncio

#--------------------------------------------------------------------------
# Configuration: Use a dedicated directory for code files.
# Use environment variable CODE_EXEC_DIR (if set); otherwise, fall back to a directory
# inside your project.
#--------------------------------------------------------------------------
DEFAULT_CODE_EXEC_DIR = os.path.join(os.getcwd(), "code_exec_files")
CODE_EXEC_DIR = os.environ.get("CODE_EXEC_DIR", DEFAULT_CODE_EXEC_DIR)
os.makedirs(CODE_EXEC_DIR, exist_ok=True)
#
# Example:
# For local testing, you can set in your shell:
#   export CODE_EXEC_DIR=/home/mamata/my_code_files
# In production (e.g. on Render), configure CODE_EXEC_DIR via your environment settings.
#

#--------------------------------------------------------------------------
# Create a temporary (but persistent) code file in CODE_EXEC_DIR.
#--------------------------------------------------------------------------
def create_temp_file(content, extension):
    """
    Writes code content to a file in CODE_EXEC_DIR and returns its absolute path.
    Replaces any literal "\\n" with actual newline characters.
    Uses a unique filename based on uuid.
    """
    
    # Generate a unique filename
    filename = f"code_{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(CODE_EXEC_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path

#--------------------------------------------------------------------------
# Environment for docker command execution.
#--------------------------------------------------------------------------
def get_clean_env():
    env = os.environ.copy()
    # Ensure Docker knows the correct host socket (if needed)
    env['DOCKER_HOST'] = 'unix:///var/run/docker.sock'
    return env

#--------------------------------------------------------------------------
# Compilation function for C/C++ code.
#--------------------------------------------------------------------------
async def compile_source(language, source_filepath, mount_dir):
    """
    Compiles C/C++ code.
    Returns a tuple: (success_flag, compiler output, binary_name)
    """
    filename = os.path.basename(source_filepath)
    binary_name = filename + ".out"
    
    if language == "c":
        compile_cmd = [
            "docker", "run", "--rm",
            "--memory=256m", "--cpus=1",
            "-v", f"{mount_dir}:/code",
            "code_executor_image",
            "gcc", f"/code/{filename}", "-o", f"/code/{binary_name}", "-lm"
        ]
    elif language in ("cpp", "c++"):
        compile_cmd = [
            "docker", "run", "--rm",
            "--memory=256m", "--cpus=1",
            "-v", f"{mount_dir}:/code",
            "code_executor_image",
            "g++", f"/code/{filename}", "-o", f"/code/{binary_name}", "-std=c++17", "-lm", "-pthread"
        ]
    else:
        return (False, "Unsupported language for compilation", None)
    
    proc = await asyncio.create_subprocess_exec(
        *compile_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=get_clean_env()
    )
    
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        return (True, stdout.decode('utf-8'), binary_name)
    else:
        return (False, stderr.decode('utf-8'), None)

#--------------------------------------------------------------------------
# Start an interactive docker container for a given language.
#--------------------------------------------------------------------------
async def start_interactive_docker(language, source_filepath, mount_dir):
    """
    Launches a Docker container for interactive code execution.
    For Python, it creates a wrapper that overrides input() so that prompts are flushed.
    For C/C++, it first compiles the code and then runs the binary.
    Returns an asyncio subprocess.Process for the container.
    """
    filename = os.path.basename(source_filepath)
    
    if language == "python":
        # Create a Python wrapper that flushes prompt output immediately.
        wrapper_content = f"""
import sys, os 
# Read the original code.
with open('/code/{filename}', 'r') as f:
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
        # Save the wrapper in our persistent directory.
        wrapper_filepath = create_temp_file(wrapper_content, "py")
        wrapper_name = os.path.basename(wrapper_filepath)
        cmd = [
            "docker", "run", "--rm", "-i",
            "--memory=256m", "--cpus=1",
            "-v", f"{mount_dir}:/code",
            "code_executor_image",
            "python3", "-u", f"/code/{wrapper_name}"
        ]
    elif language in ("c", "cpp", "c++"):
        compile_success, compile_output, binary_name = await compile_source(language, source_filepath, mount_dir)
        if not compile_success:
            raise Exception("Compilation Error:\n" + compile_output)
        cmd = [
            "docker", "run", "--rm", "-i",
            "--memory=256m", "--cpus=1",
            "-v", f"{mount_dir}:/code",
            "code_executor_image",
            f"/code/{binary_name}"
        ]
    elif language == "javascript":
        # Additional languages can be extended here.
        raise Exception("JavaScript interactive session not implemented.")
    else:
        raise Exception("Unsupported language for interactive session.")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=get_clean_env()
    )
    return process

#--------------------------------------------------------------------------
# Example usage within your asynchronous context:
# Assuming 'code' is the code string and 'language' is something like "python"
# In your Channels consumer, you might do:
#
#    ext = "py" if language == "python" else "c" / "cpp"
#    source_filepath = create_temp_file(code, ext)
#    mount_dir = os.path.dirname(os.path.abspath(source_filepath))
#    process = await start_interactive_docker(language, source_filepath, mount_dir)
#
# Then, manage process.stdin, process.stdout, etc.
#--------------------------------------------------------------------------
