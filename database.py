import sqlite3
import jellyfish

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()


def create_leagues_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie+'_leagues(id INT PRIMARY KEY, site STRING, name STRING)')


def delete_leagues_table(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie + '_leagues')


def create_matches_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie + '_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')


def delete_matches_table(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie +'_matches')


def create_match_odds_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie + 'match_odds(id INT PRIMARY KEY, home FLOAT, draw FLOAT, away FLOAT, hd FLOAT, da FLOAT, ha FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')


def delete_match_odds_table(bookie):
    c.execute("DROP TABLE IF EXISTS" + bookie + "_match_odds")


def create_all_fortuna_tables():
    create_leagues_table('Fortuna')
    create_matches_table('Fortuna')
    create_match_odds_table('Fortuna')


def delete_all_fortuna_tables():
    delete_leagues_table('Fortuna')
    delete_matches_table('Fortuna')
    delete_match_odds_table('Fortuna')


def create_all_forbet_tables():
    create_leagues_table('Forbet')
    create_matches_table('Forbet')
    create_match_odds_table('Forbet')


def delete_all_forbet_tables():
    delete_leagues_table('Forbet')
    delete_matches_table('Forbet')
    delete_match_odds_table('Forbet')


def create_all_lvbet_tables():
    create_leagues_table('Lvbet')
    create_matches_table('Lvbet')
    create_match_odds_table('Lvbet')


def delete_all_lvbet_tables():
    delete_leagues_table('Lvbet')
    delete_matches_table('Lvbet')
    delete_match_odds_table('Lvbet')


def create_all_milenium_tables():
    create_leagues_table('Milenium')
    create_matches_table('Milenium')
    create_match_odds_table('Milenium')


def delete_all_milenium_tables():
    delete_leagues_table('Milenium')
    delete_matches_table('Milenium')
    delete_match_odds_table('Milenium')


def create_all_sts_tables():
    create_leagues_table('Sts')
    create_matches_table('Sts')
    create_match_odds_table('Sts')


def delete_all_sts_tables():
    delete_leagues_table('Sts')
    delete_matches_table('Sts')
    delete_match_odds_table('Sts')


def create_all_tables(): #tworzenie wszystkich tabel
    create_all_fortuna_tables()
    create_all_forbet_tables()
    create_all_lvbet_tables()
    create_all_milenium_tables()
    create_all_sts_tables()


def delete_all_tables():
    delete_all_fortuna_tables()
    delete_all_forbet_tables()
    delete_all_lvbet_tables()
    delete_all_milenium_tables()
    delete_all_sts_tables()


