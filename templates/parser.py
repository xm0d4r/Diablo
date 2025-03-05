import re
import os

def read_file(results_file):
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            return f.readlines()
    return []

def parse_nmap(results_file):
    lines = read_file(results_file)
    open_ports = []
    parsing_ports = False

    for line in lines:
        if line.startswith("PORT"):
            parsing_ports = True

        if parsing_ports:
            if "open" in line and ("tcp" in line or "udp" in line):
                parts = line.split()
                if len(parts) >= 4 and parts[1] == "open":
                    open_ports.append(f"{parts[0]} (open - {parts[2]})\n")

            if not line.strip():
                break
    return "\n".join(open_ports) if open_ports else "No open ports detected."

def parse_webanalyze(results_file):
    lines = read_file(results_file)
    webanalyze_results = []
    captured_urls = set()

    for line in lines:
        if any(start in line for start in ["================================================================================", "Execution date", "Initiating scan for target", "Elapsed scan time"]):
            continue
        line = line.strip()

        if line.startswith(('http://', 'https://')):
            url = f"<strong>{line}</strong>"
            if url not in captured_urls:
                captured_urls.add(url)
                if webanalyze_results:
                    webanalyze_results.append("")
                webanalyze_results.append(url)
        elif line:
            webanalyze_results.append(line)

    return "\n".join(webanalyze_results)

def parse_shcheck(results_file):
    lines = read_file(results_file)
    missing_headers = []
    current_url = None
    current_missing_headers = []

    for line in lines:
        line = line.strip()

        if line.startswith("[*] Analyzing headers of"):
            if current_url:
                missing_headers.append((current_url, current_missing_headers))
            current_url = line
            current_missing_headers = []
        elif line.startswith("[!] Missing security header:"):
            header = line.replace("[!] Missing security header: ", "").strip()
            if header:
                current_missing_headers.append(header)

    if current_url:
        missing_headers.append((current_url, current_missing_headers))

    return [f"<strong>{url.strip()}</strong>\n" + "\n".join(headers) for url, headers in missing_headers]

def parse_testssl(results_file):
    lines = read_file(results_file)
    executions = []
    current_execution = []

    for line in lines:
        line = line.strip()

        if any(skip in line for skip in ["================================================================================", "Execution date", "Initiating scan for target", "Elapsed scan time"]):
            continue

        if any(keyword in line for keyword in ["Testing protocols via sockets except NPN+ALPN", "Testing cipher categories", "Testing server defaults (Server Hello)"]):
            if current_execution:
                executions.append("\n".join(current_execution))
            current_execution = [f"<strong>{line}</strong>"]
        elif line:
            current_execution.append(line)

    if current_execution:
        executions.append("\n".join(current_execution))

    return "\n\n".join(executions)

def parse_enum4linux(results_file):
    lines = read_file(results_file)
    parsed_results = []
    capture_section = False
    section_buffer = []
    title_pattern = r"={5,}\s*\(?(.*?)\)?\s*={5,}"

    for line in lines:
        line = line.strip()

        if any(skip in line for skip in ["================================================================================", "Execution date", "Initiating scan for target", "Elapsed scan time"]):
            continue

        if line.startswith("Starting enum4linux"):
            capture_section = True

        if capture_section:
            title_match = re.match(title_pattern, line)
            if title_match:
                if section_buffer:
                    parsed_results.append("\n".join(section_buffer))
                    section_buffer = []
                parsed_results.append(f"\n<strong>{title_match.group(1).strip()}</strong>")
                continue

            if line:
                section_buffer.append(line)

    if section_buffer:
        parsed_results.append("\n".join(section_buffer))

    return "\n".join(parsed_results)

def parse_shortscan(results_file):
    lines = read_file(results_file)
    shortscan_results = []

    for line in lines:
        line = line.strip()

        if any(skip in line for skip in ["================================================================================", "Execution date", "Initiating scan for target", "Elapsed scan time"]):
            continue

        if line.startswith("🌀 Shortscan"):
            shortscan_results.append(f"<strong>{line}</strong>")
        elif line:
            shortscan_results.append(line)

    return "\n".join(shortscan_results)

def parse_netexec(results_file):
    lines = read_file(results_file)
    parsed_results = []

    for line in lines:
        line = line.strip()

        if any(skip in line for skip in ["================================================================================", "Execution date", "Initiating scan for target", "Elapsed scan time"]):
            continue

        if line:
            parsed_results.append(line)

    return "\n".join(parsed_results)