from configuration.commands import COMMAND
from core import execute_command, process_tool
from datetime import datetime

def execute_iis_shortname(target):
    """
    Runs a scan to retrieve short file names in IIS.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute IIS ShortName Scan (this command may need to be adjusted)
    command = COMMAND["shortscan"].format(target=target)
    #command = f"shortscan {target}"
    result = execute_command(command)
    tool = "shortscan"
    
    process_tool(target, result, tool, start_time)