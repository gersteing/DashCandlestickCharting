import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go
from datetime import datetime, date, time, timedelta, timezone
import numpy as np
import pytz

##load our local style sheet
external_stylesheets = ['css/charts.css']
## create our Flask Server application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##converts a datetime object to a unix timestamp on microseconds. The reason is the
##dash graph objects expect a microsecond time value if the xaxis is a date range. 
##dt argument must be a datetime object that is timezone aware with tz set to utc timezone
def to_unix_microseconds(dt):
    global utcTimeZone
    epoch =  datetime.fromtimestamp(0, tz=utcTimeZone)
    unixTimeStamp = (dt - epoch).total_seconds()
    return unixTimeStamp * 1000


##returns an aware date time object that uses utc for the timezone (tzinfo)
## millesconds arg must be from a datetime object that was utc timezone aware when converted to microseconds
def utc_milleseconds_to_date(microseconds):
    global utcTimeZone
    ##convert microseconds to seconds 
    seconds = microseconds/1000
    ##create datetime object from seconds value
    parsedDateTime = datetime.fromtimestamp(seconds)
    ##localize this object back to utc timezone. 
    d_aware =  parsedDateTime.astimezone(utcTimeZone)
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
    
##gets the ordinal index (zero based index) of the bar in the data frame at the given time
def getRowIndexOfTime(currentDateTime):
##    print('getRowIndexOfTime function called with arguments ' + str(currentDateTime) )
    ##make our data and dateformat object available in scope of function
    global df
    global dateformat
    ## round our date to a five minute increment using rounding function since our bar time period is 5 minutes.
    roundedDateTime = roundToFiveMinutes(currentDateTime)
##    print('object type returned from roundToFiveMinutes function ' + str(type(roundedDateTime)))
    ##format our date as a MySQL date string. This will be used to locate the bar date in the pandas data frame
    indexTimeString = roundedDateTime.strftime(dateformat)
##    print('index string for time value ' + indexTimeString)
    ##get the ordinal row of the bar with that MySQL time stamp by using numpy array where function on the time column.
    rowIndex = np.where(df['time']==indexTimeString)[0]
##    print('row index of date in csv file: ' + str(rowIndex[0]))
    ## the numpy where function returns list of indexes if it finds more than one row that matches the search so we only return the first
    ## item in the list which is an integer that is the row number in our data for the bar with the correct MySQL date.
    ## Note that this is not very robust. There is no error handling here if a row is NOT found in the data with that database.
    ## In my experience there are periodically times when the x slider is adjusted and I get an error, but if I adjust the slider again,
    ## it usually runs the script and works fine. I more robust solution would be to have a function that makes sure we locate a valid
    ## record in the dataframe every time. If your data is very sparse this could be a problem. 
    return rowIndex[0]
    
##rounds up a dateTime to five minute increments. Our bar data is based on five minute bars, but this could be adjusted
## to any bar period
def roundToFiveMinutes(tm):
    ##set bar period to which we will round our time data like a five minute bar period for example
    barPeriod = 5
    ##zero out any seconds or microseconds on the datetime
    roundedDateTime = tm.replace(second = 0, microsecond = 0)
    ##get the minute  value of the date time object and if it is greater than 5 set it to 5, less than 5 set to 0
    minuteValue = roundedDateTime.minute
    ##get the remainder of datetime minute value divided by the bar period (5 minutes in our case)
    differenceMinutes = minuteValue%barPeriod
    ##subract the remainder from the datetime minute value
    minuteValue = minuteValue - differenceMinutes
    ##reset the minute value on the date time object so it is now a five minute increment
    roundedDateTime = roundedDateTime.replace(minute = minuteValue)
    return roundedDateTime

##round values to be within our boundary extremes for the x axis. The x range slider controls did not return consistent
##time code values and would sometimes be out of bounds of the date ranges of the actual data in the chart. We use this
##method to make sure the values we get from the x axis range slider never exceed the actual time range of available data. 
def keepInXAxisBounds(value):
    global minTimeStamp
    global maxTimeStamp
    adjustedValue = 0
    ##basically this says if the bar slider returns a value outside of our established minimum and maximum range, round it up or down
    ## so it stays between the min and max values. I found the x slider would return values greater than the min and max range values
    ## we set on occasion so I don't truxt the Dash x range slider to return valid values at its extremes that always fall within our assigned
    ## min and max range. 
    if(value > maxTimeStamp):
        adjustedValue = maxTimeStamp
    elif(value < minTimeStamp):
        adjustedValue = minTimeStamp
    else:
        adjustedValue = value
    return adjustedValue

##returns a set of annotations to be used on the chart to label bar numbers.
def getChartBarNumbers():
    global df
    chartBarNumbers = []
    for index, row in df.iterrows():
        
        xValue = row['time']
        yValue = row['low'] - .0001
        annotation = dict(
            x=xValue, y=yValue, xref='x', yref= 'y',
            showarrow=False, xanchor='center',
            text=index, font=dict(
                family='Arial',
                size=10,
                color='#000000'
            )
        )
        chartBarNumbers.append(annotation)
    return chartBarNumbers


