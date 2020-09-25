"""
save information from evry days to file as dict

"""
import os
import json
from datetime import datetime
from data_tools.mapping import read_mapping
import time
import pickle #zapis słownika

detections_path = '/media/slawekstu/CREDO1/Api/credo-data-export/detections/'

string = "Detections_analysis/activity/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
save_path=back_to_main_path+"data_save/detections_analysis/activity/"

def read_file():
    dict = {}
    for year in range(2018, 2021):
        dict[year] = {}
        for id_day in range(1, 366):
            dict[year][id_day] = {}
            dict[year][id_day]["visible"] = 0
            dict[year][id_day]["unvisible"] = 0
            dict[year][id_day]["device"] = []
            dict[year][id_day]["users"] = []


    list_file = os.listdir(detections_path)
    #list_file = []
    #for i in range (15):
     #   list_file.append(list_files[i])
    i=0
    for file_name in list_file:
        print(i,file_name)
        i+=1
        temp_dict = {}
        json_path = detections_path + file_name
        with open(json_path) as json_file:
            json_load = json.load(json_file)

        for detection in json_load['detections']:
            user = detection["user_id"]
            device = detection["device_id"]
            timestamp = detection["timestamp"]/1000

            data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            tm_data = time.strptime(str(data_str), '%Y-%m-%d')
            id_year = id_days = tm_data.tm_year
            id_day = tm_data.tm_yday
            if 2017< id_year <2021:
                if id_year == 2018 and id_day < 165:#14-06-2018 poczatek dzialania apki v2
                    continue
                else:
                    if str(detection["visible"])=="True":
                        visible = "visible"
                    else:
                        visible = "unvisible"

                    dict[id_year][id_day][visible] += 1
                    if device not in dict[id_year][id_day]["device"]:
                        dict[id_year][id_day]["device"].append(device)
                    if user not in dict[id_year][id_day]["users"]:
                        dict[id_year][id_day]["users"].append(user)

    for id_year in range(2018, 2021):
        for id_day in range(1, 366):
            dict[id_year][id_day]["device"] = len(dict[id_year][id_day]["device"])
            dict[id_year][id_day]["users"] = len(dict[id_year][id_day]["users"])
    return  dict

def save_to_file(detections, path_save, file_name):
    os.makedirs(path_save, exist_ok=True)
    print(path_save + file_name)
    outfile = open(path_save + file_name, 'wb')
    pickle.dump(detections, outfile)
    outfile.close()


def main():
    #dictionary = read_file()
    #save_to_file(dictionary, save_path, "summary")
    dict = read_mapping("devices")
    print(len(dict))

if __name__ == '__main__':
    main()