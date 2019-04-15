import Fortuna
import Forbet
import database
import proxy

database.delete_table()
database.create_table()
Fortuna.load_leagues()
Forbet.load_leagues()
database.insert_teams()
# # database.teams_from_league()
# print(proxy.get_actual_proxy())
# print(len(proxy.get_proxies()))
