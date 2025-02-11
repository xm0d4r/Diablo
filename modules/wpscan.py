from configuration.commands import COMMAND
from core import execute_command,process_tool
from datetime import datetime

def execute_wpscan(target):
    """
    Runs a scan to gather information about the WordPress site.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute WPScan (this command may need adjustments)
    command = COMMAND["wpscan"].format(target=target)
    #command = f" wpscan --url {target} --enumerate p --random-user-agent --throttle 5 --plugins-detection passive --plugins-version-detection passive --detection-mode passive --request-timeout 10 --connect-timeout 10 --disable-tls-checks {target}"
    result = execute_command(command)
    tool = "wpscan"
    
    process_tool(target, result, tool, start_time)