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
            selection = -1


    if selection == 1:
        manageJobs(db)
    elif selection == 2:
        db.runPriceChecks()
    elif selection == 3:
        db.graphJobs()
    else:
        print("ERROR")
        sys.exit()



def manageJobs(db):
    print("Manage jobs")


if __name__ == "__main__":
    main()
