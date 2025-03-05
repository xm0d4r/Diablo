from configuration.commands import COMMAND
from core.utils.command_execution import execute_command
from core.utils.file_operations import process_result_to_file
from datetime import datetime

def execute_testssl(target, target_dir):
    """
    Runs TestSSL to analyze the TLS/SSL configuration of a server.
    """
    
    # Check if the target has http:// or https://
    if target.startswith("http://"):
        return  # If it already has http://, do nothing

    elif target.startswith("https://"): 
        # Set start time
        start_time = datetime.now()

        # Execute TestSSL
        command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["testssl"])
        result = execute_command(command)
        tool = "testssl"
        
        process_result_to_file(target, result, tool, start_time, target_dir)
    else:
        return
    