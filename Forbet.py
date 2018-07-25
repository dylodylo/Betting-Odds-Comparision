import Fortuna
from typing import NamedTuple
from bs4 import BeautifulSoup
import requests
import database

class League_Fortuna:
    league_id : int
    league_name: str
    league_site: str
    def __init__(self, id, name, site):
        self.league_id = id
        self.league_name = name
        self.league_site = site
        return

#ładuje stronę danej ligi
    def load_league(self):
        page_link = self.league_site
        # fetch the content from url
        page_response = requests.get(page_link, timeout=5)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")

        #odd_container = page_content('td', class_='col_bet') #zbiera wszystkie kursy
        match_containers = page_content.find_all('div', {"data-gamename": "1X2"}) #zbiera wszystkie mecze (zespol1 - zespol 2)
        print(type(match_containers))
        print(len(match_containers))
        print(page_link)
        load_matches_odds(match_containers)
        return


#ładuje WWSZYSTKIE ligi do kontenera
def load_leagues():
    football_leagues = []
    counter = 0
    page_link = 'https://www.iforbet.pl/zaklady-bukmacherskie'
    # fetch the content from url
    page_response = requests.get(page_link, timeout=5)
    # parse html
    page_content = BeautifulSoup(page_response.content, "html.parser")
    sports_container = page_content('input', id=True, type='checkbox')

    '''        if sports_container[0].attrs['id'] == 'sport-179':
          del sports_container[0]'''
    for_check = ["sport-179"]

    for a in sports_container:
        link_text = a.attrs['id'][7:]
        print('Link: https://www.iforbet.pl/oferta/8/' + link_text)
        a_league_site = 'https://www.iforbet.pl/oferta/8/' + link_text
        a_league_id = counter
        a_league_name = "league " + str(counter)
        a = League_Fortuna(a_league_id, a_league_name, a_league_site);
        football_leagues.append(a)
        counter = counter + 1
    b = 1
    while b < len(football_leagues):
        football_leagues[b].load_league()
        b = b + 1
    return
find_match = False
class Match_Odds:
    match_id : int
    team_1: str
    team_2: str
    odd_1 : float
    odd_2 : float
    odd_X : float
    odd_1X : float
    odd_2X : float
    odd_12 : float

def choose_team(team_name):
    return {
        "Cracovia Kraków": "Cracovia"
    }.get(team_name, team_name)

#ładowanie kursów meczów z danej ligi (podstrony)
    #match containers przechowuje wszystkie mecze (zespoły), a odd container wszystkie kursy
def load_matches_odds(match_containers):
    matches = []
    counter=0

    while counter < len(match_containers):
        which_match = 0  # pozwala na znalezienie meczu, ktory znajduje sie w liscie
        multi_match_id = Match_Odds()
        global find_match
        find_match = False
        for a in matches:
            if str(a.match_id) == match_containers[counter].get('data-gameid'):
                find_match = True
                multi_match_id = a
                break
        if find_match == False:
            matches.append(Match_Odds)
            which_match = len(matches) - 1
            print(match_containers[counter]['data-gameid'])
            losowa_zmiena = match_containers[counter]['data-gameid']
            matches[which_match].match_id = int(match_containers[counter]['data-gameid'])
            print(match_containers[counter]['data-eventname'])
            print('Kurs na \n' + '1' + '      ' + 'X' + '      ' + '2' + '      ' + '1X' + '      ' + '2X' + '      ' + '12')
            matches[which_match].odd_1 = match_containers[counter]['data-outcomeodds']
            dash_position = str(match_containers[counter]['data-eventname']).find('-')
            matches[which_match].team_1 = choose_team(str(match_containers[counter]['data-eventname'])[:dash_position - 1])
            matches[which_match].team_2 = choose_team(str(match_containers[counter]['data-eventname'])[dash_position + 2:])
        else:
            which_match = matches.index(multi_match_id)
            if match_containers[counter]['data-outcomename'] == 'X':
                matches[which_match].odd_X = match_containers[counter]['data-outcomeodds']
            else:
                matches[which_match].odd_2 = match_containers[counter]['data-outcomeodds']
                print(matches[which_match].odd_1 + '   ' + matches[which_match].odd_X + '   ' + matches[which_match].odd_2)
                database.Forbet_odds_data_entry(matches[which_match].match_id, matches[which_match].odd_1, matches[which_match].odd_X, matches[which_match].odd_2)
                database.Forbet_match_entry(matches[which_match].match_id, matches[which_match].team_1, matches[which_match].team_2)
        counter = counter+1
    return