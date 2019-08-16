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


def matchleagues(bookie1, bookie2):
    fortuna_matches = database.select_matches_from_league(bookie1)
    for match in fortuna_matches:
        league_matched = database.is_league_matched(bookie1, str(match[3]))
        if not league_matched:
            data = database.select_matches_from_league_with_date_and_team1(bookie2, match[0], match[2])
            league2_matched = database.is_league_matched(bookie2, data[0][3])
            if not league2_matched:
                if len(data)>0:
                    database.insert_matched_leagues(match[3], match[4], data[0][3], data[0][4], bookie1, bookie2)
                    print(data)
                else:
                    data = database.select_matches_from_league_with_date_and_team2(bookie2, match[1], match[2])
                    if len(data) > 0:
                        database.insert_matched_leagues(match[3], match[4], data[0][3], data[0][4], bookie1, bookie2)
                        print(data)
            else:
                if len(data)>0:
                    database.update_matched_leagues(match[3], match[4], bookie1, bookie2, data[0][3])
                    print(data)
                else:
                    data = database.select_matches_from_league_with_date_and_team2(bookie2, match[1], match[2])
                    if len(data) > 0:
                        database.update_matched_leagues(match[3], match[4], bookie1, bookie2, data[0][3])
                        print(data)


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
                        team1matched = database.is_team_matched(bookie1, fortunaoneid)
                        team2matched = database.is_team_matched(bookie1, fortunatwoid)
                        if not team1matched and not team2matched:
                            database.insert_matched_teams(fortunaoneid, forbetoneid, bookie1match[0], bookie2match[0], bookie1, bookie2)
                            database.insert_matched_teams(fortunatwoid, forbettwoid, bookie1match[1], bookie2match[1], bookie1, bookie2)
                            print(bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        if team1matched and not team2matched:
                            database.update_matched_teams(forbetoneid, bookie2match[0],
                                                          bookie2, bookie1, fortunaoneid)
                            database.insert_matched_teams(fortunatwoid, forbettwoid, bookie1match[1], bookie2match[1],
                                                          bookie1, bookie2)
                            print(
                                bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        if not team1matched and team2matched:
                            database.insert_matched_teams(fortunaoneid, forbetoneid, bookie1match[0], bookie2match[0],
                                                          bookie1, bookie2)
                            database.update_matched_teams(forbettwoid, bookie2match[1],
                                                          bookie2, bookie1, fortunatwoid)
                            print(
                                bookie1match[0] + " " + bookie1match[1] + " " + bookie2match[0] + " " + bookie2match[1])
                        break


def matchmatches(bookie1, bookie2):
    database.delete_matched_matches_table()
    database.create_matched_matches_table()
    matches = database.select_matches_from_bookie(bookie1)
    for match in matches:
        print(match)
        teamonename = database.get_matched_team_name(bookie2, bookie1, str(match[1]))
        teamtwoname = database.get_matched_team_name(bookie2, bookie1, str(match[2]))
        c.execute('SELECT id FROM ' + bookie2 + '_matches WHERE date = "' + (match[3]) + '" AND (t1 = "' + str(teamonename) +
                                                                      '" OR t2 = "' + str(teamtwoname) + '")')
        data = c.fetchall()
        print(data)
        if len(data)>0:
            c.execute('INSERT INTO matches (' + bookie1 + 'id, ' + bookie2 + 'id) VALUES (' + str(match[0]) + ', ' + str(data[0][0]) + ')')
            conn.commit()

        #TODO: IF fobetnamone or forbetnametwo = '' ale jedno z nich jest zmatchowane to zmatchuj ten drugi


def main(bookie1, bookie2):
    matchleagues(bookie1, bookie2)
    matchteams(bookie1, bookie2)
    matchmatches(bookie1, bookie2)
    c.execute("SELECT " + bookie1 + "id, " + bookie2 + "id FROM matches")
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