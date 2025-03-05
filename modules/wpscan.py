from configuration.commands import COMMAND
from core.utils.command_execution import execute_command
from core.utils.file_operations import process_result_to_file
from datetime import datetime

def execute_wpscan(target, target_dir):
    """
    Runs a scan to gather information about the WordPress site.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute WPScan
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["wpscan"])
    result = execute_command(command)
    tool = "wpscan"
    
    process_result_to_file(target, result, tool, start_time, target_dir)