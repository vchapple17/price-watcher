# Python 2.7
import csv

from JobDetailClass import JobDetail
# from FlightInfoClass import FlightInfo


#
# MAIN:
#
# Search for flight prices for all future jobs
# Save new flight prices
def main():
    # Get Job details
    jobs = JobDetail.getJobDetailsArray()

    # ask user which job to graph
    selection = 0
    while(selection < 1 or selection > len(jobs)):
        print("Select Flight Description")
        for i in range(len(jobs)):
            print("\t" + str(i+1) + " - " + jobs[i].getDetailsLine())
        selection = input("Selection: " )
        try:
            selection = int(selection)
        except:
            selection = 0
    selection -= 1      #adjust indexing

    # Get array of Trace Data for Job selction
    jobs[selection].graphTraces()
if __name__ == "__main__":
    main()




# dataFile = "flight_log.csv"
# try:
#     f = open(dataFile, 'r')        # read
# except IOError:
#     print("Could not read file:", fname)
#     sys.exit(1)
#
# with f:
#     reader = csv.reader(f, delimiter=',')
#
#     for row in reader:
#         print(row[4].strip())
#         if row[4] == "1095":
#             print("1095")
#
#         pass #do stuff here


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
