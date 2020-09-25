"""
use after separator.py
"""
import os
import json
from datetime import datetime

detections_path = "/media/slawekstu/CREDO1/Api/paczki_michala/"

path_to_file_after_filtr = detections_path + "data_set/"
path_to_save_summary = detections_path + "distribution/"

information_about_device = {}
information_about_device_per_day = {}

def select_analyze():
    i = 0
    list_file = os.listdir(path_to_file_after_filtr)
    for file in list_file:
        Dict_detections_to_json = {}
        adres_file = path_to_file_after_filtr + file
        print(i, adres_file)
        i += 1
        with open(adres_file) as json_file:
            json_load = json.load(json_file)

        for record in json_load["detections"]:
            key = record["timestamp"]
            key = str(datetime.fromtimestamp(key / 1000).strftime('%Y/%m/%d'))

            if key not in Dict_detections_to_json:
                Dict_detections_to_json[key] = {}
            device_id = int(record["device_id"])

            if device_id not in Dict_detections_to_json[key]:
                Dict_detections_to_json[key][device_id] = []

            Dict_detections_to_json[key][device_id].append(record)

        for key in Dict_detections_to_json:
            for device_id in Dict_detections_to_json[key]:
                path_to_save_summary_category = path_to_save_summary+ "/json/" + str(key) + "/" + str(device_id) + "/"
                os.makedirs(path_to_save_summary_category, exist_ok=True)
                with open(path_to_save_summary_category + file, 'w') as json_file:
                    dictionary = {'detections': []}
                    list_detections = []
                    for detections in Dict_detections_to_json[key][device_id]:
                        list_detections.append(detections)
                    dictionary['detections'] = list_detections
                    json.dump(dictionary, json_file, indent=4)


def main():
    select_analyze()

if __name__ == '__main__':
    main()