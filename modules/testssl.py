from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_testssl(target):
    """
    Runs TestSSL to analyze the TLS/SSL configuration of a server.
    """

    # Check if the target has http:// or https://
    if target.startswith("http://"):
        return  # If it already has http://, do nothing

    else: 
        target.startswith("https://")
        # If it has https://, run TestSSL directly
        run_testssl(target)


def run_testssl(target):
    """Runs TestSSL with the provided URL and records the elapsed time."""

    # Set start time
    start_time = datetime.now()

    # Execute TestSSL
    command = f"testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)

    # Modify the path to save the results file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'
    
    # Save the result in a file, passing start_time to calculate the elapsed time
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_testssl' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restore the original target after processing
    target = original_target