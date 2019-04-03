from bs4 import BeautifulSoup
import requests

def get_actual_proxy():
    # we have to change proxy each time when we get banned
    used_proxies = set()
    print(used_proxies)
    proxies = get_proxies()
    for proxy in proxies:
        print('looking for new proxy')
        if try_proxy(proxy):
            if proxy not in used_proxies:
                print('got new one')
                actual_proxy = proxy
                return actual_proxy


def try_proxy(proxy):
    try:
        r = requests.get('https://google.com',
                     proxies={"http": "http://"+proxy, "https": "http://"+proxy}, timeout=10)
        print(r.text())
        return True
    except:
        print(f'bad proxy {proxy}')
        return False


def get_proxies():
    proxy_url = 'https://free-proxy-list.net/'
    soup = BeautifulSoup(requests.get(proxy_url).text, 'html.parser')
    proxies = set()
    for proxy in soup.find(id='proxylisttable').tbody.find_all('tr'):
        proxies.add(
            f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
    return proxies

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