"""
use after distribution.py
"""
import datetime
import json
import os
import time

import matplotlib.pyplot as plt
from math import sqrt

detections_path = "/media/slawekstu/CREDO1/Api/paczki_michala/distribution/"
moun_part = detections_path+"json/"
path_save = detections_path+"clasyfication/"

Dict_moun = {}
Dict_moun_all = {}
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

def average_100 (id_day,year,device,device_days_detection):
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
        year_ago = our_day_agos[0]
        id_days = time.strptime(str(our_day_ago), "%Y-%m-%d").tm_yday
        if id_days in Dict_moun[device][year]:
            temp_day=Dict_moun[device][year][id_days]
            dot += temp_day["dot"]
            worms += temp_day["worms"]
            all += temp_day["all"]
            line += temp_day["line"]
            x_day_in_100_days +=1


    dot = dot / x_day_in_100_days
    worms = worms / x_day_in_100_days
    all = all / x_day_in_100_days
    line = line / x_day_in_100_days

    Dict = {}
    Dict["dot"] = dot
    Dict["worms"] = worms
    Dict["all"] = all
    Dict["line"] = line
    Dict["todays"] = todays

    return Dict


def average_100_for_all(id_day, year, days_detection):
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

    dot = dot / x_day_in_100_days
    worms = worms / x_day_in_100_days
    all = all / x_day_in_100_days
    line = line / x_day_in_100_days

    Dict = {}
    Dict["dot"] = dot
    Dict["worms"] = worms
    Dict["all"] = all
    Dict["line"] = line
    Dict["todays"] = todays
    Dict["devices"] = Dict_moun_all[year][id_day]["devices"]

    return Dict


