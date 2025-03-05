import re
import requests
import warnings

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

