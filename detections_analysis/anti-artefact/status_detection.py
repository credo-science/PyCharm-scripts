"""
PURPOSE OF THE SCRIPT:
After analyzing the detection, you can think about the analysis by date, device, team.
The script will allow you to select options and the summary and save the summary

Each file will be analyzed separately, the results will be saved at the end of the analysis (one) of the file into a helper file.
After checking all detections, the second function will load the auxiliary files and divide them by day.

We do this because it may turn out that several files may have detections in the range that interests us.
We skip keeping everything in memory so as not to clog it with a large number of files

LAST EDITION OF THE SCRIPT: 23.06.2020
"""

import os
import json
from datetime import datetime

home = os.path.dirname(os.path.abspath(__file__)) + '/'
string = "detections_analysis/anti-artefact/"
back_to_main_path = home[:-len(string)]
path_to_file_after_filtr = back_to_main_path + "data_save/detections_analysis/anti-artefact/LA/"
path_to_save_summary = back_to_main_path + "data_save/detections_analysis/anti-artefact/LA/summary_after_filtr/"

information_about_device = {}
information_about_device_per_day = {}
os.makedirs(path_to_save_summary + "about_device/", exist_ok=True)

file_end_read = path_to_save_summary+"file_end_read.txt"

def select_analyze():
    """
    First we create detection in time,
    next step create detection list in device in one day

    type_detections have 3 options: too_often,bad,good
    we always create two files
    - summary -> showing numbers
        one detections: data,user,deviceid,team,number detections in one day(day from data)
    - grouping detection, e.g. by device (saving all detection features)
    """
    list_file = {}
    option_adres = ["too_often", "bad", "good"]

    for name_category in option_adres:
        i = 0
        list_file[name_category] = os.listdir(path_to_file_after_filtr + name_category + "/")

        for file in list_file[name_category]:
            Dict_detections = {}
            Dict_detections_to_json = {}
            Dict_detections[name_category] = {}
            Dict_detections_to_json[name_category] = {}
            adres_file = path_to_file_after_filtr + name_category+"/"+ file
            print(i, name_category, adres_file)
            i += 1
            with open(adres_file) as json_file:
                json_load = json.load(json_file)

            for record in json_load["detections"]:
                key = record["timestamp"]
                key = str(datetime.fromtimestamp(key / 1000).strftime('%Y/%m/%d'))

                if key not in Dict_detections[name_category]:
                    Dict_detections[name_category][key] = {}
                    Dict_detections_to_json[name_category][key] = {}
                detection_id = int(record["id"])
                device_id = int(record["device_id"])
                timestamp = int(record["timestamp"])
                team_id = int(record["team_id"])
                user_id = int(record["user_id"])
                too_often = int(record["artifact_too_often"])
                data_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                only_data = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                rest = timestamp % 1000

                if device_id not in Dict_detections[name_category][key]:
                    Dict_detections[name_category][key][device_id] = []
                    Dict_detections_to_json[name_category][key][device_id] = []
                if device_id not in information_about_device:
                    information_about_device[device_id] = {}
                    information_about_device[device_id]["all"] = 0
                    information_about_device[device_id]["too_often"] = 0
                    information_about_device[device_id]["bad"] = 0
                    information_about_device[device_id]["good"] = 0

                    information_about_device[device_id]["user_id"] = user_id
                    information_about_device[device_id]["team_id"] = team_id
                    information_about_device_per_day[device_id] = {}

                if only_data not in information_about_device_per_day[device_id]:
                    information_about_device_per_day[device_id][only_data] = {}
                    information_about_device_per_day[device_id][only_data]["all"] = 0
                    information_about_device_per_day[device_id][only_data]["too_often"] = 0
                    information_about_device_per_day[device_id][only_data]["bad"] = 0
                    information_about_device_per_day[device_id][only_data]["good"] = 0
                    information_about_device_per_day[device_id][only_data]["user_id"] = user_id
                    information_about_device_per_day[device_id][only_data]["team_id"] = team_id

                record_save = ("%d,\t%d,\t%d,\t%d,\t%s,\t%d,\t%d,\t%d" % (
                team_id, user_id, device_id, detection_id, data_time, rest, timestamp, too_often,))
                Dict_detections[name_category][key][device_id].append(record_save)
                Dict_detections_to_json[name_category][key][device_id].append(record)
                information_about_device[device_id]["all"] += 1
                information_about_device[device_id][name_category] += 1
                information_about_device_per_day[device_id][only_data]["all"] += 1
                information_about_device_per_day[device_id][only_data][name_category] += 1

            for name_category in Dict_detections:
                files = file.split(".")
                for key in Dict_detections[name_category]:
                    for device_id in Dict_detections[name_category][key]:
                        path_to_save_summary_category = path_to_save_summary + name_category + "/txt/" + str(
                            key) + "/" + str(device_id) + "/"
                        os.makedirs(path_to_save_summary_category, exist_ok=True)
                        f = open(path_to_save_summary_category + files[0] + ".txt", "w")
                        f.write("team_id,user_id,device_id,detection_id,data_time,milisecons,timestamp,too_often\n")
                        for detection in Dict_detections[name_category][key][device_id]:
                            f.write(str(detection) + "\n")
                        f.close()

            for name_category in Dict_detections_to_json:
                for key in Dict_detections_to_json[name_category]:
                    for device_id in Dict_detections[name_category][key]:
                        path_to_save_summary_category = path_to_save_summary + name_category + "/json/" + str(
                            key) + "/" + str(device_id) + "/"
                        os.makedirs(path_to_save_summary_category, exist_ok=True)
                        with open(path_to_save_summary_category + file, 'w') as json_file:
                            dictionary = {'detections': []}
                            list_detections = []
                            for detections in Dict_detections_to_json[name_category][key][device_id]:
                                list_detections.append(detections)
                            dictionary['detections'] = list_detections
                            json.dump(dictionary, json_file, indent=4)