## create a utc timezone object that we will assign to all datetime objects and use for all datetime to microsecond conversion and vice versa
utcTimeZone = timezone.utc
##I don't know why by on the plotly chart the range is
##always four hours off if the actual time stamps fed into the chart.
##The chartShift variable is used to make an adjustment to the time range each time
##the x range values are assigned to the chart to correct this. It does not seem to be a problem with the
##datetime objects or their conversion. It seems to be an issue were when you assign the x range values, the chart is four hours off.
##I don't know if plotly is somehow using a local time zone according to my computer system time, but it is odd that it is four hours off
##because I am on east coast time with a utc offset of -04:56 for my time zone compared to utc.
##This is four hours of seconds converted to microseconds (1 second/1000)
chartShift = 14400 * 1000
dateformat = '%Y-%m-%d %H:%M:%S'
##read test bar data from csv file
rowLimit = 500
df = pd.read_csv("20180923TradingTestDataExportCSV.csv")
df = df[:rowLimit]

##print('data types in frame: ' + str(df.dtypes))
##print(df.head())
##print(df.tail())

##df2= df.loc[:,['time','high']]
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
##get dates as time stamps to set x slider min and max values in microseconds 
minTimeStamp = to_unix_microseconds(dateMin)
maxTimeStamp = to_unix_microseconds(dateMax)
##set the xmin and xmax range for the chart which seems to be four hours off the actual time assigned so this uses the chartShift adjustment
##The chart accepts microsecond values. 
minTimeStampChart = minTimeStamp +  chartShift
maxTimeStampChart = maxTimeStamp + chartShift
sliderStep = timedelta(minutes=5).total_seconds() * 1000
tickPadding = .0002

##Get the price extremes for the bar data in the graph.
##In this case it is the first and last bar of our data. Use to set he yaxis starting values
startinPriceExtreme = findPriceExtreme(dateMin,dateMax)
##add a two tick (tick being .0001) to the chart y range values so bars are not all the way on the edge of the chart. 
newRangeLow = round(startinPriceExtreme[0], 4) - tickPadding
newRangeHigh = round(startinPriceExtreme[1], 4) + tickPadding

##print('starting min date ' +str(dateMin))
##print('starting max date ' +str(dateMax))
##print('min timestamp for x slider ' +str(minTimeStamp))
##print('max timestamp for x slider ' +str(maxTimeStamp))

##create our first candlestick trace (data series) to be plotted on our chart. Doing it this way using plotly functions gives us reference
## if we need it later. 
firstTrace = go.Candlestick(
    x=df.time,
    open=df.open,
    high=df.high,
    low=df.low,
    close=df.close)
## This is an example of a second trace which we might use for example for swing data
##secondTrace = go.Scatter(
##    x=df2.time,
##    y=df.high,
##    line=dict(
##        color='black',
##        width=1,
##        shape='linear'
##        )
##   )
##data = [firstTrace, secondTrace]

##create our list of data traces to be plotted on the chart. We will pass this to the plotly figure
data = [firstTrace]



## create our layout and assign to a variable so we can updat the layout later.
##NOTES ON PARAMATERS:
##layout variable is created so we can access the x and y range values of our graph later in our dash callback functions.
##xaxis:range - set the min and max values on the x range of the chart to our minimum and maximum dates of the available data plus our offset of
##four hours which for some reason the graph always seems off by four hours. This was calculated above
##and assigned to the minTimeStampChart and maxTimeStampChart variables.
##yaxis:range - Also assign our min and max y range which is based on the max(high) and min(low) of all the bars in our available data to start with.
##the y min and max were calculated and stored in the newRangeLow and newRangeHigh variables already.
##autorange - make sure the ranges don't automatically scale since we are setting
##height - customize the height of our graph here. Dash defaults are too small to display bar data well.
##dtick - set the graph to show every price tick which in the bar data we are using is $.0001
layout = go.Layout(
    xaxis=dict(
        autorange=False,
        rangeslider=dict(
            visible = False
        ),
        type='date',
        range=[minTimeStampChart,maxTimeStampChart] 
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
    annotations = getChartBarNumbers(),
    height = 800
    
)
##create our figure with our data and our layout
figure = go.Figure(data=data,layout=layout)

##create our Dash Graph using our figure. This is the Dash component that allows display of plotly figures as html output.
graph =dcc.Graph(
    id='graph-with-slider',
    figure = figure
)

##assign this graph to our Flask application inside a div tag. Add the x slideer also using the dcc range slider component
##set the min and max values on the slider to our minimum and maximum dates of the available data. This was calculated above
##and assigned to the minTimeStamp and maxTimeStamp variables.
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
##Make our data, layout, and our y range padding values available in the scope of this function. 
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
    xminChartValue = to_unix_microseconds(xminDate) + chartShift
    xmaxChartValue = to_unix_microseconds(xmaxDate) + chartShift
##    print('setting xmin and xmax millesecond values on x range to : [' + str(xminChartValue) + ',' + str(xmaxChartValue) + ']')
    
##next calculate any change to the graph range based on y slider
##    print('get range of yaxis' + str(layout['yaxis']['range']))
##find bars in date range
    newYRange = findPriceExtreme(xminDate,xmaxDate)
    newRangeLow = round(newYRange[0], 4) - tickPadding
    newRangeHigh = round(newYRange[1], 4) + tickPadding
##    print('new range low and high for y axis ' + str(newRangeLow) + ',' + str(newRangeHigh))
    layout['xaxis']['range']=[xminChartValue,xmaxChartValue]
    layout['yaxis']['range']=[newRangeLow,newRangeHigh]

    ##now that we have updated our layout, assign it to our figure by returning thes values which reset the data and layout properties of the figure.
    ##Note that this is why we made sure to create a reference to our layout. Another strategy could be to update your data and replot it, but here
    ##we just update the layout, and pass back in the same data to the figure. 
    return{
        'data': data,
        'layout':layout
    }





##start the Flask Server to run the app on start up. 
if __name__ == '__main__':
    app.run_server()
