from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.get('https://www.milenium.pl/zaklady-bukmacherskie')
time.sleep(5)
driver.find_element_by_css_selector('.ui-button.ui-corner-all.ui-widget.ui-button-icon-only.ui-dialog-titlebar-close').click()
driver.find_element_by_id("close_cookies").click()
driver.execute_script('offer_sport_toggle(1)')
element = driver.find_elements_by_xpath("//input[@class='league'][@type='checkbox']")
#element = driver.find_element_by_xpath("//span[input[@id='l4761']]")
counter = 1
try:
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
        sports_container = page_content('td', class_='nameevent')
        for x in sports_container:
            print(x.text)
        time.sleep(1)
        e.click()
        time.sleep(1)
        print(counter)
        counter = counter + 1
except:
    print("koniec pilki")
