from configuration.commands import COMMAND
from core import execute_command, process_tool
from datetime import datetime

def execute_enum4linux(target):
    """
    Run Enum4linux to enumerate information from a Windows system.
    """
    # Set start time
    start_time = datetime.now()

    # Run Enum4linux
    command = COMMAND["enum4linux"].format(target=target)
    #command = f"enum4linux -a {target}"
    result = execute_command(command)
    tool = "enum4linux"
    
    process_tool(target, result, tool, start_time)