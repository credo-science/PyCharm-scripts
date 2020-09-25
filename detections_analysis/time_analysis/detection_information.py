import json
from os import path
from data_tools.timestamp2utc import conver2utc

home = path.dirname(path.abspath(__file__)) + '/'

def read_detections():
    detection_path = home+"detection_examples.json"
    Dict_devices = {}
    with open(detection_path) as f:
        json_load = json.load(f)

    for record in json_load["detections"]:
        device = record["device_id"]
        id = record["id"]
        time_received = record["time_received"]
        timestamp = record["timestamp"]
        frame_content = record["frame_content"]

        if str(record["visible"]) == "True":
            if device not in Dict_devices:
                Dict_devices[device]={}
                Dict_devices[device]["detection"] = {}

            Dict_devices[device]["detection"][id] = {}

            Dict_devices[device]["detection"][id]["timestamp"] = timestamp
            Dict_devices[device]["detection"][id]["time_recived"] = time_received
            Dict_devices[device]["detection"][id]["frame_content"] = frame_content

    return Dict_devices

def print_summary(dict_devices):
    for device in dict_devices:
        number_detections = len(dict_devices[device]["detection"])
        if number_detections >1:
            print("%d,\t%d "%(device,number_detections))

def check_detection(dict_devices):
    id_devices = []
    for device in dict_devices:
        id_devices.append(device)
    id_devices.sort()

    for device in id_devices:
        for detection_id in dict_devices[device]["detection"]:
            record = dict_devices[device]["detection"][detection_id]
            timestamp =record ["timestamp"]/ 1000
            ms_timestamp=record ["timestamp"]% 1000
            time_recived = record["time_recived"] / 1000
            ms_time_recived = record["time_recived"] % 1000
            time_detection = conver2utc(timestamp,"s")#[year,mont,day,hour,minute,second,day of year
            time_recived2base = conver2utc(time_recived,"s")
            print("%d, \t%s.%d, \t%s.%d, \t%d "%(device, time_detection,ms_timestamp,time_recived2base,ms_time_recived,time_recived-timestamp))



def main():
    #read_mapping("devices")
    dict_devices = read_detections()
    print_summary(dict_devices)
    check_detection(dict_devices)



if __name__ == "__main__":
    main()