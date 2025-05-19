
import sys, os 
# Read the original code.
with open('/code/code_6988d060b57745d3a8f6f40f52b6f2ed.py', 'r') as f:
    code = f.read()
exec_globals = {"__name__": "__main__"}
def custom_input(prompt=''):
    sys.stdout.write("PROMPT:" + prompt + "\n")
    sys.stdout.flush()
    return sys.stdin.readline().rstrip("\n")
exec_globals['input'] = custom_input
try:
    exec(code, exec_globals)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
