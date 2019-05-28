import sqlite3
import jellyfish

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()

def test():
    c.execute("DROP TABLE IF EXISTS Milenium_matches")
    c.execute("DROP TABLE IF EXISTS Milenium_match_odds")
    c.execute("DROP TABLE IF EXISTS Milenium_leagues")
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_leagues(id INT PRIMARY KEY, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
def get_leagues():
    query = "SELECT * FROM Lvbet_leagues"
    c.execute(query)
    result = c.fetchall()
    return result

def create_table(): #tworzenie wszystkich tabel
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Forbet_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Lvbet_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Lvbet_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Lvbet_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Sts_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Sts_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Sts_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_leagues(id INT PRIMARY KEY, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Milenium_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')

def data_entry():
    c.execute("INSERT INTO match VALUES(1, 2.5, 2.4, 3.2, 1.4, 1.3, 1.2)")
    conn.commit()
    c.close()
    conn.close()

def insert_Fortuna_leagues(id, site, name):
    try:
        c.execute("INSERT INTO Fortuna_leagues VALUES (?, ?, ?)", (id, site, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()

def Fortuna_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id):
    try:
        c.execute("INSERT INTO Fortuna_match_odds VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Fortuna_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Fortuna_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Forbet_leagues_entry(id, site, name):
    try:
        c.execute("INSERT INTO Forbet_leagues VALUES (?, ?, ?)", (id, site, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()

def Forbet_odds_data_entry(id, odd1, oddx, odd2, league_id):
    try:
        c.execute("INSERT INTO Forbet_match_odds VALUES (?, ?, ?, ?, 0, 0, 0, ?)", (id, odd1, oddx, odd2, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Forbet_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Forbet_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Lvbet_leagues_entry(id, site, name):
    try:
        c.execute("INSERT INTO Lvbet_leagues VALUES (?, ?, ?)", (id, site, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()

def Lvbet_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id):
    try:
        c.execute("INSERT INTO Lvbet_match_odds VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Lvbet_odds_data_entry_not_full(id, odd1, oddx, odd2, league_id):
    try:
        c.execute("INSERT INTO Lvbet_match_odds VALUES (?, ?, ?, ?, 0, 0, 0, ?)", (id, odd1, oddx, odd2, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Lvbet_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Lvbet_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Sts_leagues_entry(id, site, name):
    try:
        c.execute("INSERT INTO Sts_leagues VALUES (?, ?, ?)", (id, site, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()

def Sts_odds_data_entry(id, odd1, oddx, odd2, league_id):
    try:
        c.execute("INSERT INTO Sts_match_odds VALUES (?, ?, ?, ?, 0, 0, 0, ?)", (id, odd1, oddx, odd2, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Sts_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Sts_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Milenium_leagues_entry(id, name):
    try:
        c.execute("INSERT INTO Milenium_leagues VALUES (?, ?)", (id, name))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()

def Milenium_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id):
    try:
        c.execute("INSERT INTO Milenium_match_odds VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Milenium_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Milenium_matches VALUES (?, ?, ?)', (id, t1, t2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Milenium_league_delete(leagueid):
    try:
        c.execute("DELETE FROM Milenium_leagues WHERE id= (?)", (leagueid,))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def delete_table(): #usuwanie wszystkich tabel
    c.execute("DROP TABLE IF EXISTS Fortuna_match_odds")
    c.execute("DROP TABLE IF EXISTS Forbet_match_odds")
    c.execute("DROP TABLE IF EXISTS Fortuna_matches")
    c.execute("DROP TABLE IF EXISTS Forbet_matches")
    c.execute("DROP TABLE IF EXISTS Fortuna_leagues")
    c.execute("DROP TABLE IF EXISTS Forbet_leagues")
    c.execute("DROP TABLE IF EXISTS Lvbet_matches")
    c.execute("DROP TABLE IF EXISTS Lvbet_match_odds")
    c.execute("DROP TABLE IF EXISTS Lvbet_leagues")
    c.execute("DROP TABLE IF EXISTS Sts_matches")
    c.execute("DROP TABLE IF EXISTS Sts_match_odds")
    c.execute("DROP TABLE IF EXISTS Sts_leagues")
    c.execute("DROP TABLE IF EXISTS Milenium_matches")
    c.execute("DROP TABLE IF EXISTS Milenium_match_odds")
    c.execute("DROP TABLE IF EXISTS Milenium_leagues")

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