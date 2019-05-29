from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import itertools
import requests
import re

import sqlite3
import jellyfish

conn = sqlite3.connect('bazadanych.db')
c = conn.cursor()


def forbet_teams():
    driver = webdriver.Firefox()
    driver.get("https://stats.iforbet.pl/pl/soccer/events")
    sleep(5)
    # on click action
    elements = driver.find_elements_by_xpath("//div[@class='leftMenu__item leftMenu__item--nested1' and @data-menu]/div[@class='leftMenu__subheader']")
    def get_leagues():
        urls = list()
        #count = 0
        for e in elements:
            e.click()
            html = driver.page_source
            sleep(3)
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

def fortuna_teams():
    league = list()
    countries = list()
    teams = dict()

    fortuna = requests.get('https://s5.sir.sportradar.com/fortuna2/pl/1')
    html = fortuna.content
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.findAll("a",{"class":"list-group-item"})
    for y in urls:
        countries.append(y.attrs['href'])
    for leagues in countries:
        page = requests.get('https://s5.sir.sportradar.com'+leagues)
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        leagues = soup.findAll("a", {"class": "list-group-item"})
        #leagues_names = soup.findAll("span",{"class":"vertical-align-middle"})
        #for leagues_name in leagues_names:
        #   print (leagues_name.text)
        for y in leagues:
            league.append(y.attrs['href'])

    count = 0
    for link in league:
        key = link
        page = requests.get('https://s5.sir.sportradar.com' + link)
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        names = soup.findAll("div", {"class": "hidden-sm-up wrap"})
        for name in names:
            if key not in teams:
                teams[key]=[]
                teams[key].append(name.text)
            else:
                teams[link].append(name.text)
        if (count == 3):
            return teams
        else:
            count = count + 1
    return teams



def teams_database():
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_teams(id INT PRIMARY KEY, team_name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_teams(id INT PRIMARY KEY, team_name STRING)')

    try:
        for team in fortuna_teams():
            c.execute("INSERT INTO Fortuna_teams VALUES (?, ?)", (id, team))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def relationship_database():
    c.execute('CREATE TABLE IF NOT EXISTS Relationship_table (id INT PRIMARY KEY, team_name STRING, id_fortuna STRING, id_forbet STRING)')

print (fortuna_teams())