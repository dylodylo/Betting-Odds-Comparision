from flask import Flask, render_template,jsonify,g
import json
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/')
def home():
    jsonmatch =[{"druzyna1": "Gruzja", "kursdruzyna1": 1.05, "remis": 13.5, "druzyna2": "Gibraltar", "kursdruzyna2": 38.2}, {"druzyna1": "Czarnog\u00f3ra", "kursdruzyna1": 1.9, "remis": 3.4, "druzyna2": "Kosowo", "kursdruzyna2": 4.31}, {"druzyna1": "Czechy", "kursdruzyna1": 1.75, "remis": 3.65, "druzyna2": "Bu\u0142garia", "kursdruzyna2": 4.83}, {"druzyna1": "Ukraina", "kursdruzyna1": 2.6, "remis": 3.1, "druzyna2": "Serbia", "kursdruzyna2": 2.89}, {"druzyna1": "Litwa", "kursdruzyna1": 2.25, "remis": 3.2, "druzyna2": "Luksemburg", "kursdruzyna2": 3.38}, {"druzyna1": "Dania", "kursdruzyna1": 1.65, "remis": 3.85, "druzyna2": "Irlandia", "kursdruzyna2": 5.35}, {"druzyna1": "Norwegia", "kursdruzyna1": 2.25, "remis": 3.25, "druzyna2": "Rumunia", "kursdruzyna2": 3.33}, {"druzyna1": "WyspyOwcze", "kursdruzyna1": 34.7, "remis": 14.0, "druzyna2": "Hiszpania", "kursdruzyna2": 1.05}, {"druzyna1": "Szwecja", "kursdruzyna1": 1.06, "remis": 13.0, "druzyna2": "Malta", "kursdruzyna2": 30.95}, {"druzyna1": "\u0141otwa", "kursdruzyna1": 5.07, "remis": 3.65, "druzyna2": "Izrael", "kursdruzyna2": 1.72}, {"druzyna1": "MacedoniaP\u0142n.", "kursdruzyna1": 5.15, "remis": 3.7, "druzyna2": "Polska", "kursdruzyna2": 1.7}, {"druzyna1": "Austria", "kursdruzyna1": 1.75, "remis": 3.5, "druzyna2": "S\u0142owenia", "kursdruzyna2": 5.12}, {"druzyna1": "Chorwacja", "kursdruzyna1": 1.6, "remis": 3.9, "druzyna2": "Walia", "kursdruzyna2": 5.84}, {"druzyna1": "Islandia", "kursdruzyna1": 1.65, "remis": 3.8, "druzyna2": "Albania", "kursdruzyna2": 5.45}, {"druzyna1": "Estonia", "kursdruzyna1": 4.48, "remis": 3.3, "druzyna2": "IrlandiaP\u0142n.", "kursdruzyna2": 1.9}, {"druzyna1": "Azerbejd\u017can", "kursdruzyna1": 3.34, "remis": 3.05, "druzyna2": "W\u0119gry", "kursdruzyna2": 2.35}, {"druzyna1": "Mo\u0142dawia", "kursdruzyna1": 1.5, "remis": 4.15, "druzyna2": "Andora", "kursdruzyna2": 6.9}, {"druzyna1": "Rosja", "kursdruzyna1": 1.01, "remis": 23.0, "druzyna2": "SanMarino", "kursdruzyna2": 52.48}, {"druzyna1": "Finlandia", "kursdruzyna1": 3.18, "remis": 3.3, "druzyna2": "Bo\u015bniaiHercegowina", "kursdruzyna2": 2.3}, {"druzyna1": "Armenia", "kursdruzyna1": 1.18, "remis": 7.0, "druzyna2": "Liechtenstein", "kursdruzyna2": 16.05}, {"druzyna1": "Bia\u0142oru\u015b", "kursdruzyna1": 15.8, "remis": 7.05, "druzyna2": "Niemcy", "kursdruzyna2": 1.18}, {"druzyna1": "Turcja", "kursdruzyna1": 5.93, "remis": 3.75, "druzyna2": "Francja", "kursdruzyna2": 1.62}, {"druzyna1": "Szkocja", "kursdruzyna1": 1.52, "remis": 4.1, "druzyna2": "Cypr", "kursdruzyna2": 6.63}, {"druzyna1": "Belgia", "kursdruzyna1": 1.03, "remis": 17.0, "druzyna2": "Kazachstan", "kursdruzyna2": 43.6}, {"druzyna1": "Grecja", "kursdruzyna1": 4.31, "remis": 3.25, "druzyna2": "W\u0142ochy", "kursdruzyna2": 1.95}, {"druzyna1": "Czechy", "kursdruzyna1": 1.8, "remis": 3.55, "druzyna2": "Czarnog\u00f3ra", "kursdruzyna2": 4.2}, {"druzyna1": "Bu\u0142garia", "kursdruzyna1": 1.85, "remis": 3.5, "druzyna2": "Kosowo", "kursdruzyna2": 4.02}, {"druzyna1": "Ukraina", "kursdruzyna1": 1.1, "remis": 9.5, "druzyna2": "Luksemburg", "kursdruzyna2": 16.42}, {"druzyna1": "Serbia", "kursdruzyna1": 1.1, "remis": 9.5, "druzyna2": "Litwa", "kursdruzyna2": 26.13}, {"druzyna1": "Irlandia", "kursdruzyna1": 1.01, "remis": 20.0, "druzyna2": "Gibraltar", "kursdruzyna2": 28.43}, {"druzyna1": "Dania", "kursdruzyna1": 1.25, "remis": 5.5, "druzyna2": "Gruzja", "kursdruzyna2": 10.7}, {"druzyna1": "Hiszpania", "kursdruzyna1": 1.22, "remis": 6.5, "druzyna2": "Szwecja", "kursdruzyna2": 12.64}, {"druzyna1": "Malta", "kursdruzyna1": 13.71, "remis": 6.0, "druzyna2": "Rumunia", "kursdruzyna2": 1.23}, {"druzyna1": "WyspyOwcze", "kursdruzyna1": 6.96, "remis": 4.6, "druzyna2": "Norwegia", "kursdruzyna2": 1.4}, {"druzyna1": "Polska", "kursdruzyna1": 1.45, "remis": 4.35, "druzyna2": "Izrael", "kursdruzyna2": 7.51}, {"druzyna1": "\u0141otwa", "kursdruzyna1": 4.32, "remis": 3.3, "druzyna2": "S\u0142owenia", "kursdruzyna2": 1.85}, {"druzyna1": "MacedoniaP\u0142n.", "kursdruzyna1": 4.02, "remis": 3.5, "druzyna2": "Austria", "kursdruzyna2": 1.85}, {"druzyna1": "Kazachstan", "kursdruzyna1": 1.05, "remis": 13.0, "druzyna2": "SanMarino", "kursdruzyna2": 21.76}, {"druzyna1": "Azerbejd\u017can", "kursdruzyna1": 4.2, "remis": 3.3, "druzyna2": "S\u0142owacja", "kursdruzyna2": 1.95}, {"druzyna1": "Niemcy", "kursdruzyna1": 1.03, "remis": 16.0, "druzyna2": "Estonia", "kursdruzyna2": 23.87}, {"druzyna1": "Bia\u0142oru\u015b", "kursdruzyna1": 2.75, "remis": 3.15, "druzyna2": "IrlandiaP\u0142n.", "kursdruzyna2": 2.7}, {"druzyna1": "W\u0119gry", "kursdruzyna1": 2.98, "remis": 3.15, "druzyna2": "Walia", "kursdruzyna2": 2.5}, {"druzyna1": "Islandia", "kursdruzyna1": 2.4, "remis": 3.15, "druzyna2": "Turcja", "kursdruzyna2": 3.15}, {"druzyna1": "Andora", "kursdruzyna1": 35.45, "remis": 15.0, "druzyna2": "Francja", "kursdruzyna2": 1.02}, {"druzyna1": "Albania", "kursdruzyna1": 1.55, "remis": 3.9, "druzyna2": "Mo\u0142dawia", "kursdruzyna2": 5.76}, {"druzyna1": "Rosja", "kursdruzyna1": 1.25, "remis": 5.75, "druzyna2": "Cypr", "kursdruzyna2": 9.87}, {"druzyna1": "Belgia", "kursdruzyna1": 1.12, "remis": 8.75, "druzyna2": "Szkocja", "kursdruzyna2": 14.68}, {"druzyna1": "Liechtenstein", "kursdruzyna1": 12.7, "remis": 5.75, "druzyna2": "Finlandia", "kursdruzyna2": 1.25}, {"druzyna1": "W\u0142ochy", "kursdruzyna1": 1.6, "remis": 3.95, "druzyna2": "Bo\u015bniaiHercegowina", "kursdruzyna2": 5.07}, {"druzyna1": "Grecja", "kursdruzyna1": 1.45, "remis": 4.3, "druzyna2": "Armenia", "kursdruzyna2": 6.53}]
    return render_template("homepage.html", jsonmatch=jsonmatch)

@app.route('/liga-mistrzow')
def add_numbers():
    cur=get_db().cursor() 
    cur.execute("select t1,t2,jed,X,dwa,jx,Xd,jd FROM (select * FROM Fortuna_match_odds WHERE Fortuna_match_odds.league_id=25 )AS F Inner join Fortuna_matches  On F.id = Fortuna_matches.id  ")
    wyn=cur.fetchall()
    return jsonify(wyn)



#sqlliteconnecting

DATABASE = 'bazadanych.db'
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
 


if __name__ == '__main__':
    app.run()


