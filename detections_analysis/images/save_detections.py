import base64
import os
import json


string = "Detections_analysis/images/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
start_path=back_to_main_path+"data_save/detections_analysis/"
path_files  =  start_path+"anti-artefact/LA/"

def read_file(category="good"):
    path = path_files+category +"/"
    list_file = os.listdir(path)
    our_file = list_file[10]
    json_path = path + our_file

    with open(json_path) as json_file:
        json_load = json.load(json_file)

    for detection in json_load['detections']:
        frame_content = detection["frame_content"]
        id = detection["id"]
        option = 0
        if category == "good":
            solidity = detection["solidity"]
            ellipticity = detection["ellipticity"]

            if float(solidity) == 1.0 or float(ellipticity) <= 0.2:
                option = 1
            elif float(ellipticity) > 0.2 and float(ellipticity) <= 0.6:
                option = 2

            elif float(solidity) <= 0.7 and float(ellipticity) > 0.6:
                option = 3

        obrazek = frame_content.encode('ascii')
        adres = start_path+"/images/"+str(category)+"/"+str(option)+"/"
        os.makedirs(adres, exist_ok=True)
        with open(adres+ str(id) + ".png", "wb") as fh:
            fh.write(base64.decodebytes(obrazek))

def soldity(category="good"):
    path = path_files + category + "/"
    list_file = os.listdir(path)
    our_file = list_file[10]
    json_path = path + our_file

    with open(json_path) as json_file:
        json_load = json.load(json_file)

    for detection in json_load['detections']:
        frame_content = detection["frame_content"]
        id = detection["id"]
        option = 0
        if category == "good":
            solidity = detection["solidity"]

            if 0.0< float(solidity) < 0.1:
                option = "0_1"

            if 0.1< float(solidity) < 0.2:
                option = "0_2"
            if 0.2< float(solidity) < 0.3:
                option = "0_3"
            if 0.3< float(solidity) < 0.4:
                option = "0_4"
            if 0.4< float(solidity) < 0.5:
                option = "0_5"
            if 0.5< float(solidity) < 0.6:
                option = "0_6"
            if 0.6< float(solidity) < 0.7:
                option = "0_7"
            if 0.7< float(solidity) < 0.8:
                option = "0_8"
            if 0.8< float(solidity) < 0.9:
                option = "0_9"
            if 0.9< float(solidity) < 1:
                option = "1"

        obrazek = frame_content.encode('ascii')
        adres = start_path + "/images/soldity/" + str(option) + "/"
        os.makedirs(adres, exist_ok=True)
        with open(adres + str(id) + ".png", "wb") as fh:
            fh.write(base64.decodebytes(obrazek))


def ellipticity(category="good"):
    path = path_files + category + "/"
    list_file = os.listdir(path)
    our_file = list_file[10]
    json_path = path + our_file

    with open(json_path) as json_file:
        json_load = json.load(json_file)

    for detection in json_load['detections']:
        frame_content = detection["frame_content"]
        id = detection["id"]
        option = 0
        if category == "good":
            ellipticity = detection["ellipticity"]

            if 0.0 < float(ellipticity) <= 0.1:
                option = "0_1"

            if 0.1 < float(ellipticity) <= 0.2:
                option = "0_2"
            if 0.2 < float(ellipticity) <= 0.3:
                option = "0_3"
            if 0.3 < float(ellipticity) <= 0.4:
                option = "0_4"
            if 0.4 < float(ellipticity) <= 0.5:
                option = "0_5"
            if 0.5 < float(ellipticity) <= 0.6:
                option = "0_6"
            if 0.6 < float(ellipticity) <= 0.7:
                option = "0_7"
            if 0.7 < float(ellipticity) <= 0.8:
                option = "0_8"
            if 0.8 < float(ellipticity) <= 0.9:
                option = "0_9"
            if 0.9 < float(ellipticity) <= 1:
                option = "1"
        length = detection["major_axis_length"]
        if float(length)>0.0:
            obrazek = frame_content.encode('ascii')
            adres = start_path + "/images/ellipticity2/" + str(option) + "/"
            os.makedirs(adres, exist_ok=True)
            with open(adres +str(length)+"_"+ str(id) + ".png", "wb") as fh:
                fh.write(base64.decodebytes(obrazek))

def main():
   read_file()
   read_file("bad")
   soldity()
   ellipticity()

if __name__ == '__main__':
   main()
