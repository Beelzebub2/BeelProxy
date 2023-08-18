import json
import os
import shutil
from colorama import Style


class JSONConfigHandler:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                try:
                    config = json.load(file)
                    return config
                except json.JSONDecodeError:
                    print("Error: Invalid JSON format in the config file.")
        return {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_file_path, "w") as file:
            json.dump(self.config, file, indent=4)


config_handler = JSONConfigHandler("config.json")
VERSION = config_handler.get("Version")
THEME = config_handler.get("Theme")
NOTIFICATIONS = config_handler.get("Notifications")
NOTIFICATIONS_THEME = config_handler.get("Notifications_theme")
LINE = "─" * shutil.get_terminal_size().columns


def blackwhite(text):
    os.system("")
    faded = ""
    red = 40
    green = 40
    blue = 40
    for line in text.splitlines():
        faded += f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n"
        if not red == 255 and not green == 255 and not blue == 255:
            red += 40
            green += 40
            blue += 40
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
            red -= 15
            if red < 0:
                red = 0
    return fade


def water(text):
    os.system("")
    fade = ""
    green = 30
    for line in text.splitlines():
        fade += f"\033[38;2;0;{green};255m{line}\033[0m\n"
        if not green == 255:
            green += 40
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


def pinkneon(text):
    os.system("")
    fade = ""
    blue = 255
    for line in text.splitlines():
        fade += f"\033[38;2;255;0;{blue}m{line}\033[0m\n"
        if not blue == 0:
            blue -= 20
            if blue < 0:
                blue = 0
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
                                                                                


{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            f"""  
{LINE}
[1] HTTP / HTTPS                                | [5] Remove duplicates
[2] SOCKS4                                      | [6] Scrape proxies
[3] SOCKS5                                      | [7] Settings 
[4] Check All
{LINE}"""
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
                                                                                


{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}  
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
                                            

                                                                

{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            f"""
Current Theme: {THEME.capitalize()}
{LINE}
[1] Cyan                                        | [5] Water
[2] Fire                                        | [6] pink neon
[3] Blackwhite                                  | [7] Exit
[4] Purple
{LINE}"""
        )
    )


def settings_menu(type1, type2):
    return (
        type1(
            f"""


            ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
            ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
            ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
            ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
            ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
            ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝        



{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            f"""  
{LINE}
[1] Theme                                       | [3] Default workers
[2] Sound Notifications                         | [4] Exit     
{LINE}                             
"""
        )
    )


def notifications_menu(type1, type2):
    return (
        type1(
            f"""


            ███╗   ██╗ ██████╗ ████████╗██╗███████╗██╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
            ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
            ██╔██╗ ██║██║   ██║   ██║   ██║█████╗  ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
            ██║╚██╗██║██║   ██║   ██║   ██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
            ██║ ╚████║╚██████╔╝   ██║   ██║██║     ██║╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
            ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                                                                            



{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            f"""
State: {NOTIFICATIONS} Theme: {NOTIFICATIONS_THEME.capitalize()}
{LINE}
[1] Notifications theme                           | [3] Exit
[2] Turn ON/OFF                                                          
{LINE}"""
        )
    )


def notifications_theme_menu(type1, type2):
    return (
        type1(
            f"""


            ███╗   ██╗ ██████╗ ████████╗██╗███████╗██╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
            ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
            ██╔██╗ ██║██║   ██║   ██║   ██║█████╗  ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
            ██║╚██╗██║██║   ██║   ██║   ██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
            ██║ ╚████║╚██████╔╝   ██║   ██║██║     ██║╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
            ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                                                                            



{Style.BRIGHT}> Created by Beelzebub2 {Style.BRIGHT}- {VERSION}
{Style.BRIGHT}> https://github.com/Beelzebub2{Style.RESET_ALL}                                                      
"""
        )
        + type2(
            f"""
State: {NOTIFICATIONS} Theme: {NOTIFICATIONS_THEME.capitalize()}
{LINE}
[1] Big-sur                           | [5] Pokemon
[2] Chime                             | [6] Sonic
[3] Mario                             | [7] Zelda
[4] Material                          | [8] Exit 
{LINE}"""
        )
    )


def new_update(type1, current_version):
    return type1(
        f"""
            ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
            ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
            ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
            ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
            ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
            ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
            BeelProxy {current_version} is outdated """
    )


def updated(type1):
    return type1(
        f"""

            ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██████╗ ██╗
            ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║
            ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║  ██║██║
            ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ██║  ██║╚═╝
            ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██████╔╝██╗
             ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝ ╚═╝
              
            Successfully updated Beelproxy!                                                       
"""
    )
