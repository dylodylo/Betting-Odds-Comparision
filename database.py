import sqlite3

conn = sqlite3.connect('bazadanych.db')

c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_match_odds(id INT PRIMARY KEY, jed FLOAT, X FLOAT, dwa FLOAT, jX FLOAT, Xd FLOAT, jd FLOAT)')
    c.execute('CREATE TABLE IF NOT EXISTS Fortuna_matches(id INT PRIMARY KEY, t1 STRING t2 STRING)')
    c.execute('CREATE TABLE IF NOT EXISTS Forbet_matches(id INT PRIMARY KEY, t1 STRING t2 STRING)')
def data_entry():
    c.execute("INSERT INTO match VALUES(1, 2.5, 2.4, 3.2, 1.4, 1.3, 1.2)")
    conn.commit()
    c.close()
    conn.close()

def Fortuna_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12):
    c.execute("INSERT INTO Fortuna_match_odds VALUES (?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12))
    conn.commit()

def Forbet_odds_data_entry(id, odd1, oddx, odd2, odd1x, oddx2, odd12):
    c.execute("INSERT INTO Forbet_match_odds VALUES (?, ?, ?, ?, ?, ?, ?)", (id, odd1, oddx, odd2, odd1x, oddx2, odd12))
    conn.commit()

def Fortuna_match_entry(id, t1, t2):
    c.execute('INSERT INTO Fortuna_match_odds VALUES (?, ?, ?)', (id, t1, t2))
    conn.comit()

def Forbet_match_entry(id, t1, t2):
    c.execute('INSERT INTO Forbet_match_odds VALUES (?, ?, ?)', (id, t1, t2))
    conn.comit()

def delete_table():
    c.execute("DROP TABLE @VarTable")