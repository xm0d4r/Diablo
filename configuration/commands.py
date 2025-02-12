COMMAND = {
    "enum4linux": [
        "enum4linux",              # Comando principal
        "-a",                      # Modo de auditoría completo
        "{target}"                 # El objetivo (dirección IP o dominio)
    ],
    "ffuf": [
        "ffuf",                    # Comando principal
        "-u", "{target}FUZZ",      # URL con el lugar para insertar fuzzing
        "-w", "../dependencies/ffuf/test.txt",   # Ruta al archivo de diccionario de palabras
        "-H", "'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'",  # Header User-Agent
        "-c",                      # Mostrar resultados en color
        "-ac"                      # Activar el modo de evitar casos de repetición
    ],
    "shortscan": [
        "shortscan",               # Comando principal
        "{target}"                 # El objetivo
    ],
    "netexec": [
        "netexec",                 # Comando principal
        "smb",                     # Protocolo SMB
        "{target}",                # El objetivo
        "-u", "''",                # Usuario vacío para la autenticación
        "-p", "''",                # Contraseña vacía para la autenticación
        "--shares"                # Mostrar los recursos compartidos
    ],
    "nmap": [
        "nmap",                    # Comando principal
        "-Pn",                     # No realizar descubrimiento de hosts
        "-sS",                     # Escaneo SYN (escaneo sigiloso)
        "--min-rate", "10000",     # Establecer tasa mínima de paquetes por segundo
        "--max-retries", "3",      # Número máximo de reintentos en caso de fallo
        "-p", "80,443,445,8080,8443",  # Puertos a escanear (HTTP, HTTPS, SMB)
        "{target}",                # El objetivo
        "-vv"                      # Nivel de verborrea (más detalles)
    ],
    "shcheck": [
        "shcheck.py",              # Comando principal para comprobar cabeceras
        "-d",                      # Opción para detectar cabeceras
        "{target}"                 # El objetivo
    ],
    "testssl": [
        "testssl",                 # Comando principal
        "--protocols",             # Mostrar los protocolos soportados
        "--server-defaults",       # Usar la configuración predeterminada del servidor
        "-s",                      # Comprobar todas las opciones disponibles
        "--connect-timeout", "5",  # Establecer tiempo de espera para la conexión
        "--openssl-timeout", "5",  # Establecer tiempo de espera para OpenSSL
        "{target}"                 # El objetivo
    ],
    "webanalyze": [
        "webanalyze",              # Comando principal
        "-apps", "../dependencies/webanalyze/technologies.json",  # Ruta al archivo de tecnologías
        "-host", "{target}"        # El objetivo
    ],
    "wpscan": [
        "wpscan",                  # Comando principal
        "--url", "{target}",       # URL del objetivo
        "--enumerate", "p",        # Enumerar plugins
        "--random-user-agent",     # Usar un agente de usuario aleatorio
        "--throttle", "5",         # Establecer límite de solicitudes por segundo
        "--plugins-detection", "passive",  # Detección pasiva de plugins
        "--plugins-version-detection", "passive",  # Detección pasiva de versiones de plugins
        "--detection-mode", "passive",      # Modo pasivo de detección
        "--request-timeout", "10", # Tiempo de espera para solicitudes
        "--connect-timeout", "10", # Tiempo de espera para la conexión
        "--disable-tls-checks",    # Deshabilitar comprobaciones TLS
        "{target}"                 # El objetivo
    ]
}
