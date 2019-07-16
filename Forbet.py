from bs4 import BeautifulSoup
import requests
import database

bookie = "Forbet"

months = {
    "sty" : "1",
    "lut" : "2",
    "mar" : "3",
    "kwi" : "4",
    "maj" : "5",
    "cze" : "6",
    "lip" : "7",
    "sie" : "8",
    "wrz" : "9",
    "paź" : "10",
    "lis" : "11",
    "gru" : "12",
}

#ładuje stronę danej ligi
def load_matches():
    leagues = database.get_leagues(bookie)
    for x in leagues:
        page_link = x[1]
        # fetch the content from url
        page_response = requests.get(page_link, timeout=10)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")

        #odd_container = page_content('td', class_='col_bet') #zbiera wszystkie kursy
        match_containers = page_content.find_all('div', {"data-gamename": "1X2"}) #zbiera wszystkie mecze (zespol1 - zespol 2)
        dates_container = page_content.find_all('div', {"class": "events-group"})
        dates = []
        for date in dates_container:
            hours = date('div', class_="event-panel")
            day = date.text[date.text.find(",")+2:date.text.find(":")-2]
            trueday = day[:2]
            month = day[day.find(" ")+1:][:3]
            month = ' '.join([months.get(i, i) for i in month.split()])
            for h in hours:
                hour = h.text[:5]
                dates.append("2019-" + month + "-" + trueday + " " + hour)

        if len(match_containers) != 0:
            print(type(match_containers))
            print(len(match_containers))
            print(page_link)
            load_matches_odds(match_containers, dates, x[0])


#ładuje WWSZYSTKIE ligi do kontenera
def load_leagues():
    page_link = 'https://www.iforbet.pl/zaklady-bukmacherskie'
    # fetch the content from url
    page_response = requests.get(page_link, timeout=10)
    # parse html
    page_content = BeautifulSoup(page_response.content, "html.parser")
    sports_container = page_content('div', id='cat-1')
    leagues_container = sports_container[0].find_all('input', id=True)
    for index, a in enumerate(leagues_container):
        link_text = a.attrs['id'][7:]
        league_site = 'https://www.iforbet.pl/oferta/8/' + link_text
        league_id = index
        league_name = "league " + str(index)
        database.insert_league(bookie, league_id, league_name, league_site)
        print(league_site)

#ładowanie kursów meczów z danej ligi (podstrony)
    #match containers przechowuje wszystkie mecze (zespoły), a odd container wszystkie kursy
def load_matches_odds(match_containers, dates, league_id):

    for index, match in enumerate(match_containers):
        if index % 3 == 0:
            print(match['data-gameid'])
            match_id = int(match['data-gameid'])
            print(match['data-eventname'])
            print('Kurs na \n' + '1' + '      ' + 'X' + '      ' + '2' + '      ' + '1X' + '      ' + '2X' + '      ' + '12')
            home = match_containers[index]['data-outcomeodds']
            dash_position = str(match_containers[index]['data-eventname']).find('-')
            team1 = str(match_containers[index]['data-eventname'])[:dash_position - 1]
            team2 = str(match_containers[index]['data-eventname'])[dash_position + 2:]
            draw = match_containers[index+1]['data-outcomeodds']
            away = match_containers[index+2]['data-outcomeodds']
            print(home + '   ' + draw + '   ' + away)
            if database.is_match_in_db(bookie, match_id):
                if not database.compare_odds(bookie, match_id, (float(home), float(draw), float(away), 0.0, 0.0, 0.0)):
                    database.update_odds(bookie, match_id, home, draw, away)

            else:
                database.insert_odds(bookie, match_id, league_id, home, draw, away)
                #zapis do bazy danych meczu (powiązanie z kursami po id)
                database.insert_match(bookie, match_id, team1, team2, dates[int(index/3)])

if __name__ == '__main__':
    load_matches()
