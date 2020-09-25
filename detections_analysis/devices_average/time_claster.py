"""
PURPOSE OF THE SCRIPT:
graph where the point on the histogram is the
sum detection in the window 5 days, also depends on the time
spent in the given days
graph for all device
+ % detection with type "line"

LAST EDITION OF THE SCRIPT: 16.09.2020
"""
# Library
import os
import pickle

import matplotlib.pyplot as plt
from math import sqrt


string = "Detections_analysis/devices_average/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
start_path=back_to_main_path+"data_save/detections_analysis/"

path_read   =   start_path+"devices_average/clasyfication/sums/"
path_save   =   start_path+"devices_average/window/"

def read_dict_detection():
    infile = infile = open(path_read+"all", 'rb')
    Dict_detection_all = pickle.load(infile)
    infile.close()

    infile = open(path_read+"devices", 'rb')
    Dict_detection_devices= pickle.load(infile)
    infile.close()

    return Dict_detection_all, Dict_detection_devices


def prepere_data(Dict_moun_all,n_days):
    Dict_detect ={"dot":[],"line":[],"worms":[],"all":[],"devices":[],"pings":[]}
    Dict_detect["normalize"] ={"dot":[],"line":[],"worms":[],"all":[]}
    data_window = []
    error = {"dot":[],"line":[],"worms":[],"all":[]}
    error["normalize"] = {"dot":[],"line":[],"worms":[],"all":[]}

    window_days = {}

    i=0
    temp_dict = {}
    id = 0
    for year in Dict_moun_all:
        for id_day in range(1, 366):
            i+=1
            number_day = i%n_days
            temp_dict[number_day]={}
            temp_dict[number_day]["year"]=year
            temp_dict[number_day]["days"] = id_day
            if number_day%n_days ==0:
                #print(temp_dict)
                window_days[id] = temp_dict
                id+=1
                temp_dict = {}

    for window in window_days:
        number_all = 0
        number_dot = 0
        number_worms = 0
        number_line = 0
        number_pings = 0
        data_window.append(window)
        for day in window_days[window]:
            id_day = window_days[window][day]["days"]
            id_year = window_days[window][day]["year"]
            if id_day in Dict_moun_all[id_year]:
                element = Dict_moun_all[id_year][id_day]

                number_all += element["all"]
                number_dot += element["dot"]
                number_worms += element["worms"]
                number_line += element["line"]
                number_pings += element["pings"]["time_work"]

        if number_all>0:
            Dict_detect["normalize"]["all"].append(number_all / number_all)
            error["normalize"]["all"].append(sqrt(number_all) / number_all)

            Dict_detect["normalize"]["dot"].append(number_dot / number_all)
            error["normalize"]["dot"].append(sqrt(number_dot) / number_all)

            Dict_detect["normalize"]["worms"].append(number_worms / number_all)
            error["normalize"]["worms"].append(sqrt(number_worms) / number_all)

            Dict_detect["normalize"]["line"].append(number_line / number_all)
            error["normalize"]["line"].append(sqrt(number_line) / number_all)
            # sum
            Dict_detect["all"].append(number_all)
            error["all"].append(sqrt(number_all))

            Dict_detect["dot"].append(number_dot)
            error["dot"].append(sqrt(number_dot))

            Dict_detect["worms"].append(number_worms)
            error["worms"].append(sqrt(number_worms))

            Dict_detect["line"].append(number_line)
            error["line"].append(sqrt(number_line))

            Dict_detect["pings"].append(number_pings / (24 * 60 * 60 * 1000))  # in days

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

    return Dict_detect, error, data_window


def print_plot_for_all(Dict_detect, error, data_window, n_days):
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

    binsy = data_window
    #ALL Category (dot,worms,line)
    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [73, 146]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    #ax2 = ax1.twinx()

    ax1.plot(binsy, line, "g--", label="line")
    ax1.plot(binsy, dot, "r*", label="dot")
    ax1.plot(binsy, worms, "b^", label="worms")
    plt.title("summary of years from window: "+ str(n_days)+" days,year: " + str("2018-2020"))
    ax1.set_ylabel('Sum of the number of detections')
    #ax2.set_ylabel('Normalize')
    ax1.set_xlabel('Window with 5 days, Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend()
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/window_all.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()


    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [73, 146]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    ax2 = ax1.twinx()

    ax1.errorbar(binsy, line_norm,yerr=err_line_norm,mfc='red',ls='none', label='line')
    ax2.plot(binsy, pings, "r*", label="time work(in days)")
    plt.title("summary of years from window: "+ str(n_days)+" days,year: " + str("2018-2020"))
    ax1.set_ylabel('Sum of the number of detections - normalize')
    ax2.set_ylabel('sum of time work (in days)')
    ax1.set_xlabel('Window with 5 days, Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/window_all2.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(figsize=(12, 7))
    xposition = [73, 146]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.errorbar(binsy, line_norm,yerr=err_line_norm,mfc='red',ls='none', label='line')
    plt.title("summary of years from window: "+ str(n_days)+" days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections - normalize')
    plt.xlabel('Window with 5 days, Day since 1.01.2018')
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_window2.png",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(figsize=(12, 7))
    xposition = [73, 146]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.errorbar(binsy, all,yerr=err_all,mfc='red',mec='green', ls=':',label='all')
    plt.title("summary of years from window: "+ str(n_days)+" days,year: " + "2018 - 2020")
    plt.ylabel('Sum of the number of detections')
    plt.xlabel('Window with 5 days, Day since 1.01.2018')
    #plt.ylim(0.0, 0.15)
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/error_moun_window.png",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

def main():
    Dict_moun_all, Dict_moun = read_dict_detection()

    n_days = 5
    Dict_detect, error, data_window =prepere_data(Dict_moun_all,n_days)
    print_plot_for_all(Dict_detect, error, data_window, n_days)

if __name__ == '__main__':
    main()