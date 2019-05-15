from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import Fortuna
import time
import requests
import unidecode

# specify the url
urlpage = 'https://lvbet.pl/pl/zaklady-bukmacherskie/5/pilka-nozna'
print(urlpage)
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()
driver.get(urlpage)
time.sleep(3)


#parse html
page_content = BeautifulSoup(driver.page_source, "html.parser")
sports_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')

football_countries = []
counter = 0
for a in sports_container:
    link_text = a.attrs['href']
    if link_text != '/pl/zaklady-bukmacherskie':
        print('Link: https://lvbet.pl' + link_text)
        a_league_site = 'https://lvbet.pl' + link_text
        a_league_id = counter
        a_league_name = "league " + str(counter)
        country = Fortuna.League_Fortuna(a_league_id, a_league_name, a_league_site)
        football_countries.append(country)
        counter =+1

football_leagues = []
countries = football_countries
for x in countries:
    counter = 0
    print(x.league_site)
    driver.get(str(x.league_site))
    page_content = BeautifulSoup(driver.page_source, "html.parser")
    leagues_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
    for y in leagues_container:
        link_text = y.attrs['href']
        if link_text != '/pl/zaklady-bukmacherskie':
            print('https://lvbet.pl' + link_text)
            a_league_site = 'https://lvbet.pl' + link_text
            a_league_id = counter
            a_league_name = "league " + str(counter)
            country = Fortuna.League_Fortuna(a_league_id, a_league_name, a_league_site)
            football_leagues.append(country)
            counter = counter +1


for x in football_leagues:
    link = x.league_site
    print(link)
    driver.get(str(link))
    time.sleep(3)
    slash = link.rfind('/')
    text = link[slash+1:]
    p = text.rfind('%')
    text2 = text[:p]
    text_array = list(text2)
    if '-' in text_array:
        isdash = 1
    else:
        isdash = 0
    while isdash == 1:
        index = text_array.index('-')
        text_array[index] = ' '
        if '-' in text_array:
            isdash = 1
        else:
            isdash = 0
    newtext = "".join(text_array)

    page_content = BeautifulSoup(driver.page_source, "html.parser")
    matches_container = page_content('div', class_='row lv-table-entry')
    for y in matches_container:
        teams = y('div', class_='col-d-5 col-t-12 teams')
        teams3 = y.find_all('p')
        odds = y('div', class_="col-d-2 col-md-3 col-sd-2 col-t-3 col-st-6 col-sm-12 ng-star-inserted")
        odds2 = y('div', class_="col-d-2 col-md-3 col-sd-2 col-t-3 col-st-6 col-sm-hidden ng-star-inserted")
        foramoment = unidecode.unidecode(teams[0].text.lower())
        slice = foramoment.find(newtext)
        slice = slice+len(newtext)
        try:
            oddsarray = odds[0].text.split(' ')
            print(teams[0].text[slice+2:] + oddsarray[1] + ' ' + oddsarray[3] + ' ' + oddsarray[5] + ' ' + odds2[0].text)
        except:
            print("Problem z listami odds")