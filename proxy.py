from bs4 import BeautifulSoup
import requests

headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
}


def get_actual_proxy(proxies, used_proxies):
    # we have to change proxy each time when we get banned
    if len(proxies) == 0:
        proxies = get_proxies()
    print('looking for new proxy')
    for proxy in proxies:
        if try_proxy(proxy):
            if proxy not in used_proxies:
                print('got new one')
                actual_proxy = {
                "http": 'http://'+proxy,
                "https": 'http://'+proxy
                }
                return (actual_proxy, used_proxies)
        else:
            used_proxies.append(proxy)
            if len(proxies) == 0:
                proxies = get_proxies()

def try_proxy(proxy):
    try:
        url = 'https://httpbin.org/ip'
        proxies = {
            "http": 'http://'+proxy,
            "https": 'http://'+proxy
        }
        response = requests.get(url, proxies=proxies)
        print(response.json())
        return True
    except:
        print(f'bad proxy {proxy}')
        return False


def get_proxies():
    proxy_url = 'https://free-proxy-list.net/'
    soup = BeautifulSoup(requests.get(proxy_url).text, 'html.parser')
    proxies = []
    for proxy in soup.find(id='proxylisttable').tbody.find_all('tr'):
        proxies.append(
            f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
    return proxies


