import os
import json
detections_path = '/media/slawekstu/CREDO1/Api/credo-data-export/detections/'

string = "Detections_analysis/raw_data/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
save_path=back_to_main_path+"data_save/detections/"

def read_file():
    #list_files = os.listdir(detections_path)
    #temp_dict = {}
    #list_file = []
    #for i in range (15):
    #    list_file.append(list_files[i])
    list_file = os.listdir(detections_path)
    i = 0
    for file_name in list_file:
        print(i, file_name)
        i+=1
        temp_dict = {}
        json_path = detections_path + file_name
        with open(json_path) as json_file:
            json_load = json.load(json_file)

        for detection in json_load['detections']:
            source = detection["source"]
            if source not in temp_dict:
                temp_dict[source] = {}
                temp_dict[source]["visible"] = []
                temp_dict[source]["unvisible"] = []

            if str(detection["visible"])=="True":
                visible = "visible"
            else:
                visible = "unvisible"

            temp_dict[source][visible].append(detection)

        for sources in temp_dict:
            for visibles in temp_dict[sources]:
                if len(temp_dict[sources][visibles])>0:
                    path_save = save_path+visibles+"/"+sources+"/"
                    os.makedirs(path_save, exist_ok=True)
                    with open(path_save+file_name, 'w') as json_file:  # zapisujemy dobre detekcje do jsona
                        dictionary = {'detections': []}
                        dictionary['detections'] = temp_dict[sources][visibles]
                        json.dump(dictionary, json_file, indent=4)


def main():
    read_file()

if __name__ == '__main__':
    main()