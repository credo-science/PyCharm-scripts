"""
PURPOSE OF THE SCRIPT:
graph where the point on the histogram is the
sum detection in the last 100 days, also depends on the time
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


def sum_X (device,device_days_detection,Dict_moun,days):
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

def sum_X_for_all(id_day,year,days_detection,Dict_moun_all,days):
    """

    :param id_day: the number of the day of the year
    :param year: year of our detection
    :param days - number sum of days
    :return: new Dict for all day, all device with information (dot,worms,line, all,todays)
    """
    dot = 0
    worms = 0
    all = 0
    line = 0  # moun
    x_day_in_days = 0
    pings=0
    todays = days_detection["todays"]
    for day_ago in range(days):
        our_day_ago = todays - datetime.timedelta(days=day_ago)
        our_day_agos = str(our_day_ago).split("-")
        year_ago = int(our_day_agos[0])
        id_days = time.strptime(str(our_day_ago), "%Y-%m-%d").tm_yday
        if id_days in Dict_moun_all[year_ago]:
            temp_day = Dict_moun_all[year_ago][id_days]
            pings +=temp_day["pings"]["time_work"]
            dot += temp_day["dot"]
            worms += temp_day["worms"]
            all += temp_day["all"]
            line += temp_day["line"]
            x_day_in_days += 1

    Dict = {}
    Dict["dot"] = dot
    Dict["worms"] = worms
    Dict["all"] = all
    Dict["line"] = line
    Dict["in100days"] = x_day_in_days
    Dict["todays"] = todays
    Dict["pings"] = pings
    Dict["devices"] = Dict_moun_all[year][id_day]["devices"]

    return Dict

def prepere_data(Dict_moun_all,days):
    """
    Create Dict with value to plots
    :return: Dict_detect,error,data_days
    where
    Dict_detect - dict with sum and normalize for:  dot,line,worms,
    error- error for dot,line,worms,
    data_days - list of ID days - (need for OX in plot)
    """
    Dict_detect ={"dot":[],"line":[],"worms":[],"all":[],"devices":[],"pings":[]}
    Dict_detect["normalize"] ={"dot":[],"line":[],"worms":[],"all":[]}
    data_days = []
    error = {"dot":[],"line":[],"worms":[],"all":[]}
    error["normalize"] = {"dot":[],"line":[],"worms":[],"all":[]}


    i = 0
    for year in Dict_moun_all:
        for id_day in range(1, 366):
            i += 1
            data_days.append(i)
            if id_day in Dict_moun_all[year]:
                days_detection = Dict_moun_all[year][id_day]
                sum_temp = sum_X_for_all(id_day, year, days_detection,Dict_moun_all,days)
                Dict_detect["devices"].append(sum_temp["devices"])
                ping = days_detection["pings"]
                print(year,id_day,round(ping["time_work"]/(24*60*60*1000),2),len(days_detection["devices"]),ping["devices"])#time all device in days(24h)
                #time in 1 days
                #Dict_detect["pings"].append(ping["time_work"]/(24*60*60*1000))#in days
                #time in X days
                Dict_detect["pings"].append(sum_temp["pings"] / (24 * 60 * 60 * 1000))  # in days

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
                Dict_detect["pings"].append(0)

                Dict_detect["normalize"]["all"].append(0)
                error["normalize"]["all"].append(0)
                Dict_detect["normalize"]["dot"].append(0)
                error["normalize"]["dot"].append(0)
                Dict_detect["normalize"]["worms"].append(0)
                error["normalize"]["worms"].append(0)
                Dict_detect["normalize"]["line"].append(0)
                error["normalize"]["line"].append(0)
    return Dict_detect,error,data_days


def print_plot_for_all(Dict_detect,error,data_days,days):
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
    line_norm = Dict_detect["normalize"]["line"]
    err_line_norm = error["normalize"]["line"]
    pings = Dict_detect["pings"]#time in 1 day


    #ALL Category (dot,worms,line)
    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    #ax2 = ax1.twinx()
    binsy = data_days
    ax1.plot(binsy, line, "g--", label="line")
    ax1.plot(binsy, dot, "r*", label="dot")
    ax1.plot(binsy, worms, "b^", label="worms")
    plt.title("summary of years from (sum"+ str(days)+") days,year: " + str("2018-2020"))
    ax1.set_ylabel('Sum of the number of detections')
    #ax2.set_ylabel('Normalize')
    ax1.set_xlabel('Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend()
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/all.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()


    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    ax2 = ax1.twinx()
    binsy = data_days
    ax1.errorbar(binsy, line_norm,yerr=err_line_norm,mfc='red',ls='none', label='line')
    ax2.plot(binsy, pings, "r*", label="time work(in days)")
    plt.title("summary of years from (sum"+ str(days)+") days,year: " + str("2018-2020"))
    ax1.set_ylabel('Sum of the number of detections - normalize')
    ax2.set_ylabel('sum of time work (in days)')
    ax1.set_xlabel('Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/all2.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.errorbar(binsy, line_norm,yerr=err_line_norm,mfc='red',ls='none', label='line')
    plt.title("summary of years from (sum"+ str(days)+") days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections - normalize')
    plt.xlabel('Day since 1.01.2018')
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_all@.png",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.errorbar(binsy, all,yerr=err_all,mfc='red',mec='green', ls=':',label='all')
    plt.title("summary of years from (sum"+ str(days)+") days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections')
    plt.xlabel('Day since 1.01.2018')
    #plt.ylim(0.0, 0.15)
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_all.png",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()


def main():

    infile = open(path_save+"all", 'rb')
    Dict_moun_all = pickle.load(infile)
    infile.close()

    infile = open(path_save+"devices", 'rb')
    Dict_moun = pickle.load(infile)
    infile.close()

    days = 100
    Dict_detect,error,data_days = prepere_data(Dict_moun_all,days)
    print_plot_for_all(Dict_detect,error,data_days,days)

if __name__ == '__main__':
    main()