import os
import sys
import shutil
import socket
import threading
import time
import json
import requests
import socks
import importlib
from concurrent.futures import ThreadPoolExecutor


from colorama import Fore, Style
import chime
from tqdm import tqdm

import utilities.updater as u
import utilities.themes as t
import utilities.scrapper as s


# Constant Variables
CONFIG_FILE = "config.json"
PROXY_FILE = "proxy_list.txt"
WORKING_HTTP = "HTTP-HTTPS.txt"
WORKING_SOCKS4 = "SOCKS4.txt"
WORKING_SOCKS5 = "SOCKS5.txt"
SHOW_PROGRESS = 5  # time (seconds) between each progress update (not precise)


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
        if u.search_for_updates():
            try:
                python = sys.executable
                os.execl(python, python, *sys.argv)
            except KeyboardInterrupt:
                print(
                    f"\n\n{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
                )
                sys.exit()

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
        self.notifications_menu = t.notifications_menu(self.theme, self.theme)
        self.notifications_theme_menu = t.notifications_theme_menu(
            self.theme, self.theme
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
        def remove_duplicates_from_file(file_path, default=False):
            start_time = time.time()
            lines_seen = set()
            total_duplicates_removed = 0

            with open(file_path, "r") as inputf:
                lines = inputf.readlines()

            with open(file_path, "w") as output:
                if default:
                    lines_iterator = tqdm(
                        enumerate(lines),
                        total=len(lines),
                        desc=f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{Fore.LIGHTMAGENTA_EX + self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET}{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Cleaning: {file_path}",
                        unit=" lines",
                        bar_format="{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}{postfix}]",
                        ncols=round(self.console_width * 0.9),
                        ascii=True,
                        smoothing=0.1,
                        colour="GREEN",
                    )
                    for idx, line in lines_iterator:
                        if line not in lines_seen:
                            output.write(line)
                            lines_seen.add(line)
                        else:
                            total_duplicates_removed += 1
                else:
                    for line in lines:
                        if line not in lines_seen:
                            output.write(line)
                            lines_seen.add(line)
                        else:
                            total_duplicates_removed += 1

            end_time = time.time()
            elapsed_time = end_time - start_time

            timestamp = self.get_timestamp()
            if not default:
                if self.state == "ON":
                    self.play_chime()
                print(
                    f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{Fore.LIGHTMAGENTA_EX + timestamp + Fore.LIGHTBLUE_EX}]{Fore.RESET} "
                    f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}[FINISHED] {Fore.LIGHTWHITE_EX}Removed {total_duplicates_removed:,} duplicate lines from {file_path} in {elapsed_time:.2f} seconds."
                )
                input("Go back to menu...")
                if self.state == "ON":
                    self.stop_event.set()
            else:
                self.duplicate_stats.append(
                    f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{Fore.LIGHTMAGENTA_EX + timestamp + Fore.LIGHTBLUE_EX}]{Fore.RESET} "
                    f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}[FINISHED] {Fore.LIGHTWHITE_EX}Removed {total_duplicates_removed:,} duplicate lines from {file_path} in {elapsed_time:.2f} seconds."
                )

        default_files = [WORKING_HTTP, WORKING_SOCKS4, WORKING_SOCKS5, PROXY_FILE]

        input_file = input(
            f"File name.txt or File path {Fore.BLUE}[{Fore.LIGHTMAGENTA_EX}For output files cleanup click enter{Fore.BLUE}]: "
        )

        if input_file and not os.path.isfile(input_file):
            if self.state == "ON":
                self.play_chime(error=True)
            print(f"{Fore.LIGHTRED_EX + Style.BRIGHT}[ERROR] File not found")
            input("Go back to menu...")
            return

        if input_file:
            remove_duplicates_from_file(input_file)
        else:
            for default_file in default_files:
                remove_duplicates_from_file(default_file, True)
            if self.state == "ON":
                self.play_chime()
            self.clear()
            print(self.info_menu)
            print("\n" + "\n".join(self.duplicate_stats))
            input("Go back to menu...")
            if self.state == "ON":
                self.stop_event.set()

        self.main()

    def clear(self):
        os.system("clear" if os.name == "posix" else "cls")

    def get_timestamp(self):
        current_time = time.localtime()
        timestamp = time.strftime("%H:%M:%S", current_time)
        return timestamp

    def internet_access(self):
        try:
            try:
                socks.set_default_proxy()
                socket.socket = socket.socket
            except:
                pass
            response = requests.get("https://www.google.com", timeout=10)
            return True
        except (requests.ConnectionError, requests.exceptions.ReadTimeout):
            try:
                response = requests.get("https://www.example.com", timeout=10)
                return True
            except (
                requests.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.ConnectionError,
            ):
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

    def worker_input(self, settings=None):
        if settings:
            try:
                workers = input(
                    f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} {Fore.LIGHTWHITE_EX}New workers default? Current: {self.workers}. {Style.BRIGHT + Fore.LIGHTYELLOW_EX}In [check all] function workers will be 3 times this\n"
                )
                if workers:
                    config_handler.set("Workers", int(workers))
                    self.workers = int(workers)
                else:
                    if self.state == "ON":
                        chime.error()
                    input(f"{Fore.RED + Style.BRIGHT}[ERROR] invalid input...")
                    self.worker_input(True)
            except ValueError:
                if self.state == "ON":
                    chime.error()
                input(f"{Fore.RED + Style.BRIGHT}[ERROR] invalid input...")
                self.worker_input(True)
            return
        try:
            workers = input(
                f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} {Fore.LIGHTWHITE_EX}How many workers do you want? (try 100 - 1000) default: {self.workers}. {Style.BRIGHT + Fore.LIGHTYELLOW_EX}In [check all] function workers will be 3 times this\n"
            )
            if workers:
                self.workers = int(workers)
            else:
                self.workers = self.workers
        except ValueError:
            self.workers = self.workers

        self.clear()
        print(self.info_menu)
        if self.state == "ON":
            chime.info()
        print(
            f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Style.BRIGHT}{Fore.LIGHTGREEN_EX}[START]{Fore.LIGHTWHITE_EX} Checking {len(self.proxy_list):,} proxies{Fore.RESET} {Fore.LIGHTWHITE_EX} {Style.BRIGHT}With {self.workers:,} workers",
            end="\r",
        )

    def load_theme(self, theme):
        importlib.reload(t)
        self.menu = t.menu_theme(theme, theme)
        self.info_menu = t.info_theme(theme)
        self.theme_menu = t.theme_menu(theme, theme)
        self.notifications_menu = t.notifications_menu(theme, theme)
        self.notifications_theme_menu = t.notifications_theme_menu(theme, theme)
        self.settings_menu = t.settings_menu(theme, theme)

    def theme_manager(self):
        theme_options = {
            "1": "cyan",
            "2": "fire",
            "3": "blackwhite",
            "4": "purple",
            "5": "water",
            "6": "pinkneon",
        }

        self.clear()
        print(self.theme_menu)
        aws = input(f"{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: ")

        if aws in theme_options:
            chosen_theme = theme_options[aws]
            theme = getattr(t, chosen_theme)
            config_handler.set("Theme", chosen_theme)
            self.load_theme(theme)
        elif aws == "7":
            self.main()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()
            self.theme_manager()
        self.theme_manager()

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
        aws = input(f"{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: ")

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
        notifications_menu_options = {
            "1": self.notifications_theme_manager,
            "2": self.toggle_notifications,
            "3": self.main,
        }

        self.clear()
        print(self.notifications_menu)
        aws = input(f"{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: ")

        selected_action = notifications_menu_options.get(aws)

        if selected_action:
            selected_action()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()

        self.main()

    def toggle_notifications(self):
        if self.state == "ON":
            self.state = "OFF"
            config_handler.set("Notifications", "OFF")
        else:
            self.state = "ON"
            config_handler.set("Notifications", "ON")

        self.load_theme(self.theme)
        self.clear()
        self.notifications_menu_manager()

    def settings_menu_manager(self):
        settings_menu_options = {
            "1": self.theme_manager,
            "2": self.notifications_menu_manager,
            "3": lambda: self.worker_input(True),
            "4": self.main,
        }

        print(self.settings_menu)
        aws = input(f"{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: ")

        selected_action = settings_menu_options.get(aws)

        if selected_action:
            selected_action()
        else:
            print(f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{aws}" Is not a valid option...')
            input()
            self.settings_menu_manager()

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
                self.socks4_failed_count += 1
            return False

        try:
            response = requests.get("http://www.example.com", timeout=10)
            if response.status_code == 200:
                with self.count_lock:
                    self.socks4_working_count += 1
                return True
            else:
                with self.count_lock:
                    self.socks4_failed_count += 1
                return False
        except requests.RequestException:
            with self.count_lock:
                self.socks4_failed_count += 1
            return False

    def check_socks5(self, proxy):
        try:
            proxy = proxy.split(":")
            socks.set_default_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            socket.socket = socks.socksocket
        except ValueError:
            with self.count_lock:
                self.socks5_failed_count += 1
            return False

        try:
            response = requests.get("http://www.example.com", timeout=10)
            if response.status_code == 200:
                with self.count_lock:
                    self.socks5_working_count += 1
                return True
            else:
                with self.count_lock:
                    self.socks5_failed_count += 1
                return False
        except requests.RequestException:
            with self.count_lock:
                self.socks5_failed_count += 1
            return False

    def check_all(self):
        self.worker_input()
        start_time = time.time()
        with ThreadPoolExecutor(3) as executor:
            executor.submit(self.start, self.check_http)
            executor.submit(self.start, self.check_socks4)
            executor.submit(self.start, self.check_socks5)
        end_time = time.time()
        self.clear()
        print(self.info_menu)
        if self.state == "ON":
            self.play_chime()
        elapsed_time = end_time - start_time
        print(
            f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Fore.LIGHTGREEN_EX + Style.BRIGHT}[FINISHED]{Fore.LIGHTWHITE_EX} Working proxies -{Fore.LIGHTCYAN_EX + Style.BRIGHT} HTTP/HTTPS: {self.working_count:,}{Fore.LIGHTBLUE_EX + Style.BRIGHT} Socks4: {self.socks4_working_count:,} {Fore.LIGHTMAGENTA_EX + Style.BRIGHT}Socks5: {self.socks5_working_count:,}{Fore.RESET} in {elapsed_time:.2f} seconds"
        )
        input("Go back to menu...")
        if self.state == "ON":
            self.stop_event.set()
        self.main()

    def start(self, mode):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(mode, proxy) for proxy in self.proxy_list]
            try:
                last_progress_time = time.time()
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
                    current_time = time.time()

                    if current_time - last_progress_time >= SHOW_PROGRESS:
                        last_progress_time = current_time
                        progress_mode_mapping = {
                            self.check_http: (
                                self.working_count,
                                "HTTP/HTTPS",
                                self.failed_count,
                            ),
                            self.check_socks4: (
                                self.socks4_working_count,
                                "SOCKS4",
                                self.socks4_failed_count,
                            ),
                            self.check_socks5: (
                                self.socks5_working_count,
                                "SOCKS5",
                                self.socks5_failed_count,
                            ),
                        }
                        (
                            self.working_proxies,
                            Current_protocol,
                            Current_failed,
                        ) = progress_mode_mapping.get(mode, self.working_count)
                        progress_message = (
                            f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} "
                            f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}[PROGRESS]{Fore.LIGHTWHITE_EX + Style.BRIGHT} Protocol: {Current_protocol}"
                            f"{Fore.LIGHTCYAN_EX} Processed {round(i / len(self.proxy_list) * 100, 2)}% of proxies - "
                            f"{Fore.GREEN}Working proxies: {self.working_proxies:,} {Fore.RED}Failed proxies: {Current_failed:,}"
                        )
                        print(" " * self.console_width, end="\r")
                        print(
                            progress_message,
                            end="\r",
                            flush=True,
                        )

            except KeyboardInterrupt:
                for future in futures:
                    future.cancel()
                if self.state == "ON":
                    chime.info()
                print(
                    f"\n\n{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
                )
                sys.exit()

    def read_proxy_file(self):
        with open(self.proxy_file, "r") as file:
            self.proxy_list = file.read().splitlines()

    def main(self):
        try:
            self.clear()
            self.read_proxy_file()
            self.working_count = 0
            self.failed_count = 0
            self.socks4_working_count = 0
            self.socks5_working_count = 0
            self.socks4_failed_count = 0
            self.socks5_failed_count = 0
            self.duplicate_stats = []
            self.console_width = shutil.get_terminal_size().columns
            internet_access = self.internet_access()
            if not internet_access:
                self.clear()
                if self.state == "ON":
                    chime.error()
                print(self.info_menu)
                input(
                    f"{Style.BRIGHT}{Fore.RED}[ERROR] You need internet access or a better network connection"
                )
                self.main()
                return

            print(self.menu)
            aws = input(
                f"{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: "
            )
            self.handle_menu_choice(aws)

        except KeyboardInterrupt:
            print(
                f"\n{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Style.BRIGHT + Fore.LIGHTBLUE_EX}KeyboardInterrupt detected. Exiting gracefully.{Fore.RESET}"
            )
            if self.state == "ON":
                chime.info(sync=True)
            sys.exit(0)

    def handle_menu_choice(self, choice):
        menu_actions = {
            "1": (
                self.worker_input,
                self.read_proxy_file,
                lambda: self.start(self.check_http),
            ),
            "2": (
                self.worker_input,
                self.read_proxy_file,
                lambda: self.start(self.check_socks4),
            ),
            "3": (
                self.worker_input,
                self.read_proxy_file,
                lambda: self.start(self.check_socks5),
            ),
            "4": (self.check_all, self.read_proxy_file),
            "5": (self.remove_duplicates, self.main),
            "6": (s.proxy_scrape, self.main),
            "7": (self.clear, self.settings_menu_manager),
        }

        action = menu_actions.get(choice)

        if action:
            for func in action:
                func()
        else:
            print(
                f'{Style.BRIGHT} {Fore.LIGHTRED_EX}"{choice}" Is not a valid option...'
            )
            input()
            self.main()

        self.clear()
        print(self.info_menu)
        print(
            f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ self.get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET} {Fore.LIGHTGREEN_EX}[FINISHED] {Fore.LIGHTWHITE_EX} Total proxies: {len(self.proxy_list):,} {Fore.GREEN}Total Working proxies: { self.working_proxies:,} {Fore.RED}Failed proxies: {self.failed_count:,}{Fore.RESET}"
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
        "pinkneon": t.pinkneon,
    }
    THEME = theme_mapping.get(theme, t.fire)
    STATE = config_handler.get("Notifications")
    VERSION = config_handler.get("Version")
    NOTIFICATION_THEME = config_handler.get("Notifications_theme")
    DEFAULT_WORKERS = config_handler.get("Workers")  # find the best number for your cpu
    proxy_checker = ProxyChecker(
        PROXY_FILE,
        WORKING_HTTP,
        WORKING_SOCKS4,
        WORKING_SOCKS5,
        DEFAULT_WORKERS,
        THEME,
        STATE,
        NOTIFICATION_THEME,
    )
    proxy_checker.main()
