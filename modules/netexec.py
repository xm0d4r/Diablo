from configuration.commands import COMMAND
from core.utils import execute_command, process_tool
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
    
    process_tool(target, result, tool, start_time, target_dir)