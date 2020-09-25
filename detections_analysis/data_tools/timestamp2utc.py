from datetime import datetime
import time

def conver2utc(timestamp,types="d"):
    """
    function convert timestamp to utc
    :param timestamp: datatime in timestamp(10 char)
    :return: data_time string or dict information about day)
    struc of data_time i.e:
    if "d" ->dict:
    time.struct_time(tm_year=2020, tm_mon=8, tm_mday=31, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=244, tm_isdst=-1)
    if "s" -> string:
    %Y-%m-%d %H:%M:%S
    """
    data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    tm_data = time.strptime(str(data_str), '%Y-%m-%d %H:%M:%S')
    if types == "d":
        data_time = tm_data
    else:
        data_time = data_str
    return data_time