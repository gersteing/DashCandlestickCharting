## date conversion tests
import pytz
from datetime import datetime, date, time, timedelta, timezone

##Test code to ensure our date to microsecond conversion functions are working. 

##converts a datetime object to a unix timestamp on microseconds. The reason is the
##dash graph objects expect a microsecond time value if the xaxis is a date range. 
def to_unix_microseconds(dt):
    global utcTimeZone
    epoch =  datetime.fromtimestamp(0, tz=utcTimeZone)
    unixTimeStamp = (dt - epoch).total_seconds()
    return unixTimeStamp * 1000


##returns an aware date time object that uses localTimeZone for the timezone informatino (tzinfo)
def utc_milleseconds_to_date(microseconds):
    global utcTimeZone
    seconds = microseconds/1000
    ##datetime.fromtimestamp seems to return a time stamp that was four hours off the time stamp of my actual data.
    ##I think the function returns a naive date time object but I am not clear what time zone is assumed. I thought it was utc
    ##but I am in US/Eastern time where the offset should be -5 hours for east coast time, not -4 hours.
    ##Long story short,to make the timetamps works with the graph, every time I convert a timestamp from the slider
    ##to a datetime object, I needed to localize the time (adjust the datetime object) it to the timezone used when for actual bar data
    ##which in my case was US/Eastern time.  
    ##Otherwise the date range we assign to the chart will not match the actual datetime of our bar data and our y range
    ##values do not get calculated correctly.
    parsedDateTime = datetime.fromtimestamp(seconds)
    ##localize this object back to time zone of the source bar data. My data time stamps were in east coast time.
    ##Adjust the localTimeZone variable to what ever your data time zone is if you are not on east coast time.
    d_aware =  parsedDateTime.astimezone(utcTimeZone)
    return d_aware

utcTimeZone = timezone.utc
localTimeZone = pytz.timezone('US/Eastern')
dateformat = '%Y-%m-%d %H:%M:%S'

testDate = '2012-07-08 18:05:00'
dateNaive = dateMin = datetime.strptime(testDate,dateformat)
dateLocalAware = dateNaive.replace(tzinfo=localTimeZone)
microsecondLocalAware = to_unix_microseconds(dateLocalAware)

print('dateNaive ' + str(dateNaive))
print('dateLocalAware ' + str(dateLocalAware))
print('microsecondLocalAware ' + str(microsecondLocalAware))
print('convert local microseconds back to date using utc_milleseconds_to_date function')
returnedDate = utc_milleseconds_to_date(microsecondLocalAware)
print('returned date ' + str(returnedDate))


dateUTCAware = dateNaive.replace(tzinfo=utcTimeZone)
microsecondUTCAware = to_unix_microseconds(dateUTCAware)
print('dateUTCAware ' + str(dateUTCAware))
print('microsecondUTCAware ' + str(microsecondUTCAware))
print('convert utc microseconds back to date using utc_milleseconds_to_date function')
returnedDate = utc_milleseconds_to_date(microsecondUTCAware)
print('returned date ' + str(returnedDate))
