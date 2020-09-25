"""
Save the received detection list

Structure of dict:
detections[device_id][list of detections]
"""
import json
import os

def save_to_json(detections,path_save,file_name):
    """
    Save the received detection list
    :param detections: dict with detections
    :param path_save: where save
    :param file_name: name file to save
    Structure of dict:
detections[device_id][list of detections]
    :return: nothing, only save
    """
    os.makedirs(path_save, exist_ok=True)

    dict_detections =[]
    for device_id in detections:
        if len(detections[device_id])>0:
            for record in detections[device_id]:
                dict_detections.append(record)
    if len(dict_detections)>0:
        if ".json" not in file_name:
            adres =path_save + file_name+".json"
        else:
            adres = path_save + file_name
        with open(adres, 'w') as json_file:  # zapisujemy dobre detekcje do jsona
            dictionary = {'detections': []}
            dictionary['detections'] = dict_detections
            json.dump(dictionary, json_file, indent=4)