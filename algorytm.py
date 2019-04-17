from bs4 import BeautifulSoup
import requests
import re
#https://stats.iforbet.pl/pl/soccer/competitions/premier-league,1528
#https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498
#https://stats.iforbet.pl/pl/soccer/competitions/bundesliga,1556

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
    print (teams_forbet)

#begin_pos = (str(table_body).find(str1))
#end_pos = (str(table_body).find(str2))
#print (begin[begin_pos:end_pos])
#print(soup.prettify())



#from bs4 import BeautifulSoup
#from selenium import webdriver
#import requests

#driver = webdriver.Firefox()
#driver.get("https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498/tables?cs_id=33385&type=fulltime")

#html = driver.page_source
#soup = BeautifulSoup(html)
#out = soup.findAll('h5')
#print(out)

# https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals
# https://stats.iforbet.pl/pl/soccer/competitions/lotto-ekstraklasa,1498/tables?cs_id=33385&type=fulltime
#page_response = requests.get("https://www.efortuna.pl/pl/strona_glowna/statistiky/index.html")
#page_content = BeautifulSoup(page_response.content, "html.parser")


#for row in rows:
#    cols=row.find_all('td')
#    cols=[x.text.strip() for x in cols]
#    print (cols)
