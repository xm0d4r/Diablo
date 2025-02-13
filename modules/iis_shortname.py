from configuration.commands import COMMAND
from core.utils import execute_command, process_tool
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
    
    process_tool(target, result, tool, start_time, target_dir)