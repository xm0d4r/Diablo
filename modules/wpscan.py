from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_wpscan(target):
    """
    Runs a scan to gather information about the WordPress site.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute WPScan (this command may need adjustments)
    command = f" wpscan --url {target} --enumerate p --random-user-agent --throttle 5 --plugins-detection passive --plugins-version-detection passive --detection-mode passive --request-timeout 10 --connect-timeout 10 --disable-tls-checks {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modify the path to save the results file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Save the result in a file
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_wpscan' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restore the original target after WPScan
    target = original_target