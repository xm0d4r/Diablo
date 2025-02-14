import os
import subprocess
import re
from configuration.commands import COMMAND
from core.utils import save_output_to_file, clean_url,check_effective_url,target_with_slash
from core.menu import ffuf_banner
from core.config import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_ffuf(target,target_dir):
    """
    Run FFUF to perform fuzzing on a website and save only the results found.
    """
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    original_target = target
    
    # Ensure that the URL has a trailing slash specifically for FFUF
    target = target_with_slash(target)

    # Check if the effective target is the same as the target (needed for FFUF)
    if effective_target == target:

        # Ensure that the URL has a trailing slash specifically for FFUF
        target = target_with_slash(effective_target)

        # Execute FFUF with the chosen protocol
        run_ffuf(target, original_target, start_time, target_dir)

def run_ffuf(target, original_target, start_time, target_dir):
    """Execute FFUF with the URL provided"""
    
    # Command to run FFUF
    command = [part.format(target=target) if "{target}" in part else part for part in COMMAND["ffuf"]]
    ffuf_banner(command)

    # Run FFUF and capture only the results found.
    try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
                output = ""
                relevant_lines = []
                for line in process.stdout:
                    print(line, end="")
                    output += line

                    # Check for server saturation based on duration and request per second
                    if "Duration:" in line and "req/sec" in line:
                        duration_match = re.search(r"Duration: \[(\d+:\d+:\d+)\]", line)
                        req_sec_match = re.search(r"(\d+) req/sec", line)

                        if duration_match and req_sec_match:
                            total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_match.group(1).split(":"))))
                            req_sec = int(req_sec_match.group(1))

                            if total_seconds >= 2 and 0 <= req_sec <= 20:
                                print("\nServer saturation. Stopping FFUF and continuing with the next module.")
                                save_results(original_target, relevant_lines, start_time, target_dir)  # Save the results
                                process.terminate()  # Terminate the process
                                return

                    # Collect relevant lines from the output
                    if any(keyword in line for keyword in ["[Status:", "[Size:", "[Words:", "[Lines:"]):
                        relevant_lines.append(line)
    except Exception as e:
        print(f"Error running FFUF: {e}")
        return

    save_results(original_target, relevant_lines, start_time, target_dir)  # Save the results

def save_results(original_target, relevant_lines, start_time, target_dir):
    """Save the relevant results to a file"""
    target = clean_url(original_target)  # Clean the URL for use in file paths
    results_folderpath = f"{target_dir}/"
    os.makedirs(results_folderpath, exist_ok=True)
    output_file_path = os.path.join(results_folderpath, f"ffuf{RESULTS_FILEEXTENSION}")
    save_output_to_file("".join(relevant_lines), output_file_path, target, start_time)  # Save the output to a file



