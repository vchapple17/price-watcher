#python 2.7
from config import database
import sys

# from JobDetailClass import JobDetail
# from FlightInfoClass import FlightInfo
# from datetime import date, timedelta, datetime, time

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

    # MAIN MENU
    selection = 0
    numOptions = 3
    while selection < 1 or selection > numOptions:
        prompt  = " MENU\n"
        prompt += "======\n"
        prompt += "1 - Manage Jobs\n"
        prompt += "2 - Run Price Check\n"
        prompt += "3 - Graph Prices\n"
        prompt += ">> "

        selection = raw_input(prompt)
        try:
            selection = int(selection)
        except:
            selection == -1

    db = database(user, password, host, db)
    if selection == 1:
        manageJobs(db)
    elif selection == 2:
        db.runPriceChecks()
    elif selection == 3:
        graphJobs(db)
    else:
        print("ERROR")
        sys.exit()



def manageJobs(db):
    print("Manage jobs")
    pass

def priceCheck(db):
    print("Run price check")

    pass

def graphJobs(db):
    print("graph")
    pass

if __name__ == "__main__":
    main()
