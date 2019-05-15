from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import requests
import re
from selenium.webdriver.common.by import By
#https://stats.iforbet.pl/pl/soccer/competitions/premier-league,1528
#https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498
#https://stats.iforbet.pl/pl/soccer/competitions/bundesliga,1556
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

leagues = { 'https://stats.iforbet.pl/pl/soccer/competitions/bundesliga,1556',
            'https://stats.iforbet.pl/pl/soccer/competitions/premier-league,1528',
            'https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498',
            'https://stats.iforbet.pl/pl/soccer/competitions/laliga-santander,1507',
            'https://stats.iforbet.pl/pl/soccer/competitions/serie-a,1639',
            'https://stats.iforbet.pl/pl/soccer/competitions/ligue-1,2131',
            'https://stats.iforbet.pl/pl/soccer/competitions/liga-nos,1550',
            'https://stats.iforbet.pl/pl/soccer/competitions/eredivisie,1625'
            }
for x in leagues:
    page = requests.get(x)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_body = soup.find_all('body')

    urls = str(re.findall(r'<a[\s]+[^>]*?href[\s]?=[\s\"\']*(.*?)[\"\']*.*?>([^<]+|.*?)?<\/a>', str(table_body)))
    teams_forbet = re.findall("'\w+[\s]\w+'", urls, re.UNICODE)

driver = webdriver.Firefox()
driver.get("https://stats.iforbet.pl/pl/soccer/events")
sleep(5)
# on click action
html = driver.page_source
elements = driver.find_elements_by_xpath("//div[@class='leftMenu__item leftMenu__item--nested1' and @data-menu]/div[@class='leftMenu__subheader']")

urls = []
for e in elements:
    e.click()
    html = driver.page_source
    sleep(1)
    soup = BeautifulSoup(html, 'html.parser')
    urls = urls + soup.findAll('div', {"class": "leftMenu__content leftMenu__content--hidden opened"})
#
leagues = str(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', urls))
print(leagues)

