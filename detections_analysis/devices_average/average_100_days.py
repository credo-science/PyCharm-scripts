"""
PURPOSE OF THE SCRIPT:
graph where the point on the histogram is the
average detection in the last 100 days, also depends on the time
spent in the given days
graph for one device

LAST EDITION OF THE SCRIPT: 13.07.2020
"""


#Library
import os
import datetime
import time
import matplotlib.pyplot as plt
from data_tools.set_timestamp import convert_to_timestamp
from data_tools.read_ping import read_ping

string = "Detections_analysis/devices_average/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
start_path=back_to_main_path+"data_save/Detections_analysis/"
path_files_astrophy  =  start_path+"anti-artefact/after_filtr/summary_after_filtr/about_device/"
path_save   =   start_path+"devices_average/"

dict_detection = {}
average_dict_detection = {}
def load_file_to_dict():
    list_file = os.listdir(path_files_astrophy)

    for file in list_file:
        device_id,txt = file.split(".")
        adres_file=path_files_astrophy+file
        with open(adres_file) as fp:
            Lines = fp.readlines()
            for line in Lines:
                team_id, user_id, only_data, all, too_often, bad, good, procent = line.split(",")
                year,month,day = only_data.split("-")
                year = int(year)

                if device_id not in dict_detection:
                    dict_detection[device_id] = {}
                if year not in dict_detection[device_id]:
                    dict_detection[device_id][year] = {}

                today = datetime.date(int(year), int(month), int(day))
                todays = str(today)
                id_day = time.strptime(todays, "%Y-%m-%d").tm_yday

                if id_day not in dict_detection[device_id][year]:
                    dict_detection[device_id][year][id_day] = {}
                    dict_detection[device_id][year][id_day]["all"] = all
                    dict_detection[device_id][year][id_day]["too_often"] = too_often
                    dict_detection[device_id][year][id_day]["bad"] = bad
                    dict_detection[device_id][year][id_day]["good"] = good
                    dict_detection[device_id][year][id_day]["data"] = only_data



def average_100 (device_id):
    if device_id not in average_dict_detection:
        average_dict_detection[device_id]={}
    for year in dict_detection[device_id]:
        year = int(year)
        if year not in average_dict_detection[device_id]:
            average_dict_detection[device_id][year] = {}
        for id_data in dict_detection[device_id][year]:
            average_dict_detection[device_id][year][id_data]={}
            all = 0
            too_often = 0
            bad = 0
            good = 0
            x_day_in_100_days = 0
            data = dict_detection[device_id][year][id_data]["data"]
            year,month,day = data.split("-")
            year = int(year)
            todays = datetime.date(year,int(month),int(day))
            for day_ago in range(100):
                our_day_ago = todays - datetime.timedelta(days=day_ago)
                our_day_agos = str(our_day_ago).split("-")
                year_ago = int(our_day_agos[0])
                id_days = time.strptime(str(our_day_ago), "%Y-%m-%d").tm_yday

                if year_ago in dict_detection[device_id] and id_days in dict_detection[device_id][year_ago]:
                    temp_day=dict_detection[device_id][year_ago][id_days]
                    all += int(temp_day["all"])
                    too_often += int(temp_day["too_often"])
                    bad += int(temp_day["bad"])
                    good += int(temp_day["good"])
                    x_day_in_100_days +=1

            all = all / x_day_in_100_days
            too_often = too_often / x_day_in_100_days
            bad = bad / x_day_in_100_days
            good = good / x_day_in_100_days

            average_dict_detection[device_id][year][id_data]["all"] = all
            average_dict_detection[device_id][year][id_data]["too_often"] = too_often
            average_dict_detection[device_id][year][id_data]["bad"] = bad
            average_dict_detection[device_id][year][id_data]["good"] = good


def print_plot(list_detection,device_id):
    for year in list_detection:
        all = []
        too_often = []
        bad = []
        good = []
        data_days = []
        for id_day in range(367):
            if id_day in list_detection[year]:
                record = list_detection[year][id_day]
                data_days.append(id_day)
                all.append(record["all"])
                too_often.append(record["too_often"]/(record["all"]/100))
                bad.append(record["bad"]/(record["all"]/100))
                good.append(record["good"]/(record["all"]/100))


        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        number_bins     =   len(all)
        if number_bins>10:
            binsy = data_days
            ax1.plot(binsy, too_often, "r*", label="too_often")
            ax1.plot(binsy, bad, "m.", label=" bad")
            ax1.plot(binsy, good, "g.", label=" good")
            ax2.plot(binsy, all, "b*", label=" all")
      #      ax2.plot(binsy, muon_alls_per_device, "m--", label=" mouns/device")
            plt.title("summary of years from (average 100) days, year: "+str(year)+" for device:"+str(device_id))
            ax1.set_ylabel('average number of detections - normalize')
            ax2.set_ylabel('procent of good detections')
                    #plt.yscale("log")
            ax1.set_xlabel('day of year ')
            ax1.grid(True)
            ax1.legend(loc=4)
            ax2.legend(loc=2)
            os.makedirs(path_save+"/device_detection/"+str(year), exist_ok=True)
            plt.savefig(path_save+"/device_detection/"+str(year)+"/"+str(device_id)+".png")
            plt.clf()
            plt.cla()
            plt.close()


def main():
    load_file_to_dict()
    start = convert_to_timestamp(2018, 6, 13)
    stop = convert_to_timestamp(2020, 7, 13)
    users_devices = read_ping(start, stop)
    for device_id in dict_detection:
        print(device_id)
        average_100(device_id)
        print_plot(average_dict_detection[device_id],device_id)


if __name__ == '__main__':
    main()