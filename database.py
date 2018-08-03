import sqlite3
import jellyfish

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Fortuna_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_leagues(id INT PRIMARY KEY, site STRING, name STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT, league_id INT, FOREIGN KEY(league_id) REFERENCES Forbet_leagues(id))')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')

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

def delete_table():
    c.execute("DROP TABLE IF EXISTS Fortuna_match_odds")
    c.execute("DROP TABLE IF EXISTS Forbet_match_odds")
    c.execute("DROP TABLE IF EXISTS Fortuna_matches")
    c.execute("DROP TABLE IF EXISTS Forbet_matches")
    c.execute("DROP TABLE IF EXISTS Fortuna_leagues")
    c.execute("DROP TABLE IF EXISTS Forbet_leagues")

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