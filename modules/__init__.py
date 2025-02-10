# __init__.py

# Puedes importar las funciones principales o clases de cada módulo aquí,
# para que sea más fácil acceder a ellas sin tener que importar el módulo completo.

from core.utils import verify_nmap_services, built_targets,check_effective_url
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
