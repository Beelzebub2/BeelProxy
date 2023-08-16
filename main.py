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
        self, proxy_file, working_proxies_file, failed_proxies_file, workers, theme
    ):
        self.proxy_file = proxy_file
        self.working_proxies_file = working_proxies_file
        self.failed_proxies_file = failed_proxies_file
        self.workers = workers
        self.count_lock = threading.Lock()
        self.theme = theme
        self.menu = t.menu_theme(self.theme, self.theme)
        self.info_menu = t.info_theme(self.theme)
        self.theme_menu = t.theme_menu(self.theme, self.theme)
        chime.theme("material")

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
        chime.info()
        print(
            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[START]{Fore.LIGHTWHITE_EX} Checking {len(self.proxy_list)} proxies{Fore.RESET} {Fore.LIGHTWHITE_EX} {Style.BRIGHT}With {self.workers} workers",
            end="\r",
        )

    def load_theme(self, theme):
        self.menu = t.menu_theme(theme, theme)
        self.info_menu = t.info_theme(theme)
        self.theme_menu = t.theme_menu(theme, theme)

    def theme_manager(self):
        self.clear()
        print(self.theme_menu)
        aws = input("Choice: ")
        if aws == "1":
            config_handler.set("Theme", "cyan")
            self.load_theme(t.cyan)
        elif aws == "2":
            config_handler.set("Theme", "fire")
            self.load_theme(t.fire)
        elif aws == "3":
            config_handler.set("Theme", "blackwhite")
            self.load_theme(t.blackwhite)
        elif aws == "4":
            config_handler.set("Theme", "purple")
            self.load_theme(t.purple)
        elif aws == "5":
            config_handler.set("Theme", "water")
            self.load_theme(t.water)
        elif aws == "6":
            self.main()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()
            self.theme_manager()
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
                chime.error()
                print(self.info_menu)
                input(f"{Style.BRIGHT}{Fore.RED}[ERROR] You need internet access")
                return

            print(self.menu)
            aws = input("Choice: ")
            self.clear()
            print(self.info_menu)

            if os.path.exists(self.working_proxies_file):
                os.remove(self.working_proxies_file)
            if os.path.exists(self.failed_proxies_file):
                os.remove(self.failed_proxies_file)

            if aws == "1":
                self.worker_input()
                self.start(self.check_http)
            elif aws == "2":
                self.worker_input()
                self.start(self.check_socks4)
            elif aws == "3":
                self.worker_input()
                self.start(self.check_socks5)
            elif aws == "4":
                self.theme_manager()
            else:
                print(
                    f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...'
                )
                input()
                self.main()

            self.clear()
            print(self.info_menu)
            print(
                f"{Fore.LIGHTGREEN_EX}[FINISHED] {Fore.LIGHTWHITE_EX} Total proxies: {len(self.proxy_list)} {Fore.GREEN}Total Working proxies: {self.working_count} {Fore.RED}Failed proxies: {self.failed_count}{Fore.RESET}"
            )
            self.play_chime()
            input(f"\n{Fore.LIGHTWHITE_EX + Style.BRIGHT}Go back to menu...")
            self.stop_event.set()
            self.main()
        except KeyboardInterrupt:
            chime.info()
            print(
                f"\n{Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
            )
            sys.exit(0)


if __name__ == "__main__":
    config_file = "config.json"
    config_handler = JSONConfigHandler(config_file)
    theme = config_handler.get("Theme")
    theme_mapping = {
        "fire": t.fire,
        "purple": t.purple,
        "cyan": t.cyan,
        "blackwhite": t.blackwhite,
        "water": t.water,
    }
    if theme in theme_mapping:
        theme = theme_mapping[theme]
    else:
        theme = t.fire

    proxy_checker = ProxyChecker(
        "proxy_list.txt", "working_proxies.txt", "failed_proxies.txt", 50, theme
    )
    proxy_checker.main()
