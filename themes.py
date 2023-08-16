import os

from colorama import Fore, Style


def blackwhite(text):
    os.system("")
    faded = ""
    red = 40
    green = 40
    blue = 40
    for line in text.splitlines():
        faded += f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n"
        if not red == 255 and not green == 255 and not blue == 255:
            red += 20
            green += 20
            blue += 20
            if red > 255 and green > 255 and blue > 255:
                red = 255
                green = 255
                blue = 255
    return faded


def cyan(text):
    os.system("")
    fade = ""
    blue = 100
    for line in text.splitlines():
        fade += f"\033[38;2;0;255;{blue}m{line}\033[0m\n"
        if not blue == 255:
            blue += 15
            if blue > 255:
                blue = 255
    return fade


def purple(text):
    os.system("")
    fade = ""
    red = 255
    for line in text.splitlines():
        fade += f"\033[38;2;{red};0;180m{line}\033[0m\n"
        if not red == 0:
            red -= 20
            if red < 0:
                red = 0
    return fade


def water(text):
    os.system("")
    fade = ""
    green = 10
    for line in text.splitlines():
        fade += f"\033[38;2;0;{green};255m{line}\033[0m\n"
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return fade


def fire(text):
    os.system("")
    fade = ""
    green = 250
    for line in text.splitlines():
        fade += f"\033[38;2;255;{green};0m{line}\033[0m\n"
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return fade


def menu_theme(type1, type2):
    return (
        type1(
            f"""

        ██████╗ ███████╗███████╗██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
        ██╔══██╗██╔════╝██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
        ██████╔╝█████╗  █████╗  ██║     ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
        ██╔══██╗██╔══╝  ██╔══╝  ██║     ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
        ██████╔╝███████╗███████╗███████╗██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
        ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                                                                


{Style.BRIGHT}> Created by Beelzebub2
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            """  
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] HTTP / HTTPS                                | [3] SOCKS5
[2] SOCKS4                                      | [4] Theme
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""
        )
    )


def info_theme(type1):
    return type1(
        f"""

        ██████╗ ███████╗███████╗██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
        ██╔══██╗██╔════╝██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
        ██████╔╝█████╗  █████╗  ██║     ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
        ██╔══██╗██╔══╝  ██╔══╝  ██║     ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
        ██████╔╝███████╗███████╗███████╗██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
        ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                                                                


{Style.BRIGHT}> Created by Beelzebub22 {Style.RESET_ALL}    
{Style.BRIGHT}> Ctrl+c to cancel actions/exit program  {Style.RESET_ALL}                                                         
"""
    )


def theme_menu(type1, type2):
    return (
        type1(
            f"""


            ████████╗██╗  ██╗███████╗███╗   ███╗███████╗
            ╚══██╔══╝██║  ██║██╔════╝████╗ ████║██╔════╝
               ██║   ███████║█████╗  ██╔████╔██║█████╗  
               ██║   ██╔══██║██╔══╝  ██║╚██╔╝██║██╔══╝  
               ██║   ██║  ██║███████╗██║ ╚═╝ ██║███████╗
               ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
                                            

                                                                

{Style.BRIGHT}> Created by Beelzebub2
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            """  
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] Cyan                                        | [4] Purple
[2] Fire                                        | [5] Water
[3] Blackwhite                                  | [6] Exit
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""
        )
    )
