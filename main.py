import Fortuna
import Forbet
# import milenium
import lvbet
import database
import sqlite3
# import proxy
# import sts
# import algorytm

#database.delete_all_tables()
#database.create_all_tables()
# Fortuna.scrap()
# Forbet.load_leagues()
# Forbet.load_matches()
#lvbet.scrap()
# algorytm.fortuna_insert()
# algorytm.relationship_database()
#milenium.scrap()
#sts.startscrappingSTS()


#database.insert_all_teams()

conn = sqlite3.connect('bazadanych.db')

cur = conn.cursor()

cur.execute("SELECT * FROM matches")
res = cur.fetchall()
fortunaid = []
forbetid = []
matches = []
fortunaodds = [[0,0,0,0]]
forbetodds = [[0,0,0,0]]
lvbetodds = [[0,0,0,0]]
for match in res:
    print(match)
    fortunaid.append(match[1])
    forbetid.append(match[2])
    if match[1] is not None:
        cur.execute("SELECT * FROM Fortuna_match_odds WHERE id = " + str(match[1]))
        fortunaodds = cur.fetchall()
    else:
        fortunaodds[0][1] = 0
        fortunaodds[0][2] = 0
        fortunaodds[0][3] = 0
    if match[2] is not None:
        cur.execute("SELECT * FROM Forbet_match_odds WHERE id = " + str(match[2]))
        forbetodds = cur.fetchall()
    else:
        forbetodds[0][1] = 0
        forbetodds[0][2] = 0
        forbetodds[0][3] = 0
    if match[3] is not None:
        cur.execute("SELECT * FROM Lvbet_match_odds WHERE id = " + str(match[3]))
        lvbetodds = cur.fetchall()
        if lvbetodds
    else:
        lvbetodds[0][1] = 0
        lvbetodds[0][2] = 0
        lvbetodds[0][3] = 0
    if match[1] is not None:
        cur.execute("SELECT * FROM Fortuna_matches WHERE id = " + str(match[1]))
        teams = cur.fetchall()
    elif match[2] is not None:
        cur.execute("SELECT * FROM Fortuna_matches WHERE id = " + str(match[2]))
        teams = cur.fetchall()
    else:
        cur.execute("SELECT * FROM Fortuna_matches WHERE id = " + str(match[3]))
        teams = cur.fetchall()
    hodds = [fortunaodds[0][1], forbetodds[0][1], lvbetodds[0][1]]
    dodds = [fortunaodds[0][2], forbetodds[0][2], lvbetodds[0][2]]
    aodds = [fortunaodds[0][3], forbetodds[0][3], lvbetodds[0][3]]
    hmax = hodds.index(max(hodds))
    dmax = dodds.index(max(dodds))
    amax = aodds.index(max(aodds))