from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import g
app = Flask(__name__)

DATABASE = 'bazadanych.db'


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




@app.route('/')


def index():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM matches")
    res = cur.fetchall()
    fortunaid = []
    forbetid = []
    matches = []
    fortunaodds = [[0, 0, 0, 0]]
    forbetodds = [[0, 0, 0, 0]]
    lvbetodds = [(0, 0, 0, 0)]
    for match in res:
        print(match)
        fortunaid.append(match[1])
        forbetid.append(match[2])
        if match[1] is not None:
            cur.execute("SELECT * FROM Fortuna_match_odds WHERE id = " + str(match[1]))
            fortunaodds = cur.fetchall()
        else:
            fortunaodds = [[0, 0, 0, 0]]

        if match[2] is not None:
            cur.execute("SELECT * FROM Forbet_match_odds WHERE id = " + str(match[2]))
            forbetodds = cur.fetchall()
        else:
            forbetodds = [[0, 0, 0, 0]]

        if match[3] is not None:
            cur.execute("SELECT * FROM Lvbet_match_odds WHERE id = " + str(match[3]))
            lvbetodds = cur.fetchall()
            if lvbetodds == []:
                lvbetodds = [(0, 0, 0, 0)]
        else:

            lvbetodds = [(0, 0, 0, 0)]
        if match[1] is not None:
            cur.execute("SELECT * FROM Fortuna_matches WHERE id = " + str(match[1]))
            teams = cur.fetchall()
        elif match[2] is not None:
            cur.execute("SELECT * FROM Forbet_matches WHERE id = " + str(match[2]))
            teams = cur.fetchall()

        else:
            cur.execute("SELECT * FROM Lvbet_matches WHERE id = " + str(match[3]))
            teams = cur.fetchall()

        print(fortunaodds)
        print(forbetodds)
        print(lvbetodds)
        hodds = [fortunaodds[0][1], forbetodds[0][1], lvbetodds[0][1]]
        dodds = [fortunaodds[0][2], forbetodds[0][2], lvbetodds[0][2]]
        aodds = [fortunaodds[0][3], forbetodds[0][3], lvbetodds[0][3]]
        hmax = hodds.index(max(hodds))
        dmax = dodds.index(max(dodds))
        amax = aodds.index(max(aodds))
        if hmax == 0:
            home = fortunaodds[0][1]
            hbookie = "Fortuna"
        if hmax == 1:
            home = forbetodds[0][1]
            hbookie = "Forbet"
        if hmax == 2:
            home = lvbetodds[0][1]
            hbookie = "Lvbet"
        if dmax == 0:
            draw = fortunaodds[0][2]
            dbookie = "Fortuna"
        if dmax == 1:
            draw = forbetodds[0][2]
            dbookie = "Forbet"
        if dmax == 2:
            draw = lvbetodds[0][2]
            dbookie = "Lvbet"
        if amax == 0:
            away = fortunaodds[0][3]
            abookie = "Fortuna"
        if amax == 1:
            away = forbetodds[0][3]
            abookie = "Forbet"
        if amax == 2:
            away = lvbetodds[0][3]
            abookie = "Lvbet"

        m = (teams[0][1], teams[0][2], teams[0][3], home, hbookie, draw, dbookie, away, abookie)
        matches.append(m)

    print(len(matches))
    return render_template("index.html", matches = matches)


if __name__ == "__main__":
    app.run(debug=True)