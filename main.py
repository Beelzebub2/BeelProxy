import os
import socket
import sys
import threading
import time
from colorama import Fore, Style
import requests
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import socks
import themes as t
import json
import chime

# Constant Variables
CONFIG_FILE = "config.json"
PROXY_FILE = "proxy_list.txt"
WORKING_PROXIES_FILE = "working_proxies.txt"
FAILED_PROXIES_FILE = "failed_proxies.txt"
DEFAULT_WORKERS = 50


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
        working_proxies_file,
        failed_proxies_file,
        workers,
        theme,
        state,
        noti_theme,
    ):
        self.proxy_file = proxy_file
        self.working_proxies_file = working_proxies_file
        self.failed_proxies_file = failed_proxies_file
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

    def save_to_file(self, proxy, filename):
        with open(filename, "a") as file:
            file.write(proxy + "\n")

    def clear(self):
        os.system("clear" if os.name == "posix" else "cls")

    def internet_access(self):
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
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
                f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} {Fore.LIGHTWHITE_EX}How many workers do you want? (recommended 50 - 100) default: 20\n"
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
            config_handler.set("Theme", chosen_theme)
            self.load_theme(getattr(t, chosen_theme))
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
            else:
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
        elif aws == 3:
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

    def check_all(self, proxy):
        http = mp.Process(target=self.check_http, args=(proxy,))
        socks4 = mp.Process(target=self.check_socks4, args=(proxy,))
        socks5 = mp.Process(target=self.check_socks5, args=(proxy,))
        http.start()
        socks4.start()
        socks5.start()

    def start(self, mode):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(mode, proxy) for proxy in self.proxy_list]

            try:
                for i, (proxy, future) in enumerate(
                    zip(self.proxy_list, futures), start=1
                ):
                    is_working = future.result()

                    if is_working:
                        self.save_to_file(proxy, self.working_proxies_file)
                    else:
                        self.save_to_file(proxy, self.failed_proxies_file)

                    if i % self.workers == 0:
                        print(
                            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[PROGRESS]{Fore.LIGHTCYAN_EX} Processed {round(self.working_count + self.failed_count / len(self.proxy_list), 2)}% of proxies - {Fore.GREEN}Working proxies: {self.working_count} {Fore.RED}Failed proxies: {self.failed_count}",
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
            print("Under development...")
            input()
            self.main()
        elif choice == "5":
            self.settings_menu_manager()
        else:
            print(
                f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{choice}" Is not a valid option...'
            )
            input()
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
        WORKING_PROXIES_FILE,
        FAILED_PROXIES_FILE,
        DEFAULT_WORKERS,
        theme,
        state,
        notifications_theme,
    )
    proxy_checker.main()