def print_plot():
    """
    Create plot with muons histogram for one device.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    for device in Dict_moun:
        print(device)
        for year in Dict_moun[device]:
            dot = []
            worms = []
            muon_line = []
            moun = []
            data_days = []
            alls = []
            for id_day in range(1,366):
                if id_day in Dict_moun[device][year]:
                    device_days_detection = Dict_moun[device][year][id_day]
                    average_temp = average_100(id_day,year,device,device_days_detection)

                    dot.append(average_temp["dot"]/average_temp["all"])
                    alls.append(average_temp["all"])
                    worms.append(average_temp["worms"]/average_temp["all"])
                    moun.append(average_temp["line"])
                    muon_line.append(average_temp["line"]/average_temp["all"])
                    data_days.append(id_day)

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            binsy = data_days
            ax1.plot(binsy, muon_line, "g+", label="moun")
            ax1.plot(binsy, dot, "r-", label="dot")
            ax1.plot(binsy, worms, "b^", label="worms")
            #ax1.plot(binsy, moun_no, "r-", label="moun isn't")

            #ax2.plot(binsy, alls, "y.", label=" all")
            #ax2.plot(binsy, moun, "m--", label=" mouns")
            plt.title("summary of years from (average 100) days,\nyear: "+str(year)+" for mouns, device: "+str(device))
            ax1.set_ylabel('average number of detections - normalize')
            #ax2.set_ylabel('number of detection')
                    #plt.yscale("log")
            ax1.set_xlabel('day of year ')
            ax1.grid(True)
            ax1.legend()
            ax1.set_ylim([0.00,1.00])
            #ax2.set_ylim([0, 450])
            #ax2.legend(loc=1)
            os.makedirs(path_save + str(year), exist_ok=True)
            plt.savefig(path_save+str(year)+"/"+str(device)+".png")
            plt.clf()
            plt.cla()
            plt.close()

def print_plot_for_all():
    """
    Create plot with muons histogram for all devices.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    for year in Dict_moun_all:
        dot = []
        worms = []
        muon_line = []
        moun = []
        data_days = []
        number_devices = []
        alls = []
        error = []
        moun_error=[]
        for id_day in range(1,366):
            data_days.append(id_day)
            if id_day in Dict_moun_all[year]:
                days_detection = Dict_moun_all[year][id_day]
                average_temp = average_100_for_all(id_day,year,days_detection)

                dot.append(average_temp["dot"]/average_temp["all"])
                alls.append(average_temp["all"])
                worms.append(average_temp["worms"]/average_temp["all"])
                moun.append(average_temp["line"])
                muon_line.append(average_temp["line"]/average_temp["all"])
                number_devices.append(average_temp["devices"])
                #data_days.append(id_day)
                error.append(sqrt(average_temp["line"]) / average_temp["all"])
                moun_error.append(sqrt(average_temp["line"]))
            else:
                dot.append(0)
                alls.append(0)
                worms.append(0)
                moun.append(0)
                muon_line.append(0)
                number_devices.append(0)
                #data_days.append(id_day)
                error.append(0)
                moun_error.append(0)
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        binsy = data_days
        ax1.plot(binsy, muon_line, "g-", label="line")
        ax1.plot(binsy, dot, "r*", label="dot")
        ax1.plot(binsy, worms, "b^", label="worms")
        #ax2.plot(binsy, number_devices, "k-", label=" number_devices")
        #ax2.plot(binsy, moun, "m--", label=" mouns")
        plt.title("summary of years from (average 100) days,year: " + str(year))
        ax1.set_ylabel('average number of detections - normalize')
        #ax2.set_ylabel('number of detection')
        # plt.yscale("log")
        ax1.set_xlabel('day of year ')
        ax1.grid(True)
        ax1.legend(loc=2)
        ax1.set_ylim([0.00, 1.00])
        # ax2.set_ylim([0, 450])
        #ax2.legend(loc=1)
        os.makedirs(path_save + str(year), exist_ok=True)
        plt.savefig(path_save + str(year) + "/all.png")
        plt.clf()
        plt.cla()
        plt.close()


        plt.errorbar(binsy, muon_line, yerr=error, label='moun (line')
        plt.title("summary of years from (average 100) days,year: " + str(year)+" for mouns(line)")
        plt.ylabel('average number of detections - normalize')
        plt.xlabel('day of year ')
        plt.ylim(0.0,0.2)
        plt.grid(True)
        plt.legend(loc=2)
        os.makedirs(path_save + str(year), exist_ok=True)
        plt.savefig(path_save + str(year) + "/error_moun_all.png")
        plt.clf()
        plt.cla()
        plt.close()

        plt.errorbar(binsy, moun, yerr=moun_error, label='moun (line')
        plt.plot(binsy, moun, "k-")
        plt.title("summary of years from (average 100) days,year: " + str(year)+" for mouns(line)")
        plt.ylabel('average number of detections')
        plt.xlabel('day of year ')
        plt.grid(True)
        plt.legend(loc=2)
        os.makedirs(path_save + str(year), exist_ok=True)
        plt.savefig(path_save + str(year) + "/error_moun_all2.png")
        plt.clf()
        plt.cla()
        plt.close()


