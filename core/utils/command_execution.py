import subprocess
import re
import sys
import time
from core.menu.menu import tool_banner

def execute_command(command):
    """
    Executes a command and updates status dynamically on the same line.
    """
    try:
        # Extract protocol and target
        protocol_target = extract_protocol_target(command)
        protocol_suffix = f" ({protocol_target[0].upper()})" if protocol_target else ""

        # Initial banner with a moving indicator
        tool_banner(command, dynamic=True, status_char='|', protocol_suffix=protocol_suffix)

        # Execute the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Dynamic indicator loop
        indicator_chars = ['|', '/', '-', '\\']
        indicator_index = 0
        while process.poll() is None:
            tool_banner(command, dynamic=True, status_char=indicator_chars[indicator_index], protocol_suffix=protocol_suffix)
            indicator_index = (indicator_index + 1) % len(indicator_chars)
            time.sleep(0.1)  # Adjust speed of the indicator

        # Get the output after the process finishes
        stdout, stderr = process.communicate()
        output = stdout.strip()

        if process.returncode == 0:
            tool_banner(command, dynamic=True, status_char='✅', final=True, protocol_suffix=protocol_suffix)
            if not output:
                return "No output from the command was obtained."
            return output
        else:
            error_msg = f"Error executing command: {command}\n"
            error_msg += f"Standard output (stdout):\n{stdout.strip() if stdout else 'N/A'}\n"
            error_msg += f"Error output (stderr):\n{stderr.strip() if stderr else 'N/A'}\n"
            tool_banner(command, dynamic=True, status_char='❌', final=True, protocol_suffix=protocol_suffix)
            return error_msg

    except Exception as e:
        tool_banner(command, dynamic=True, status_char='❌', final=True, protocol_suffix="")
        return f"An unexpected error occurred: {e}"

def extract_protocol_target(command):
    """
    Extracts the protocol (HTTP or HTTPS) and target from the command.
    """
    tool_names = ["webanalyze", "shcheck", "ffuf"]
    for tool in tool_names:
        if tool in command:
            match = re.search(r'(https?://[^ ]+)', command)
            if match:
                url = match.group(1)
                protocol = url.split("://")[0]
                return protocol, url
    return None

# Ctrl+C operation
def signal_handler(sig, frame):
    global interrupted
    print("\nExiting the tool...")
    print("\n🔥😈 Diablo is done. Savor the spoils. 😈🔥\n")
    interrupted = True
    sys.exit(0)

