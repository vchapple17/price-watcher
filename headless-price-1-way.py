# from selenium import webdriver
from datetime import date, timedelta, datetime, time
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
from JobDetailClass import JobDetail
from FlightInfoClass import FlightInfo

print("Loading...")

#
# MAIN:
#
# Search for flight prices for all future jobs
# Save new flight prices
def main():
    # Get Job details
    jobs = JobDetail.getJobDetailsArray()

    for i in jobs:
        # Check date is within 6 months
        DEPART_DATE = i.day
        six_months_away = datetime.now() + timedelta(days=210)
        departDate = datetime.strptime(DEPART_DATE, '%m/%d/%Y')
        if departDate <= six_months_away:
            # Get Flight Cost from Southwest
            FlightInfo.saveFlightCosts(i)

if __name__ == "__main__":
    main()
