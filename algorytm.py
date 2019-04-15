from bs4 import BeautifulSoup
from selenium import webdriver
import requests

driver = webdriver.Firefox()
driver.get("https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498/tables?cs_id=33385&type=fulltime")

html = driver.page_source
soup = BeautifulSoup(html)
out = soup.findAll('h5')
print(out)

# https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals
# https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498/tables?cs_id=33385&type=fulltime
#page_response = requests.get("https://www.efortuna.pl/pl/strona_glowna/statistiky/index.html")
#page_content = BeautifulSoup(page_response.content, "html.parser")


#for row in rows:
#    cols=row.find_all('td')
#    cols=[x.text.strip() for x in cols]
#    print (cols)
