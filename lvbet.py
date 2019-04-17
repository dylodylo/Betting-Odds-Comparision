from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import Fortuna
import re
import os
import xml
import time
import pandas as pd
import requests

# specify the url
urlpage = 'https://lvbet.pl/pl/zaklady-bukmacherskie/5/pilka-nozna'
print(urlpage)
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()
driver.get(urlpage)
time.sleep(3)
football_countries = []
counter = 0
# parse html
form = driver.find_element_by_xpath('//*[@class="col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted"]')
page_content = BeautifulSoup(driver.page_source, "html.parser")
sports_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')


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
counter = 0
countries = football_countries
for x in countries:
    print(x.league_site)
    driver.get(str(x.league_site))
    page_content = BeautifulSoup(driver.page_source, "html.parser")
    leagues_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
    for y in leagues_container:
        link_text = y.attrs['href']
        if link_text != '/pl/zaklady-bukmacherskie':
            print(x.league_site + link_text)
            a_league_site = x.league_site + link_text
            a_league_id = counter
            a_league_name = "league " + str(counter)
            country = Fortuna.League_Fortuna(a_league_id, a_league_name, a_league_site)
            football_leagues.append(country)
            counter = +1

# import sys
# from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QUrl
# page_link = None
#
# class Page(QWebEnginePage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebEnginePage.__init__(self)
#         self.html = ''
#         self.loadFinished.connect(self._on_load_finished)
#         self.load(QUrl(url))
#         self.app.exec_()
#
#     def _on_load_finished(self):
#         self.html = self.toHtml(self.Callable)
#         print('Load finished')
#
#     def Callable(self, html_str):
#         self.html = html_str
#         self.app.quit()
#
#
# #ładuje WWSZYSTKIE ligi do kontenera
# def load_countries():
#     football_countries = []
#     counter = 0
#     global page_link
#     page_link = Page('https://lvbet.pl/pl/zaklady-bukmacherskie/5/pilka-nozna')
#     # fetch the content from url
#     #page_response = requests.get(page_link, timeout=5)
#     # parse html
#     page_content = BeautifulSoup(page_link.html, "html.parser")
#     sports_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
#
#     for a in sports_container:
#         link_text = a.attrs['href']
#         if link_text != '/pl/zaklady-bukmacherskie':
#             print('Link: https://lvbet.pl' + link_text)
#             a_league_site = 'https://lvbet.pl' + link_text
#             a_league_id = counter
#             a_league_name = "league " + str(counter)
#             country = Fortuna.League_Fortuna(a_league_id, a_league_name, a_league_site)
#             football_countries.append(country)
#             counter =+1
#     return football_countries
#
# def load_leagues():
#     football_leagues = []
#     counter = 0
#     countries = load_countries()
#     for x in countries:
#         print(x.league_site)
#         global page_link
#         page_link = Page(str(x.league_site))
#         page_content = BeautifulSoup(page_link.html, "html.parser")
#         leagues_container = page_content('a', class_='col-d-3 col-mt-4 col-st-6 col-sm-12 ng-star-inserted')
#         for y in leagues_container:
#             link_text = y.attrs['href']
#             if link_text != '/pl/zaklady-bukmacherskie':
#                 print(x.league_site + link_text)
#                 a_league_site = x.league_site + link_text
#                 a_league_id = counter
#                 a_league_name = "league " + str(counter)
#                 country = Fortuna.League_Fortuna(a_league_id, a_league_name, a_league_site)
#                 football_leagues.append(country)
#                 counter = +1
#     return football_leagues
#
#
# load_leagues()