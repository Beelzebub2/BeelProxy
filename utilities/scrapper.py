import os
import asyncio
import time
from colorama import Fore, Style
from tqdm import tqdm
import httpx
import re


import utilities.sources as s
import utilities.updater as u


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def get_timestamp():
    current_time = time.localtime()
    timestamp = time.strftime("%H:%M:%S", current_time)
    return timestamp


async def fetchProxies(url, custom_regex, progress_bar):
    async with httpx.AsyncClient() as client:
        proxies = []  # List to collect the yielded proxies
        try:
            response = await client.get(url, timeout=5)
            proxylist = response.text
            proxylist = proxylist.replace("null", "")
            custom_regex = custom_regex.replace(
                "%ip%", r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            )
            custom_regex = custom_regex.replace("%port%", r"(\d{1,5})")
            proxy_count = 0  # Counter for the proxies collected
            for proxy in re.findall(re.compile(custom_regex), proxylist):
                proxies.append(f"{proxy[0]}:{proxy[1]}")
                proxy_count += 1
            progress_bar.update(
                proxy_count
            )  # Update progress bar with collected proxy count
            return proxies  # Return the list of collected proxies
        except Exception:
            return []


async def scrape_proxies(file, play, state):
    proxieslog = []
    u.set_console_title("Scraping proxies")
    startTime = time.time()

    proxy_sources = s.proxysources

    with tqdm(
        desc=f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[{ Fore.LIGHTMAGENTA_EX+ get_timestamp() + Fore.LIGHTBLUE_EX}]{Fore.RESET}{Style.BRIGHT} Scraping Proxies",
        unit=" proxies",
        ascii=True,
        smoothing=0.1,
        colour="GREEN",
    ) as pbar:
        tasks = []
        for url in proxy_sources:
            tasks.append(fetchProxies(url[0], url[1], pbar))

        for task in asyncio.as_completed(tasks):
            proxies = await task
            proxieslog.extend(proxies)

    proxies = list(set(proxieslog))
    with open(file, "w") as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    execution_time = time.time() - startTime
    repeated = len(proxieslog) - len(proxies)
    print(
        f"{Fore.LIGHTGREEN_EX}Done! Scraped {Fore.LIGHTMAGENTA_EX}{len(proxies):,}{Fore.LIGHTWHITE_EX} |{Fore.LIGHTYELLOW_EX} Removed {Fore.LIGHTRED_EX}{repeated:,}{Fore.RESET}{Fore.YELLOW} Repeated proxies {Fore.LIGHTWHITE_EX}in total => {Fore.BLUE}proxies.txt{Fore.RESET} in {round(execution_time, 2)}s"
    )
    play()
    input("Go back to the menu...")
