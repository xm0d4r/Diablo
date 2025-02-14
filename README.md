# Diablo - Automated Security Reconnaissance

## Overview
Diablo is an automated security reconnaissance tool designed to assist security auditors in efficiently gathering information about a target. The tool integrates various scanning modules, allowing users to analyze web services, network protocols, and potential security weaknesses with minimal manual effort. In addition, it has a profile that allows Google Dorking.

## Features
- **Nmap Scan**: Performs network scans to detect open ports and services.
- **IIS ShortName Scan**: Identifies short file names on IIS servers.
- **NetExec**: Retrieves SMB network information.
- **Enum4Linux**: Enumerates SMB shares and users.
- **Shcheck**: Validates HTTP/HTTPS security configurations.
- **TestSSL**: Analyzes SSL/TLS configurations.
- **Webanalyze**: Detects technologies used by a web application.
- **WPScan**: Scans WordPress installations for vulnerabilities.
- **FFUF**: Performs fuzzing attacks for directory and subdomain discovery.
- **Diablork**: Module for Google Dorking.

## Installation
### Prerequisites
- Python 3.8+
- Ensure that external tools such as `nmap`, `testssl`, `wpscan`, `webanalyze`, `IIS ShortName Scan`, `NetExec`, `Enum4Linux`, `Shcheck`, and `FFUF` are installed and accessible from the command line.
- Add to PATH the tools: `export PATH=$PATH:/path/to/tool`

## Usage
Run the tool with a specified target:
```bash
python diablo.py <target_url/ip_or_file>
```
### Example
```bash
python diablo.py https://example.com
```
OR
```bash
python diablo.py ../targets/targets.txt
```

## Modules & Execution
The tool intelligently executes modules based on the detected services:
- **Nmap Scan**: If port 445 is open, `NetExec` and `Enum4Linux` will run.
- **Webanalyze**: If IIS is detected, `IIS ShortName Scan` runs. If WordPress is detected, `WPScan` runs.
- **Shcheck**: Runs on HTTP/HTTPS targets.
- **TestSSL**: Runs on HTTPS targets.
- **FFUF**: Used for directory and subdomain fuzzing.
- **Diablork**: Module for Google Dorking.

## Output
Results are stored in structured files under the `results/` directory:
```
results/
 ├── example.com/
 │   ├── example.com_nmap.txt
 │   ├── example.com_webanalyze.txt
 │   ├── example.com_testssl.txt
 │   ├── example.com_wpscan.txt
 │   ├── example.com_ffuf.txt
 │   ├── example.com_shortscan.txt
 │   ├── example.com_shcheck.txt 
 │   ├── example.com_netexec.txt 
 │   ├── example.com_enum4linux.txt 
 │   ├── example.com_dorks.html
```

## Nmap
You can modify the `nmap` command line in `modules/nmap.py` and add the ports you want to detect or any other command of any other module.

## Future Improvements
- Integration of additional reconnaissance tools.
- Improved result parsing and reporting.
- Multi-threaded execution for faster scanning.

## Disclaimer
This tool is intended for legal security assessments only. Unauthorized use against systems you do not own is prohibited and may be illegal.

---

## Collaborators
- [xm0d4r](https://github.com/xm0d4r)
- [Th34t0m1c](https://github.com/Th34t0m1c)
- [gomezander](https://github.com/gomezander)
- [agarma](https://github.com/agarma)