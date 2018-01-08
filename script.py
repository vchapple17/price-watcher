from config import database
import sys

try:
    user = sys.argv[1]
except:
    user = 'price_watcher'

try:
    host = sys.argv[2]
except:
    host = 'localhost'

try:
    password = sys.argv[3]
except:
    password = 'password'

try:
    db = sys.argv[4]
except:
    db = 'price_watcher'

db = database(user, password, host, db)

db.runPriceChecks()
