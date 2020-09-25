"""
Read file and seperate per day
"""
import os
import json
from datetime import datetime
import time
import pickle

detections_path = '/media/slawekstu/CREDO1/Api/credo-data-export/detections/'
home = os.path.dirname(os.path.abspath(__file__))+'/'
string = "detections_analysis/data_set/"

back_to_main_path = home[:-len(string)]
save_path = back_to_main_path +"data_save/detections_analysis/data_set/raw/"
file_list = save_path+ 'file_analysis_completed.txt'

def start():
    list_file_json = os.listdir(detections_path)
    index = 0

    for json_file in range(len(list_file_json)):#file where we have name file which files we have finished reading
        file_was_read = check_file(list_file_json[json_file])

        if file_was_read == 0:
            current_file = detections_path + list_file_json[json_file]
            file_name=list_file_json[json_file].split(".")
            file_name=file_name[0]# [0] - name file, [1] - ".json"
            print(index,"/",len(list_file_json),file_name)

            seperate(current_file,file_name)
        index += 1

def check_file(file_name):
    """

    :param file_name: checked the file name
    :param file_list: file with a list of files that have already been checked
    :return:
    """
    file_was_read = 0  # 0 - no, 1 - yes
    if str(os.path.isfile(file_list)) == "True":
        f = open(file_list, "r")
        for line in f:
            line = line.rstrip("\n")
            if str(line) == str(file_name):
                print(line, "was readed, we don't read this file")
                file_was_read = 1
        f.close()

    return file_was_read

def seperate(current_file,file_name):
    with open(current_file) as json_file:
        json_load = json.load(json_file)

    temp_dict = {}
    json_path = detections_path + file_name
    with open(json_path+".json") as json_file:
        json_load = json.load(json_file)

    for detection in json_load['detections']:
        source = detection["source"]
        device_id = detection["device_id"]
        if source not in temp_dict:
            temp_dict[source] = {}
            temp_dict[source]["visible"] = {}
            temp_dict[source]["unvisible"] = {}

        if str(detection["visible"]) == "True":
            visible = "visible"
        else:
            visible = "unvisible"

        timestamp = detection["timestamp"]/1000
        data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        dt = tm_data = time.strptime(str(data_str), '%Y-%m-%d %H:%M:%S')
        tm_data = ("%s/%s/%s/"%(dt.tm_year,dt.tm_mon,dt.tm_mday))
        if dt.tm_yday not in temp_dict[source][visible]:
            temp_dict[source][visible][dt.tm_yday] = {}
            temp_dict[source][visible][dt.tm_yday]["string"] = tm_data
            temp_dict[source][visible][dt.tm_yday]["detections"]=[]

        temp_dict[source][visible][dt.tm_yday]["detections"].append(detection)

    for sources in temp_dict:
        for visibles in temp_dict[sources]:
            for dataset in temp_dict[sources][visibles]:
                if len(temp_dict[sources][visibles][dataset]["string"]) > 0:
                    path_save = save_path +sources + "/"+ visibles + "/" + temp_dict[sources][visibles][dataset]["string"]
                    os.makedirs(path_save, exist_ok=True)
                    #print(path_save)
                    outfile = open(path_save + file_name, 'wb')
                    pickle.dump(temp_dict[sources][visibles][dataset]["detections"], outfile)
                    outfile.close()


    f = open(file_list, "a")
    f.write(file_name + ".json\n")
    f.close()

def join_files():
    #files = os.listdir(save_path)
    path = save_path
    files = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]
    for sources in files:
        path = save_path+sources+"/"
        files = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]

        for visible in files:
            path = save_path + sources + "/"+visible+"/"
            files = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for year in files:
                ypath = path+str(year)+"/"
                months = [f for f in os.listdir(ypath) if os.path.isdir(os.path.join(ypath, f))]
                for month in months:
                    mpath = ypath + str(month) + "/"
                    days = [f for f in os.listdir(mpath) if os.path.isdir(os.path.join(mpath, f))]
                    for day in days:
                        dpath = mpath + str(day) + "/"
                        print(dpath)
                        files_day = [f for f in os.listdir(dpath) if os.path.isfile(os.path.join(dpath, f))]
                        print(files_day)
                        dict = []
                        for file in files_day:
                            if ".json" not in str(file):
                                infile = open(dpath+file, 'rb')
                                dict.append(pickle.load(infile))
                                infile.close()
                        dict_detections = []
                        for id in range(len(dict)):
                            dict_detections +=dict[id]
                        start = int(datetime(int(year), int(month), int(day), 0, 0).timestamp())
                        stop = int(datetime(int(year), int(month), int(day), 0, 0).timestamp())
                        file_name = "export_"+str(start)+"000_"+str(stop)+"000.json"
                        with open(dpath + file_name, 'w') as json_file:
                            dictionary = {'detections': []}
                            dictionary['detections'] = dict_detections
                            json.dump(dictionary, json_file, indent=4)



def main():
    start()
    join_files()

if __name__ == '__main__':
    main()