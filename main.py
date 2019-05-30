import Fortuna
import Forbet
import milenium
import lvbet
import database
import proxy
import sts

#database.delete_all_tables()
#database.create_all_tables()
Fortuna.load_leagues()
#Forbet.load_leagues()
#lvbet.scrap()
#milenium.scrap()
#sts.startscrappingSTS()

#database.insert_all_teams()

# if database.is_match_in_db(21181515):
#     database.update_odds("Fortuna", 21181515, 3, 2, 1)
#     print(database.get_match_odds("Fortuna", 21181515))
#     print(database.compare_odds("Fortuna", 21181515, (3,2,3,0,0,0)))
# else:
#     print("print")