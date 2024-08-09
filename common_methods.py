import subprocess
def run_command_and_print(command):
    output = []
    with subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line, end='')  # Print each line in real-time
            output.append(line)  # Append each line to the list

    # After the loop, you can join the output list into a single string if needed
    captured_output = ''.join(output)
    return captured_output