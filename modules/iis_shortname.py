from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_iis_shortname(target):
    """
    Runs a scan to retrieve short file names in IIS.
    """
    # Set start time
    start_time = datetime.now()
    
    # Execute IIS ShortName Scan (this command may need to be adjusted)
    command = f"shortscan {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modify the path to save the file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Save the result to a file
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_shortscan' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restore the original target after IIS ShortName scan
    target = original_target