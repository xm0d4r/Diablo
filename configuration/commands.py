COMMAND = {
    "enum4linux": [
        "enum4linux",              # Main command
        "-a",                      # Full audit mode
        "{target}"                 # Target (IP address or domain)
    ],
    "ffuf": [
        "ffuf",                    # Main command
        "-u", "{target}FUZZ",      # URL with the fuzzing point (without /)
        "-w", "../dependencies/ffuf/test.txt",   # Path to the wordlist dictionary file
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",  # User-Agent header
        "-c",                      # Show results in color
        "-ac",                      # Enable deduplication avoidance mode
        "-fc", "403"                # Filter out results with different status codes
    ],
    "shortscan": [
        "shortscan",               # Main command
        "{target}"                 # Target
    ],
    "netexec": [
        "netexec",                 # Main command
        "smb",                     # SMB protocol
        "{target}",                # Target
        "-u", "''",                # Empty username for authentication
        "-p", "''",                # Empty password for authentication
        "--shares"                # Show shared resources
    ],
    "nmap": [
        "nmap",                    # Main command
        "-Pn",                     # Do not perform host discovery
        "-sS",                     # SYN scan (stealth scan)
        "--min-rate", "10000",     # Set minimum packet rate per second
        "--max-retries", "3",      # Maximum number of retries on failure
        "-p", "80,443,445,8080,8443",  # Ports to scan (HTTP, HTTPS, SMB)
        "{target}",                # Target
        "-vv"                      # Verbosity level (more details)
    ],
    "shcheck": [
        "shcheck.py",              # Main command to check headers
        "-d",                      # Option to detect headers
        "{target}"                 # Target
    ],
    "testssl": [
        "testssl",                 # Main command
        "--protocols",             # Show supported protocols
        "--server-defaults",       # Use server’s default settings
        "-s",                      # Check all available options
        "--connect-timeout", "5",  # Set connection timeout
        "--openssl-timeout", "5",  # Set OpenSSL timeout
        "{target}"                 # Target
    ],
    "webanalyze": [
        "webanalyze",              # Main command
        "-apps", "../dependencies/webanalyze/technologies.json",  # Path to technologies file
        "-host", "{target}"        # Target
    ],
    "wpscan": [
        "wpscan",                  # Main command
        "--url", "{target}",       # Target URL
        "--enumerate", "p",        # Enumerate plugins
        "--random-user-agent",     # Use a random user agent
        "--throttle", "5",         # Set request rate limit per second
        "--plugins-detection", "passive",  # Passive plugin detection
        "--plugins-version-detection", "passive",  # Passive plugin version detection
        "--detection-mode", "passive",      # Passive detection mode
        "--request-timeout", "10", # Request timeout
        "--connect-timeout", "10", # Connection timeout
        "--disable-tls-checks",    # Disable TLS checks
        "{target}"                 # Target
    ]
}