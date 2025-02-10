from core import execute_command, save_output_to_file, clean_url, check_effective_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from modules import execute_iis_shortname, execute_wpscan   
from datetime import datetime

def execute_webanalyze(target):
    """
    Runs Webanalyze to detect the technologies used by the website.
    """
    # Save the original target
    original_target = target

    # Set start time
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    # Ensure the URL has a trailing slash specifically for FFUF
    if not target.endswith('/'):
        target_with_slash = target + '/'
    else:
        target_with_slash = target

    if effective_target == target_with_slash:
        # Execute Webanalyze
        command = f"webanalyze -apps ../dependencies/webanalyze/technologies.json -host {target}"
        result = execute_command(command)

        target = clean_url(target)

        # Modify the path to save the results file
        RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

        # Save the result in a file, adding the elapsed time
        save_output_to_file(result, RESULTS_FOLDERPATH + target + '_webanalyze' + RESULTS_FILEEXTENSION, original_target, start_time)

        # Restore the original target after Webanalyze
        target = original_target

        # Analyze the result to decide whether to run IIS Shortname Scan
        if "IIS" in result:
            print("Microsoft-IIS detected. Running IIS Shortname Scan...")
            execute_iis_shortname(target)
        
        # Analyze the result to decide whether to run WPScan
        if "WordPress" in result:
            print("WordPress detected. Running WPScan...")
            execute_wpscan(target)