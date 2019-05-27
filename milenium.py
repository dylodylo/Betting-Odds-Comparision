from selenium import webdriver
import time
from bs4 import BeautifulSoup

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
#element = element.find_element_by_xpath("//input[@class='league'][@type='checkbox']")
counter = 1
for e in element:
        e.click()
        time.sleep(1)
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
        page_content = BeautifulSoup(driver.page_source, "html.parser")
        match_container = page_content('td', class_='nameevent')
        odds_container = page_content('td', class_='c type_odds')
        for match, odds in zip(match_container, odds_container):
            print(match.text)
            trueodds = odds.find_all('a')
            if len(trueodds) == 6:
                lastodds = []
                for odd in trueodds:
                    if odd.text == '':
                        lastodds.append('1')
                    else:
                        lastodds.append(odd.text)
                print(lastodds)
                print(lastodds[0] + ' ' + lastodds[1] + ' ' + lastodds[2] + ' ' + lastodds[3] + ' ' + lastodds[4] + ' ' + lastodds[5] + ' ')
        e.click()
        time.sleep(1)
        print(counter)
        counter = counter + 1
