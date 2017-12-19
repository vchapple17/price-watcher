from CONSTANTS import CONSTANTS
# import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
import datetime as datetime
import numpy as np

#
# Job Details class:
#
class JobDetail:
    JOB_DETAILS_FILENAME = CONSTANTS.JOB_DETAILS_FILENAME()#"flight_log.csv"
    JOB_DETAILS_NUM_COLS = CONSTANTS.JOB_DETAILS_NUM_COLS()#4
    FLIGHT_FILENAME = CONSTANTS.FLIGHT_FILENAME()

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

    def graphTraces(self):
        offline.init_notebook_mode()

        # Graph File Name
        graph_name = "graph_"
        graph_name += self.getDepartDay() + "_"
        graph_name += self.getDepartCity() + "_"
        graph_name += self.getArriveCity() + "_"
        graph_name += self.getFlightType()

        # Get Data
        #Log Date, Departure, Arrival, Date, Type, Flight,DepartTime,ArriveTime,Duration,Cost,Nonstop
        flightFile = open(JobDetail.FLIGHT_FILENAME, "r")
        flightFile.readline();

        job = self.getDepartCity() + self.getArriveCity() + self.getDepartDay() + self.getFlightType()
        flights = dict()
        for line in flightFile:
            line = line.rstrip()
            array = line.split(",")
            if job == array[1] + array[2] + array[3] + array[4]:
                flightDetail = array[5] + array[6] + array[7] + array[8]
                try:
                    flights[flightDetail].append( array )
                except:
                    flights[flightDetail] = [ array ]
                # print (flightDetail, flights[flightDetail])
        data = []

        for key, flight in flights.iteritems():
            data_x = []
            data_y = []
            data_name = flight[0][5] + " @ " + flight[0][6]
            for i in range(len(flight)):
                data_x.append(datetime.datetime.strptime(flight[i][0], "%Y-%m-%d %H:%M:%S.%f"))
                data_y.append(int(flight[i][9]))

            data.append(
                go.Scatter(
                    x = data_x,
                    y = data_y,
                    mode = 'lines+markers',
                    name = data_name
                )
            )
        # Graph Data
        layout = go.Layout(
            title=self.getDetailsLine(),
            font=dict(size=16),
            width=800,
            height=640
        )

        offline.plot(
            { 'data': data, 'layout': layout},
            image='png'
        )
        return

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
