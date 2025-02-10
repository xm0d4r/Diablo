from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_enum4linux(target):
    """
    Run Enum4linux to enumerate information from a Windows system.
    """
    # Set start time
    start_time = datetime.now()

    original_target = target
    target = clean_url(target)

    # Run Enum4linux
    command = f"enum4linux -a {target}"
    result = execute_command(command)
    
    # Modify path to save file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Save the result in a file
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_enum4linux'+ RESULTS_FILEEXTENSION, target,start_time)

    # Restore the original target after _enum4linux
    target = original_target