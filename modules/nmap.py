from configuration.commands import COMMAND
from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from core.utils import verify_nmap_services
from modules import execute_netexec, execute_enum4linux
from datetime import datetime
import re

def execute_nmap(target):
    """
    Runs Nmap for a more detailed scan of the target and checks for open ports.
    If open ports are found, it calls verify_nmap_services to build the targets.
    """
    # Save the original target
    original_target = target

    # Check if the target contains http or https and temporarily remove it
    target = clean_url(target)
    
    # Set start time
    start_time = datetime.now()

    # Execute Nmap
    command = COMMAND["nmap"].format(target=target)
    #command = f"nmap -Pn -sS --min-rate 10000 --max-retries 3 -p 80,443,445,8080,8443 {target} -vv"
    result = execute_command(command)

    # Check if Nmap found open ports
    if not is_ports_open(result):
        print(f"No open ports found in {target}. Stopping module execution.")
        return []  # Return an empty list if no open ports are found

    # Call verify_nmap_services to get the ports and build the targets
    targets = verify_nmap_services(target, result)

    if not targets:
        print(f"No HTTP/HTTPS/SSL services were found for the target {target}.")
        return []  # Return an empty list if no HTTP/HTTPS ports are found

    # Modify the path to save the file
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'
    
    # Save the result to a file, passing start_time to calculate the elapsed time
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_nmap' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restore the original target after Nmap
    target = original_target

    if "Discovered open port 445/tcp" in result:
        print("Port 445 detected. Running NetExec and Enum4Linux...")
        execute_netexec(target)
        execute_enum4linux(target)

    return targets  # Return the list of constructed targets


def is_ports_open(nmap_result):
    """
    Checks if Nmap found open ports in the result.
    """
    # Look for lines containing 'open' in the Nmap result
    open_ports = re.findall(r'\d+/tcp\s+open', nmap_result)

    # Return True if at least one open port is found
    return bool(open_ports)