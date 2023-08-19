proxysources = [
    ("http://spys.me/proxy.txt", "%ip%:%port% "),
    (
        "http://www.httptunnel.ge/ProxyListForFree.aspx",
        ' target="_new">%ip%:%port%</a>',
    ),
    (
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json",
        '"ip":"%ip%","port":"%port%",',
    ),
    (
        "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
        '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%',
    ),
    (
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
        "%ip%:%port% (.*?){2}-.-S \\+",
    ),
    (
        "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
        '%ip%", "type": "http", "port": %port%',
    ),
    (
        "https://www.sslproxies.org/",
        "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>",
    ),
    (
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all",
        "%ip%:%port%",
    ),
    (
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "%ip%:%port%",
    ),
    (
        "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
        "%ip%:%port%",
    ),
    ("https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'),
    (
        "https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json",
        '"ip": "%ip%",\n.*?"port": "%port%",',
    ),
    ("https://www.proxy-list.download/api/v1/get?type=http", "%ip%:%port%"),
    ("https://www.proxy-list.download/api/v1/get?type=https", "%ip%:%port%"),
    ("https://free-proxy-list.net/anonymous-proxy.html", "%ip%:%port%"),
    ("https://www.us-proxy.org/", "%ip%:%port%"),
    ("https://www.sslproxies.org/", "%ip%:%port%"),
    ("https://www.socks-proxy.net/", "%ip%:%port%"),
]


def source_checker(proxy_source_url, proxy_format):
    # Replace %ip% and %port% placeholders with actual IP and port
    proxy_url = proxy_source_url.replace("%ip%", "proxy_ip_here").replace(
        "%port%", "proxy_port_here"
    )

    try:
        response = requests.get(proxy_url, timeout=10)
        if response.status_code == 200:
            print(f"Proxy source {proxy_source_url} is working.")
            return True
        else:
            print(
                f"Proxy source {proxy_source_url} returned a non-200 status code: {response.status_code}"
            )
    except requests.RequestException as e:
        print(f"Proxy source {proxy_source_url} is not working. Error: {e}")


if __name__ == "__main__":
    import requests

    new_list = []
    for p, p_format in proxysources:
        if source_checker(p, p_format):
            new_list.append((p, p_format))
    print(new_list)
