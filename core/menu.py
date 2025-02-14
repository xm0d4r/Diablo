from __future__ import print_function
import time
import random
import sys
import time


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

class colors:
    CRED2 = "\033[91m"
    CBLUE2 = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"

def ffuf_banner(command):
    print(f"\n{colors.BOLD}{colors.CBLUE2}----------------------------------------------------------------------------------------------------")
    print(f"                                            Tool: ffuf                                                     ")
    print(f"{colors.BOLD}{colors.CBLUE2}----------------------------------------------------------------------------------------------------{colors.ENDC}")
    print(f"\n{colors.BOLD}Executing: {" ".join(command)}{colors.ENDC}")

def profile_banner(profile):
    print(f"\n{colors.RED}{colors.BOLD}----------------------------------------------------------------------------------------------------{colors.RED} ")
    print(f"{colors.RED}                                        Profile: {profile}                                                       {colors.RED}")
    print(f"{colors.RED}----------------------------------------------------------------------------------------------------{colors.RED}{colors.ENDC} ")

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

    # Request the user to select a profile
    choice = input("\nDesired option: ")

    profiles = {
        '1': 'Recon',
        '2': 'Google Dorking',
        '3': 'Exit'
    }

    # Validate the option and return the selected profile.
    return profiles.get(choice, None)

