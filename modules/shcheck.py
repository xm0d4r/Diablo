from configuration.commands import COMMAND
from core.utils import execute_command, check_effective_url,process_tool,target_with_slash
from datetime import datetime

def execute_shcheck(original_target, target_dir):
    """
    Runs shcheck to validate HTTP/HTTPS configurations on the target.
    """

    # Set start time
    start_time = datetime.now()

    target = original_target

    effective_target = check_effective_url(original_target)

    # Ensure that the URL has a trailing slash
    target = target_with_slash(original_target)

    if effective_target == target:
        # Execute shcheck
        command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["shcheck"])
        result = execute_command(command)
        tool = "shcheck"
        process_tool(original_target, result, tool, start_time, target_dir)
