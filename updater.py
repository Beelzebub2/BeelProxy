from base64 import b64decode
import json
import time
import requests
import os
import shutil
from zipfile import ZipFile
from colorama import Fore, Style
import themes as t


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
repository_owner = "Beelzebub2"
repository_name = "BeelProxy"
file_path = "config.json"
current_version = config_handler.get("Version")


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def set_console_title(title):
    system_type = os.name

    if system_type == "nt":  # Windows
        os.system("title " + title)
    else:  # Unix-like systems
        os.system("echo -ne '\033]0;" + title + "\007'")


def get_latest_version():
    response = requests.get(
        f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}"
    )

    if response.status_code == 200:
        content = response.json()
        content_data = content["content"]
        decoded_content = b64decode(content_data).decode("utf-8").strip()
        json_data = json.loads(decoded_content)
        version = json_data.get("Version")

        return version
    else:
        return None


online_version = get_latest_version()
theme = config_handler.get("Theme")
theme_mapping = {
    "fire": t.fire,
    "purple": t.purple,
    "cyan": t.cyan,
    "blackwhite": t.blackwhite,
    "water": t.water,
}
theme = theme_mapping.get(theme, t.fire)


def search_for_updates():
    try:
        clear()
        set_console_title("Checking For Updates. . .")

        if online_version != current_version:
            set_console_title("New Update Found!")
            print(t.new_update(theme, current_version))
            choice = input(
                f"{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}You want to update to the latest version? (Y to update): {Fore.RED}"
            )

            if choice.lower() == "y" or choice.lower() == "yes":
                print(f"{Fore.WHITE}\nUpdating. . .")
                set_console_title("Updating...")
                new = requests.get(
                    f"https://github.com/Beelzebub2/BeelProxy/archive/refs/heads/main.zip"
                )
                with open("BeelProxyr.zip", "wb") as zipfile:
                    zipfile.write(new.content)
                with ZipFile("BeelProxyr.zip", "r") as filezip:
                    filezip.extractall()
                os.remove("BeelProxyr.zip")
                cwd = os.getcwd() + "\\BeelProxy-main"
                shutil.copytree(cwd, os.getcwd(), dirs_exist_ok=True)
                shutil.rmtree(cwd)
                config_handler.set("Version", online_version)
                clear()
                print(t.updated(theme))
                set_console_title(f"Update Successfully Finished!")
                time.sleep(2)
                os.system("start.bat")
                os._exit(0)
    except KeyboardInterrupt:
        print(
            f"\n{Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
        )
