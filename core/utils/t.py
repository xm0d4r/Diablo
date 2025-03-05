import subprocess
import os
import re
import sys
import requests
import warnings
import time
from datetime import datetime
from configuration.global_config import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from core.menu.menu import tool_banner

def clean_url(target):
    """ 
    Remove 'http://' or 'https://', any specified port and CIDR suffix (such as /16, /24, etc.) from the target.
    """
    # Remove the scheme (http:// or https://)
    target = re.sub(r'^https?://', '', target)
    # Remove any specified port
    target = re.sub(r':\d+', '', target)
    # Remove any CIDR suffixes (/16, /24, etc.)
    target = re.sub(r'/\d+', '', target)
    # Remove #
    target = re.sub(r'#.*', '', target)
    # Remove trailing slash if exists
    target = target.rstrip('/')
   
    return target

def extract_protocol_target(command):
    """
    Extracts the protocol (HTTP or HTTPS) and target from the command.
    """
    tool_names = ["webanalyze", "shcheck", "ffuf"]
    for tool in tool_names:
        if tool in command:
            match = re.search(r'(https?://[^ ]+)', command)
            if match:
                url = match.group(1)
                protocol = url.split("://")[0]
                return protocol, url
    return None

def execute_command(command):
    """
    Executes a command and updates status dynamically on the same line.
    """
    try:
        # Extract protocol and target
        protocol_target = extract_protocol_target(command)
        protocol_suffix = f" ({protocol_target[0].upper()})" if protocol_target else ""

        # Initial banner with a moving indicator
        tool_banner(command, dynamic=True, status_char='|', protocol_suffix=protocol_suffix)

        # Execute the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Dynamic indicator loop
        indicator_chars = ['|', '/', '-', '\\']
        indicator_index = 0
        while process.poll() is None:
            tool_banner(command, dynamic=True, status_char=indicator_chars[indicator_index], protocol_suffix=protocol_suffix)
            indicator_index = (indicator_index + 1) % len(indicator_chars)
            time.sleep(0.1)  # Adjust speed of the indicator

        # Get the output after the process finishes
        stdout, stderr = process.communicate()
        output = stdout.strip()

        if process.returncode == 0:
            tool_banner(command, dynamic=True, status_char='✅', final=True, protocol_suffix=protocol_suffix)
            if not output:
                return "No output from the command was obtained."
            return output
        else:
            error_msg = f"Error executing command: {command}\n"
            error_msg += f"Standard output (stdout):\n{stdout.strip() if stdout else 'N/A'}\n"
            error_msg += f"Error output (stderr):\n{stderr.strip() if stderr else 'N/A'}\n"
            tool_banner(command, dynamic=True, status_char='❌', final=True, protocol_suffix=protocol_suffix)
            return error_msg

    except Exception as e:
        tool_banner(command, dynamic=True, status_char='❌', final=True, protocol_suffix="")
        return f"An unexpected error occurred: {e}"


def save_output_to_file(output, filename, target, start_time):
    """
    Saves the output of a command or the result of a module to a file,
    adding the date and time of execution, without ANSI escape sequences.
    It also adds the elapsed time since the start of the scan.
    """
    try:
        # Remove ANSI escape sequences (colors and other formats)
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)  # Removes colors
        output = re.sub(r'\x1b\[[0-9]*K', '', output)  # Removes the line deletion code [2K
        
        # Obtain current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # If the start time was provided, calculate the elapsed time.
        if start_time:
            elapsed_time = datetime.now() - start_time
            elapsed_time_str = str(elapsed_time).split('.')[0]  # Remove microseconds
        else:
            elapsed_time_str = "N/A"  # If start time is not provided, enter “N/A”.
        
        # Prepare header with date and elapsed time
        header = f"\n{'='*80}\nExecution date: {timestamp}\n{'='*80}\nInitiating scan for target: {target}\n"
        header += f"Elapsed scan time: {elapsed_time_str}\n{'='*80}\n\n\n"
        
        # Write header and result to file
        with open(filename, 'a') as file:
            file.write(header)
            file.write(output + "\n")
    except Exception as e:
        print(f"Error saving file {filename}: {str(e)}")

def create_folder(target_dir):
    """
    Creates a folder in the specified path.
    """

    # Create the complete path
    full_path = os.path.join(RESULTS_DIRECTORY, target_dir)
    
    try:
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder: {e}")

    return full_path


