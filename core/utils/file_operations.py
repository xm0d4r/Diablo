import os
import re
from datetime import datetime
from core.utils.network_operations import clean_url
from configuration.global_config import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def save_output_to_file(output, filename, target, start_time):
    """
    Saves the output of a command or the result of a module to a file,
    adding the date and time of execution, without ANSI escape sequences.
    It also adds the elapsed time since the start of the scan.
    """
    try:
        # Remove ANSI escape sequences (colors and other formats)
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)  # Removes colors
        output = re.sub(r'\x1b\[[0-9]*K', '', output)  # Removes the line deletion code [2K
        
        # Obtain current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # If the start time was provided, calculate the elapsed time.
        if start_time:
            elapsed_time = datetime.now() - start_time
            elapsed_time_str = str(elapsed_time).split('.')[0]  # Remove microseconds
        else:
            elapsed_time_str = "N/A"  # If start time is not provided, enter “N/A”.
        
        # Prepare header with date and elapsed time
        header = f"\n{'='*80}\nExecution date: {timestamp}\n{'='*80}\nInitiating scan for target: {target}\n"
        header += f"Elapsed scan time: {elapsed_time_str}\n{'='*80}\n\n\n"
        
        # Write header and result to file
        with open(filename, 'a') as file:
            file.write(header)
            file.write(output + "\n")
    except Exception as e:
        print(f"Error saving file {filename}: {str(e)}")

def create_folder(target_dir):
    """
    Creates a folder in the specified path.
    """

    # Create the complete path
    full_path = os.path.join(RESULTS_DIRECTORY, target_dir)
    
    try:
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder: {e}")

    return full_path

def get_target_from_file(target_file):
    """
    Read targets from a file.
    """
    with open(target_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def process_result_to_file(target, result, tool, start_time, target_dir):
    """
    Processes modules by cleaning the target URL, 
    saving the result to a file, and restoring the original target.

    :param target: The original target URL
    :param result: The result to be saved
    :param start_time: The start time of the process
    :return: The original target (restored)
    """
    original_target = target
    target = clean_url(target)

    # Modify the path to save the results file
    results_folderpath = f"{target_dir}/"

    # Save the result in a file, adding the elapsed time
    save_output_to_file(result, f"{results_folderpath}{tool}{RESULTS_FILEEXTENSION}", original_target, start_time)
    # Restore the original target after scan
    return original_target

