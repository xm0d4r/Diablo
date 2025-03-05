import re

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