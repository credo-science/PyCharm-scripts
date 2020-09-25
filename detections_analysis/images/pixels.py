import json
from os import path
from images.histogram import *
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import cv2


home = path.dirname(path.abspath(__file__)) + '/'

string = "Detections_analysis/images/"
back_to_main_path = home[:-len(string)]
save_folder = 'data_save/'+string
save_path = back_to_main_path+save_folder+"2/"

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


def search_max_pixels(dict_devices):
    max_pixels_all = []
    for device in dict_devices:
        max_pixels = []
        if len(dict_devices[device]["detection"])>1:
            for detection_id in dict_devices[device]["detection"]:
                record = dict_devices[device]["detection"][detection_id]

                img = record["frame_content"]
                im_bytes = base64.b64decode(img)
                img = pil = Image.open(BytesIO(im_bytes))
                imgs = np.asarray(pil.convert('L'))

                max_pixels.append(np.max(imgs))
                max_pixels_all.append(np.max(imgs))
            histogram(max_pixels,save_path + "max_average/",device)
    histogram(max_pixels_all, save_path + "max_average/", "all")


def histogram(value, path_saves,name):
    plt.xlabel("value of pixel")
    plt.ylabel("frequency of events")
    plt.title("The value of the brightest pixel for the device: " + str(name))

    plt.hist(value, 256, [0, 256], label = "number of detections: "+str(len(value)))
    plt.legend()
    os.makedirs(path_saves, exist_ok=True)
    plt.yscale("log")
    plt.savefig(path_saves + str(name) + ".png")

    plt.clf()
    plt.cla()
    plt.close()


def value_of_pixels(dict_devices):#MAŁO CIEKAWE
    for device in dict_devices:
        Dict_image = {}
        for detection_id in dict_devices[device]["detection"]:
            Dict_image[detection_id] ={}
            record = dict_devices[device]["detection"][detection_id]

            img = record["frame_content"]
            im_bytes = base64.b64decode(img)
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            name = str(detection_id)+".png"

            path_save = save_path+"pixels/"+str(device)+"/"
            hist(img, path_save, name)
            color_hist(img, path_save+ "color/", name)

def main():
    dict_devices = read_detections()
    search_max_pixels(dict_devices)
    value_of_pixels(dict_devices)

if __name__ == "__main__":
    main()