#python 2.7
from config import database
import sys

#
# MAIN:
#
def main():
    print("USAGE: python2 " + sys.argv[0] + " username host password database")
    try:
        user = sys.argv[1]
    except:
        user = 'user'

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

    database(user, password, host, db)

if __name__ == "__main__":
    main()
