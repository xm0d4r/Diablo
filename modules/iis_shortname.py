from configuration.commands import COMMAND
from core.utils.command_execution import execute_command
from core.utils.file_operations import process_result_to_file
from datetime import datetime

def execute_iis_shortname(target, target_dir):
    """
    Runs a scan to retrieve short file names in IIS.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute IIS ShortName Scan
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["shortscan"])
    result = execute_command(command)
    tool = "shortscan"
    
    process_result_to_file(target, result, tool, start_time, target_dir)