def about_device():
    dict_device = []
    sum_all = 0
    sum_too_often = 0
    sum_bad = 0
    sum_good = 0
    for device_id in information_about_device:
        dict_device.append(device_id)
    dict_device.sort()
    f = open(path_to_save_summary + "about_device.txt", "w")
    f.write("team_id,user_id,device_id,all,too_often,bad,good,procent\n")
    for device in dict_device:
        device_id = information_about_device[device]
        all = device_id["all"]
        too_often = device_id["too_often"]
        bad = device_id["bad"]
        good = device_id["good"]
        team_id = device_id["team_id"]
        user_id = device_id["user_id"]
        sum_all += all
        sum_too_often += too_often
        sum_bad += bad
        sum_good += good
        try:
            procent = round(good / all, 4) * 100
        except:
            procent = 0
        f.write("%d,%d,%d,%d,%d,%d,%d,%f\n" % (team_id, user_id, device, all, too_often, bad, good, procent))
    f.write("nl.całości,%d,%d,%d,%d\n" % (sum_all, sum_too_often, sum_bad, sum_good))
    f.write("procentowo,%.2f,%.2f,%.2f,%.2f\n" % (
    sum_all / sum_all, sum_too_often / sum_all, sum_bad / sum_all, sum_good / sum_all))
    f.close()


def about_device_per_day():
    dict_device = []
    for device_id in information_about_device_per_day:
        dict_device.append(device_id)
    dict_device.sort()
    for device in dict_device:
        device_id = information_about_device_per_day[device]
        f = open(path_to_save_summary + "about_device/" + str(device) + ".txt", "w")
        for only_data in device_id:
            info_day = device_id[only_data]
            all = info_day["all"]
            too_often = info_day["too_often"]
            bad = info_day["bad"]
            good = info_day["good"]

            team_id = info_day["team_id"]
            user_id = info_day["user_id"]
            try:
                procent = round(good / all, 4) * 100
            except:
                procent = 0

            f.write("%d,%d,%s,%d,%d,%d,%d,%f\n" % (team_id, user_id, only_data, all, too_often, bad, good, procent))
        f.close()


def main():
    select_analyze()
    about_device()
    about_device_per_day()


if __name__ == '__main__':
    main()