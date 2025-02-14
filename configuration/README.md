# Configuration

This folder contains configuration files used across the tool. The main file included here is `commands.py`, which defines a set of commands for various reconnaissance tools.

## `commands.py`

The `commands.py` file contains a dictionary named `COMMAND`, which maps tool names to their respective command-line execution strings. These commands are formatted with `{target}`, allowing dynamic substitution of the target during execution.

### Available Commands

```python
COMMAND = {
    "enum4linux": "enum4linux -a {target}",
    "ffuf": "ffuf -u {target}FUZZ -w ../dependencies/ffuf/test.txt -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0' -c -ac",
    "shortscan": "shortscan {target}",
    "netexec": "netexec smb {target} -u '' -p '' --shares",
    "nmap": "nmap -Pn -sS --min-rate 10000 --max-retries 3 -p 80,443,445,8080,8443 {target} -vv",
    "shcheck": "shcheck.py -d {target}",
    "testssl": "testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}",
    "webanalyze": "webanalyze -apps ../dependencies/webanalyze/technologies.json -host {target}",
    "wpscan": "wpscan --url {target} --enumerate p --random-user-agent --throttle 5 --plugins-detection passive --plugins-version-detection passive --detection-mode passive --request-timeout 10 --connect-timeout 10 --disable-tls-checks {target}"
}
```

### Description of Commands

- **enum4linux**: Performs enumeration of SMB shares, users, and other network details.
- **ffuf**: Executes a fuzzing scan using wordlists to find hidden directories or files.
- **shortscan**: A fast scanning tool for network reconnaissance.
- **netexec**: Performs SMB enumeration and privilege escalation checks.
- **nmap**: Runs a fast Nmap scan on commonly used ports.
- **shcheck**: Checks for security headers on web applications.
- **testssl**: Scans for SSL/TLS vulnerabilities on a target.
- **webanalyze**: Identifies technologies used by a web application.
- **wpscan**: Scans WordPress sites for vulnerabilities and plugins.

### Usage

This dictionary is imported by different modules to execute specific commands dynamically based on the provided target. Ensure that all dependencies (e.g., `ffuf`, `nmap`, `wpscan`) are installed before running the tool.

---

For any modifications, update `commands.py` accordingly to reflect the necessary changes.

