import os
from jinja2 import Environment, FileSystemLoader
from core.utils import clean_url
from datetime import datetime

def parse_nmap(results_file):
    # Extract open ports from Nmap
    with open(results_file, 'r') as f:
        lines = f.readlines()

    open_ports = []
    parsing_ports = False  # Variable to detect when the port table starts

    for line in lines:
        # Start processing the ports section when we find "PORT STATE SERVICE"
        if line.startswith("PORT"):
            parsing_ports = True

        # If we are in the ports section, process only lines containing "open"
        if parsing_ports:
            if "open" in line and ("tcp" in line or "udp" in line):
                parts = line.split()
                if len(parts) >= 4:
                    port_protocol = parts[0]
                    state = parts[1]
                    service = parts[2]
                    
                    # Add only open ports
                    if state == "open":
                        open_ports.append(f"{port_protocol} (open - {service})\n")
            
            if line.strip() == "":
                break

    return open_ports

def parse_webanalyze(results_file):
    # Read the Webanalyze file
    with open(results_file, 'r') as f:
        lines = f.readlines()

    webanalyze_results = []
    captured_urls = set()  # Use a set to avoid duplicate URLs

    for line in lines:
        # Remove separation delimiters and unnecessary lines
        if "================================================================================" in line or line.startswith("Execution date") or line.startswith("Initiating scan for target") or line.startswith("Elapsed scan time"):
           continue 

        line = line.strip()  # Trim leading and trailing whitespace

        # If we find a line with a URL (http:// or https://), start capturing the section
        if line.startswith('http://') or line.startswith('https://'):
            url = f"<strong>{line}</strong>"
            # Capture only if we haven't processed this URL before
            if url not in captured_urls:
                captured_urls.add(url)
                if webanalyze_results:
                    # Add a line break between previous URL entries
                    webanalyze_results.append("")
                webanalyze_results.append(url)  # Add the detected URL
        elif line:  # If the line is not empty and we are capturing
            webanalyze_results.append(line)  # Add the detected service

    return "\n".join(webanalyze_results)

def parse_shcheck(results_file):
    # Read the ShCheck file
    with open(results_file, 'r') as f:
        lines = f.readlines()

    # List to store formatted results
    missing_headers = []
    current_url = None
    current_missing_headers = []

    for line in lines:
        line = line.strip()

        # Identify when a header analysis starts
        if line.startswith("[*] Analyzing headers of"):
            if current_url:  # If there's a previous analysis, add it to the list
                if current_url.strip():
                    missing_headers.append((current_url, current_missing_headers))
            current_url = line  # Store the new URL
            current_missing_headers = []  # Reset the list of missing headers
        elif line.startswith("[!] Missing security header:"):
            # Extract the missing header name
            header = line.replace("[!] Missing security header: ", "").strip()
            if header:  # Only add non-empty headers
                current_missing_headers.append(header)

    if current_url and current_url.strip():
        missing_headers.append((current_url, current_missing_headers))

    # Format the output for HTML
    formatted_results = []
    for url, headers in missing_headers:
        formatted_results.append(f"<strong>{url.strip()}</strong>")
        for header in headers:
            formatted_results.append(f"{header}")

    return formatted_results

def parse_testssl(results_file):
    # Extract all TestSSL content
    try:
        with open(results_file, 'r') as f:
            lines = f.readlines()

        executions = []
        current_execution = []

        for line in lines:
            line = line.strip()
            
            # Add bold formatting before important sections
            if "Testing protocols via sockets except NPN+ALPN" in line:
                if current_execution:
                    executions.append("\n".join(current_execution))
                current_execution = [f"<strong>{line}</strong>"]
            elif "Testing cipher categories" in line:
                if current_execution:
                    executions.append("\n".join(current_execution))
                current_execution = [f"<strong>{line}</strong>"]
            elif "Testing server defaults (Server Hello)" in line:
                if current_execution:
                    executions.append("\n".join(current_execution))
                current_execution = [f"<strong>{line}</strong>"]
            elif line:
                current_execution.append(line)

        # Add the last execution if it exists
        if current_execution:
            executions.append("\n".join(current_execution))

        # Add space between executions
        formatted_results = "\n\n".join(executions)

        return formatted_results
    except Exception as e:
        pass

def generate_html(results_dir, target):

    target = clean_url(target)
    nmap_file = os.path.join(results_dir, target, f'{target}_nmap.txt')
    webanalyze_file = os.path.join(results_dir, target, f'{target}_webanalyze.txt')
    testssl_file = os.path.join(results_dir, target, f'{target}_testssl.txt')
    shcheck_file = os.path.join(results_dir, target, f'{target}_shcheck.txt')
    ffuf_file = os.path.join(results_dir, target, f'{target}_ffuf.txt')
    enum4linux_file = os.path.join(results_dir, target, f'{target}_enum4linux.txt')
    iis_shortname_file = os.path.join(results_dir, target, f'{target}_iis_shortname.txt')
    netexec_file = os.path.join(results_dir, target, f'{target}_netexec.txt')
    wpscan_file = os.path.join(results_dir, target, f'{target}_wpscan.txt')

    # Functions to parse each module (replace as needed)
    def parse_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []

    open_ports = parse_nmap(nmap_file)
    services = parse_webanalyze(webanalyze_file)
    testssl_info = parse_testssl(testssl_file)
    missing_headers = parse_shcheck(shcheck_file)
    ffuf_results = parse_file(ffuf_file)
    enum4linux_results = parse_file(enum4linux_file)
    iis_shortname_results = parse_file(iis_shortname_file)
    netexec_results = parse_file(netexec_file)
    wpscan_results = parse_file(wpscan_file)

    # Create Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('../template/'))
    template = env.get_template('template.html')

    # Render the HTML
    html_content = template.render(
        target=target,
        open_ports=open_ports,
        services=services,
        testssl_info=testssl_info,
        missing_headers=missing_headers,
        ffuf_results=ffuf_results,
        enum4linux_results=enum4linux_results,
        iis_shortname_results=iis_shortname_results,
        netexec_results=netexec_results,
        wpscan_results=wpscan_results
    )

    # Save the HTML file
    html_file_path = os.path.join(results_dir, target, f'{target}_recon_report.html')
    with open(html_file_path, 'w') as f:
        f.write(html_content)

    print(f"\nHTML report generated: {html_file_path}")
