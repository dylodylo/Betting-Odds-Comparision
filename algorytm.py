import difflib
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
        #tests
        count = 0
        #
        for e in elements:
            e.click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            urls.append(str(soup.findAll('div', {"class": "leftMenu__content leftMenu__content--hidden opened"})))
            # tests
            if(count==10): break
            else: count=count+1
            #
        return urls

    urls = get_leagues()
    leagues = list()
    for url in urls:
        leagues.append(re.findall('href=[\'"]?([^\'" >]+)', url))

    teams = list()
    for x in itertools.chain.from_iterable(leagues):
        page = requests.get(x)
        soup = BeautifulSoup(page.content, 'html.parser')
        table_body = soup.find_all('body')
        name = str(re.findall(r'<a[\s]+[^>]*?href[\s]?=[\s\"\']*(.*?)[\"\']*.*?>([^<]+|.*?)?<\/a>', str(table_body)))
        teams_forbet = re.findall("'\w+[\s]\w+'", name, re.UNICODE)
        #print(str(x)+": "+str(teams_forbet))
        for team in teams_forbet:
             teams.append(team)
    return teams

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
    # tests
    count = 0
    #
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
        # tests
        if (count == 10):
           return teams

        else:
            count = count + 1
    return teams

scrapped_fortuna = list()
for key, values in fortuna_teams().items():
    for value in values:
        scrapped_fortuna.append(value)

def forbet_insert():
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_teams(forbet_id INTEGER PRIMARY KEY,team_name STRING)')
    insert_teams = list()
    insert_teams = forbet_teams()
    try:
        without_duplicates = list(dict.fromkeys(insert_teams))
        for team in without_duplicates:
            c.execute('INSERT INTO Forbet_teams VALUES (NULL, ?)', (team,))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def fortuna_insert():
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_teams(fortuna_id INTEGER PRIMARY KEY, team_name STRING)')
    insert_teams = list()
    insert_teams = scrapped_fortuna
    try:
        without_duplicates = list(dict.fromkeys(insert_teams))
        for team in without_duplicates:
            c.execute('INSERT INTO Fortuna_teams VALUES (NULL, ?)', ("'" +team+ "'",))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()


def relationship_database():
    c.execute("select * from Fortuna_teams")
    records = c.fetchall()
    fortuna = list()
    for row in records:
        fortuna.append(row[1])

    c.execute("select * from Forbet_teams")
    records = c.fetchall()
    forbet= list()
    for row in records:
        forbet.append(row[1])

    c.execute('CREATE TABLE IF NOT EXISTS Relationship_table (team_name STRING, id_fortuna STRING, id_forbet STRING)')
    # test
    count = 0
    #
    try:
         for team in forbet:
             if (count==1000): break
             else: count=count+1
             if(team in fortuna):
                 c.execute("INSERT INTO Relationship_table VALUES (?, ?, ?)", (team, fortuna.index(team), forbet.index(team) ))
                 conn.commit()
             else:
                 name = difflib.get_close_matches(team,fortuna,cutoff=0.95)
                 if name:
                    c.execute("INSERT INTO Relationship_table VALUES (?, ?, ?)", (team, fortuna.index(name[0]), forbet.index(team) ))
                    conn.commit()
                 else: continue
    except sqlite3.IntegrityError as ie:
        pass


#fortuna_insert()
#forbet_insert()
relationship_database()
