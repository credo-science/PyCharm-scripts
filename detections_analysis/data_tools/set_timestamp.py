import datetime
import time

def convert_to_timestamp(year=2018,month=1,day=1,hour=0,minuts=0,precision="s"):
    timestamp = (datetime.datetime(year,month,day, hour, minuts).strftime("%s"))
    if precision == "ms":
        timestamp +="000"
    return int(timestamp)

def string_to_timestamp(data, format):
    timestamp = time.mktime(datetime.datetime.strptime(data,format).timetuple())
    return timestamp