import os
import socket
import sys
import threading
import time
from colorama import Fore, Style
import requests
from concurrent.futures import ThreadPoolExecutor
import socks
import themes as t
import json
import chime

# Constant Variables
CONFIG_FILE = "config.json"
PROXY_FILE = "proxy_list.txt"
WORKING_HTTP = "HTTP-HTTPS.txt"
WORKING_SOCKS4 = "SOCKS4.txt"
WORKING_SOCKS5 = "SOCKS5.txt"
DEFAULT_WORKERS = 20
VERSION = "v1.1"


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


class ProxyChecker:
    def __init__(
        self,
        proxy_file,
        WORKING_HTTP,
        WORKING_SOCKS4,
        WORKING_SOCKS5,
        workers,
        theme,
        state,
        noti_theme,
    ):
        self.proxy_file = proxy_file
        self.WORKING_HTTP = WORKING_HTTP
        self.WORKING_SOCKS4 = WORKING_SOCKS4
        self.WORKING_SOCKS5 = WORKING_SOCKS5
        self.workers = workers
        self.count_lock = threading.Lock()
        self.theme = theme
        self.state = state
        self.notification_theme = noti_theme
        self.menu = t.menu_theme(self.theme, self.theme)
        self.info_menu = t.info_theme(self.theme)
        self.theme_menu = t.theme_menu(self.theme, self.theme)
        self.notifications_menu = t.notifications_menu(
            self.theme, self.theme, self.state, self.notification_theme
        )
        self.notifications_theme_menu = t.notifications_theme_menu(
            self.theme, self.theme, self.state, self.notification_theme
        )
        self.settings_menu = t.settings_menu(self.theme, self.theme)
        chime.theme(self.notification_theme)
        self.set_console_title(f"BeelProxy {VERSION}")

    def save_to_file(self, proxy, filename):
        with open(filename, "a") as file:
            file.write(proxy + "\n")

    def set_console_title(self, title):
        system_type = os.name

        if system_type == "nt":  # Windows
            os.system("title " + title)
        else:  # Unix-like systems
            os.system("echo -ne '\033]0;" + title + "\007'")

    def remove_duplicates(self):
        input_file = input("File name.txt or File path: ")
        if not os.path.isfile(input_file):
            if self.state == "ON":
                chime.error()
            print(f"{Fore.LIGHTRED_EX + Style.BRIGHT}[ERROR] File not found")
        lines_seen = set()
        with open(input_file, "r") as inputf:
            lines = inputf.readlines()

        with open(input_file, "w") as output:
            for line in lines:
                if line not in lines_seen:
                    output.write(line)
                    lines_seen.add(line)
        if self.state == "ON":
            self.play_chime()
        print(
            f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}[FINISHED] {Fore.LIGHTWHITE_EX}Removed all duplicate lines from file"
        )
        input("Go back to menu...")
        if self.state == "ON":
            self.stop_event.set()
        self.main()

    def clear(self):
        os.system("clear" if os.name == "posix" else "cls")

    def internet_access(self):
        try:
            response = requests.get("https://www.google.com", timeout=10)
            return True
        except requests.ConnectionError or requests.exceptions.ReadTimeout:
            return False

    def play_chime_manager(self):
        if self.state == "OFF":
            return
        self.stop_event = threading.Event()
        while not self.stop_event.is_set():
            chime.success()
            time.sleep(3)

    def play_chime(self):
        notification = threading.Thread(target=self.play_chime_manager, daemon=True)
        notification.start()

    def worker_input(self):
        try:
            workers = input(
                f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} {Fore.LIGHTWHITE_EX}How many workers do you want? (recommended 20 - 50) default: 20\n"
            )
            if workers:
                self.workers = int(workers)
            else:
                self.workers = 20
        except ValueError:
            self.workers = 20

        self.clear()
        print(self.info_menu)
        if self.state == "ON":
            chime.info()
        print(
            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[START]{Fore.LIGHTWHITE_EX} Checking {len(self.proxy_list)} proxies{Fore.RESET} {Fore.LIGHTWHITE_EX} {Style.BRIGHT}With {self.workers} workers",
            end="\r",
        )

    def load_theme(self, theme):
        self.menu = t.menu_theme(theme, theme)
        self.info_menu = t.info_theme(theme)
        self.theme_menu = t.theme_menu(theme, theme)
        self.notifications_menu = t.notifications_menu(
            theme, theme, self.state, self.notification_theme
        )
        self.notifications_theme_menu = t.notifications_theme_menu(
            theme, theme, self.state, self.notification_theme
        )
        self.settings_menu = t.settings_menu(theme, theme)

    def theme_manager(self):
        theme_options = {
            "1": "cyan",
            "2": "fire",
            "3": "blackwhite",
            "4": "purple",
            "5": "water",
        }

        self.clear()
        print(self.theme_menu)
        aws = input("Choice: ")

        if aws in theme_options:
            chosen_theme = theme_options[aws]
            theme = getattr(t, chosen_theme)
            config_handler.set("Theme", chosen_theme)
            self.load_theme(theme)
        elif aws == "6":
            self.main()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()
            self.theme_manager()
        self.main()

    def notifications_theme_manager(self):
        theme_options = {
            "1": "big-sur",
            "2": "chime",
            "3": "mario",
            "4": "material",
            "5": "pokemon",
            "6": "sonic",
            "7": "zelda",
        }
        self.clear()
        print(self.notifications_theme_menu)
        aws = input("Choice: ")

        if aws in theme_options:
            chosen_theme = theme_options[aws]
            chime.theme(chosen_theme)
            self.notification_theme = chosen_theme
            config_handler.set("Notifications_theme", chosen_theme)
            self.load_theme(self.theme)
            self.clear()
            self.notifications_theme_manager()
        elif aws == "8":
            self.main()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()
            self.notifications_theme_manager()

    def notifications_menu_manager(self):
        self.clear()
        print(self.notifications_menu)
        aws = input("Choice: ")
        if aws == "1":
            self.notifications_theme_manager()
        if aws == "2":
            if self.state == "ON":
                self.state = "OFF"
                config_handler.set("Notifications", "OFF")
                self.load_theme(self.theme)
                self.clear()
                self.notifications_menu_manager()
                return
            self.state = "ON"
            config_handler.set("Notifications", "ON")
            self.load_theme(self.theme)
            self.clear()
            self.notifications_menu_manager()

        if aws == "3":
            self.main()

    def settings_menu_manager(self):
        print(self.settings_menu)
        aws = input("Choice: ")
        if aws == "1":
            self.theme_manager()
        elif aws == "2":
            self.notifications_menu_manager()
        elif aws == "3":
            self.main()

    def check_http(self, proxy):
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}",
        }

        try:
            response = requests.get(
                "http://www.example.com", proxies=proxies, timeout=10
            )
            if response.status_code == 200:
                with self.count_lock:
                    self.working_count += 1
                return True
            else:
                with self.count_lock:
                    self.failed_count += 1
                return False
        except requests.RequestException:
            with self.count_lock:
                self.failed_count += 1
            return False

    def check_socks4(self, proxy):
        try:
            proxy = proxy.split(":")
            socks.set_default_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
            socket.socket = socks.socksocket
        except ValueError:
            with self.count_lock:
                self.failed_count += 1
            return False

        try:
            response = requests.get("http://www.example.com", timeout=10)
            if response.status_code == 200:
                with self.count_lock:
                    self.socks4_working_count += 1
                return True
            else:
                with self.count_lock:
                    self.failed_count += 1
                return False
        except requests.RequestException:
            with self.count_lock:
                self.failed_count += 1
            return False

    def check_socks5(self, proxy):
        try:
            proxy = proxy.split(":")
            socks.set_default_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            socket.socket = socks.socksocket
        except ValueError:
            with self.count_lock:
                self.failed_count += 1
            return False

        try:
            response = requests.get("http://www.example.com", timeout=10)
            if response.status_code == 200:
                with self.count_lock:
                    self.socks5_working_count += 1
                return True
            else:
                with self.count_lock:
                    self.failed_count += 1
                return False
        except requests.RequestException:
            with self.count_lock:
                self.failed_count += 1
            return False

    def check_all(self):
        self.worker_input()
        self.clear()
        print(self.info_menu)
        if self.state == "ON":
            chime.info()
        print(
            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[START]{Fore.LIGHTWHITE_EX} Checking all proxies with all protocols{Fore.RESET}{Fore.LIGHTWHITE_EX} {Style.BRIGHT}With {self.workers} workers",
            end="\r",
        )
        self.start(self.check_http)
        self.clear()
        print(self.info_menu)
        self.start(self.check_socks4)
        self.clear()
        print(self.info_menu)
        self.start(self.check_socks5)
        self.clear()
        print(self.info_menu)
        if self.state == "ON":
            self.play_chime()
        print(
            f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}[FINISHED]{Fore.LIGHTWHITE_EX} Working proxies -{Fore.LIGHTCYAN_EX + Style.BRIGHT} HTTP/HTTPS: {self.working_count}{Fore.LIGHTBLUE_EX + Style.BRIGHT} Socks4: {self.socks4_working_count} {Fore.LIGHTMAGENTA_EX + Style.BRIGHT}Socks5: {self.socks5_working_count}{Fore.RESET}"
        )
        input("Go back to menu...")
        if self.state == "ON":
            self.stop_event.set()
        self.main()

    def start(self, mode):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(mode, proxy) for proxy in self.proxy_list]
            self.failed_count = 0
            try:
                for i, (proxy, future) in enumerate(
                    zip(self.proxy_list, futures), start=1
                ):
                    is_working = future.result()

                    if is_working:
                        if mode == self.check_http:
                            self.save_to_file(proxy, self.WORKING_HTTP)
                        elif mode == self.check_socks4:
                            self.save_to_file(proxy, self.WORKING_SOCKS4)
                        elif mode == self.check_socks5:
                            self.save_to_file(proxy, self.WORKING_SOCKS5)

                    if i % self.workers == 0:
                        progress_mode_mapping = {
                            self.check_http: (self.working_count, "HTTP/HTTPS"),
                            self.check_socks4: (self.socks4_working_count, "SOCKS4"),
                            self.check_socks5: (self.socks5_working_count, "SOCKS5"),
                        }
                        (
                            self.working_proxies,
                            Current_protocol,
                        ) = progress_mode_mapping.get(mode, self.working_count)

                        print(
                            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[PROGRESS]{Fore.LIGHTWHITE_EX + Style.BRIGHT} Protocol: {Current_protocol}{Fore.LIGHTCYAN_EX} Processed {round(i / len(self.proxy_list) * 100, 2)}% of proxies - {Fore.GREEN}Working proxies: {self.working_proxies} {Fore.RED}Failed proxies: {self.failed_count}",
                            end="\r",
                            flush=True,
                        )

            except KeyboardInterrupt:
                for future in futures:
                    future.cancel()
                if self.state == "ON":
                    chime.info()
                print(
                    f"\n\n{Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
                )
                input(f"\n{Fore.LIGHTWHITE_EX + Style.BRIGHT}Go back to menu...")
                self.main()

    def main(self):
        try:
            self.clear()
            with open(self.proxy_file, "r") as file:
                self.proxy_list = file.read().splitlines()

            self.working_count = 0
            self.failed_count = 0
            self.socks4_working_count = 0
            self.socks5_working_count = 0
            internet_access = self.internet_access()
            if not internet_access:
                self.clear()
                if self.state == "ON":
                    chime.error()
                print(self.info_menu)
                input(f"{Style.BRIGHT}{Fore.RED}[ERROR] You need internet access")
                return

            print(self.menu)
            aws = input("Choice: ")
            self.handle_menu_choice(aws)

        except KeyboardInterrupt:
            print(
                f"\n{Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
            )
            if self.state == "ON":
                chime.info(sync=True)
            sys.exit(0)

    def handle_menu_choice(self, choice):
        if choice == "1":
            self.worker_input()
            self.start(self.check_http)
        elif choice == "2":
            self.worker_input()
            self.start(self.check_socks4)
        elif choice == "3":
            self.worker_input()
            self.start(self.check_socks5)
        elif choice == "4":
            self.check_all()
        elif choice == "5":
            self.remove_duplicates()
        elif choice == "6":
            self.clear()
            self.settings_menu_manager()
        else:
            print(
                f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{choice}" Is not a valid option...'
            )
            input()
            self.main()
        self.clear()
        print(self.info_menu)
        print(
            f"{Fore.LIGHTGREEN_EX}[FINISHED] {Fore.LIGHTWHITE_EX} Total proxies: {len(self.proxy_list)} {Fore.GREEN}Total Working proxies: { self.working_proxies} {Fore.RED}Failed proxies: {self.failed_count}{Fore.RESET}"
        )
        self.play_chime()
        input(f"\n{Fore.LIGHTWHITE_EX + Style.BRIGHT}Go back to menu...")
        self.stop_event.set()
        self.main()


if __name__ == "__main__":
    config_handler = JSONConfigHandler(CONFIG_FILE)
    theme = config_handler.get("Theme")
    theme_mapping = {
        "fire": t.fire,
        "purple": t.purple,
        "cyan": t.cyan,
        "blackwhite": t.blackwhite,
        "water": t.water,
    }
    theme = theme_mapping.get(theme, t.fire)
    state = config_handler.get("Notifications")
    notifications_theme = config_handler.get("Notifications_theme")
    proxy_checker = ProxyChecker(
        PROXY_FILE,
        WORKING_HTTP,
        WORKING_SOCKS4,
        WORKING_SOCKS5,
        DEFAULT_WORKERS,
        theme,
        state,
        notifications_theme,
    )
    proxy_checker.main()
