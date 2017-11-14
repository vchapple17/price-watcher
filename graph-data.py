import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/vchapple17/price-watcher/master/flight_log.csv?token=AKQQJum8IJF17oNxPlZTvDPGjwYAGqduks5aDoSTwA%3D%3D")

data = [go.Scatter(
          x=df.Date,
          y=df['AAPL.Close'])]

# Create traces
#https://plot.ly/python/line-and-scatter/

# 1 graph for each job?
# multiple traces (number of flights that day for each graph.
#
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
