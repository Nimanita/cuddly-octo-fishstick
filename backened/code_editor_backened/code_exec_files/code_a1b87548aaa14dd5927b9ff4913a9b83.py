
    import sys, os, json
    # Preserve original standard input and output.
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Read the original code to be executed.
    with open('/code/code_c646b091c7b743ce99ab6558fc911595.py', 'r') as f:
        code = f.read()

    exec_globals = {"__name__": "__main__"}

    def custom_input(prompt=''):
        # Instead of printing plain text, send a JSON message with
        # 'action': 'output' and an additional parameter 'prompt': true.
        prompt_obj = {"action": "output", "data": prompt, "prompt": True}
        sys.stdout.write(json.dumps(prompt_obj) + "\n")
        sys.stdout.flush()
        # Read user input from original stdin.
        return original_stdin.readline().rstrip("\n")

    # Override built-in input with our custom input.
    exec_globals['input'] = custom_input

    try:
        exec(code, exec_globals)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
    