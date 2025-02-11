from configuration.commands import COMMAND
from core import execute_command, process_tool
from datetime import datetime

def execute_netexec(target):
    """
    Runs Netexec to gather SMB network information from the target.
    """
    # Set start time
    start_time = datetime.now()

    # Execute Netexec (SMB command)
    command = COMMAND["netexec"].format(target=target)
    result = execute_command(command)
    tool = "netexec"
    
    process_tool(target, result, tool, start_time)