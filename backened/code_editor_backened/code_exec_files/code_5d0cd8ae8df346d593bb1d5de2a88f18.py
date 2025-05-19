
import sys, os, json
# Read the original code.
with open('/code/code_431efa22d32343b280e29b22648245ba.py', 'r') as f:
    code = f.read()
exec_globals = {"__name__": "__main__"}
def custom_input(prompt=''):
    prompt_obj = {"action": "output", "data": prompt, "prompt": True}
    sys.stdout.write(json.dumps(prompt_obj) + "<<<EOM>>>\n")
    sys.stdout.flush()
    return sys.stdin.readline().rstrip("\n")
exec_globals['input'] = custom_input
try:
    exec(code, exec_globals)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
