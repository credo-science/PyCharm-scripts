"""


"""

from data_tools.mapping import read_mapping
import os

from data_tools.set_timestamp import convert_to_timestamp
from data_tools.read_ping import read_ping

string = "Detections_analysis/devices/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]  # delete
start_path=back_to_main_path+"data_save/Detections_analysis/"
sumarry_path = start_path +"anti-artefact/after_filtr/summary_after_filtr/about_device.txt"

list_device=[1266, 1397, 7044, 7045, 7046, 7047, 7048,
             7050, 7571, 7600, 7752, 7927, 7928, 7968,
             8237, 8257, 8258, 8259, 8260, 8288, 8289, 8327]

info_devices = {}

def about_devices(device_detection_summary,users_devices,mapp_devices):
    fa = open(start_path + "info_devices.txt", "w")
    fa.write("id;user_id;device_type;device_model;system_version;all;too_often;bad;good;procent;time_work;deect_per_hour\n")
    for device in device_detection_summary:
        try:
            id = device
            info = mapp_devices[id]

            user_id = info['user_id']
            device_idczek = info['id']
            print(id,device_idczek,user_id)
            device_type = info['device_type']
            device_model = info['device_model']
            system_version = info['system_version']

            detection = device_detection_summary[id]
            all = detection["all"]
            too_often = detection["too_often"]
            bad= detection["bad"]
            good = detection["good"]
            procent = float(detection["procent"])

            if id in users_devices:
                time_work = users_devices[id]["ping"]/60 #time in hour
                good = int(good)
                if good>100 and time_work>100:
                    detect_per_hour = str("%.2f"%(good/time_work)).replace(".",",")
                    time_work = str("%.2f"%(time_work)).replace(".",",")
                    procent = str("%.2f"%(procent)).replace(".",",")
                    fa.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
                             % (id, user_id, device_type, device_model, system_version,all, too_often, bad, good, procent,
                                time_work, detect_per_hour))
        except:
            continue
    fa.close()

def summary_work():
    detection_devices = {}
    with open(sumarry_path) as fp:
        Lines = fp.readlines()
        for line in Lines:
            try:
                #error is in 2 last line - its line with all summary
                team_id, user_id, device_id, all, too_often, bad, good, procent = line.split(",")
                if len(device_id)<6:#we dont read first line
                    detection_devices[int(device_id)] ={}
                    detection_devices[int(device_id)]["all"] = all
                    detection_devices[int(device_id)]["too_often"] = too_often
                    detection_devices[int(device_id)]["bad"] = bad
                    detection_devices[int(device_id)]["good"] = good
                    detection_devices[int(device_id)]["procent"] = procent
                    detection_devices[int(device_id)]["user"] = user_id

            except:
                continue

    return detection_devices

def main():
    start = convert_to_timestamp(2018, 6, 13)
    stop = convert_to_timestamp(2020, 7, 13)
    users_devices = read_ping(start, stop)
    device_detection_summary = summary_work()
    mapp_devices = read_mapping("devices")

    about_devices(device_detection_summary,users_devices,mapp_devices)




if __name__ == '__main__':
    main()