def print_plot2():
    """
    Create plot with muons histogram for one device.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    for device in Dict_moun:
        print(device)
        for year in Dict_moun[device]:
            dot = []
            worms = []
            muon_line = []
            moun = []
            data_days = []
            alls = []
            for id_day in range(367):
                if id_day in Dict_moun[device][year]:
                    device_days_detection = Dict_moun[device][year][id_day]

                    dot.append(device_days_detection["dot"]/device_days_detection["all"])
                    alls.append(device_days_detection["all"])
                    worms.append(device_days_detection["worms"]/device_days_detection["all"])
                    moun.append(device_days_detection["line"])
                    muon_line.append(device_days_detection["line"]/device_days_detection["all"])
                    data_days.append(id_day)

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            binsy = data_days
            ax1.plot(binsy, muon_line, "g-", label="moun")
            ax1.plot(binsy, dot, "r*", label="dot")
            ax1.plot(binsy, worms, "b^", label="worms")
            #ax1.plot(binsy, moun_no, "r-", label="moun isn't")

            #ax2.plot(binsy, alls, "y.", label=" all")
            #ax2.plot(binsy, moun, "m--", label=" mouns")
            plt.title("summary of years from days,\nyear: "+str(year)+" for mouns, device: "+str(device))
            ax1.set_ylabel('number of detections - normalize')
            #ax2.set_ylabel('number of detection')
                    #plt.yscale("log")
            ax1.set_xlabel('day of year ')
            ax1.grid(True)
            ax1.legend()
            ax1.set_ylim([0.00,1.00])
            #ax2.set_ylim([0, 450])
            #ax2.legend(loc=1)
            os.makedirs(path_save+"/no_average/" + str(year), exist_ok=True)
            plt.savefig(path_save+"/no_average/"+str(year)+"/"+str(device)+".png")
            plt.clf()
            plt.cla()
            plt.close()

def print_plot_for_all2():
    """
    Create plot with muons histogram for all devices.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    for year in Dict_moun_all:
        dot = []
        worms = []
        muon_line = []
        moun = []
        data_days = []
        number_devices = []
        alls = []
        error = []
        moun_error=[]
        for id_day in range(1,366):
            data_days.append(id_day)
            if id_day in Dict_moun_all[year]:
                days_detection = Dict_moun_all[year][id_day]

                dot.append(days_detection["dot"]/days_detection["all"])
                alls.append(days_detection["all"])
                worms.append(days_detection["worms"]/days_detection["all"])
                moun.append(days_detection["line"])
                muon_line.append(days_detection["line"]/days_detection["all"])
                number_devices.append(days_detection["devices"])
                error.append(sqrt(days_detection["line"]) / days_detection["all"])
                moun_error.append(sqrt(days_detection["line"]))
            else:
                dot.append(0)
                alls.append(0)
                worms.append(0)
                moun.append(0)
                muon_line.append(0)
                number_devices.append(0)
                #data_days.append(id_day)
                error.append(0)
                moun_error.append(0)
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        binsy = data_days
        ax1.plot(binsy, muon_line, "g-", label="line")
        ax1.plot(binsy, dot, "r*", label="dot")
        ax1.plot(binsy, worms, "b^", label="worms")
        plt.title("summary of years from days,year: " + str(year))
        ax1.set_ylabel('average number of detections - normalize')
        ax1.set_xlabel('day of year ')
        ax1.grid(True)
        ax1.legend(loc=2)
        ax1.set_ylim([0.00, 1.00])
        os.makedirs(path_save+"/no_average/" + str(year), exist_ok=True)
        plt.savefig(path_save+"/no_average/" + str(year) + "/all.png")
        plt.clf()
        plt.cla()
        plt.close()


        plt.errorbar(binsy, muon_line, yerr=error, label='moun (line')
        plt.title("summary of years from (average 100) days,year: " + str(year)+" for mouns(line)")
        plt.ylabel('average number of detections - normalize')
        plt.xlabel('day of year ')
        plt.ylim(0.0,0.2)
        plt.grid(True)
        plt.legend(loc=2)
        os.makedirs(path_save+"/no_average/" + str(year), exist_ok=True)
        plt.savefig(path_save+"/no_average/" + str(year) + "/error_moun_all.png")
        plt.clf()
        plt.cla()
        plt.close()

        plt.errorbar(binsy, moun, yerr=moun_error, label='moun (line')
        plt.plot(binsy, moun, "k-")
        plt.title("summary of years from (average 100) days,year: " + str(year)+" for mouns(line)")
        plt.ylabel('average number of detections')
        plt.xlabel('day of year ')
        plt.grid(True)
        plt.legend(loc=2)
        os.makedirs(path_save+"/no_average/" + str(year), exist_ok=True)
        plt.savefig(path_save+"/no_average/" + str(year) + "/error_moun_all2.png")
        plt.clf()
        plt.cla()
        plt.close()


def starter():
    list_year ={2018,2019,2020}#{2018,2019,2020}
    list_file = os.listdir(detections_path)
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

    print("start starter")
    starter()
    print("start plot")
    print_plot()
    print_plot_for_all()
    print("start plot2")
    #no average_100
    print_plot2()
    print_plot_for_all2()
    print(rodzaje)

if __name__ == '__main__':
    main()