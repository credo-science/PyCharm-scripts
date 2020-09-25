"""
PURPOSE OF THE SCRIPT:
graph where the point on the histogram is the
average detection in the last 100 days, also depends on the time
spent in the given days
graph for all device
+ % detection with type "line"

LAST EDITION OF THE SCRIPT: 12.07.2020
"""


import datetime
import json
# Library
import os
import time
import pickle

import matplotlib.pyplot as plt
from math import sqrt

string = "Detections_analysis/devices_average/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
start_path=back_to_main_path+"data_save/detections_analysis/"
path_files_astrophy  =  start_path+"anti-artefact/LA/summary_after_filtr/"
moun_part = path_files_astrophy+"good/json/"
path_save   =   start_path+"devices_average/clasyfication/sums/"


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

    today = datetime.date(int(year), int(month), int(days))
    todays = str(today)
    id_day = time.strptime(todays, "%Y-%m-%d").tm_yday

    if id_day not in Dict_moun_all[year]:
        Dict_moun_all[year][id_day] = {}
        Dict_moun_all[year][id_day]["dot"] = 0
        Dict_moun_all[year][id_day]["line"] = 0
        Dict_moun_all[year][id_day]["worms"] = 0
        Dict_moun_all[year][id_day]["all"] = 0
        Dict_moun_all[year][id_day]["devices"] = 0
        Dict_moun_all[year][id_day]["todays"] = today

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

    Dict_moun_all[year][id_day]["devices"] +=1
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

def sum_100 (id_day,year,device,device_days_detection):
    """
    :param id_day: the number of the day of the year
    :param year: year of our detection
    :param device: id of the currently analyzed device
    :param device_days_detection: dict of detection
    :return: new Dict for all day, one device with information (dot,worms,line, all,todays)
    """
    dot = 0
    worms = 0
    all = 0
    line = 0#moun
    x_day_in_100_days=0

    todays = device_days_detection["todays"]
    for day_ago in range(100):
        our_day_ago = todays - datetime.timedelta(days=day_ago)
        our_day_agos = str(our_day_ago).split("-")
        year_ago = int(our_day_agos[0])
        id_days = time.strptime(str(our_day_ago), "%Y-%m-%d").tm_yday
        if id_days in Dict_moun[device][year_ago]:
            temp_day=Dict_moun[device][year_ago][id_days]
            dot += temp_day["dot"]
            worms += temp_day["worms"]
            all += temp_day["all"]
            line += temp_day["line"]
            x_day_in_100_days +=1


    Dict = {}
    Dict["dot"] = dot
    Dict["worms"] = worms
    Dict["all"] = all
    Dict["line"] = line
    Dict["todays"] = todays

    return Dict

def sum_100_for_all(id_day, year, days_detection):
    """

    :param id_day: the number of the day of the year
    :param year: year of our detection
    :return: new Dict for all day, all device with information (dot,worms,line, all,todays)
    """
    dot = 0
    worms = 0
    all = 0
    line = 0  # moun
    x_day_in_100_days = 0

    todays = days_detection["todays"]
    for day_ago in range(100):
        our_day_ago = todays - datetime.timedelta(days=day_ago)
        our_day_agos = str(our_day_ago).split("-")
        year_ago = int(our_day_agos[0])
        id_days = time.strptime(str(our_day_ago), "%Y-%m-%d").tm_yday
        if id_days in Dict_moun_all[year_ago]:
            temp_day = Dict_moun_all[year_ago][id_days]
            dot += temp_day["dot"]
            worms += temp_day["worms"]
            all += temp_day["all"]
            line += temp_day["line"]
            x_day_in_100_days += 1

    Dict = {}
    Dict["dot"] = dot
    Dict["worms"] = worms
    Dict["all"] = all
    Dict["line"] = line
    Dict["in100days"] = x_day_in_100_days
    Dict["todays"] = todays
    Dict["devices"] = Dict_moun_all[year][id_day]["devices"]

    return Dict

