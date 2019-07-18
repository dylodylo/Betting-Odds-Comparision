import sqlite3
from datetime import datetime
import itertools
import database

conn = sqlite3.connect('bazadanych.db')
c = conn.cursor()

# database.insert_all_teams()
#
# def create_matchedleagues_table():
#     c.execute("DROP TABLE IF EXISTS matchedleagues_table")
#     c.execute('CREATE TABLE IF NOT EXISTS matchedleagues_table(idFortuna INT, siteFortuna STRING, '
#               'idForbet INT, siteForbet STRING, FOREIGN KEY (idFortuna) REFERENCES Fortuna_leagues(id), FOREIGN KEY '
#               '(idForbet) REFERENCES Forbet_leagues(id))')
#     conn.commit()
#
#
# def create_matchedteams_table():
#     c.execute("DROP TABLE IF EXISTS matchedteams")
#     c.execute('CREATE TABLE IF NOT EXISTS matchedteams(id INTEGER PRIMARY KEY, idFortuna INT, idForbet INT, '
#               'nameFortuna STRING, nameForbet STRING, FOREIGN KEY (idFortuna) REFERENCES Fortuna_teams(id), '
#               'FOREIGN KEY (idForbet) REFERENCES Forbet_teams(id))')
#     conn.commit()
#
# create_matchedleagues_table()
# create_matchedteams_table()
# def matchleagues():
#     c.execute("SELECT t1, t2, date, league_id, site FROM Fortuna_matches AS fm INNER JOIN Fortuna_leagues AS fl ON "
#               "fm.league_id = fl.id")
#     fortuna_matches = c.fetchall()
#     c.execute("SELECT t1, t2, date, league_id FROM Forbet_matches")
#     forbet_matches = c.fetchall()
#     for match in fortuna_matches:
#         c.execute("SELECT t1, t2, date, league_id, site FROM Forbet_matches AS fm INNER JOIN Forbet_leagues AS fl ON "
#                   "fm.league_id = fl.id WHERE t1 = '" + match[0] + "' AND date = '"
#                   + match[2] + "'")
#         data = c.fetchall()
#         if len(data)>0:
#             c.execute("SELECT idFortuna FROM matchedleagues_table WHERE idFortuna = " + str(match[3]))
#             check = c.fetchall()
#             if len(check) == 0:
#                 c.execute("INSERT INTO matchedleagues_table VALUES (?, ?, ?, ?)",
#                           (match[3], match[4], data[0][3], data[0][4]))
#                 conn.commit()
#             if len(data)>1:
#                 print("okurwaco")
#             print(data)
#         c.execute("SELECT t1, t2, date, league_id, site FROM Forbet_matches AS fm INNER JOIN Forbet_leagues AS fl ON "
#                   "fm.league_id = fl.id WHERE t1 = '" + match[1] + "' AND date = '"
#                   + match[2] + "'")
#         data = c.fetchall()
#         if len(data) > 0:
#             c.execute("SELECT idFortuna FROM matchedleagues_table WHERE idFortuna = " + str(match[3]))
#             check = c.fetchall()
#             if len(check) == 0:
#                 c.execute("INSERT INTO matchedleagues_table VALUES (?, ?, ?, ?)",
#                           (match[3], match[4], data[0][3], data[0][4]))
#                 conn.commit()
#             if len(data) > 1:
#                 print("okurwaco")
#             print(data)
#
#
# matchleagues()
#
# def matchteams():
#     c.execute("SELECT idFortuna, idForbet FROM matchedleagues_table")
#     data = c.fetchall()
#
#     for league in data:
#         c.execute("SELECT t1, t2, date FROM Fortuna_matches WHERE league_id = " + str(league[0]))
#         fortuna_matches = c.fetchall()
#         print(fortuna_matches)
#         c.execute("SELECT t1, t2, date FROM Forbet_matches WHERE league_id = " + str(league[1]))
#         forbet_matches = c.fetchall()
#         print(forbet_matches)
#         for fortunamatch in fortuna_matches:
#             for forbetmatch in forbet_matches:
#                 fortunatime = datetime.strptime(fortunamatch[2], '%Y-%m-%d %H:%M')
#                 forbettime = datetime.strptime(forbetmatch[2], '%Y-%m-%d %H:%M')
#
#                 if fortunatime == forbettime:
#                     fortunaone = fortunamatch[0].rstrip(".").replace(".", " ").split(" ")
#                     fortunatwo = fortunamatch[1].rstrip(".").replace(".", " ").split(" ")
#                     forbetone = forbetmatch[0].rstrip(".").replace(".", " ").split(" ")
#                     forbettwo = forbetmatch[1].rstrip(".").replace(".", " ").split(" ")
#                     findone = any([a == b for (a, b) in itertools.product(fortunaone, forbetone)]) == True
#                     findtwo = any([a == b for (a, b) in itertools.product(fortunatwo, forbettwo)]) == True
#
#                     if findone or findtwo:
#                         c.execute('SELECT id from Fortuna_teams WHERE Fortuna_name = "' + fortunamatch[0] + '"')
#                         fortunaoneid = c.fetchall()
#                         c.execute('SELECT id from Fortuna_teams WHERE Fortuna_name = "' + fortunamatch[1] + '"')
#                         fortunatwoid = c.fetchall()
#                         c.execute('SELECT id from Forbet_teams WHERE Forbet_name = "' + forbetmatch[0] + '"')
#                         forbetoneid = c.fetchall()
#                         c.execute('SELECT id from Forbet_teams WHERE Forbet_name = "' + forbetmatch[1] + '"')
#                         forbettwoid = c.fetchall()
#                         c.execute("INSERT INTO matchedteams VALUES (?, ?, ?, ?, ?)",
#                                   (None, fortunaoneid[0][0], forbetoneid[0][0], fortunamatch[0], forbetmatch[0]))
#                         conn.commit()
#                         c.execute("INSERT INTO matchedteams VALUES (?, ?, ?, ?, ?)",
#                                   (None, fortunatwoid[0][0], forbettwoid[0][0], fortunamatch[1], forbetmatch[1]))
#                         conn.commit()
#                         print(fortunamatch[0] + " " + fortunamatch[1] + " " + forbetmatch[0] + " " + forbetmatch[1])

