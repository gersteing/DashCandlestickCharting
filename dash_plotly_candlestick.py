import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go
from datetime import datetime, date, time, timedelta, timezone
import numpy as np
import pytz


external_stylesheets = ['css/charts.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


##converts a datetime object to a unix timestamp on milliseconds. The reason is the
##dash graph objects expect a millisecond time value if the xaxis is a date range. 
def to_unix_milliseconds(dt):
    global utcTimeZone
    epoch =  datetime.fromtimestamp(0, tz=utcTimeZone)
    unixTimeStamp = (dt - epoch).total_seconds()
    return unixTimeStamp * 1000


##returns an aware date time object that uses localTimeZone for the timezone informatino (tzinfo)
def utc_milleseconds_to_date(milliseconds):
    global localTimeZone
    seconds = milliseconds/1000
    ##datetime.fromtimestamp seems to return a time stamp that was four hours off the time stamp of my actual data.
    ##I think the function returns a naive object but I am not clear what time zone is assumed. I thought it was utc
    ##but I am in US/Eastern time where the offset should be -5 hours for east coast time, not -4 hours.
    ##Long story short,to make the timetamps works wiht the graph, every time I convert a timestamp from the slider
    ##to a date, I needed to convert it to the timezone of the actual bar data. In my case, that was east coast time. 
    ##Otherwise the date range we assign to the chart will not match the actual datetime of our bar data and our y range
    ##values do not get calculated correctly.
    parsedDateTime = datetime.fromtimestamp(seconds)
    ##convert this object back to our local time zone because my data time stamps were in east coast time.
    ##Adjust localTimeZone if you are not on east coast time.
    d_aware =  parsedDateTime.astimezone(localTimeZone)
    return d_aware

##finds the maximum price or minimum price of the bars in a date range
##by default max is set to true meaning find the max price. If this is false
##the function returns the mininum price.
def findPriceExtreme(startTime, endTime):
##    print('findPriceExtreme function called with arguments ' + str(startTime) + ' and ' + str(endTime) )
    minRowIndex = getRowIndexOfTime(startTime)
    maxRowIndex = getRowIndexOfTime(endTime)
##    print('minRowIndex : ' + str(minRowIndex))
##    print('maxRowIndex : ' + str(maxRowIndex))
##    print('found data minRow: ' + str(df.iloc[minRowIndex]))
##    print('found data maxRow: ' + str(df.iloc[maxRowIndex]))
    sl = slice(minRowIndex,maxRowIndex + 1)
##    print('slice object ' + str(sl))
    viewBarData = df.iloc[sl]
##    print(viewBarData.head())
##    print(viewBarData.tail())
## example df.agg({'A' : ['sum', 'min'], 'B' : ['min', 'max']})
    maxBarHigh = max(viewBarData['high'])
   
    minBarLow = min(viewBarData['low'])
##    print('maxBarHigh : ' + str(maxBarHigh))
##    print('maxBarLow : ' + str(minBarLow))
    return [minBarLow,maxBarHigh]
    
##gets the index of the bar in the data frame at the given time
def getRowIndexOfTime(currentDateTime):
##    print('getRowIndexOfTime function called with arguments ' + str(currentDateTime) )
    global df
    global dateformat
    roundedDateTime = roundToFiveMinutes(currentDateTime)
##    print('object type returned from roundToFiveMinutes function ' + str(type(roundedDateTime)))
    indexTimeString = roundedDateTime.strftime(dateformat)
##    print('index string for time value ' + indexTimeString)
    rowIndex = np.where(df['time']==indexTimeString)[0]

    ##rowIndex = np.where(df['time']==indexTimeString)[0]
##    print('row index of date in csv file: ' + str(rowIndex[0]))
    return rowIndex[0]
    
##rounds up a dateTime to five minute increments. Our bar data is based on five minute bars, but this could be adjusted
## to any bar period
def roundToFiveMinutes(tm):
    ##set bar period to which we will round our time data like a five minute bar period for example
    barPeriod = 5
    ##zero out any seconds or milliseconds on the datetime
    roundedDateTime = tm.replace(second = 0, microsecond = 0)
    ##get the minute  value of the date time object and if it is greater than 5 set it to 5, less than 5 set to 0
    minuteValue = roundedDateTime.minute
    differenceMinutes = minuteValue%barPeriod
    minuteValue = minuteValue - differenceMinutes
    roundedDateTime = roundedDateTime.replace(minute = minuteValue)
    return roundedDateTime

##round values to be within our boundary extremes for the x axis. The x range slider controls did not return consistent
##time code values and would sometimes be out of bounds of the date ranges of the actual data in the chart. We use this
##method to make sure the values we get from the x axis range slider never exceed the actual time range of available data. 
def keepInXAxisBounds(value):
    global minTimeStamp
    global maxTimeStamp
    adjustedValue = 0
    if(value > maxTimeStamp):
        adjustedValue = maxTimeStamp
    elif(value < minTimeStamp):
        adjustedValue = minTimeStamp
    else:
        adjustedValue = value
    return adjustedValue

utcTimeZone = timezone.utc
localTimeZone = pytz.timezone('US/Eastern')
dateformat = '%Y-%m-%d %H:%M:%S'
##read test bar data from csv file
df = pd.read_csv("20180923TradingTestDataExportCSV.csv")
df = df[:500]
##print('data types in frame: ' + str(df.dtypes))
##print(df.head())
##print(df.tail())

df2= df.loc[:,['time','high']]
##print('df2 head')
##print(df2.head())


##get the min and max time stamp string from the data frame
dateMin = min(df['time'])
dateMax = max(df['time'])
##convert to a normal python datetime object
dateMin = datetime.strptime(dateMin,dateformat)
dateMax = datetime.strptime(dateMax,dateformat)

##make datetime object timezone aware
dateMin = dateMin.replace(tzinfo=utcTimeZone)
dateMax = dateMax.replace(tzinfo=utcTimeZone)
##get dates as time stamps to set x slider min and max values
minTimeStamp = to_unix_milliseconds(dateMin)
maxTimeStamp = to_unix_milliseconds(dateMax)
sliderStep = timedelta(minutes=5).total_seconds() * 1000
tickPadding = .0002

##Get the price extremes for the bar data in the graph.
##In this case it is the first and last bar of our data. Use to set he yaxis starting values

startinPriceExtreme = findPriceExtreme(dateMin,dateMax)
newRangeLow = round(startinPriceExtreme[0], 4) - tickPadding
newRangeHigh = round(startinPriceExtreme[1], 4) + tickPadding

##print('starting min date ' +str(dateMin))
##print('starting max date ' +str(dateMax))
##print('min timestamp for x slider ' +str(minTimeStamp))
##print('max timestamp for x slider ' +str(maxTimeStamp))



firstTrace = go.Candlestick(
    x=df.time,
    open=df.open,
    high=df.high,
    low=df.low,
    close=df.close)
## This is an example of a second trace which we might use for example for swing data
secondTrace = go.Scatter(
    x=df2.time,
    y=df.high,
    line=dict(
        color='black',
        width=1,
        shape='linear'
        )
   )
data = [firstTrace, secondTrace]

layout = go.Layout(
    xaxis=dict(
        autorange=False,
        rangeslider=dict(
            visible = False
        ),
        type='date',
        range=[to_unix_milliseconds(dateMin),to_unix_milliseconds(dateMax)]
    ),
    yaxis=dict(
        title='Ticks',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='lightgrey'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        exponentformat='e',
        showexponent='all',
        tickmode='linear',
        tick0=0.500,
        dtick=.0001,
        autorange=False,
        range=[newRangeLow,newRangeHigh]
        
    ),
    height = 800
)
figure = go.Figure(data=data,layout=layout)

graph =dcc.Graph(
    id='graph-with-slider',
    figure = figure
)
    
app.layout = html.Div([
    graph,
    html.Label('X Range Slider'),
    dcc.RangeSlider(
        id='x-range-slider',
        min=minTimeStamp,
        max=maxTimeStamp,
        step=sliderStep,
        value=[minTimeStamp, maxTimeStamp],
        allowCross=False,
        updatemode='mouseup'
    )
])



##get this callback working. See https://dash.plot.ly/getting-started-part-2
@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('x-range-slider', 'value')
     ])