def prepere_data():
    """
    Create Dict with value to plots
    :return: Dict_detect,error,data_days
    where
    Dict_detect - dict with sum and normalize for:  dot,line,worms,
    error- error for dot,line,worms,
    data_days - list of ID days - (need for OX in plot)
    """
    Dict_detect ={"dot":[],"line":[],"worms":[],"all":[],"devices":[]}
    Dict_detect["normalize"] ={"dot":[],"line":[],"worms":[],"all":[]}
    data_days = []
    error = {"dot":[],"line":[],"worms":[],"all":[]}
    error["normalize"] = {"dot":[],"line":[],"worms":[],"all":[]}

    i = 0
    for year in Dict_moun_all:
        i+=1
        for id_day in range(1, 366):
            i += 1
            data_days.append(i)
            if id_day in Dict_moun_all[year]:
                days_detection = Dict_moun_all[year][id_day]
                sum_temp = sum_100_for_all(id_day, year, days_detection)
                Dict_detect["devices"].append(sum_temp["devices"])

                number_all = sum_temp["all"]
                number_dot = sum_temp["dot"]
                number_worms = sum_temp["worms"]
                number_line = sum_temp["line"]
                #normalize
                Dict_detect["normalize"]["all"].append(number_all/number_all)
                error["normalize"]["all"].append(sqrt(number_all)/number_all)

                Dict_detect["normalize"]["dot"].append(number_dot/number_all)
                error["normalize"]["dot"].append(sqrt(number_dot)/number_all)

                Dict_detect["normalize"]["worms"].append(number_worms/number_all)
                error["normalize"]["worms"].append(sqrt(number_worms)/number_all)

                Dict_detect["normalize"]["line"].append(number_line/number_all)
                error["normalize"]["line"].append(sqrt(number_line)/number_all)
                #sum
                Dict_detect["all"].append(number_all)
                error["all"].append(sqrt(number_all))

                Dict_detect["dot"].append(number_dot)
                error["dot"].append(sqrt(number_dot))

                Dict_detect["worms"].append(number_worms)
                error["worms"].append(sqrt(number_worms))

                Dict_detect["line"].append(number_line)
                error["line"].append(sqrt(number_line))

            else:
                Dict_detect["dot"].append(0)
                error["dot"].append(0)
                Dict_detect["worms"].append(0)
                error["worms"].append(0)
                Dict_detect["line"].append(0)
                error["line"].append(0)
                Dict_detect["devices"].append(0)
                Dict_detect["all"].append(0)
                error["all"].append(0)

                Dict_detect["normalize"]["all"].append(0)
                error["normalize"]["all"].append(0)
                Dict_detect["normalize"]["dot"].append(0)
                error["normalize"]["dot"].append(0)
                Dict_detect["normalize"]["worms"].append(0)
                error["normalize"]["worms"].append(0)
                Dict_detect["normalize"]["line"].append(0)
                error["normalize"]["line"].append(0)
    return Dict_detect,error,data_days


def print_plot_for_all(Dict_detect,error,data_days):
    """
    Create plot with muons histogram for all devices.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    line = Dict_detect["line"]
    dot = Dict_detect["dot"]
    worms = Dict_detect["worms"]
    all = Dict_detect["all"]
    err_all = error["all"]
    err_line = error["line"]


    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    binsy = data_days
    ax1.plot(binsy, line, "g--", label="line")
    ax1.plot(binsy, dot, "r*", label="dot")
    ax1.plot(binsy, worms, "b^", label="worms")
    # ax2.plot(binsy, number_devices, "k-", label=" number_devices")
    # ax2.plot(binsy, moun, "m--", label=" mouns")
    plt.title("summary of years from (sum 100) days,year: " + str("2018-2020"))
    ax1.set_ylabel('Sum of the number of detections - normalize')
    # ax2.set_ylabel('number of detection')
    # plt.yscale("log")
    ax1.set_xlabel('Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend(loc=2)
    # ax2.set_ylim([0, 450])
    # ax2.legend(loc=1)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/all.png")
    plt.clf()
    plt.cla()
    plt.close()
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    #plt.errorbar(binsy, dot,"b+", yerr=error["dot"], label='dot')
    plt.errorbar(binsy, line,yerr=err_line,mfc='red',mec='green',ls='none', fmt='o', label='line')
    #plt.errorbar(binsy, worms,"b^", yerr=error["worms"], label='worms')
    plt.title("summary of years from (sum 100) days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections - normalize')
    plt.xlabel('Day since 1.01.2018')
    #plt.ylim(0.0, 0.15)
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_all@.png")
    plt.clf()
    plt.cla()
    plt.close()

    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.errorbar(binsy, all,yerr=err_all,mfc='red',mec='green', ls=':',label='all')
    plt.title("summary of years from (sum 100) days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections - normalize')
    plt.xlabel('Day since 1.01.2018')
    #plt.ylim(0.0, 0.15)
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_all.png")
    plt.clf()
    plt.cla()
    plt.close()

def starter():
    list_year ={2018}#{2018,2019,2020}
    list_file = os.listdir(path_files_astrophy)
    for year in list_year:
        path = moun_part+str(year)+"/"
        list_file = os.listdir(path)
        for month in list_file:
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

def main():

    #print("start starter")
    #starter()
    #print("start plot")
    #Dict_moun = {}
    #Dict_moun_all = {}
    infile = infile = open(path_save+"all.json", 'rb')
    Dict_moun_all = pickle.load(infile)
    infile.close()

    infile = open(path_save+"devices.json", 'rb')
    Dict_moun = pickle.load(infile)
    infile.close()

    Dict_detect,error,data_days = prepere_data()
    print_plot_for_all(Dict_detect,error,data_days)

if __name__ == '__main__':
    main()