# matchteams()

def matchmatches():
    c.execute("DROP TABLE IF EXISTS matches")
    c.execute("CREATE TABLE IF NOT EXISTS matches(id INTEGER PRIMARY KEY, Fortunaid INT, Forbetid INT, FOREIGN KEY (Fortunaid)" 
              "REFERENCES Fortuna_matches (id), FOREIGN KEY (Forbetid) REFERENCES Forbet_matches(id))")

    c.execute("SELECT * FROM Fortuna_matches")
    matches = c.fetchall()
    for match in matches:
        print(match)
        c.execute('SELECT nameForbet FROM matchedteams WHERE nameFortuna = "' + str(match[1]) + '"')
        forbetnameone = c.fetchall()
        if len(forbetnameone):
            forbetnameone = forbetnameone[0][0]
        else:
            forbetnameone = ''
        c.execute('SELECT nameForbet FROM matchedteams WHERE nameFortuna = "' + str(match[2]) + '"')
        forbetnametwo = c.fetchall()
        if len(forbetnametwo):
            forbetnametwo = forbetnametwo[0][0]
        else:
            forbetnametwo = ''
        c.execute('SELECT id FROM Forbet_matches WHERE date = "' + (match[3]) + '" AND (t1 = "' + str(forbetnameone) +
                                                                      '" OR t2 = "' + str(forbetnametwo) + '")')
        data = c.fetchall()
        print(data)
        if len(data)>0:
            c.execute('INSERT INTO matches VALUES (?, ?, ?)', (None, match[0], data[0][0]))
            conn.commit()


c.execute("SELECT * FROM matches")
matches = c.fetchall()
for match in matches:
    c.execute('SELECT * FROM Fortuna_matches WHERE id = "' + str(match[1]) + '"')
    teams = c.fetchall()
    print(teams[0][1] + " - " + teams[0][2])
    c.execute('SELECT * FROM Fortuna_match_odds WHERE id = "' + str(match[1]) + '"')
    fortunamatch = c.fetchall()
    c.execute('SELECT * FROM Forbet_match_odds WHERE id = "' + str(match[2]) + '"')
    forbetmatch = c.fetchall()
    print("Kursy w Fortunie:")
    print(str(fortunamatch[0][1]) + " " + str(fortunamatch[0][2]) + " " + str(fortunamatch[0][3]) + " " + str(
        fortunamatch[0][4]) + " " + str(fortunamatch[0][5]) + " " + str(fortunamatch[0][6]))
    print("Kursy w Forbecie:")
    print(str(forbetmatch[0][1]) + " " + str(forbetmatch[0][2]) + " " + str(forbetmatch[0][3]))

