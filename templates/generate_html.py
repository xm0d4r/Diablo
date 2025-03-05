import os
from jinja2 import Environment, FileSystemLoader
from core.utils.network_operations import clean_url
from configuration.global_config import colors
from templates.parser import (
    parse_nmap, parse_webanalyze, parse_testssl, parse_shcheck, 
    parse_netexec, parse_enum4linux, parse_shortscan
)

def generate_html(results_dir, targets, folder_name):
    # Clean the target URLs

    cleaned_targets = [clean_url(target) for target in targets]
    
    # Define the filenames for each tool's results
    files = {
        "nmap": "nmap.txt",
        "webanalyze": "webanalyze.txt",
        "testssl": "testssl.txt",
        "shcheck": "shcheck.txt",
        "ffuf": "ffuf.txt",
        "enum4linux": "enum4linux.txt",
        "iis_shortname": "shortscan.txt",
        "netexec": "netexec.txt",
        "wpscan": "wpscan.txt"
    }
      
    # Set up the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('../templates/'))
    template = env.get_template('template_summary.html') 

    target_reports = {}
    
    # Iterate over each cleaned target
    for target in cleaned_targets:
        target_dir = os.path.join(results_dir, target)
        
        # Parse the results for each tool and store them in the target_reports dictionary
        target_reports[target] = {
            'open_ports': parse_nmap(os.path.join(target_dir, files['nmap'])),
            'services': parse_webanalyze(os.path.join(target_dir, files['webanalyze'])),
            'testssl_info': parse_testssl(os.path.join(target_dir, files['testssl'])),
            'missing_headers': parse_shcheck(os.path.join(target_dir, files['shcheck'])),
            'ffuf_results': parse_netexec(os.path.join(target_dir, files['ffuf'])),
            'enum4linux_results': parse_enum4linux(os.path.join(target_dir, files['enum4linux'])),
            'iis_shortname_results': parse_shortscan(os.path.join(target_dir, files['iis_shortname'])),
            'netexec_results': parse_netexec(os.path.join(target_dir, files['netexec'])),
            'wpscan_results': parse_netexec(os.path.join(target_dir, files['wpscan']))
        }
    
    # Render the summary HTML content using the template
    summary_html_content = template.render(target_reports=target_reports)
    summary_html_file_path = os.path.join(results_dir, f"{folder_name}_recon_report_summary.html")
    
    # Write the rendered HTML content to a file
    with open(summary_html_file_path, 'w') as f:
        f.write(summary_html_content)
    
    # Print the path to the generated HTML report
    print(f"\n{colors.GREEN}{colors.BOLD}Report summary generated in:{colors.ENDC} {colors.UNDERLINE}{summary_html_file_path.replace('../', '')}{colors.ENDC}")