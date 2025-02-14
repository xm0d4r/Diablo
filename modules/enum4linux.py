from configuration.commands import COMMAND
from core.utils import execute_command, process_tool
from datetime import datetime

def execute_enum4linux(target, target_dir):
    """
    Run Enum4linux to enumerate information from a Windows system.
    """
    # Set start time
    start_time = datetime.now()

    # Run Enum4linux
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["enum4linux"])
    result = execute_command(command)
    tool = "enum4linux"
    
    process_tool(target, result, tool, start_time, target_dir)