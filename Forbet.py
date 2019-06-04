import Fortuna
from typing import NamedTuple
from bs4 import BeautifulSoup
import requests
import database
import unicodedata

bookie = "Forbet"


def shave_marks(txt):
    """This method removes all diacritic marks from the given string"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)


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
        page_response = requests.get(page_link, timeout=10)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")

        #odd_container = page_content('td', class_='col_bet') #zbiera wszystkie kursy
        match_containers = page_content.find_all('div', {"data-gamename": "1X2"}) #zbiera wszystkie mecze (zespol1 - zespol 2)
        if len(match_containers) == 0:
            return 0
        print(type(match_containers))
        print(len(match_containers))
        print(page_link)
        load_matches_odds(match_containers, self.league_id)
        return len(match_containers)


#ładuje WWSZYSTKIE ligi do kontenera
def load_leagues():
    football_leagues = []
    counter = 0
    page_link = 'https://www.iforbet.pl/zaklady-bukmacherskie'
    # fetch the content from url
    page_response = requests.get(page_link, timeout=10)
    # parse html
    page_content = BeautifulSoup(page_response.content, "html.parser")
    sports_container = page_content('div', id='cat-1')

    '''        if sports_container[0].attrs['id'] == 'sport-179':
          del sports_container[0]'''
    for_check = ["sport-179"]
    leagues_container = sports_container[0].find_all('input', id=True)
    for a in leagues_container:
        link_text = a.attrs['id'][7:]
        print('Link: https://www.iforbet.pl/oferta/8/' + link_text)
        a_league_site = 'https://www.iforbet.pl/oferta/8/' + link_text
        a_league_id = counter
        a_league_name = "league " + str(counter)
        a = League_Fortuna(a_league_id, a_league_name, a_league_site);
        if a.load_league() > 0:
            database.insert_league(bookie, a_league_id, a_league_name, a_league_site)
        counter = counter + 1

    '''b = 0
    while b < len(football_leagues):
        football_leagues[b].load_league()
        b = b + 1'''
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

'''def choose_team(team_name):
    return {
        "Cracovia Kraków": "Cracovia"
    }.get(team_name, team_name)'''

#ładowanie kursów meczów z danej ligi (podstrony)
    #match containers przechowuje wszystkie mecze (zespoły), a odd container wszystkie kursy
def load_matches_odds(match_containers, league_id):
    matches = []
    counter=0

    for index, match in enumerate(match_containers):
        if index % 3 == 0:
            print(match['data-gameid'])
            match_id = int(match['data-gameid'])
            print(match['data-eventname'])
            print('Kurs na \n' + '1' + '      ' + 'X' + '      ' + '2' + '      ' + '1X' + '      ' + '2X' + '      ' + '12')
            home = match_containers[index]['data-outcomeodds']
            dash_position = str(match_containers[counter]['data-eventname']).find('-')
            team1 = str(match_containers[counter]['data-eventname'])[:dash_position - 1]
            team2 = str(match_containers[counter]['data-eventname'])[dash_position + 2:]
            draw = match_containers[index+1]['data-outcomeodds']
            away = match_containers[index+2]['data-outcomeodds']
            print(home + '   ' + draw + '   ' + away)
            if database.is_match_in_db(match_id):
                if not database.compare_odds(bookie, match_id, (home, draw, away)):
                    database.update_odds(bookie, match_id, home, draw, away)

            else:
                database.insert_odds(bookie, match_id, league_id, home, draw, away)
                #zapis do bazy danych meczu (powiązanie z kursami po id)
                database.insert_match(bookie, match_id, team1, team2)
