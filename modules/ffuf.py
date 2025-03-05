import os
import subprocess
import re
import time
from configuration.commands import COMMAND
from core.utils.command_execution import extract_protocol_target
from core.utils.file_operations import save_output_to_file
from core.utils.parsing_operations import target_with_slash
from core.utils.network_operations import check_effective_url,clean_url
from core.menu.menu import ffuf_banner
from configuration.global_config import RESULTS_FILEEXTENSION
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

    # Run FFUF and capture only the results found.
    try:
                # Extract protocol and target
        protocol_target = extract_protocol_target(" ".join(command))

        protocol_suffix = f" ({protocol_target[0].upper()})" if protocol_target else ""

        # Initial banner with a moving indicator
        ffuf_banner(dynamic=True, status_char='|', protocol_suffix=protocol_suffix)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        indicator_chars = ['|', '/', '-', '\\']
        indicator_index = 0

        while process.poll() is None:
            ffuf_banner(dynamic=True, status_char=indicator_chars[indicator_index],protocol_suffix=protocol_suffix)
            indicator_index = (indicator_index + 1) % len(indicator_chars)
            time.sleep(0.1)

        output = ""
        relevant_lines = []
        for line in process.stdout:
            output += line

            # Check for server saturation based on duration and request per second
            if "Duration:" in line and "req/sec" in line:
                duration_match = re.search(r"Duration: \[(\d+:\d+:\d+)\]", line)
                req_sec_match = re.search(r"(\d+) req/sec", line)

                if duration_match and req_sec_match:
                    total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_match.group(1).split(":"))))
                    req_sec = int(req_sec_match.group(1))

                    if total_seconds >= 2 and 0 <= req_sec <= 20:
                        #print("\nServer saturation. Stopping FFUF.")
                        save_results(original_target, relevant_lines, start_time, target_dir)  # Save the results
                        process.terminate()  # Terminate the process
                        ffuf_banner(dynamic=True, status_char='🛑', final=True,protocol_suffix=protocol_suffix) # add a stop character.
                        return

            # Collect relevant lines from the output
            if any(keyword in line for keyword in ["[Status:", "[Size:", "[Words:", "[Lines:"]):
                relevant_lines.append(line)

        if process.returncode == 0:
            ffuf_banner(dynamic=True, status_char='✅', final=True,protocol_suffix=protocol_suffix)
        else:
            ffuf_banner(dynamic=True, status_char='❌', final=True,protocol_suffix=protocol_suffix)

    except Exception as e:
        ffuf_banner(dynamic=True, status_char='❌', final=True,protocol_suffix="")
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