def is_valid_ip_or_domain(target):
    """
    Verify if the input is a valid IP or domain.
    """
    # Check for IP (IPv4)
    ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_regex, target):
        return True

    # Clean the domain before validating it
    target = clean_url(target)

    # Check if it is a valid domain, allowing subdomains and scripts
    domain_regex = r'^(?!-)(?!.*-$)(?!.*\.\.)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,}$'
    if re.match(domain_regex, target):
        return True

    return False

# Ctrl+C operation
def signal_handler(sig, frame):
    global interrupted
    print("\nExiting the tool...")
    print("\n🔥😈 Diablo is done. Savor the spoils. 😈🔥\n")
    interrupted = True
    sys.exit(0)


def get_target_from_file(target_file):
    """
    Read targets from a file.
    """
    with open(target_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def verify_nmap_services(target, nmap_result):
    """
    Checks whether HTTP, HTTPS or SSL/HTTP services were found in the Nmap result.
    If no such services are found, returns all open ports as target:port.

    Args:
        target (str): The name of the host or domain.
        nmap_result (str): Nmap result as a string.

    Returns:
        set: Set of constructed targets.
    """
    # Regular expressions to search for http, https or ssl/http services
    patterns = [
        (r"(\d+)/tcp\s+open\s+http", 'http'),       # http
        (r"(\d+)/tcp\s+open\s+https", 'https'),     # https
        (r"(\d+)/tcp\s+open\s+ssl/http", 'ssl/http') # ssl/http
    ]

    found_ports = {}  # Dictionary to store ports with detected services
    all_ports = set()  # Set to collect all open ports

    # Search for HTTP/HTTPS services in Nmap output
    for pattern, protocol in patterns:
        matches = re.findall(pattern, nmap_result)
        for port in matches:
            found_ports[port] = protocol  # Store port with its protocol

    # Find all open ports, regardless of protocol
    all_open_ports = re.findall(r"(\d+)/tcp\s+open", nmap_result)
    all_ports.update(all_open_ports)

    # If HTTP/HTTPS services were found, use those, otherwise return all open ports
    if found_ports:
        unique_ports = [(protocol, port) for port, protocol in found_ports.items()]
    else:
        unique_ports = [(None, port) for port in all_ports]  # No protocol

    return built_targets(target, unique_ports)

def built_targets(target, ports):
    """
    Constructs the targets for the ports found according to the service (http, https, ssl/http).
    If no known service is found, returns target:port.

    Args:
        target (str): The name of the host or domain.
        ports (list): List of tuples with the protocol and port found.

    Returns:
        set: Set of constructed targets.
    """
    protocols = {
        'http': 'http://',
        'https': 'https://',
        'ssl/http': 'https://',  # SSL/HTTP
    }

    targets = set()

    for protocol, port in ports:
        if protocol in protocols:
            targets.add(f"{protocols[protocol]}{target}:{port}")
        else:
            targets.add(f"{target}:{port}")  # If no protocol, return target:port

    return targets

def target_with_slash(target):
    """
    Adds a slash to the target if it does not have one.
    
    Args:
        target (str): The target to check.
        
    Returns:
        str: The target with a slash at the end.
    """
    return target if target.endswith('/') else target + '/'

def check_effective_url(target):
    """
    Gets the effective URL after resolving any redirects.
    
    param target: The target URL to check.
    return: The effective URL after redirects.
    """

    # Check if the domain is really valid
    try:
        # Disable the SSL unverified warning
        warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
        # Make a HEAD request to obtain information without downloading all the content.
        response = requests.head(target, allow_redirects=True, timeout=10, verify=False)
        effective_url = response.url
        
        return effective_url
    except requests.exceptions.RequestException as e:
        return None
    
def process_result_to_file(target, result, tool, start_time, target_dir):
    """
    Processes modules by cleaning the target URL, 
    saving the result to a file, and restoring the original target.

    :param target: The original target URL
    :param result: The result to be saved
    :param start_time: The start time of the process
    :return: The original target (restored)
    """
    original_target = target
    target = clean_url(target)

    # Modify the path to save the results file
    results_folderpath = f"{target_dir}/"

    # Save the result in a file, adding the elapsed time
    save_output_to_file(result, f"{results_folderpath}{tool}{RESULTS_FILEEXTENSION}", original_target, start_time)
    # Restore the original target after scan
    return original_target
