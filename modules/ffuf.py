import os
import subprocess
import re
from configuration.commands import COMMAND
from core import save_output_to_file, clean_url,check_effective_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

# Define ANSI escape codes for bold and color
bold = "\033[1m"
blue = "\033[94m"
reset = "\033[0m"

def execute_ffuf(target):
    """
    Run FFUF to perform fuzzing on a website and save only the results found.
    """
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    original_target = target
    
    # Ensure that the URL has a trailing slash specifically for FFUF
    if not target.endswith('/'):
        target = target + '/'
    else:
        target = target

    if effective_target == target:

        # Check if the target has http:// or https://
        target = effective_target if effective_target.endswith('/') else effective_target + '/'

        # Execute FFUF with the chosen protocol
        run_ffuf(target, original_target, start_time)

def run_ffuf(target, original_target, start_time):
    """Execute FFUF with the URL provided"""
    
    # Command to run FFUF
    command = COMMAND["ffuf"].format(target=target).split()

    print(f"\n{bold}{blue}----------------------------------------------------------------------------------------------------")
    print(f"                                            Tool: ffuf                                                     ")
    print(f"{bold}{blue}----------------------------------------------------------------------------------------------------{reset}")
    print(f"\n{bold}Ejecutando: {command}{reset}")

    # Run FFUF and capture only the results found.
    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
            output = ""
            relevant_lines = []
            for line in process.stdout:
                print(line, end="")  # Display each line on screen in real time
                output += line

                # Check the duration condition and requests per second
                if "Duration:" in line and "req/sec" in line:
                    duration_match = re.search(r"Duration: \[(\d+:\d+:\d+)\]", line)
                    req_sec_match = re.search(r"(\d+) req/sec", line)

                    if duration_match and req_sec_match:
                        duration = duration_match.group(1)
                        req_sec = int(req_sec_match.group(1))

                        # Convert duration to seconds for comparison
                        h, m, s = map(int, duration.split(":"))
                        total_seconds = h * 3600 + m * 60 + s

                        if total_seconds >= 2 and 0 <= req_sec <= 20:
                            print("\nServer saturation. Stopping FFUF and continuing with the next module.")
                            # Clean and save the results
                            target = clean_url(original_target)
                            RESULTS_FOLDERPATH = os.path.join(RESULTS_DIRECTORY, target)
                            os.makedirs(RESULTS_FOLDERPATH, exist_ok=True)

                            # Save only the relevant results in a file
                            output_file_path = os.path.join(RESULTS_FOLDERPATH, f"{target}_ffuf{RESULTS_FILEEXTENSION}")
                            save_output_to_file("".join(relevant_lines), output_file_path, original_target, start_time)
                            original_target = target
                            process.terminate()
                            return

                # Filter relevant lines with results found
                if any(keyword in line for keyword in ["[Status:", "[Size:", "[Words:", "[Lines:"]):
                    relevant_lines.append(line)
    except Exception as e:
        print(f"Error running FFUF: {e}")
        return

    # Clean and save the results
    target = clean_url(original_target)
    RESULTS_FOLDERPATH = os.path.join(RESULTS_DIRECTORY, target)
    os.makedirs(RESULTS_FOLDERPATH, exist_ok=True)

    # Save only relevant results in a file
    output_file_path = os.path.join(RESULTS_FOLDERPATH, f"{target}_ffuf{RESULTS_FILEEXTENSION}")
    save_output_to_file("".join(relevant_lines), output_file_path, original_target, start_time)

    original_target = target