def insert_league(bookie, id, name, site =''):
    try:
        c.execute("INSERT INTO " + bookie + "_leagues VALUES (?, ?, ?)", (id, site, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()


def insert_odds(bookie, id, league_id, odd1, oddx, odd2, odd1x = 0, oddx2 = 0, odd12 = 0):
    try:
        c.execute("INSERT INTO " + bookie + "_match_odds VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()


def insert_match(bookie, id, t1, t2):
    try:
        c.execute('INSERT INTO ' + bookie + '_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()


def delete_league(bookie, id):
    try:
        c.execute("DELETE FROM " + bookie + "_leagues WHERE id= (?)", (id))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()


def get_leagues(bookie):
    c.execute("SELECT * FROM " + bookie + "_leagues")
    result = c.fetchall()
    return result


#funkcja do umieszczania zespołów w tabeli
def insert_teams():
    c.execute("DROP TABLE IF EXISTS Teams")
    c.execute("CREATE TABLE IF NOT EXISTS Teams(id INT_PRIMARY_KEY, fortuna_name STRING)")
    c.execute("SELECT t1 FROM Fortuna_matches")
    data = c.fetchall()
    i = 0
    for row in data:
        row = str(row)[2:].rstrip("\',)")
        c.execute("SELECT fortuna_name FROM Teams WHERE fortuna_name = '"+row+"'")
        pom = c.fetchall()
        if  len(pom) > 0:
            pass
        else:
            c.execute('INSERT INTO Teams (id, fortuna_name) VALUES (?,?)', (i, row))
            i = i+1
    c.execute("SELECT t2 FROM Fortuna_matches")
    data = c.fetchall()
    for row in data:
        row = str(row)[2:].rstrip("\',)")
        c.execute("SELECT fortuna_name FROM Teams WHERE fortuna_name = '"+row+"'")
        pom = c.fetchall()
        if  len(pom) > 0:
            pass
        else:
            c.execute('INSERT INTO Teams (id, fortuna_name) VALUES (?,?)', (i, row))
            i = i+1
    print(data)
    conn.commit()

#funkcja do sprawdzania poprawności dodania lig
def show_league_matches():
    c.execute("SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.name = 'ekstraklasa'")
    data = c.fetchall()
    print(data)
    c.execute("SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.name = 'league 0'")
    data = c.fetchall()
    print(data)

def match_leagues():

    c.execute("SELECT * FROM Fortuna_leagues")
    leagues_Fortuna_data = c.fetchall()
    c.execute("SELECT * FROM Forbet_leagues")
    leagues_Forbet_data = c.fetchall()
    c.execute("CREATE TABLE IF NOT EXISTS Matched_Leagues (forbet_id INT, fortuna_id INT)")
    MatchedLeaguesFA = [0] * leagues_Fortuna_data.__sizeof__()
    MatchedLeaguesFT = [0] * leagues_Forbet_data.__sizeof__()
    findLeague = None
    for row in leagues_Fortuna_data:
        if MatchedLeaguesFA[row[0]] == False:
            c.execute("SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = " + str(row[0]))
            Fortuna_matches_data = c.fetchall()
            for fone_match in Fortuna_matches_data:
                for roow in leagues_Forbet_data:
                    findLeague = False
                    #if MatchedLeaguesFT[roow[0]] == False:
                    c.execute("SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = " + str(roow[0]))
                    Forbet_matches_data = c.fetchall()
                    for one_match in Forbet_matches_data:
                        if jellyfish.jaro_distance(str(fone_match[0]), str(one_match[0])) > 0.8 or jellyfish.jaro_distance(str(fone_match[1]), str(one_match[1])) > 0.8:
                            print(Forbet_matches_data)
                            print(Fortuna_matches_data)
                            s = input('match? y/n -> ')
                            if s == 'y':
                                findLeague = True
                                MatchedLeaguesFT[roow[0]] = True
                                MatchedLeaguesFA[row[0]] = True
                                c.execute("INSERT INTO Matched_Leagues VALUES (?, ?)", (roow[0], row[0]
                                                                                       ))
                                conn.commit()
                                break
                    if findLeague == True:
                        break
                if findLeague == True:
                    break

def teams_from_league():
    c.execute("SELECT * FROM Matched_Leagues")
    leagues_data = c.fetchall()
    i = 0
    isFind = False
    listaostaczena = []
    for row in leagues_data:
        forbetid = row[0]
        fortunaid = row[1]
        forbettoDelete = []
        fortunatoDelete = []
        c.execute(
            "SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(fortunaid)+"'")
        fortuna_teams = c.fetchall()
        print(len(fortuna_teams))
        c.execute(
            "SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(forbetid)+"'")
        forbet_teams = c.fetchall()
        for rowinforbet in forbet_teams:
                for rowinfortuna in fortuna_teams:
                    #print (str(rowinforbet[0]) + " " + str(jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]))+" "+ str(rowinfortuna[0]) + " " + str(rowinforbet[1]) + " " + str(jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1])) + " " + str(rowinfortuna[1]))
                    if jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]) > 0.7 and jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1]) > 0.7:
                        print(rowinforbet + rowinfortuna)
                        i +=1
                        forbettoDelete.append(rowinforbet)
                        fortunatoDelete.append(rowinfortuna)
                        listaostaczena.append(rowinforbet)
                        listaostaczena.append(rowinfortuna)
                        isFind = True
                        break
                if isFind == False:
                    print(rowinforbet)
                else:
                    isFind = False

        if len(forbettoDelete) > 0:
            for rowinrow in forbettoDelete:
                forbet_teams.remove(rowinrow)
        if len(fortunatoDelete) > 0:
            for rowinrow2 in fortunatoDelete:
                if len(fortuna_teams) > 0:
                    try:
                        fortuna_teams.remove(rowinrow2)
                    except ValueError:
                        print("blad z meczem " + str(rowinrow2))
        print(forbet_teams)
        print(fortuna_teams)
    print(i)
    for row in leagues_data:
        forbetid = row[0]
        fortunaid = row[1]
        forbettoDelete = []
        fortunatoDelete = []
        c.execute(
            "SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(fortunaid)+"'")
        fortuna_teams = c.fetchall()
        print(len(fortuna_teams))
        c.execute(
            "SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(forbetid)+"'")
        forbet_teams = c.fetchall()
        for rowinforbet in forbet_teams:
                for rowinfortuna in fortuna_teams:
                    if rowinfortuna in listaostaczena:
                        isFind == True
                    else:
                        #print (str(rowinforbet[0]) + " " + str(jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]))+" "+ str(rowinfortuna[0]) + " " + str(rowinforbet[1]) + " " + str(jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1])) + " " + str(rowinfortuna[1]))
                        if jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]) > 0.6 and jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1]) > 0.6:
                            print(rowinforbet + rowinfortuna)
                            i +=1
                            forbettoDelete.append(rowinforbet)
                            fortunatoDelete.append(rowinfortuna)
                            listaostaczena.append(rowinforbet)
                            listaostaczena.append(rowinfortuna)
                            isFind = True
                            break
                if isFind == False:
                    print(rowinforbet)
                else:
                    isFind = False
        listaostaczena.append(forbettoDelete)
        listaostaczena.append(fortunatoDelete)
        if len(forbettoDelete) > 0:
            for rowinrow in forbettoDelete:
                forbet_teams.remove(rowinrow)
        if len(fortunatoDelete) > 0:
            for rowinrow2 in fortunatoDelete:
                if len(fortuna_teams) > 0:
                    try:
                        fortuna_teams.remove(rowinrow2)
                    except ValueError:
                        print("blad z meczem " + str(rowinrow2))
        print(forbet_teams)
        print(fortuna_teams)
    print(i)
    for row in leagues_data:
        forbetid = row[0]
        fortunaid = row[1]
        forbettoDelete = []
        fortunatoDelete = []
        c.execute(
            "SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(fortunaid)+"'")
        fortuna_teams = c.fetchall()
        print(len(fortuna_teams))
        c.execute(
            "SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(forbetid)+"'")
        forbet_teams = c.fetchall()
        for rowinforbet in forbet_teams:
                for rowinfortuna in fortuna_teams:
                    if rowinfortuna in listaostaczena:
                        isFind == True
                    else:
                        #print (str(rowinforbet[0]) + " " + str(jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]))+" "+ str(rowinfortuna[0]) + " " + str(rowinforbet[1]) + " " + str(jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1])) + " " + str(rowinfortuna[1]))
                        if jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]) > 0.5 and jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1]) > 0.5:
                            print(rowinforbet + rowinfortuna)
                            i +=1
                            forbettoDelete.append(rowinforbet)
                            fortunatoDelete.append(rowinfortuna)
                            listaostaczena.append(rowinforbet)
                            listaostaczena.append(rowinfortuna)
                            isFind = True
                            break
                if isFind == False:
                    print(rowinforbet)
                else:
                    isFind = False
        listaostaczena.append(forbettoDelete)
        listaostaczena.append(fortunatoDelete)
        if len(forbettoDelete) > 0:
            for rowinrow in forbettoDelete:
                forbet_teams.remove(rowinrow)
        if len(fortunatoDelete) > 0:
            for rowinrow2 in fortunatoDelete:
                if len(fortuna_teams) > 0:
                    try:
                        fortuna_teams.remove(rowinrow2)
                    except ValueError:
                        print("blad z meczem " + str(rowinrow2))
        print(forbet_teams)
        print(fortuna_teams)
    print(i)
    for row in leagues_data:
        forbetid = row[0]
        fortunaid = row[1]
        forbettoDelete = []
        fortunatoDelete = []
        c.execute(
            "SELECT t1, t2 FROM Fortuna_matches AS fm INNER JOIN Fortuna_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Fortuna_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(fortunaid)+"'")
        fortuna_teams = c.fetchall()
        print(len(fortuna_teams))
        c.execute(
            "SELECT t1, t2 FROM Forbet_matches AS fm INNER JOIN Forbet_match_odds AS fmo ON fmo.id = fm.id INNER JOIN Forbet_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.id = '"+str(forbetid)+"'")
        forbet_teams = c.fetchall()
        for rowinforbet in forbet_teams:
                for rowinfortuna in fortuna_teams:
                    if rowinfortuna in listaostaczena:
                        isFind == True
                    else:
                        #print (str(rowinforbet[0]) + " " + str(jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]))+" "+ str(rowinfortuna[0]) + " " + str(rowinforbet[1]) + " " + str(jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1])) + " " + str(rowinfortuna[1]))
                        if jellyfish.jaro_winkler(rowinforbet[0], rowinfortuna[0]) > 0.4 and jellyfish.jaro_winkler(rowinforbet[1], rowinfortuna[1]) > 0.4:
                            print(rowinforbet + rowinfortuna)
                            i +=1
                            forbettoDelete.append(rowinforbet)
                            fortunatoDelete.append(rowinfortuna)
                            listaostaczena.append(rowinforbet)
                            listaostaczena.append(rowinfortuna)
                            isFind = True
                            break
                if isFind == False:
                    print(rowinforbet)
                else:
                    isFind = False
        listaostaczena.append(forbettoDelete)
        listaostaczena.append(fortunatoDelete)
        if len(forbettoDelete) > 0:
            for rowinrow in forbettoDelete:
                forbet_teams.remove(rowinrow)
        if len(fortunatoDelete) > 0:
            for rowinrow2 in fortunatoDelete:
                if len(fortuna_teams) > 0:
                    try:
                        fortuna_teams.remove(rowinrow2)
                    except ValueError:
                        print("blad z meczem " + str(rowinrow2))
        print(forbet_teams)
        print(fortuna_teams)
    print(i)
    y = 0
    for x in range(len(listaostaczena)):
        print(str(listaostaczena[y][0]) + " " + str(listaostaczena[y+1][0]))
        print(str(listaostaczena[y][1]) + " " + str(listaostaczena[y + 1][1]))
        y += 2