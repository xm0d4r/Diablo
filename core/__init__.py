# __init__.py

# You can import the main functions or classes of each module here,
# to make it easier to access them without having to import the whole module.

from .config import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from .menu import show_menu, ffuf_banner,profile_banner
from .html import  generate_html
from .utils import execute_command, save_output_to_file, clean_url,is_valid_ip_or_domain
from .utils import signal_handler,get_target_from_file,check_effective_url,process_tool, target_with_slash
from configuration.commands import COMMAND