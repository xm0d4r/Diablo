from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_netexec(target):
    """
    Runs Netexec to gather SMB network information from the target.
    """
    # Set start time
    start_time = datetime.now()

    original_target = target
    target = clean_url(target)

    # Execute Netexec (SMB command)
    command = f"netexec smb {target} -u '' -p '' --shares"
    result = execute_command(command)
    
    # Modify the path to save the file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Save the result to a file
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_netexec' + RESULTS_FILEEXTENSION, target, start_time)

    # Restore the original target after _enum4linux
    target = original_target