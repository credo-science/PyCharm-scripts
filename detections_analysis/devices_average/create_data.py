"""
PURPOSE OF THE SCRIPT:
graph where the point on the histogram is the
average detection in the last 100 days, also depends on the time
spent in the given days
graph for all device
+ % detection with type "line"

LAST EDITION OF THE SCRIPT: 12.07.2020
"""

import pickle #zapis słownika
import datetime
import json
# Library
import os
import time
from data_tools.read_ping import days_work

string = "Detections_analysis/devices_average/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
start_path=back_to_main_path+"data_save/detections_analysis/"
path_files_astrophy  =  start_path+"anti-artefact/LA/summary_after_filtr/"
moun_part = path_files_astrophy+"good/json/"
path_save   =   start_path+"devices_average/clasyfication/sums/"

Dict_moun = {}
Dict_moun_all = {}
Dict_device = {}
rodzaje = {}
rodzaje["wszystkich"] = 0
rodzaje["kresek"] = 0
rodzaje["kropek"] = 0
rodzaje["zawijasow"] = 0
def load_file_to_dict(file_path,year,month,days,device):
    """
    Wczytanie danych detekcji z pliku do słownika.
    :param file_path:
    :param year: rok detekcji w pliku
    :param month: meisiac detekcji w pliku
    :param days: dzien detekcji w pliku
    :param device: detekcje urządzenia o ID
    :return: aktualizacja słownika (globalnego)
    """

    if device not in Dict_moun:
        Dict_moun[device] = {}
    if year not in Dict_moun[device]:
        Dict_moun[device][year] = {}
    if year not in Dict_moun_all:
        Dict_moun_all[year] = {}
        Dict_device[year] = {}

    today = datetime.date(int(year), int(month), int(days))
    todays = str(today)
    id_day = int(time.strptime(todays, "%Y-%m-%d").tm_yday)

    if id_day not in Dict_moun_all[year]:
        Dict_device[year][id_day] = []
        Dict_moun_all[year][id_day] = {}
        Dict_moun_all[year][id_day]["dot"] = 0
        Dict_moun_all[year][id_day]["line"] = 0
        Dict_moun_all[year][id_day]["worms"] = 0
        Dict_moun_all[year][id_day]["all"] = 0
        Dict_moun_all[year][id_day]["devices"] = []
        Dict_moun_all[year][id_day]["pings"] = {}
        Dict_moun_all[year][id_day]["pings"]["time_work"] = 0
        Dict_moun_all[year][id_day]["pings"]["devices"] = 0
        Dict_moun_all[year][id_day]["todays"] = today

    if device not in Dict_moun_all[year][id_day]["devices"]:
        Dict_moun_all[year][id_day]["devices"].append(device)
        Dict_device[year][id_day].append(device)

    if id_day not in Dict_moun[device][year]:
        Dict_moun[device][year][id_day] = {}
        Dict_moun[device][year][id_day]["dot"] = 0
        Dict_moun[device][year][id_day]["line"] = 0
        Dict_moun[device][year][id_day]["worms"] = 0
        Dict_moun[device][year][id_day]["all"] = 0
        Dict_moun[device][year][id_day]["time"] = 0
        Dict_moun[device][year][id_day]["todays"] = today

    with open(file_path) as json_file:
        json_load = json.load(json_file)

    for detection in json_load['detections']:
        solidity = detection["solidity"]
        ellipticity = detection["ellipticity"]

        Dict_moun[device][year][id_day]["all"] += 1
        Dict_moun_all[year][id_day]["all"] +=1
        rodzaje["wszystkich"] +=1

        if float(solidity) <= 0.7 and float(ellipticity) > 0.6:
            Dict_moun[device][year][id_day]["line"] += 1 #moun
            Dict_moun_all[year][id_day]["line"] +=1
            rodzaje["kresek"] +=1

        elif float(solidity) == 1.0 or float(ellipticity) <= 0.2:
            Dict_moun[device][year][id_day]["dot"] += 1
            Dict_moun_all[year][id_day]["dot"] += 1
            rodzaje["kropek"] += 1
        elif float(ellipticity) > 0.2 and float(ellipticity) <= 0.6:
            Dict_moun[device][year][id_day]["worms"] += 1
            Dict_moun_all[year][id_day]["worms"] += 1
            rodzaje["zawijasow"] +=1


def starter():
    list_year ={2018,2019,2020}#{2018,2019,2020}
    list_file = os.listdir(path_files_astrophy)
    for year in list_year:
        path = moun_part+str(year)+"/"
        list_file = os.listdir(path)
        for month in list_file:
           # if str(month)=="10":
                path_month = path +month+"/"
                list_file_month = os.listdir(path_month)
                for days in list_file_month:
                    path_days = path_month+days+"/"
                    list_file_days = os.listdir(path_days)
                    print(year,month,days)
                    for device in list_file_days:
                        file_path = path_days+device+"/"
                        list_file_json = os.listdir(file_path)
                        for json_name in list_file_json:
                            json_path = file_path+json_name
                            load_file_to_dict(json_path,year,month,days,device)

def save_to_file(detections, path_save, file_name):
    os.makedirs(path_save, exist_ok=True)
    print(path_save + file_name)
    outfile = open(path_save + file_name, 'wb')
    pickle.dump(detections, outfile)
    outfile.close()

def time_work(pingi):
    years = [2018,2019,2020]
    for year in years:
          for id_day in range(1, 366):
              if id_day in pingi["time_work"][year] and id_day in Dict_moun_all[year]:
                  print(year,id_day,pingi["time_work"][year][id_day])
                  Dict_moun_all[year][id_day]["pings"]["time_work"] +=pingi["time_work"][year][id_day]
                  Dict_moun_all[year][id_day]["pings"]["devices"] += len(pingi["devices"][year][id_day])





def main():

    starter()
    print("etap czytania pingów")

    #create ping as:
    # Dict["time_work"][id_years][id_days]
    #and
    #Dict["devices"][id_years][id_days]
    print(Dict_device)
    pingi = days_work(Dict_device)
    print(pingi)
    print("etap analizy pingów")
    time_work(pingi)
    print("etap zapisu")
    save_to_file(Dict_moun_all,path_save,"all")
    save_to_file(Dict_moun, path_save, "devices")



if __name__ == '__main__':
    main()