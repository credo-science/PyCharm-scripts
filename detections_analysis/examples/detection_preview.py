from data_tools.image import print_img
import os
import json

string = "Detections_analysis/examples/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
main_data_path = back_to_main_path+"data_save/preview/"
detections_path = back_to_main_path+"data_save/Detections_analysis/anti-artefact/LA/good/"


def list_path(adres):
    """
    Sprawdzmy jakie mamy pliki w podanym adresie
    :param adres: ścieżka do katalogu z plikami
    :return: lista plików
    """
    list_file = os.listdir(adres)
    return list_file

def read_json(detections_path,list_file):
    """
    Wczytanie plików, podział detekcji na urządzenia
    :param detections_path: główny folder z detekcjami,
    :param list_file: lista plików w danym folderze, parametry z listą łączymy z detections_path
    :return: aktualizacja słownika detekcji
    """
    max = 1
    current = 0
    for file_name in list_file:
        if current<max:
            adres = detections_path+file_name
            with open(adres) as f:
                json_load = json.load(f)
            for record in json_load["detections"]:
                device_id = int(record["device_id"])
                timestamp = int(record["timestamp"])
                obrazek = record["frame_content"]
                adres = main_data_path+str(device_id)+"/"
                print_img(obrazek,str(timestamp),adres,1)
            current+=1


def main():
    list_file = list_path(detections_path)
    read_json(detections_path,list_file)



if __name__ == '__main__':
    main()