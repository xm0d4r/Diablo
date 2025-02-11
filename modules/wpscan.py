from configuration.commands import COMMAND
from core import execute_command,process_tool
from datetime import datetime

def execute_wpscan(target):
    """
    Runs a scan to gather information about the WordPress site.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute WPScan
    command = COMMAND["wpscan"].format(target=target)
    result = execute_command(command)
    tool = "wpscan"
    
    process_tool(target, result, tool, start_time)