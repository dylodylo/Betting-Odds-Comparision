from typing import NamedTuple
from bs4 import BeautifulSoup
import requests
import database

class League_Fortuna(object):
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
        page_response = requests.get(page_link)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")

        odd_container = page_content('td', class_='col_bet') #zbiera wszystkie kursy
        match_containers = page_content.find_all('tr', {"data-gtm-enhanced-ecommerce-variant": "mecz"}) #zbiera wszystkie mecze (zespol1 - zespol 2)
        live_match_container = page_content.find_all('td', {"class": "col_title col_title_live_running"})
        if len(match_containers) == 0:
            return 0
        print(type(match_containers))
        print(len(match_containers))
        print (page_link)
        if (len(match_containers) != 0):
            print(match_containers[0].get("data-gtm-enhanced-ecommerce-sport"))
        if len(match_containers) != 0 and str(match_containers[0].get("data-gtm-enhanced-ecommerce-sport")) in['Pilka nozna', 'Piłka nożna']:
            load_matches_odds(match_containers, odd_container, len(live_match_container), self.league_id)
        return len(match_containers)

football_leagues = []
#ładuje WWSZYSTKIE ligi do kontenera
def load_leagues():
        counter = 0
        page_link = 'https://www.efortuna.pl/pl/strona_glowna/'
        # fetch the content from url
        page_response = requests.get(page_link)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")
        sports_container = page_content('li', class_='js-sport-menu-item closed')

        '''        if sports_container[0].attrs['id'] == 'sport-179':
            del sports_container[0]'''
        for_check = ["sport-179"]
        i = 0 #counter dla sports_container
        while i<len(sports_container):
            if sports_container[i]['id'] == 'sport-179':
                del sports_container[i]
            i = i+1

        print(sports_container[0].text)
        for x  in sports_container:
            for a in x.find_all('a', href=True, text=True):
                link_text = a['href']
                print('Link:' + link_text)
                a_league_site = 'https://www.efortuna.pl' + link_text
                a_league_id = counter
                a_league_name = a_league_site[53:]
                if a_league_site[:53] == 'https://www.efortuna.pl/pl/strona_glowna/pilka-nozna/':
                    a = League_Fortuna(a_league_id, a_league_name, a_league_site);
                    if a.load_league() > 0:
                        database.insert_Fortuna_leagues(a_league_id, a_league_site, a_league_name)
                counter = counter + 1

        '''b = 0
        while b < len(football_leagues):
            football_leagues[b].load_league()
            b = b + 1'''
        return

class Match_Odds(NamedTuple):
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

        'W.Plock': "Wisła Płock",
        "Zag.Lubin": "Zagłębie Lubin",
        "Lechia G.": "Lechia Gdańsk",
        "Arka G.": "Arka Gdynia"
    }.get(team_name, team_name)'''

#ładowanie kursów meczów z danej ligi (podstrony)
    #match containers przechowuje wszystkie mecze (zespoły), a odd container wszystkie kursy
def load_matches_odds( match_containers, odd_container, live_matches, league_id):
    matches = []
    counter=0
    while counter+live_matches < len(match_containers):
            match=match_containers[counter+live_matches]
            print(match.a.text)
            dash_position = match.a.text.find("-")
            matches.append(Match_Odds)
            win_1_odd = odd_container[0+(counter*6)]
            win_2_odd = odd_container[1+(counter*6)]
            win_3_odd = odd_container[2+(counter*6)]
            win_4_odd = odd_container[3+(counter*6)]
            win_5_odd = odd_container[4+(counter*6)]
            win_6_odd = odd_container[5+(counter*6)]
            print('Kurs na \n' + '1' + '      ' + 'X' + '      ' + '2'+ '      ' + '1X' + '      ' + '2X'+ '      ' + '12')
            try:
                odd_1 = win_1_odd.a.text
            except AttributeError:
                odd_1 = '0'
            try:
                odd_X = win_2_odd.a.text
            except AttributeError:
                odd_X = '0'
            try:
                odd_2 = win_3_odd.a.text
            except AttributeError:
                odd_2 = '0'
            try:
                odd_1X = win_4_odd.a.text
            except AttributeError:
                odd_1X = '0'
            try:
                odd_2X = win_5_odd.a.text
            except AttributeError:
                odd_2X = '0'
            try:
                odd_12 = win_6_odd.a.text
            except AttributeError:
                odd_12 = '0'
            matches[counter].match_id = int(match_containers[counter+live_matches]['data-id'])
            matches[counter].team1 = str(match.a.text[:dash_position - 1]).rstrip()
            matches[counter].team2 = str(match.a.text[dash_position + 2:]).rstrip()
            matches[counter].odd_1 = odd_1.strip('\n')
            matches[counter].odd_X = odd_X.strip('\n')
            matches[counter].odd_2 = odd_2.strip('\n')
            matches[counter].odd_1X = odd_1X.strip('\n')
            matches[counter].odd_2X = odd_2X.strip('\n')
            matches[counter].odd_12 = odd_12.strip('\n')
            database.Fortuna_odds_data_entry(matches[counter].match_id, odd_1, odd_X, odd_2, odd_1X, odd_2X, odd_12, league_id)
            database.Fortuna_match_entry(matches[counter].match_id, matches[counter].team1, matches[counter].team2)
            print(matches[counter].odd_1 + '   ' + matches[counter].odd_X + '   ' + matches[counter].odd_2 + '   ' + matches[counter].odd_1X + '   ' + matches[counter].odd_2X + '   ' + matches[counter].odd_12)
            counter = counter+1
    return