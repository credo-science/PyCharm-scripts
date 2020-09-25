"""
CEL: Przykładowy skrypt wzorcowy do rozpoczęcia pracy w pythonie
AUTOR: Sławomir Stuglik
OST. EDYCJA: 15.07.2020
"""
import os
import json

string = "Detections_analysis/examples/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]

main_data_path = back_to_main_path+"data_save/Detections_analysis/"
detections_path = main_data_path+"anti-artefact/after_filtr/good/"
save_path = main_data_path+"examples/"
os.makedirs(save_path, exist_ok=True)

Dict_devices = {}

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
    max = 2
    current = 0
    for file_name in list_file:
        if current<max:
            adres = detections_path+file_name
            with open(adres) as f:
                json_load = json.load(f)
            #print (json_load.keys())
            for record in json_load["detections"]:
                device_id = int(record["device_id"])
                if device_id not in Dict_devices:
                    Dict_devices[device_id] =[]
                Dict_devices[device_id].append(record)
            current+=1

def save_detections_device(path_to_save):
    """
    Zapisanie detekcji z podziałem na urządzenie jako json
    :param path_to_save: ścieżka gdzie zapisać
    :return: nic nie zwracamy, ale zapisujemy
    """
    for device_id in Dict_devices:
        with open(path_to_save + str(device_id) + ".json", 'w') as json_file:
            dictionary = {'detections': []}
            dictionary['detections'] = Dict_devices[device_id]
            json.dump(dictionary, json_file, indent=4)

def main():
    """
    FUnkcja startowa, w niej podajemy co chcemy uruchomić
    """
    list_file = list_path(detections_path)
    read_json(detections_path,list_file)
    save_detections_device(save_path)
if __name__ == '__main__':
    main()