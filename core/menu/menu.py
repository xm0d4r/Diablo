from __future__ import print_function
import time
import random
import sys
import time
from configuration.global_config import colors


diablo = [r'''                , ,, ,                              
                | || |    ,/  _____  \.             
                \_||_/    ||_/     \_||             
                  ||       \_| . . |_/              
                  ||         |  L  |                
                 ,||         |`==='|                
                 |>|      ___`>  -<'___             
                 |>|\    /             \            
                 \>| \  /  ,    .    .  |           
                  ||  \/  /| .  |  . |  |           
                  ||\  ` / | ___|___ |  |     (     
               (( || `--'  | _______ |  |     ))  ( 
             (  )\|| (  )\ | - --- - | -| (  ( \  ))
             (\/  || ))/ ( | -- - -- |  | )) )  \(( 
              ( ()||((( ())|         |  |( (( () )
    ''', 
    r'''
                                ,     /~/'   ,--,
                               _/`, ,/'/'   /'/~
                             .'___|/ /____/'/'   __/|
                             /~  __        `\ /~~, /'
                      _,-,__/'  ,       \   /'/~/ /'
                    .~      `   \_/  / ,     "~_/'  ,-'~~~~~---,_
                    `,               `~    `~~~|   /'    ~~\__   `~\_
            |~~~/     `~---,__        _,      /'  | /~~\  _/' ~~\    `~,
            |/\`\          /'     _,-~/      /'  .' __ `/'       `~\    \ 
   |~~~/       `\`\        `-\/\/~   /'    .'    |    `| \/    |    `\_  |
   |/\`\         `,`\              /'      |_  ,' /~\ /' |' |  `\     \~\|
      `\`\    _/~~_/~'            /'      /' ~~/     /   `\ `\,  | \   |
~/      `\`\/~ _/~                ~/~~~~\/'    `\__/' \/\  `\_/\ `\~~\ |
\`\    _/~'    \               /~~'                `~~~\`~~~'   `~~'  `'__
 `\`\/~ _/~\    `\           /' _/                      `\        _,-'~~ |
   `\_/~    `\    `\       _|--'                          |      `\     |'
              `\    `\   /'          _/'                  |       /' /\|'
                /\/~~\-/'        _,-'                     |     /' /'  `
                |_`\~~~/`\     /~                          \/~~' /'
                   |`\~ \ `\   `\                           `| /'
    ''',
    r'''
                              .-"/   .-"/
                             /  (.-./  (
                            /           \      .^.
                           |  -=- -=-    |    (_|_)
                            \   /       /      // 
                             \  .=.    /       \\
                        ___.__`..;._.-'---...  //
                  __.--"        `;'     __   `-.  
        -===-.--""      __.,              ""-.  ".
          '=_    __.---"   | `__    __'   / .'  .'
          `'-""""           \             .'  .'
                             |  __ __    /   |
                             |  __ __   //`'`'
                             |         ' | //
                             |    .      |//
                            .'`., , ,,,.`'.
                           .'`',.',`.` ,.'.`
                            ',',,,,.'...',,'
                            '..,',`'.`,`,.',
                           ,''.,'.,;',.'.`.'
                           '.`.',`,;',',;,.;
                            ',`'.`';',',`',.
                             |     |     |
                             (     (     |
    '''
]

banner = (r"""
        ▓█████▄  ██▓ ▄▄▄       ▄▄▄▄    ██▓     ▒█████  
        ▒██▀ ██▌▓██▒▒████▄    ▓█████▄ ▓██▒    ▒██▒  ██▒
        ░██   █▌▒██▒▒██  ▀█▄  ▒██▒ ▄██▒██░    ▒██░  ██▒
        ░▓█▄   ▌░██░░██▄▄▄▄██ ▒██░█▀  ▒██░    ▒██   ██░
        ░▒████▓ ░██░ ▓█   ▓██▒░▓█  ▀█▓░██████▒░ ████▓▒░
        ▒▒▓  ▒ ░▓   ▒▒   ▓▒█░░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ 
        ░ ▒  ▒  ▒ ░  ▒   ▒▒ ░▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░ 
        ░ ░  ░  ▒ ░  ░   ▒    ░    ░   ░ ░   ░ ░ ░ ▒  
        ░     ░        ░  ░ ░          ░  ░    ░ ░  
        ░                          ░                """)

def profile_banner(profile):
    print(f"\n{colors.GREEN}[🔎] Profile Loaded: {profile}{colors.ENDC}")
    print(f"{colors.BOLD}{colors.GREEN}───────────────────────────────────────────────{colors.ENDC}")

def target_banner(target):
    print(f"\n{colors.YELLOW}[🎯] Target: {target}{colors.ENDC}")
    print(f"{colors.BOLD}{colors.YELLOW}───────────────────────────────────────────────{colors.ENDC}")

def ffuf_banner(dynamic=False, status_char=' ', final=False, protocol_suffix=""):
    banner = f"\r{colors.CYAN}[>] {colors.BOLD}{colors.UNDERLINE}{'ffuf'}{colors.ENDC}{protocol_suffix} {status_char} "
    sys.stdout.write(banner)
    sys.stdout.flush()
    if final:
        sys.stdout.write("\n")
        sys.stdout.flush()
        if status_char == '🛑':
            print(f"    └─{colors.CRED2} Server saturation, ffuf stopped. {colors.ENDC}")

def tool_banner(command, dynamic=False, status_char=' ', final=False, protocol_suffix=""):
    tool_name = command.split()[0]
    banner = f"\r{colors.CYAN}[>] {colors.BOLD}{colors.UNDERLINE}{tool_name}{colors.ENDC}{protocol_suffix} {status_char} "
    sys.stdout.write(banner)
    sys.stdout.flush()
    if final:
        sys.stdout.write("\n")
        sys.stdout.flush()

def show_menu():

    for col in banner:
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0010)

    x = ("""
                    Authors:  xm0d, agarma, at0mic, ander
                    """)
    for col in x:
        print(colors.CBLUE2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0040)

    y = "\n\t\t          😈 El diablo! 😈\n"
    for col in y:
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0040)

    z = "\n"
    for col in z:
        print(colors.ENDC + col, end="")
        sys.stdout.flush()
        time.sleep(0.4)

    """
    Displays an interactive menu for the user to choose the type of scan.
    """
    for col in random.choice(diablo):
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
    time.sleep(1)   
    print("\n" + colors.ENDC + col)

    print("Select the type of recognition you wish to perform:\n")
    print(" 1. Recon")
    print(" 2. Google Dorking")
    print(" 3. Exit")

def show_options():
    # Request the user to select a profile
    choice = input("\nDesired option: ")

    profiles = {
        '1': 'Recon',
        '2': 'Google Dorking',
        '3': 'Exit'
    }

    # Validate the option and return the selected profile.
    return profiles.get(choice, None)



