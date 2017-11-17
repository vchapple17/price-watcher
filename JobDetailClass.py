from CONSTANTS import CONSTANTS
#
# Job Details class:
#
class JobDetail:
    JOB_DETAILS_FILENAME = CONSTANTS.JOB_DETAILS_FILENAME()#"flight_log.csv"
    JOB_DETAILS_NUM_COLS = CONSTANTS.JOB_DETAILS_NUM_COLS()#4

    def __init__(self, depart, arrive, day, flightType):
        self.depart = depart
        self.arrive = arrive
        self.day = day
        self.flightType = flightType
    def getDepartCity(self):
        return self.depart
    def getArriveCity(self):
        return self.arrive
    def getDepartDay(self):
        return self.day
    def getFlightType(self):
        return self.flightType

    def getDetailsLine(self):
        return str(self.depart + " to " + self.arrive + " on " + self.day + " (class "+ self.flightType + ")")

    @staticmethod
    def getJobDetailsArray():
        # Read file
        jobFile = open(JobDetail.JOB_DETAILS_FILENAME, "r")
        jobArr = []
        for line in jobFile:
            line = line.rstrip()
            array = line.split(", ")
            if len(array) == JobDetail.JOB_DETAILS_NUM_COLS:

                jobArr.append( JobDetail( array[0], array[1], array[2], array[3] ) )
            else:
                print("JOB FILE CORRUPT ERROR")
                exit()

        jobFile.close()
        return jobArr
