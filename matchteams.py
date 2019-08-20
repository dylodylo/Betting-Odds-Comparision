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


#WPISUJEMY B1 I EWENTAULNIE PRZYRÓWNUJEMY DO B2
def matchleagues(bookie1, bookie2):
    matches = database.select_matches_from_bookie_with_date_league(bookie1)
    for match in matches:
        teamone = match[0]
        teamtwo = match[1]
        date = match[2]
        leagueid = match[3]
        site = match[4]
        league_matched = database.is_league_matched(bookie1, str(leagueid))
        if not league_matched:
            data = database.select_matches_from_league_with_date_and_team1(bookie2, teamone, date)
            data2 = database.select_matches_from_league_with_date_and_team2(bookie2, teamtwo, date)
            if len(data) > 0:
                b2leagueid = data[0][3]
                b2site = data[0][4]
                league2_matched = database.is_league_matched(bookie2,  b2leagueid)
                if not league2_matched:
                    database.insert_matched_leagues(leagueid, site,  b2leagueid, b2site, bookie1, bookie2)
                    print(data)
                else:
                    database.update_matched_leagues(leagueid, site, bookie1, bookie2,  b2leagueid)
                    print(data)
            elif len(data2) > 0:
                    b2leagueid = data2[0][3]
                    b2site = data2[0][4]
                    league2_matched = database.is_league_matched(bookie2,  b2leagueid)
                    if not league2_matched:
                        database.insert_matched_leagues(leagueid, site,  b2leagueid, b2site, bookie1, bookie2)
                        print(data)
                    else:
                        database.update_matched_leagues(leagueid, site, bookie1, bookie2,  b2leagueid)
                        print(data)
            #else:
               # database.insert_matched_leagues(leagueid, site, '', '', bookie1, bookie2)


def matchteams(bookie1, bookie2):
    data = database.select_leagues_from_matched_leagues(bookie1, bookie2)
    for league in data:
        bookie1matches = database.select_matches_from_matched_league(bookie1, str(league[0]))
        print(bookie1matches)
        bookie2matches = database.select_matches_from_matched_league(bookie2, str(league[1]))
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
                        fortunaoneid = database.get_team_id(bookie1, bookie1match[0])
                        fortunatwoid = database.get_team_id(bookie1, bookie1match[1])
                        forbetoneid = database.get_team_id(bookie2, bookie2match[0])
                        forbettwoid = database.get_team_id(bookie2, bookie2match[1])
                        team1matched = database.is_team_matched(bookie2, forbetoneid)
                        team2matched = database.is_team_matched(bookie2, forbettwoid)
                        if not team1matched and not team2matched:
                            database.insert_matched_teams(fortunaoneid, forbetoneid, bookie1match[0], bookie2match[0], bookie1, bookie2)
                            database.insert_matched_teams(fortunatwoid, forbettwoid, bookie1match[1], bookie2match[1], bookie1, bookie2)
                            print(bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        elif team1matched and not team2matched:
                            database.update_matched_teams(fortunaoneid, bookie2match[0],
                                                          bookie1, bookie2, forbetoneid)
                            database.insert_matched_teams(fortunatwoid, forbettwoid, bookie1match[1], bookie2match[1],
                                                          bookie1, bookie2)
                            print(
                                bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        elif not team1matched and team2matched:
                            database.insert_matched_teams(fortunaoneid, forbetoneid, bookie1match[0], bookie2match[0],
                                                          bookie1, bookie2)
                            database.update_matched_teams(fortunatwoid, bookie2match[1],
                                                          bookie1, bookie1, forbettwoid)
                            print(
                                bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        else:
                            database.update_matched_teams(fortunaoneid, bookie2match[0],
                                                          bookie1, bookie2, forbetoneid)
                            database.update_matched_teams(fortunatwoid, bookie2match[1],
                                                         bookie1, bookie2, forbettwoid)
                        break


def matchmatches(bookie1, bookie2):
    #database.delete_matched_matches_table()
    database.create_matched_matches_table()
    matches = database.select_matches_from_bookie(bookie1)
    for match in matches:
        print(match)

        c.execute('SELECT name' + bookie2 + ' FROM matched_teams WHERE name' + bookie1 + ' = "' + match[1] + '"')
        teamone = c.fetchall()
        c.execute('SELECT name' + bookie2 + ' FROM matched_teams WHERE name' + bookie1 + ' = "' + match[2] + '"')
        teamtwo = c.fetchall()
        c.execute('SELECT id FROM ' + bookie2 + '_matches WHERE date = "' + match[3] + '" AND (t1 = "' + teamone[0] +
                  '" OR t2 = "' + teamtwo[0] + '"')
        data = c.fetchall()
        if len(data) > 0:
            matchmatched = database.is_match_matched(bookie1, str(match[0]))
            matchmatched2 = database.is_match_matched(bookie2, str(data[0][0]))
            if matchmatched:
                database.update_matched_match(bookie2, bookie1, str(data[0][0]), str(match[0]))
            elif matchmatched2:
                database.update_matched_match(bookie1, bookie2, str(match[0]), str(data[0][0]))
            else:
                    c.execute('INSERT INTO matches (id' + bookie1 + ', id' + bookie2 + ') VALUES (' + str(match[0]) + ', ' + str(data[0][0]) + ')')
                    conn.commit()

        #TODO: IF fobetnamone or forbetnametwo = '' ale jedno z nich jest zmatchowane to zmatchuj ten drugi


def main(bookie1, bookie2):
    matchleagues(bookie1, bookie2)
    matchteams(bookie1, bookie2)
    matchmatches(bookie1, bookie2)
    c.execute("SELECT id" + bookie1 + ", id" + bookie2 + " FROM matches WHERE id" + bookie1 + " NOT NULL AND id" + bookie2 + " NOT NULL")
    matches = c.fetchall()
    for match in matches:
        c.execute('SELECT * FROM ' + bookie1 + '_matches WHERE id = "' + str(match[0]) + '"')
        teams = c.fetchall()
        print(teams[0][1] + " - " + teams[0][2])
        fortunamatch = database.get_match_odds(bookie1, str(match[0]))
        forbetmatch = database.get_match_odds(bookie2, str(match[1]))

        print("Kursy w " + bookie1 + ":")
        if len(fortunamatch) > 0:
            print(str(fortunamatch[0]) + " " + str(fortunamatch[1]) + " " + str(fortunamatch[2]) + " " + str(
                fortunamatch[3]) + " " + str(fortunamatch[4]) + " " + str(fortunamatch[5]))
        print("Kursy w " + bookie2 + ":")
        if len(forbetmatch) > 0:
            print(str(forbetmatch[0]) + " " + str(forbetmatch[1]) + " " + str(forbetmatch[2]) + " " + str(forbetmatch[3]) )

    c.execute("SELECT * FROM " + bookie1 + "_teams")
    teams = c.fetchall()
    for team in teams:
        c.execute("SELECT * FROM matched_teams WHERE name" + bookie1 + ' = "' + str(team[1]) + '"')
        data = c.fetchall()
        if len(data) == 0:
            print(team)


main("Fortuna", "Forbet")