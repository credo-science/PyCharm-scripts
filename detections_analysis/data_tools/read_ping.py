import json
from os import listdir,path,makedirs
from os.path import isfile, join
import time
from datetime import datetime

home_detections = "/media/slawekstu/CREDO1/Api/credo-data-export/"

def read_ping(start:int,stop:int):
    """
    Having dictionaries we can calculate the working time of each device
    We are looking for working time for set dates
    :return: Dict_users_devices
    """
    ping_path = home_detections+"pings/"
    onlyfiles = [f for f in listdir(ping_path) if isfile(join(ping_path, f))]
    Dict_users_devices = {}
    for name in onlyfiles:
        with open(ping_path+name) as f:
            json_load = json.load(f)

        for record in json_load["pings"]:
            user = record["user_id"]
            device = record["device_id"]
            if device not in Dict_users_devices:
                Dict_users_devices[device]={}
                Dict_users_devices[device]["ping"] = 0
            time_work = record["on_time"]/60000#time in minutes
            timestamp = int(record["timestamp"] / 1000)  # time in secunds
            time_received = int(record["time_received"] / 1000)
            if timestamp >= start and timestamp < stop:
                Dict_users_devices[device]["ping"]+=time_work
    return Dict_users_devices

def read_ping_days(start = 1528848000000,stop = 0):
    """
    Having dictionaries we can calculate the working time of each device
    We are looking for working time for set dates, time_work in evry day
    :return: Dict_users_devices
    """
    if stop == 0:
        ts = datetime.now()
    ping_path = home_detections+"pings/"
    onlyfiles = [f for f in listdir(ping_path) if isfile(join(ping_path, f))]
    Dict_users_devices = {}
    for name in onlyfiles:
        with open(ping_path+name) as f:
            json_load = json.load(f)

        for record in json_load["pings"]:
            user = record["user_id"]
            device = record["device_id"]
            if device not in Dict_users_devices:
                Dict_users_devices[device]={}
                Dict_users_devices[device]["ping"] = 0
            time_work = record["on_time"]
            timestamp = int(record["timestamp"] / 1000)  # time in secunds
            time_received = int(record["time_received"] / 1000)
            data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            tm_data = time.strptime(str(data_str), "%Y-%m-%d")
            id_years = tm_data.tm_year
            id_days = tm_data.tm_yday
            if id_years not in Dict_users_devices[device]:
                Dict_users_devices[device][id_years] = {}
            if id_days not in Dict_users_devices[device][id_years]:
                Dict_users_devices[device][id_years][id_days] = 0
            if timestamp >= start and timestamp < stop:
                Dict_users_devices[device]["ping"]+=time_work



            Dict_users_devices[device][id_years][id_days] +=time_work
    return Dict_users_devices


def return_timestamps(start:int,stop:int):
    """
    Having dictionaries we can calculate the working time of each device
    We are looking for working time for set dates
    :return: Dict_users_devices
    """
    ping_path = home_detections+"pings/"
    onlyfiles = [f for f in listdir(ping_path) if isfile(join(ping_path, f))]
    Dict_users_devices = {}
    for name in onlyfiles:
        with open(ping_path+name) as f:
            json_load = json.load(f)

        for record in json_load["pings"]:
            user = record["user_id"]
            device = record["device_id"]
            Dict_temp = {}
            if device not in Dict_users_devices:
                Dict_users_devices[device]={}
                Dict_users_devices[device]["record"] = []
            time_work = record["on_time"]/60000#time in minutes
            timestamp = int(record["timestamp"]/1000)#time in secunds
            time_received = int (record["time_received"]/1000)
            Dict_temp["on_time"]=time_work
            Dict_temp["timestamp"]=timestamp
            Dict_temp["time_received"] = time_received
            if timestamp >= start and timestamp < stop:
                Dict_users_devices[device]["record"].append(Dict_temp)
    return Dict_users_devices


def days_work(Dict_device,start = 1528848000000,stop = 0):
    """
    Having dictionaries we can calculate the working time of each device
    We are looking for working time for set dates, time_work in evry day
    :return: Dict_users_devices
    """
    if stop == 0:
        ts = datetime.now()
    ping_path = home_detections+"pings/"
    onlyfiles = [f for f in listdir(ping_path) if isfile(join(ping_path, f))]
    Dict = {"time_work":{},"devices":{}}

    for name in onlyfiles:
        with open(ping_path+name) as f:
            json_load = json.load(f)

        for record in json_load["pings"]:
            time_work = record["on_time"]
            if int(record["timestamp"])>1529193600000:#>2018-06-17 ->start good work our app
                timestamp = int(record["timestamp"] / 1000)  # time in secunds
                devices = str(record["device_id"])
                #if timestamp <1546300800:#01.01.2019
                data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                tm_data = time.strptime(str(data_str), "%Y-%m-%d")
                id_years = int(tm_data.tm_year)
                id_days = int(tm_data.tm_yday)
                if id_years <2021:
                    try:
                        if devices in Dict_device[id_years][id_days]:
                            print(Dict_device[id_years][id_days])
                            print(devices)
                            if id_years not in Dict["time_work"]:
                                Dict["time_work"][id_years] = {}
                                Dict["devices"][id_years] = {}
                            if id_days not in Dict["time_work"][id_years]:
                                Dict["time_work"][id_years][id_days] = 0
                                Dict["devices"][id_years][id_days] = []
                            Dict["time_work"][id_years][id_days] +=time_work
                            if devices not in Dict["devices"][id_years][id_days]:
                                Dict["devices"][id_years][id_days].append(devices)
                    except:
                        continue
    return Dict