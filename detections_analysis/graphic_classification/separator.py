"""
Skrypt do analizy paczek testowych
10.09.2020
"""
import os
import json
from data_tools.save_json import save_to_json
from data_tools.astropy_analysis import astropy_analyze

string = "Detections_analysis/graphic_classification/"
home = os.path.dirname(os.path.abspath(__file__)) + "/"
detections_path = "/media/slawekstu/CREDO1/Api/paczki_michala/"

list_users = [157,1510,4125,10069,12315,15190]

def preperate_data():
    """
    Function to extract data by device and user - but only those that are on our list "list_users"
    :return:
    """
    list_file_json = os.listdir(detections_path+"json/")
    for json_file in range(len(list_file_json)):
        operation_in_file(list_file_json[json_file])


def operation_in_file(current_file):
    Dict_devices = {}
    adres = detections_path+"json/" + current_file
    with open(adres) as f:
        json_load = json.load(f)
    for record in json_load["detections"]:
        user = int(record["user_id"])
        if user in list_users:
            device = record["device_id"]
            if device not in Dict_devices:
                Dict_devices[device] = []
            records = astropy_analyze(record)
            
            Dict_devices[device].append(records)

    path_save = detections_path+"data_set/"
    save_to_json(Dict_devices, path_save, current_file)


def main():
    preperate_data() #create json with only our device

if __name__ == '__main__':
    main()