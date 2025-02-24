from configuration.commands import COMMAND
from core.utils import execute_command, save_output_to_file, clean_url
from core.config import RESULTS_FILEEXTENSION
from core.utils import verify_nmap_services, obtainIP
from modules import execute_netexec, execute_enum4linux, execute_lazyhunter
from datetime import datetime
import re
import os

def execute_nmap(target, target_dir):
    """
    Runs Nmap for a more detailed scan of the target and checks for open ports.
    If open ports are found, it calls verify_nmap_services to build the targets.
    
    :param target: The target to scan
    :param target_dir: The base directory where results should be stored
    """
    # Save the original target
    original_target = target

    # Check if the target contains http or https and temporarily remove it
    target = clean_url(target)
    
    # Set start time
    start_time = datetime.now()

    # Execute Nmap
    command = " ".join(part.format(target=target) if "{target}" in part else part for part in COMMAND["nmap"])
    result = execute_command(command)

    # Check if Nmap found open ports
    if not is_ports_open(result):
        print(f"\nNo open ports found in {target}. Stopping module execution.")
        return []  # Return an empty list if no open ports are found

    # Call verify_nmap_services to get the ports and build the targets
    targets = verify_nmap_services(target, result)

    if not targets:
        print(f"\nNo HTTP/HTTPS/SSL services were found for the target {target}.")
        return []  # Return an empty list if no HTTP/HTTPS ports are found

    results_folderpath = f"{target_dir}/"

    os.makedirs(results_folderpath, exist_ok=True)
    
    # Save the result to a file, passing start_time to calculate the elapsed time
    save_output_to_file(result, f"{results_folderpath}nmap{RESULTS_FILEEXTENSION}", original_target, start_time)

    # Restore the original target after Nmap
    target = original_target

    IP_addr = obtainIP(target, result)

    execute_lazyhunter(IP_addr, target_dir)


    if "Discovered open port 445/tcp" in result:
        print("\n[INFO] Port 445 detected. Running NetExec and Enum4Linux...")
        execute_netexec(target, target_dir) 
        execute_enum4linux(target, target_dir) 

    return targets  # Return the list of constructed targets


def is_ports_open(nmap_result):
    """
    Checks if Nmap found open ports in the result.
    """
    # Look for lines containing 'open' in the Nmap result
    open_ports = re.findall(r'\d+/tcp\s+open', nmap_result)

    # Return True if at least one open port is found
    return bool(open_ports)