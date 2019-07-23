import sqlite3
from datetime import datetime
import itertools
import database

conn = sqlite3.connect('bazadanych.db')
c = conn.cursor()

database.insert_all_teams()

database.delete_matchedleagues_table()
database.delete_matchedteams_table()
database.create_matchedleagues_table()
database.create_matchedteams_table()


def matchleagues():
    fortuna_matches = database.select_matches_from_league("Fortuna")
    for match in fortuna_matches:
        league_matched = database.is_league_matched("Fortuna", str(match[3]))
        if not league_matched:
            data = database.select_matches_from_league_with_date_and_team1("Forbet", match[0], match[2])
            if len(data)>0:
                database.insert_matched_leagues(match[3], match[4], data[0][3], data[0][4])
                print(data)
            else:
                data = database.select_matches_from_league_with_date_and_team2("Forbet", match[1], match[2])
                if len(data) > 0:
                    database.insert_matched_leagues(match[3], match[4], data[0][3], data[0][4])
                    print(data)


def matchteams():
    data = database.select_leagues_from_matched_leagues("Fortuna", "Forbet")
    for league in data:
        bookie1matches = database.select_matches_from_matched_league("Fortuna", str(league[0]))
        print(bookie1matches)
        bookie2matches = database.select_matches_from_matched_league("Forbet", str(league[1]))
        print(bookie2matches)
        for bookie1match in bookie1matches:
            for bookie2match in bookie2matches:
                bookie1matchtime = datetime.strptime(bookie1match[2], '%Y-%m-%d %H:%M')
                bookie2matchtime = datetime.strptime(bookie2match[2], '%Y-%m-%d %H:%M')

                if bookie1matchtime == bookie2matchtime:
                    bookie1team1 = bookie1match[0].rstrip(".").replace(".", " ").split(" ") #team1 phrases
                    bookie1team2 = bookie1match[1].rstrip(".").replace(".", " ").split(" ") #team2 phrases
                    bookie2team1 = bookie2match[0].rstrip(".").replace(".", " ").split(" ")
                    bookie2team2 = bookie2match[1].rstrip(".").replace(".", " ").split(" ")

                    #find any matching phrase for teams1 or teams2
                    #so we find also if two teams have FC in name (like Liverpool FC and Everton FC)
                    findone = any([a == b for (a, b) in itertools.product(bookie1team1, bookie2team1)]) is True
                    findtwo = any([a == b for (a, b) in itertools.product(bookie1team2, bookie2team2)]) is True

                    if findone or findtwo:
                        fortunaoneid = database.get_team_id("Fortuna", bookie1match[0])
                        fortunatwoid = database.get_team_id("Fortuna", bookie1match[1])
                        forbetoneid = database.get_team_id("Forbet", bookie2match[0])
                        forbettwoid = database.get_team_id("Forbet", bookie2match[1])
                        database.insert_matched_teams(fortunaoneid, forbetoneid, bookie1match[0], bookie2match[0])
                        database.insert_matched_teams(fortunatwoid, forbettwoid, bookie1match[1], bookie2match[1])
                        print(bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])


def matchmatches():
    database.delete_matched_matches_table()
    database.create_matched_matches_table()
    matches = database.select_matches_from_bookie("Fortuna")
    for match in matches:
        print(match)
        teamonename = database.get_matched_team_name("Forbet", "Fortuna", str(match[1]))
        teamtwoname = database.get_matched_team_name("Forbet", "Fortuna", str(match[2]))
        c.execute('SELECT id FROM Forbet_matches WHERE date = "' + (match[3]) + '" AND (t1 = "' + str(teamonename) +
                                                                      '" OR t2 = "' + str(teamtwoname) + '")')
        data = c.fetchall()
        print(data)
        if len(data)>0:
            c.execute('INSERT INTO matches VALUES (?, ?, ?)', (None, match[0], data[0][0]))
            conn.commit()

        #TODO: IF fobetnamone or forbetnametwo = '' ale jedno z nich jest zmatchowane to zmatchuj ten drugi


matchleagues()
matchteams()
matchmatches()
c.execute("SELECT * FROM matches")
matches = c.fetchall()
for match in matches:
    c.execute('SELECT * FROM Fortuna_matches WHERE id = "' + str(match[1]) + '"')
    teams = c.fetchall()
    print(teams[0][1] + " - " + teams[0][2])
    fortunamatch = database.get_match_odds("Fortuna", str(match[1]))
    forbetmatch = database.get_match_odds("Forbet", str(match[2]))
    print("Kursy w Fortunie:")
    print(str(fortunamatch[0]) + " " + str(fortunamatch[1]) + " " + str(fortunamatch[2]) + " " + str(
        fortunamatch[3]) + " " + str(fortunamatch[4]) + " " + str(fortunamatch[5]))
    print("Kursy w Forbecie:")
    print(str(forbetmatch[0]) + " " + str(forbetmatch[1]) + " " + str(forbetmatch[2]) + " " + str(forbetmatch[3]) )

c.execute("SELECT * FROM Fortuna_teams")
teams = c.fetchall()
for team in teams:
    c.execute("SELECT * FROM matched_teams WHERE nameFortuna = '" + str(team[1]) + "'")
    data = c.fetchall()
    if len(data) == 0:
        print(team)