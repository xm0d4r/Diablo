import os
import sys
import signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import execute_nmap
from modules import execute_webanalyze
from modules import execute_ffuf
from modules import execute_shcheck
from modules import execute_testssl
from modules import execute_diablork
from html import generate_html
from utils import create_folder,is_valid_ip_or_domain,signal_handler,get_target_from_file
from menu import show_menu
from config import RESULTS_DIRECTORY

# Define ANSI escape codes for bold and colors
bold = "\033[1m"
rojo = "\033[91m"
reset = "\033[0m"


# Global variable to handle program interruption (Ctrl+C)
interrupted = False

# Configure the signal for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def run_profile(profile, targets):
    """
    Runs the user-selected scan profile sequentially.
    """
    for target in targets:
        create_folder(target)
        print(f"\n{rojo}{bold}----------------------------------------------------------------------------------------------------{rojo} ")
        print(f"{rojo}                                        Profile: {profile}                                                       {rojo}")
        print(f"{rojo}----------------------------------------------------------------------------------------------------{rojo}{reset} ")

        if profile == "Recon":
            # First run Nmap
            built_targets = execute_nmap(target)
            if not built_targets:
                continue  # If Nmap found no open ports, or no targets could be constructed, we move on to the next target.

            modules = [
                execute_webanalyze,
                execute_shcheck,
                execute_testssl,
                execute_ffuf
            ]
            # Run modules sequentially
            for module in modules:
                for constructed_target in built_targets:
                    module(constructed_target)  # We execute each module for each target built
            
            generate_html(RESULTS_DIRECTORY,target)

        elif profile == "Google Dorking":
            execute_diablork(target)

        else:
            print("Profile not recognized. Omitting...")
            continue

def main():
    """
    Main function of the tool that manages the interaction with the user and the execution of the modules.
    """

    # Verify if the user provided a target file or URL/IP
    if len(sys.argv) < 2:
        print("Please provide a file with targets or a URL/IP as argument.")
        sys.exit(1)

    target_input = sys.argv[1]

    # Check if the input is a file or a URL/IP
    if os.path.isfile(target_input):
        targets = get_target_from_file(target_input)
    else:
        targets = [target_input]

    # Validate if the targets are valid IPs or domains
    valid_targets = []
    for target in targets:
        if is_valid_ip_or_domain(target):
            valid_targets.append(target)
        else:
            print(f"Warning: '{target}' Not a valid IP or domain. It will be omitted.")

    if not valid_targets:
        print("No valid targets were found. The program will stop.")
        sys.exit(1)

    # Display menu only once and prompt for profile choice
    profile = show_menu()

    if profile == "Exit":
        print("\nExiting the tool...")
    elif profile:
        run_profile(profile, valid_targets)
    else:
        print("Invalid option. Please try again.")
    
    print("\n🔥😈 Diablo is done. Savor the spoils. 😈🔥\n")

if __name__ == "__main__":
    main()


