from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import itertools
import requests
import re

driver = webdriver.Firefox()
driver.get("https://stats.iforbet.pl/pl/soccer/events")
sleep(5)
# on click action
html = driver.page_source
elements = driver.find_elements_by_xpath("//div[@class='leftMenu__item leftMenu__item--nested1' and @data-menu]/div[@class='leftMenu__subheader']")

def get_leagues():
    urls = list()
    #count = 0
    for e in elements:
        e.click()
        html = driver.page_source
        sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
        urls.append(str(soup.findAll('div', {"class": "leftMenu__content leftMenu__content--hidden opened"})))
        #if(count==3): break
        #else: count=count+1
    return urls

urls = get_leagues()
leagues = list()
for url in urls:
    leagues.append(re.findall('href=[\'"]?([^\'" >]+)', url))

for x in itertools.chain.from_iterable(leagues):
    page = requests.get(x)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_body = soup.find_all('body')
    name = str(re.findall(r'<a[\s]+[^>]*?href[\s]?=[\s\"\']*(.*?)[\"\']*.*?>([^<]+|.*?)?<\/a>', str(table_body)))
    teams_forbet = re.findall("'\w+[\s]\w+'", name, re.UNICODE)
    print(str(x)+": "+str(teams_forbet))

