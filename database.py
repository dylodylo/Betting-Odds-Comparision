import sqlite3
import jellyfish

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()


def create_leagues_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie+'_leagues(id INT PRIMARY KEY, site STRING, name STRING)')


def delete_leagues_table(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie + '_leagues')


def create_matches_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie +
              '_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING, date DATETIME,league_id INT, '
              'FOREIGN KEY(league_id) REFERENCES ' + bookie + '_leagues(id))')


def delete_matches_table(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie + '_matches')


def create_match_odds_table(bookie):
    c.execute('CREATE TABLE IF NOT EXISTS ' + bookie + '_match_odds(id INT PRIMARY KEY, home FLOAT, draw FLOAT, '
                                                       'away FLOAT, hd FLOAT, da FLOAT, ha FLOAT)')


def delete_match_odds_table(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie + "_match_odds")


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


def insert_odds(bookie, id, odd1, oddx, odd2, odd1x = 0, oddx2 = 0, odd12 = 0):
    try:
        c.execute("INSERT INTO " + bookie + "_match_odds VALUES (?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def insert_match(bookie, id, t1, t2, date, league_id):
    try:
        c.execute('INSERT INTO ' + bookie + '_matches VALUES (?, ?, ?, ?, ?)', (id, t1, t2, date, league_id))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()


def delete_league(bookie, id):
    try:
        c.execute("DELETE FROM " + bookie + "_leagues WHERE id= (?)", (id,))
    except sqlite3.IntegrityError as ie:
        print("blad z dodaniem lig")
    conn.commit()


def get_leagues(bookie):
    c.execute("SELECT * FROM " + bookie + "_leagues")
    result = c.fetchall()
    return result


def get_league_matches(bookie, league_name):
    c.execute("SELECT t1, t2 FROM " + bookie + "_matches AS fm INNER JOIN "
              + bookie + "_match_odds AS fmo ON fmo.id = fm.id INNER JOIN " + bookie
              + "_leagues AS fl ON fl.id = fmo.league_id  WHERE fl.name = (?)", (league_name,))
    data = c.fetchall()
    return data


def get_match_odds(bookie, match_id):
    c.execute("SELECT home, draw, away, hd, da, ha FROM " + bookie + "_match_odds WHERE id = (?)", (match_id,))
    data = c.fetchall()
    return data[0]


def compare_odds(bookie, match_id, new_odds):
    old_odds = get_match_odds(bookie, match_id)
    if old_odds == new_odds:
        return True
    else:
        return False


def update_odds(bookie, match_id, home, draw, away, hd = '0', da = '0', ha = '0'):
    c.execute("UPDATE " + bookie + "_match_odds SET home = " + home + ", draw = " + draw + ", away = " + away + ",hd = " + hd + ", da = " + da + ", ha = " + ha + " WHERE id = " + str(match_id))
    conn.commit()
    print("Kurs meczu " + str(match_id) + " zaktualizowany!")


def is_match_in_db(bookie, match_id):
    c.execute("SELECT * FROM " + bookie + "_match_odds WHERE ID = (?)", (match_id,))
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        return True


#funkcja do umieszczania zespołów w tabeli
def insert_teams(bookie):
    c.execute("DROP TABLE IF EXISTS " + bookie + "_teams")
    c.execute("CREATE TABLE IF NOT EXISTS " + bookie + "_teams(id INT_PRIMARY_KEY, " + bookie + "_name STRING)")
    c.execute("SELECT t1 FROM " + bookie + "_matches")
    data = c.fetchall()
    i = 0
    for row in data:
        team = row[0]
        print(team)
        c.execute("SELECT " + bookie + "_name FROM " + bookie + "_teams WHERE " + bookie + '_name = "'+team+'"')
        pom = c.fetchall()
        if  len(pom) > 0:
            pass
        else:
            c.execute('INSERT INTO ' + bookie + '_teams (id, ' + bookie + '_name) VALUES (?,?)', (i, team))
            i = i+1
    c.execute("SELECT t2 FROM " + bookie + "_matches")
    data = c.fetchall()
    for row in data:
        team = row[0]
        print(team)
        c.execute("SELECT " + bookie + "_name FROM " + bookie + "_teams WHERE " + bookie + '_name = "'+team+'"')
        pom = c.fetchall()
        if len(pom) > 0:
            pass
        else:
            c.execute('INSERT INTO ' + bookie + '_teams (id, ' + bookie + '_name) VALUES (?,?)', (i, team))
            i = i+1
    print(data)
    conn.commit()

def insert_all_teams():
    insert_teams("Fortuna")
    insert_teams("Forbet")
    insert_teams("Lvbet")
    insert_teams("Milenium")


def create_matchedleagues_table():
    c.execute('CREATE TABLE IF NOT EXISTS matched_leagues(idFortuna INT, siteFortuna STRING, '
              'idForbet INT, siteForbet STRING, FOREIGN KEY (idFortuna) REFERENCES Fortuna_leagues(id), FOREIGN KEY '
              '(idForbet) REFERENCES Forbet_leagues(id))')


def create_matchedteams_table():
    c.execute('CREATE TABLE IF NOT EXISTS matched_teams(id INTEGER PRIMARY KEY, idFortuna INT, idForbet INT, '
              'nameFortuna STRING, nameForbet STRING, FOREIGN KEY (idFortuna) REFERENCES Fortuna_teams(id), '
              'FOREIGN KEY (idForbet) REFERENCES Forbet_teams(id))')


def delete_matchedleagues_table():
    c.execute("DROP TABLE IF EXISTS matched_leagues")


def delete_matchedteams_table():
    c.execute("DROP TABLE IF EXISTS matched_teams")


def select_matches_from_league(bookie):
    c.execute("SELECT t1, t2, date, league_id, site FROM " + bookie + "_matches AS fm INNER JOIN" + bookie +
              "_leagues AS fl ON fm.league_id = fl.id")
    data = c.fetchall()
    return data


def select_matches_from_league_with_date_and_team1():
    c.execute("SELECT t1, t2, date, league_id, site FROM Forbet_matches AS fm INNER JOIN Forbet_leagues AS fl ON "
              "fm.league_id = fl.id WHERE t1 = '" + match[0] + "' AND date = '"
              + match[2] + "'")