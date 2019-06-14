from selenium import webdriver
from bs4 import BeautifulSoup
import Fortuna
import time
import unidecode
import database

bookie = "Lvbet"


def load_countries(sports_container):
    countries = []
    for a in sports_container:
        link_text = a.attrs['href']
        if link_text != '/pl/zaklady-bukmacherskie':
            print('Link: https://lvbet.pl' + link_text)
            country_site = 'https://lvbet.pl' + link_text
            countries.append(country_site)
    return countries


def load_leagues(countries, driver):
    counter = 0
    for x in countries:
        print(x)
        driver.get(x)
        page_content = BeautifulSoup(driver.page_source, "html.parser")
        leagues_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
        for y in leagues_container:
            link_text = y.attrs['href']
            if link_text != '/pl/zaklady-bukmacherskie':
                print('https://lvbet.pl' + link_text)
                league_site = 'https://lvbet.pl' + link_text
                league_id = counter
                league_name = "league " + str(counter)
                database.insert_league(bookie, league_id, league_name, league_site)
                counter = counter + 1


def load_matches(driver):
    football_leagues = database.get_leagues(bookie)
    counter = 0

    for x in football_leagues:
        link = x[1]
        print(link)
        driver.get(str(link))
        time.sleep(3)
        slash = link.rfind('/')
        text = link[slash + 1:]
        p = text.rfind('%')
        dash = text.rfind('-')
        if (p > 0):
            text2 = text[:p]
        else:
            text2 = text
        if text2.endswith('-'):
            text2 = text2[:-1]
            dash = text2.rfind('-')
        dashtext = text2[dash + 1:]
        newdashtext = ' ' + dashtext + ' '
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
            oddsarray = []
            oddsarray2 = []
            teams = y('div', class_='col-d-5 col-t-12 teams')
            odds = y('div', class_="col-d-2 col-md-3 col-sd-2 col-t-3 col-st-6 col-sm-12 ng-star-inserted")
            odds2 = y('div', class_="col-d-2 col-md-3 col-sd-2 col-t-3 col-st-6 col-sm-hidden ng-star-inserted")
            foramoment = unidecode.unidecode(teams[0].text.lower())
            if foramoment.find(newdashtext) > 0:
                slice = foramoment.find(newdashtext)
                slice = slice + len(dashtext)
            else:
                slice = foramoment.find(dashtext)
                slice = slice + len(dashtext)

            # wyłuskanie zespołów
            if teams[0].text[slice + 2:].count(' - ') > 1:
                index = teams[0].text[slice + 2:].find(' - ')
                slice = slice + index + 1
                index = teams[0].text[slice:].find(' ')
                slice = slice + index
            teams = teams[0].text[slice + 2:]
            dash = teams.find('-')
            if (teams[:dash].lstrip() != teams[dash + 2:].rstrip()):  # wykluczenie nazw zakladow na zwyciezcow
                team1 = teams[:dash - 2].lstrip()
                team2 = teams[dash + 2:].rstrip()
                if team1 != '':
                    database.insert_match(bookie, counter, team1, team2)
                    print(team1 + ' - ' + team2)
                try:
                    oddsarray = odds[0].text.split(' ')
                except:
                    try:
                        oddsarray = y('div', class_='col-d-6 col-t-9 col-st-12 ng-star-inserted')[0].text.split(' ')
                    except:
                        try:
                            oddsarray = y('div', class_='col-d-3 col-md-3 col-t-5 col-st-6 ng-star-inserted')[
                                0].text.split(' ')
                        except:
                            print('brak array')
                try:
                    oddsarray2 = odds2[0].text.split(' ')
                except:
                    print('brak array2')

                if oddsarray2 and oddsarray2 != ['']:
                    try:
                        home = oddsarray[1]
                        draw = oddsarray[3]
                        away = oddsarray[5]
                        hd = oddsarray2[1]
                        da = oddsarray2[3]
                        ha = oddsarray2[5]
                        print(home + ' ' + draw + ' ' + away + ' ' + hd + ' ' + da + ' ' + ha)
                        if database.is_match_in_db(bookie, counter):
                            if not database.compare_odds(bookie, counter, (float(home), float(draw), float(away), float(hd), float(da), float(ha))):
                                database.update_odds(bookie, counter, home, draw, away, hd, da, ha)

                        else:
                            database.insert_odds(bookie, counter, x[0], home, draw, away, hd, da, ha)
                            # zapis do bazy danych meczu (powiązanie z kursami po id)
                            database.insert_match(bookie, counter, team1, team2)
                    except:
                        print("Problem z listami odds")
                else:
                    try:
                        home = oddsarray[1]
                        draw = oddsarray[3]
                        away = oddsarray[5]
                        print(home + ' ' + draw + ' ' + away)
                        if database.is_match_in_db(bookie, counter):
                            if not database.compare_odds(bookie, counter, (float(home), float(draw), float(away))):
                                database.update_odds(bookie, counter, home, draw, away)

                        else:
                            database.insert_odds(bookie, counter, x[0], home, draw, away)
                            # zapis do bazy danych meczu (powiązanie z kursami po id)
                            database.insert_match(bookie, counter, team1, team2)
                    except:
                        print("Problem z listami odds bez odds2")
                counter = counter + 1


def get_driver():
    driver = webdriver.Firefox()
    return driver


def scrap():
    driver = get_driver()
    driver.get('https://lvbet.pl/pl/zaklady-bukmacherskie/5/pilka-nozna')
    page_content = BeautifulSoup(driver.page_source, "html.parser")
    sports_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
    countries = load_countries(sports_container)
    load_leagues(countries, driver)
    load_matches(driver)
    driver.close()


if __name__ == '__main__':
    load_matches(get_driver())
