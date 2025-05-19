            import sys, os, json, builtins
            # Preserve the original standard input and output.
            original_stdin = sys.stdin
            original_stdout = sys.stdout

            # Read the original code.
            with open('/code/code_10fc21880d344801bbc29b8f539a5271.py', 'r') as f:
                code = f.read()

            exec_globals = {"__name__": "__main__"}

            # Define a custom print that outputs a JSON message appended with a marker.
            def custom_print(*args, **kwargs):
                # Combine all arguments into a single string.
                output_str = " ".join(str(arg) for arg in args)
                # Create a JSON message with a flag prompt=False.
                message = json.dumps({"action": "output", "data": output_str, "prompt": False})
                # Append the unique marker and a newline.
                sys.stdout.write(message + "<<<EOM>>>
")
                sys.stdout.flush()

            # Override the built-in print.
            builtins.print = custom_print
            exec_globals['print'] = custom_print

            # Define a custom input that sends a JSON message with prompt=True.
            def custom_input(prompt=''):
                prompt_obj = {"action": "output", "data": prompt, "prompt": True}
                sys.stdout.write(json.dumps(prompt_obj) + "<<<EOM>>>
")
                sys.stdout.flush()
                # Read user input from the original stdin.
                return original_stdin.readline().rstrip("\n")

            exec_globals['input'] = custom_input

            try:
                exec(code, exec_globals)
            except Exception as e:
                custom_print("Error: " + str(type(e).__name__) + ": " + str(e))
                sys.exit(1)
