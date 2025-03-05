from configuration.commands import COMMAND
from core.utils.command_execution import execute_command
from core.utils.file_operations import process_result_to_file
from datetime import datetime

def execute_netexec(target, target_dir):
    """
    Runs Netexec to gather SMB network information from the target.
    """
    # Set start time
    start_time = datetime.now()

    # Execute Netexec (SMB command)
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["netexec"])
    result = execute_command(command)
    tool = "netexec"
    
    process_result_to_file(target, result, tool, start_time, target_dir)