import plotly.plotly as py
import plotly.graph_objs as go
import csv

from JobDetailClass import JobDetail
# from FlightInfoClass import FlightInfo

dataFile = "flight_log.csv"
try:
    f = open(dataFile, 'r')        # read
except IOError:
    print("Could not read file:", fname)
    sys.exit(1)

with f:
    reader = csv.reader(f)
    for row in reader:
        if row[4] == 1095:
            print("1095")

        pass #do stuff here


# Get Data and Price for each Flight in job
# class Graph:
#     def __init__(self, job):
#         self.job = job
#
#
# data = [go.Scatter(
#           x=df.Date,
#           y=df['AAPL.Close']),
#           text="Hello"]

# Create traces
#https://plot.ly/python/line-and-scatter/

# 1 graph for each job?
# multiple traces (number of flights) that day for each graph.

#
# trace0 = go.Scatter(
#     x = random_x,
#     y = random_y0,
#     mode = 'markers',
#     name = 'markers'
# )
# trace1 = go.Scatter(
#     x = random_x,
#     y = random_y1,
#     mode = 'lines+markers',
#     name = 'lines+markers'
# )
# trace2 = go.Scatter(
#     x = random_x,
#     y = random_y2,
#     mode = 'lines',
#     name = 'lines'
# )
#
# data = [trace0, trace1, trace2]
# py.iplot(data, filename='scatter-mode')
