from bs4 import BeautifulSoup
import requests
import database
import proxy

bookie = "Fortuna"


def load_matches():
    leagues = database.get_leagues(bookie)
    for x in leagues:
        page_link = x[1]
        # TODO
        page_response = requests.get(page_link)
        #page_response = requests.get(page_link)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")

        odd_container = page_content('td', class_='col_bet') #zbiera wszystkie kursy
        match_containers = page_content.find_all('tr', {"data-gtm-enhanced-ecommerce-variant": "Mecz"}) #zbiera wszystkie mecze (zespol1 - zespol 2)
        live_match_container = page_content.find_all('td', {"class": "col_title col_title_live_running"}) #zbieramy mecze, które są "live", później wykluczymy je z zestawienia, bo nie są dla nich określone kursy
        print(len(match_containers))
        print (page_link)
        if (len(match_containers) != 0):
            print(match_containers[0].get("data-gtm-enhanced-ecommerce-sport"))
        if len(match_containers) != 0 and str(match_containers[0].get("data-gtm-enhanced-ecommerce-sport")) in['Pilka nozna', 'Piłka nożna']:
            load_matches_odds(match_containers, odd_container, len(live_match_container), x[0])


# ładuje WSZYSTKIE ligi do kontenera
def load_leagues():
        page_link = 'https://www.efortuna.pl/pl/strona_glowna/' #link do strony, która ma zostać sparsowana
        # fetch the content from url
        page_response = requests.get(page_link)
        # parse html
        page_content = BeautifulSoup(page_response.content, "html.parser")
        sports_container = page_content('li', class_='js-sport-menu-item closed') #do sports_container pakujemy całą zawartość, którą otacza znacznik <li class_='js-sport-menu-item closed></li>

        print(sports_container[0].text)
        for x in sports_container:
            for index, a in enumerate(x.find_all('a', href=True, text=True)): #wyłuskuję to, co jest w znaczniku <a>, bo tam jest zawarty link do konkretnej ligi
                link_text = a['href'] #z a pobieram wartość atrybutu 'href'
                #przypisanie do zmiennej url ligi
                league_site = 'https://www.efortuna.pl' + link_text
                print(league_site)
                league_id = index
                #przypisuje do nazwy ligi to, co będzie w koncowcec adresu url
                league_name = league_site[53:]
                #chcemy tylko ligi z piłki nożnej, bo inne mają inaczej rozpisane kursy
                if league_site[:53] == 'https://www.efortuna.pl/pl/strona_glowna/pilka-nozna/':
                        database.insert_league(bookie, league_id, league_name, league_site)


#ładowanie kursów meczów z danej ligi (podstrony)
    #match containers przechowuje wszystkie mecze (zespoły), a odd container wszystkie kursy

def load_matches_odds(match_containers, odd_container, live_matches, league_id):
    counter=0
    while counter+live_matches < len(match_containers):
            match=match_containers[counter+live_matches] #wybieramy kolejne mecze;nie chcemy brać pod uwagę meczów live
            print(match.a.text)
            dash_position = match.a.text.find("-") #określamy pozycję '-' aby potem pobrać nazwy zespołów
            #pobieranie kursów
            home = odd_container[0+(counter*6)]
            draw = odd_container[1+(counter*6)]
            away = odd_container[2+(counter*6)]
            hd = odd_container[3+(counter*6)]
            da = odd_container[4+(counter*6)]
            ha = odd_container[5+(counter*6)]
            print('Kurs na \n' + '1' + '      ' + 'X' + '      ' + '2'+ '      ' + '1X' + '      ' + '2X'+ '      ' + '12')
            try:
                home = home.a.text.strip('\n\r\n')
            except AttributeError:
                home = '0' #zabezpieczenie - czasami, gdy kurs jest mniejszy od 1 nie wyświetla się nic
            try:
                draw = draw.a.text.strip('\n\r\n')
            except AttributeError:
                draw = '0'
            try:
                away = away.a.text.strip('\n\r\n')
            except AttributeError:
                away = '0'
            try:
                hd = hd.a.text.strip('\n\r\n')
            except AttributeError:
                hd = '0'
            try:
                da = da.a.text.strip('\n\r\n')
            except AttributeError:
                da = '0'
            try:
                ha = ha.a.text.strip('\n\r\n')
            except AttributeError:
                ha = '0'
            match_id = int(match_containers[counter + live_matches]['data-id'])
            team1 = str(match.a.text[:dash_position - 1]).rstrip()
            team2 = str(match.a.text[dash_position + 2:]).rstrip()
            #zapis do bazy kursów (powiązanie z meczem po id)
            if database.is_match_in_db(bookie, match_id):
                if not database.compare_odds(bookie, match_id, (home, draw, away, hd, da, ha)):
                    database.update_odds(bookie, match_id, home, draw, away, hd, da, ha)

            else:
                database.insert_odds(bookie, match_id, league_id, home, draw, away, hd, da, ha)
                #zapis do bazy danych meczu (powiązanie z kursami po id)
                database.insert_match(bookie, match_id, team1, team2)
            print(home + '   ' + draw + '   ' + away + '   ' + hd + '   ' + da + '   ' + ha)
            counter += 1

def scrap():
    load_leagues()
    load_matches()