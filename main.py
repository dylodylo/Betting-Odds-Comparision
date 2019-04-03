import Fortuna
import Forbet
import database

database.delete_table()
database.create_table()
Fortuna.load_leagues()
Forbet.load_leagues()
database.insert_teams()
database.teams_from_league()
