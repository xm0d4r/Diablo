from configuration.commands import COMMAND
from core.utils import execute_command, process_tool
from datetime import datetime

def execute_lazyhunter(target, target_dir):
    """
    Runs a scan to retrieve CVEs.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute Lazy Hunter ShortName Scan
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["lazyhunter"])
    result = execute_command(command)
    tool = "lazyhunter"
    
    process_tool(target, result, tool, start_time, target_dir)