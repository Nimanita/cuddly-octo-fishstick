
import sys, os 
# Read the original code.
with open('/code/code_dacf2daa900c4c5e82200d41ff461bd8.py', 'r') as f:
    code = f.read()
exec_globals = {"__name__": "__main__"}
def custom_input(prompt=''):
    sys.stdout.write("PROMPT:" + prompt + "
")
    sys.stdout.flush()
    return sys.stdin.readline().rstrip("
")
exec_globals['input'] = custom_input
try:
    exec(code, exec_globals)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
