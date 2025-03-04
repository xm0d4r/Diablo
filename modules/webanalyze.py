from configuration.commands import COMMAND
from core.utils.command_execution import execute_command
from core.utils.file_operations import process_result_to_file
from core.utils.parsing_operations import target_with_slash
from core.utils.network_operations import check_effective_url
from modules import execute_iis_shortname, execute_wpscan 
from datetime import datetime

def execute_webanalyze(target, target_dir):
    """
    Runs Webanalyze to detect the technologies used by the website.
    """
    # Set start time
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    # Ensure the URL has a trailing slash
    target_with_slashed = target_with_slash(target)

    if effective_target == target_with_slashed:
        # Execute Webanalyze
        command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["webanalyze"])
        result = execute_command(command)
        tool = "webanalyze"

        original_target = process_result_to_file(target, result, tool, start_time, target_dir)

        # Analyze the result to decide whether to run IIS Shortname Scan
        if "IIS" in result:
            print("    └─ Microsoft-IIS detected. Running IIS Shortname Scan...")
            execute_iis_shortname(original_target, target_dir)
        
        # Analyze the result to decide whether to run WPScan
        if "WordPress" in result:
            print("    └─ WordPress detected. Running WPScan...")
            execute_wpscan(original_target, target_dir)