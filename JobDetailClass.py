#
# Job Details class:
#
class JobDetail:
    JOB_DETAILS_FILENAME = "job-details.txt"
    JOB_DETAILS_NUM_COLS = 4

    def __init__(self, depart, arrive, day, flightType):
        self.depart = depart
        self.arrive = arrive
        self.day = day
        self.flightType = flightType
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
