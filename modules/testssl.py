from configuration.commands import COMMAND
from core import execute_command, process_tool
from datetime import datetime

def execute_testssl(target):
    """
    Runs TestSSL to analyze the TLS/SSL configuration of a server.
    """

    # Check if the target has http:// or https://
    if target.startswith("http://"):
        return  # If it already has http://, do nothing

    else: 
        target.startswith("https://")
        # Set start time
        start_time = datetime.now()

        # Execute TestSSL
        command = COMMAND["testssl"].format(target=target)
        result = execute_command(command)
        tool = "testssl"
        
        process_tool(target, result, tool, start_time)
    