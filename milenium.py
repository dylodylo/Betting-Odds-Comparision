from selenium import webdriver
import time
from bs4 import BeautifulSoup
import database

bookie = "Milenium"
def ScrollSite(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrap():
    driver = webdriver.Firefox()
    driver.get('https://www.milenium.pl/zaklady-bukmacherskie')
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('.ui-button.ui-corner-all.ui-widget.ui-button-icon-only.ui-dialog-titlebar-close').click()
    except:
        print("brak x")
    driver.find_element_by_id("close_cookies").click()
    driver.execute_script('offer_sport_toggle(1)')
    time.sleep(1)
    element = driver.find_elements_by_xpath("//ul[@id='offer_league_sport_1']/li/span/input")
    counter = 1
    matchcounter = 0
    for e in element:
            e.click()
            time.sleep(1)
            ScrollSite(driver)
            page_content = BeautifulSoup(driver.page_source, "html.parser")
            match_container = page_content('td', class_='nameevent')
            odds_container = page_content('td', class_='c type_odds')
            league_container = page_content('th', class_='th_league_name')
            try:
                league = league_container[0].find('a').text
                colon = league.find(':')
                dash = league.find('-')
                league = league[dash+1:colon].lstrip()
                print(league)
                database.insert_league(bookie, counter, league)
                for match, odds in zip(match_container, odds_container):
                    dash = match.text.find('-')
                    t1 = match.text[:dash]
                    t2 = match.text[dash+1:]
                    space = t2.find('  ')
                    if space>0:
                        t2 = t2[:space]
                    print(t1 + ' - ' + t2)
                    database.insert_match(bookie, matchcounter, t1, t2)
                    matchcounter = matchcounter + 1
                    trueodds = odds.find_all('a')
                    if len(trueodds) == 6:
                        lastodds = []
                        for odd in trueodds:
                            if odd.text == '':
                                lastodds.append('1')
                            else:
                                lastodds.append(odd.text)
                        home = lastodds[0]
                        draw = lastodds[1]
                        away = lastodds[2]
                        hd = lastodds[3]
                        da = lastodds[4]
                        ha = lastodds[5]
                        print(home + ' ' + draw + ' ' + away + ' ' + hd + ' ' + da + ' ' + ha + ' ')
                        database.insert_odds(bookie, str(matchcounter), counter, home, draw, away, hd, da, ha)
                    else:
                        database.delete_league(bookie, str(counter))
                        matchcounter = matchcounter - 1
                        break
                print(counter)
                counter = counter + 1
            except AttributeError as ae:
                print("błąd z ")
                print(match_container[0].text)

            e.click()
            time.sleep(1)
    driver.close()
