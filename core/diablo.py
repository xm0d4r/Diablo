import os
import sys
import signal
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import execute_nmap, execute_webanalyze, execute_ffuf, execute_shcheck, execute_testssl, execute_diablork
from templates.generate_html import generate_html
from utils import create_folder, is_valid_ip_or_domain, signal_handler, get_target_from_file, clean_url
from menu import show_menu, profile_banner
from config import RESULTS_DIRECTORY

# Configure the signal for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def print_help():
    print("Usage: python diablo.py <target_file.txt> | <IP/URL>")
    print(" - The only argument allowed is a .txt file containing targets or a single host (IP/URL).")
    sys.exit(0)

def get_folder_name():
    folder_name = input("Enter a name for the results folder: ")
    if not folder_name:
        folder_name = datetime.now().strftime("%Y-%m-%d")  # Use the current date if no name is provided
    return folder_name

# Run the profile
def run_profile(profile, targets, execution_dir, folder_name):
    recon_profile = False

    for target in targets:
        profile_banner(profile)

        if profile == "Recon":
            recon_profile = True
            target = clean_url(target)

            target_dir = os.path.join(execution_dir, target)
            create_folder(target_dir)

            built_targets = execute_nmap(target, target_dir)
            if not built_targets:
                continue

            modules = [
                execute_webanalyze,
                execute_shcheck,
                execute_testssl,
                execute_ffuf
            ]

            for module in modules:
                for constructed_target in built_targets:
                    module(constructed_target, target_dir)

        elif profile == "Google Dorking":
            create_folder(target)
            execute_diablork(target)
    
    if recon_profile:
        generate_html(execution_dir, targets, folder_name)

def main():
    if len(sys.argv) < 2:
        print("Please provide a file with targets or a URL/IP as an argument.")
        sys.exit(1)
    
    if sys.argv[1] == "-h":
        print_help()
    
    target_input = sys.argv[1]

    if os.path.isfile(target_input):
        targets = get_target_from_file(target_input)
        targets = [clean_url(target) for target in targets]
    else:
        targets = [clean_url(target_input)]

    valid_targets = [target for target in targets if is_valid_ip_or_domain(target)]
    if not valid_targets:
        print("No valid targets found. Exiting.")
        sys.exit(1)

    profile = show_menu()
    if profile == "Exit":
        print("\nExiting the tool...")
        sys.exit(0)
    elif profile == "Recon":
        folder_name = get_folder_name()
        execution_dir = os.path.join(RESULTS_DIRECTORY, folder_name)
        os.makedirs(execution_dir, exist_ok=True)
        run_profile(profile, valid_targets, execution_dir, folder_name)
    elif profile == "Google Dorking":
        run_profile(profile, valid_targets, None, None)
    else:
        print("Invalid option. Please try again.")
    
    print("\n🔥😈 Diablo is done. Savor the spoils. 😈🔥\n")

if __name__ == "__main__":
    main()