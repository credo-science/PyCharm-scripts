import json
from os import path,listdir
from os.path import isfile, join

from data_tools.timestamp2utc import conver2utc

home = path.dirname(path.abspath(__file__)) + '/'
ping_path = "/media/slawekstu/CREDO1/Api/credo-data-export/pings/"

def time_work_all():
    onlyfiles = [f for f in listdir(ping_path) if isfile(join(ping_path, f))]
    time_work = 0
    for name in onlyfiles:
        with open(ping_path+name) as f:
            json_load = json.load(f)

        for record in json_load["pings"]:
            time_work += record["on_time"]
    time_work = time_work/(60*60*1000)#time in hour
    print (time_work)
def read_ping():
    """
    Having dictionaries we can calculate the working time of each device
    We are looking for working time for set dates
    :return: Dict_users_devices
    """
    ping_path = home+"ping_examples.json"
    Dict_devices = {}
    with open(ping_path) as f:
        json_load = json.load(f)

    for record in json_load["pings"]:
        device = record["device_id"]
        id = record["id"]
        on_time = record["on_time"]
        time_received = record["time_received"]
        timestamp = record["timestamp"]
        delta_time = record["delta_time"]

        if device not in Dict_devices:
            Dict_devices[device]={}
            Dict_devices[device]["ping"] = {}
            Dict_devices[device]["time_work"] = 0

        Dict_devices[device]["ping"][id] = {}

        Dict_devices[device]["time_work"]+=on_time
        Dict_devices[device]["ping"][id]["timestamp"] = timestamp
        Dict_devices[device]["ping"][id]["on_time"] = on_time
        Dict_devices[device]["ping"][id]["time_recived"] = time_received
        Dict_devices[device]["ping"][id]["delta_time"] = delta_time

    return Dict_devices

def print_time_work(dict_pings):
    for device in dict_pings:
        time_work = dict_pings[device]["time_work"]/ 60000
        if time_work >1:
            print("%d,\t%.2f "%(device,time_work))  # time in minutes

def check_connection(dict_pings):
    for device in dict_pings:
        for ping_id in dict_pings[device]["ping"]:
            record = dict_pings[device]["ping"][ping_id]
            timestamp =record ["timestamp"]/ 1000
            time_recived = record["time_recived"] / 1000
            time_send2base = conver2utc(timestamp,"s")#[year,mont,day,hour,minute,second,day of year
            time_recived2base = conver2utc(time_recived,"s")
            on_time = record["on_time"] / 1000
            teoretic_time = conver2utc(timestamp - on_time,"s")
            print("%d,\t%s,\t%s,\t%d,\t%d,\t%s "%(device, time_send2base,time_recived2base,time_recived-timestamp,on_time,teoretic_time))

def main():
    dict_pings = read_ping()
    print_time_work(dict_pings)
    #check_connection(dict_pings)
    #time_work_all()

if __name__ == "__main__":
    main()