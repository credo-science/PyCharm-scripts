"""
Read file and seperate per device, and year
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
save_path = back_to_main_path +"data_save/detections_analysis/data_set/raw_dev/"
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
        device_id = detection["device_id"]
        if device_id not in temp_dict:
            temp_dict[device_id] = {}
            
        timestamp = detection["timestamp"]/1000
        data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        dt = tm_data = time.strptime(str(data_str), '%Y-%m-%d %H:%M:%S')
        tm_data = ("%s/%s/%s/"%(dt.tm_year,dt.tm_mon,dt.tm_mday))
        if dt.tm_year not in temp_dict[device_id]:
            temp_dict[device_id][dt.tm_year] = {}
            temp_dict[device_id][dt.tm_year]["visible"] = {}
            temp_dict[device_id][dt.tm_year]["unvisible"] = {}
            temp_dict[device_id][dt.tm_year]["visible"]["detections"]=[]
            temp_dict[device_id][dt.tm_year]["unvisible"]["detections"] = []

        if str(detection["visible"]) == "True":
            visible = "visible"
        else:
            visible = "unvisible"

        temp_dict[device_id][dt.tm_year][visible]["detections"].append(detection)

    for device in temp_dict:
        for year in temp_dict[device]:
            for visibles in temp_dict[device][year]:
                if len(temp_dict[device][year][visibles])>0:
                    path_save = save_path +str(device) + "/"+ visibles + "/" + str(year)+"/"
                    os.makedirs(path_save, exist_ok=True)
                    #print(path_save)
                    outfile = open(path_save + file_name, 'wb')
                    pickle.dump(temp_dict[device][year][visibles]["detections"], outfile)
                    outfile.close()


    f = open(file_list, "a")
    f.write(file_name + ".json\n")
    f.close()

def join_files():
    #files = os.listdir(save_path)
    paths = save_path
    files = [ f for f in os.listdir(paths) if os.path.isdir(os.path.join(paths,f))]
    for device in files:
        print(device)
        paths = save_path+device+"/"
        files = [ f for f in os.listdir(paths) if os.path.isdir(os.path.join(paths,f))]

        for visible in files:
            paths = save_path + device + "/" + visible + "/"
            files = [f for f in os.listdir(paths) if os.path.isdir(os.path.join(paths, f))]
            for year in files:
                paths = save_path + device + "/"+visible+"/"+year+"/"
                print(paths)

                files_year = [f for f in os.listdir(paths) if os.path.isfile(os.path.join(paths, f))]
                dict = []
                for file in files_year:
                    if ".json" not in str(file):
                        infile = open(paths + file, 'rb')
                        dict.append(pickle.load(infile))
                        infile.close()

                if len(dict) > 20:
                    czesc = int(len(dict) / 15)#i.e 50/15 = 3
                    for nr_file in range(czesc + 1): #0 (0-14),1 (15-29),2(30-44),3 (45-50)
                        dict_detections = []
                        if nr_file == czesc:#i.e 3 = 3
                            for w in range(nr_file * 15, len(dict)):#save file id : 45,46,47,48,49,50
                                dict_detections += dict[w]
                        else:
                            for i in range(15):#i.e save file id : 0,1,2,3,..,13,14
                                dict_detections+= dict[nr_file * 15 + i]
                        print(len(dict_detections))
                        save_to_json(dict_detections, year, paths, part=nr_file)
                else:
                    dict_detections = []
                    for id in range(len(dict)):
                        dict_detections += dict[id]
                    print(len(dict_detections))
                    save_to_json(dict_detections, year, paths)


def save_to_json(dict_detections,year,path,part=-1):
    start = int(datetime(int(year), int(1), int(1), 0, 0).timestamp())
    stop = int(datetime(int(year), int(12), int(31), 0, 0).timestamp())
    file_name = "export_" + str(start) + "000_" + str(stop) + "000.json"
    if part >-1:
        file_name = "export_" + str(start) + "000_" + str(stop) + "000_"+str(part)+".json"
    with open(path + file_name, 'w') as json_file:
        dictionary = {'detections': []}
        dictionary['detections'] = dict_detections
        json.dump(dictionary, json_file, indent=4)
def main():
    start()
    join_files()

if __name__ == '__main__':
    main()