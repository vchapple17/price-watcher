import os
from datetime import datetime
import signal

# Catch SIGINT
def signal_handler(signal, frame):
    print("\nExiting\n")
    exit(0)

CITY_CODES_FILENAME = "city-codes.txt"
JOB_DETAILS_FILENAME = "job-details.txt"
JOB_DETAILS_NUM_COLS = 4

class JobDetail():
    def __init__(self, depart, arrive, day, flightType):
        self.depart = depart
        self.arrive = arrive
        self.day = day
        self.flightType = flightType

def displayJobs():
    try:
        jobFile = open(JOB_DETAILS_FILENAME, "r")
        print("ALL JOBS")
        print("--------")
        print jobFile.read()
        jobFile.close()
    except:
        jobFile = open(JOB_DETAILS_FILENAME, "w")
        jobFile.close()
        return

def saveJobDetails( job ):
    jobArr = getJobDetailsArray()
    jobTuple = ( job.depart, job.arrive, job.day, job.flightType )
    for i in jobArr:
        if i == jobTuple:
            print("\n\nDuplicate job. Not saved.\n\n")
            return
    # Save Information
    jobFile = open(JOB_DETAILS_FILENAME, "a")
    jobFile.write(job.depart)
    jobFile.write(", ")
    jobFile.write(job.arrive)
    jobFile.write(", ")
    jobFile.write(job.day)
    jobFile.write(", ")
    jobFile.write(job.flightType)
    jobFile.write("\n")
    jobFile.close()

def getJobDetailsArray():
    # Read file
    jobFile = open(JOB_DETAILS_FILENAME, "r")
    jobArr = []
    for line in jobFile:
        line = line.rstrip()
        array = line.split(", ")
        if len(array) == JOB_DETAILS_NUM_COLS:
            jobArr.append( ( array[0], array[1], array[2], array[3] ) )
        else:
            print("JOB FILE CORRUPT ERROR")
            exit()

    jobFile.close()
    return jobArr

def getCityCodesDict():
    # Read file
    # Map dictionary, key = three letter code, value = full city name
    cityFile = open(CITY_CODES_FILENAME, "r")
    cityDict = dict()
    for line in cityFile:
        array = line.split("\t", 1)
        cityDict[array[0]] = array[1]
        #print(array[0], cityDict[array[0]])
    cityFile.close()
    return cityDict


def promptJobDetails():
    cityDict = getCityCodesDict()

    print("\n-------------------------------------------")
    print("Please give details about a one-way flight.")
    print("-------------------------------------------")
    # DEPARTURE
    departure = raw_input("City DEPARTURE code: ")
    departure = departure.upper()
    while departure not in cityDict:
        departure = raw_input("ERROR:  Type a valid three letter city code for departure: ")
        departure = departure.upper()

    # ARRIVAL CITY
    arrival = raw_input("City ARRIVAL code: ")
    arrival = arrival.upper()
    while arrival not in cityDict or arrival == departure:
        arrival = raw_input("ERROR:  Type a valid three letter city code for arrival: ")
        arrival = arrival.upper()

    # DATE (MM/DD/YYYY)
    departDate = raw_input("Departure Date: ")
    departDate = validateDate(departDate)
    while departDate == None:
        departDate = raw_input("ERROR: Departure Date (MM/DD/YYYY): ")
        departDate = validateDate(departDate)

    departDate = departDate.strftime("%m/%d/%Y")
    # Flight type (A, B, C)
    flightType = raw_input("Choose A (business), B (Anytime), C (Wanna Get Away): ")
    flightType = flightType.upper()

    while flightType not in ("A", "B", "C"):
        flightType = raw_input("ERROR:  Type a valid single letter code for type of flight: ")
        flightType = flightType.upper()

    #Create Job Details & saveFlightInfo
    job = JobDetail(departure, arrival, departDate, flightType)
    saveJobDetails( job )

def validateDate(date):
    try:
        newDate = datetime.strptime(date, '%m/%d/%Y')
        #nowDate = datetime.now()
        # if nowDate < datetime(*(newDate)):
        return newDate
        # else:
        #     return None

    except ValueError:
        return None

def main():
    signal.signal( signal.SIGINT, signal_handler )
    os.system('cls||clear')
    while 1:
        # Show Current Jobs
        displayJobs()

        # Add job
        promptJobDetails()

if __name__ == "__main__":
    main()
