import sqlite3

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT)')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_matches(id INT PRIMARY KEY, t1 STRING, t2 STRING)')
def data_entry():
    c.execute("INSERT INTO match VALUES(1, 2.5, 2.4, 3.2, 1.4, 1.3, 1.2)")
    conn.commit()
    c.close()
    conn.close()

def Fortuna_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12):
    try:
        c.execute("INSERT INTO Fortuna_match_odds VALUES (?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Forbet_odds_data_entry(id, odd1, oddx, odd2):
    try:
        c.execute("INSERT INTO Forbet_match_odds VALUES (?, ?, ?, ?, 0, 0, 0)", (id, odd1, oddx, odd2))
    except sqlite3.IntegrityError as ie:
        pass
    conn.commit()

def Fortuna_match_entry(id, t1, t2):
    try:
        c.execute('INSERT INTO Fortuna_matches VALUES (?, ?, ?)', (id, t1, t2))
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
    c.execute("DROP TABLE Fortuna_match_odds")
    c.execute("DROP TABLE Forbet_match_odds")
    c.execute("DROP TABLE Fortuna_matches")
    c.execute("DROP TABLE Forbet_matches")

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