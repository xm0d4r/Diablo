from core import execute_command, save_output_to_file, clean_url, check_effective_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_shcheck(target):
    """
    Runs shcheck to validate HTTP/HTTPS configurations on the target.
    """

    # Set start time
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    # Ensure the URL has a trailing slash, specifically for FFUF
    if not target.endswith('/'):
        target_with_slash = target + '/'
    else:
        target_with_slash = target

    if effective_target == target_with_slash:
        # Check if the target contains http:// or https://
        command = f"shcheck.py -d {effective_target}"
        result = execute_command(command)
        save_results(result, target, target, start_time)


def save_results(result, target, full_target, start_time):
    """
    Saves the results of the shcheck command.
    """
    # Clean the target (remove http:// or https://)
    original_target = target
    target = clean_url(target)

    # Modify the path to save the results file
    LOG_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Save the result in the appropriate file, adding elapsed time
    save_output_to_file(result, LOG_FOLDERPATH + target + '_shcheck' + RESULTS_FILEEXTENSION, full_target, start_time)

    # Restore the original target after processing
    target = original_target