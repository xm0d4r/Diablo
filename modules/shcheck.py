from configuration.commands import COMMAND
from core import execute_command, check_effective_url,process_tool
from datetime import datetime

def execute_shcheck(original_target):
    """
    Runs shcheck to validate HTTP/HTTPS configurations on the target.
    """

    # Set start time
    start_time = datetime.now()

    target = original_target

    effective_target = check_effective_url(original_target)

    # Ensure the URL has a trailing slash, specifically for FFUF
    if not original_target.endswith('/'):
        target = original_target + '/'
    else:
        target = original_target

    if effective_target == target:
        # Execute shcheck
        command = COMMAND["shcheck"].format(target=target)
        #command = f"shcheck.py -d {effective_target}"
        result = execute_command(command)
        tool = "shcheck"
        process_tool(original_target, result, tool, start_time)
