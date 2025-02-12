# __init__.py

# You can import the main functions or classes of each module here,
# to make it easier to access them without having to import the whole module.

from core.utils import verify_nmap_services, built_targets,check_effective_url,target_with_slash
from core.menu import ffuf_banner
from .netexec import execute_netexec
from .enum4linux import execute_enum4linux
from .wpscan import execute_wpscan
from .iis_shortname import execute_iis_shortname
from .nmap import execute_nmap
from .webanalyze import execute_webanalyze
from .ffuf import execute_ffuf
from .shcheck import execute_shcheck
from .testssl import execute_testssl
from .diablork import execute_diablork
from configuration.commands import COMMAND
