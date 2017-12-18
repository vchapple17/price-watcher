from datetime import date, timedelta, datetime, time
from JobDetailClass import JobDetail
from FlightInfoClass import FlightInfo

from MenuClass import Menu

def getJobToExamine():
    jobs = JobDetail.getJobDetailsArray()

    selection = 0
    while(selection < 1 or selection > len(jobs)):
        for i in range(0, len(jobs)):
            print("\t" + str(i+1) + " - " + jobs[i].getDetailsLine())
        prompt = "Make a selection (1 to "+ str(len(jobs))+"): "
        selection = raw_input(prompt)
        try:
            selection = int(selection)
        except:
            selection = 0
    selection -= 1
    return jobs[selection]

#
# MAIN:
#
def main():
    job = getJobToExamine()
    # data = FlightInfo.getJobData(job)




if __name__ == "__main__":
    main()
