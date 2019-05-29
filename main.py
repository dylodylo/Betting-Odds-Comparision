import Fortuna
import Forbet
import milenium
import lvbet
import database
import proxy

database.delete_all_tables()
database.create_all_tables()
Fortuna.load_leagues()
Forbet.load_leagues()
lvbet.scrap()
milenium.scrap()
