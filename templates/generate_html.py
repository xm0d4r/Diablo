import os
from jinja2 import Environment, FileSystemLoader
from core.utils import clean_url
from templates.parser import parse_nmap, parse_webanalyze, parse_testssl, parse_shcheck, parse_netexec, parse_enum4linux, parse_shortscan

def generate_html(results_dir, target):

    target = clean_url(target)
    nmap_file = os.path.join(results_dir, target, f'{target}_nmap.txt')
    webanalyze_file = os.path.join(results_dir, target, f'{target}_webanalyze.txt')
    testssl_file = os.path.join(results_dir, target, f'{target}_testssl.txt')
    shcheck_file = os.path.join(results_dir, target, f'{target}_shcheck.txt')
    ffuf_file = os.path.join(results_dir, target, f'{target}_ffuf.txt')
    enum4linux_file = os.path.join(results_dir, target, f'{target}_enum4linux.txt')
    iis_shortname_file = os.path.join(results_dir, target, f'{target}_shortscan.txt')
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
    ffuf_results = parse_netexec(ffuf_file)
    enum4linux_results = parse_enum4linux(enum4linux_file)
    iis_shortname_results = parse_shortscan(iis_shortname_file)
    netexec_results = parse_netexec(netexec_file)
    wpscan_results = parse_file(wpscan_file)

    # Create Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('../templates/'))
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
