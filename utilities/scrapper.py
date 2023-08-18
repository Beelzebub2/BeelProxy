import requests
import re
import threading
import random
import time
from colorama import Fore
import utilities.updater as u

PROXIES_FILE = "proxies.txt"


def proxy_scrape():
    proxieslog = []
    u.set_console_title("Scraping proxies")
    startTime = time.time()

    def fetchProxies(url, custom_regex):
        try:
            proxylist = requests.get(url, timeout=5).text
            proxylist = proxylist.replace("null", "")
            custom_regex = custom_regex.replace(
                "%ip%", r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            )
            custom_regex = custom_regex.replace("%port%", r"(\d{1,5})")
            for proxy in re.findall(re.compile(custom_regex), proxylist):
                proxieslog.append(f"{proxy[0]}:{proxy[1]}")
        except Exception:
            pass

    proxysources = [
        ["http://spys.me/proxy.txt", "%ip%:%port% "],
        [
            "http://www.httptunnel.ge/ProxyListForFree.aspx",
            ' target="_new">%ip%:%port%</a>',
        ],
        [
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json",
            '"ip":"%ip%","port":"%port%",',
        ],
        [
            "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
            '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%',
        ],
        [
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
            "%ip%:%port% (.*?){2}-.-S \\+",
        ],
        [
            "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            '%ip%", "type": "http", "port": %port%',
        ],
        [
            "https://www.sslproxies.org/",
            "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>",
        ],
        [
            "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all",
            "%ip%:%port%",
        ],
        [
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "%ip%:%port%",
        ],
        [
            "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
            "%ip%:%port%",
        ],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        [
            "https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json",
            '"ip": "%ip%",\n.*?"port": "%port%",',
        ],
    ]
    threads = [
        threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        for url in proxysources
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(PROXIES_FILE, "w") as f:
        for proxy in proxies:
            for _ in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")
    execution_time = time.time() - startTime
    print(
        f"{Fore.GREEN}Done! Scraped {Fore.MAGENTA}{len(proxies):,}{Fore.GREEN} in total => {Fore.RED}proxies.txt{Fore.RESET} in {round(execution_time, 2)}ms"
    )
    input("Go back to menu...")