def adjust_ranges(xSliderValue):
    global data
    global layout
    global tickPadding
   
##first calculate any change to the graph range based on x slider
##    print('get range of xaxis' + str(layout['xaxis']['range']))
##    print('values returned by x slider ' + str(xSliderValue))
##if the values returned by the slider exceed our allowed range adjust them.
##  Range slider can't be trusted. Values returned were not consistent.
    xMinAdjusted = keepInXAxisBounds(xSliderValue[0])
    xMaxAdjusted = keepInXAxisBounds(xSliderValue[1])
##    print('x slider values corrected for out of bounds values [' + str(xMinAdjusted) + ','+ str(xMaxAdjusted) + ']') 
    xminDate = utc_milleseconds_to_date(xMinAdjusted)
    xmaxDate = utc_milleseconds_to_date(xMaxAdjusted)
##    print('x min date object ' + str(xminDate))
##    print('x max date object ' + str(xmaxDate))
    xminUTCValue = to_unix_milliseconds(xminDate)
    xmaxUTCValue = to_unix_milliseconds(xmaxDate)
##    print('setting xmin and ymin millesecond values on x range to : [' + str(xminUTCValue) + ',' + str(xmaxUTCValue) + ']')
    
##next calculate any change to the graph range based on y slider
##    print('get range of yaxis' + str(layout['yaxis']['range']))
##find bars in date range
    newYRange = findPriceExtreme(xminDate,xmaxDate)
    newRangeLow = round(newYRange[0], 4) - tickPadding
    newRangeHigh = round(newYRange[1], 4) + tickPadding
##    print('new range low and high for y axis ' + str(newRangeLow) + ',' + str(newRangeHigh))
    layout['xaxis']['range']=[xminUTCValue,xmaxUTCValue]
    layout['yaxis']['range']=[newRangeLow,newRangeHigh]
    
    return{
        'data': data,
        'layout':layout
    }






if __name__ == '__main__':
    app.run_server()
