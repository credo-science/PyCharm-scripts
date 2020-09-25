"""
if you want install credo_cf from your computer use:
pip install -e /your/path/with/package
i.e
pip install -e /media/CREDO1/Api/Skrypty/CREDO_freamwork/credo-classify-framework/

Aktualizacja 13.08.2020
"""
from credo_cf.commons.grouping import group_by_device_id
from credo_cf.image.gray import convert_to_gray_scale
from credo_cf.io.load_write import load_json
from credo_cf.io.io_utils import progress_load_filter

from credo_cf.classification.artifact.too_often import too_often
from credo_cf.classification.artifact.too_bright import too_bright

import json
import os
from datetime import datetime
from data_tools.astropy_analysis import astropy_analyze
import traceback
start_time = datetime.now().timestamp()

detections_path = '/media/slawekstu/CREDO1/Api/credo-data-export/detections/'
home = os.path.dirname(os.path.abspath(__file__))+'/'
string = "detections_analysis/anti-artefact/"#part path with name project
back_to_main_path = home[:-len(string)]


scala = "LA"#"default"#grayscale - default = (1,1,1), we can use also LA and RGB
save_folder = 'data_save/'+string
save_path = back_to_main_path+save_folder+scala+"/"
file_end_read = save_path + 'file_analysis_completed.txt'


def start_analyze(current_file,file_name):
   Dict_detection_too_offten = {}
   Dict_detection_good = {}  # Dict for good detection after filtr
   Dict_detection_bad = {}  # Dict for bad graphic detection after filtr
   print(file_name)
   try:
      obj_list,count = load_json(current_file,progress_load_filter)

      """
      Checking the specific detection and one of its features:
      print(detection[3]["device_id"])
      """

      by_device_id = group_by_device_id(obj_list)
      """
       Checking number detections one device in our file:
      for key in by_device_id:
            print(key,len(by_device_id[key])))
      """

      number  =   10
      time    =   60000
      """
      too_often(detections,number,time)
      detections  -   dict with detection in one device
      number          -   maximum number of detections over time
      time       -   time window in milliseconds (1s = 1000)
      """


      for device_id, detections in by_device_id.items():
         list_detections=[]
         for record in detections:
            if str(record["visible"])=="True":
               records = astropy_analyze(record)
               record_gray = convert_to_gray_scale(records,scala)
               list_detections.append(record_gray)#nasza lista detekcji z gray - all
         yes, no = too_often(list_detections,number,time) # yes - artefact, no - detection with good time

         """
               too_bright(detections,number,time)
               detections        -   dict with good time detection in one device
               bright_pixels     -   maximum number of bright pixels on the sli
               threshold         -   the bright pixel has a brightness greater than the threshold (range 0 - 255)
         """

         good,bad =  too_bright(no,70,70)

         yes_no_gray = delete_gray(yes)
         good_no_gray = delete_gray(good)
         bad_no_gray = delete_gray(bad)
         Dict_detection_too_offten[device_id] = yes_no_gray
         Dict_detection_good[device_id]=good_no_gray
         Dict_detection_bad[device_id] = bad_no_gray
      print("start save")

      prepare_to_save(Dict_detection_too_offten, "too_often", file_name)
      prepare_to_save(Dict_detection_good, "good", file_name)
      prepare_to_save(Dict_detection_bad, "bad", file_name)

      f = open(file_end_read, "a")
      f.write(file_name + ".json\n")
      f.close()
      print("--- %s seconds ---" % (int(datetime.now().timestamp()) - int(start_time)))

   except Exception:
      traceback.print_exc()
      print("error with read file: ",file_name)
      f = open(save_path+"error_read_file", "a")
      f.write(file_name + ".json\n")
      f.close()

def prepare_to_save(detections,part,file_name):

   path_save = save_path +part+"/"

   os.makedirs(path_save, exist_ok=True)
   save_to_json(detections, path_save, file_name)

def delete_gray(detections):
   for record in detections:
      del record["gray"]
   return detections


def save_to_json(detections, path_save, file_name):
   os.makedirs(path_save, exist_ok=True)

   dict_detections = []
   for device_id in detections:
      if len(detections[device_id]) > 0:
         for record in detections[device_id]:
            dict_detections.append(record)
   if len(dict_detections) > 0:
      print(path_save + file_name+".json")
      with open(path_save + file_name+".json", 'w') as json_file:  # zapisujemy dobre detekcje do jsona
         dictionary = {'detections': []}
         dictionary['detections'] = dict_detections
         json.dump(dictionary, json_file, indent=4)

def check_file(file_name):
   file_was_read = 0 #0 - no, 1 - yes
   if str(os.path.isfile(file_end_read)) == "True":
      f = open(file_end_read, "r")
      for line in f:
         line = line.rstrip("\n")
         if str(line) == str(file_name):
            print(line, "was readed, we don't read this file")
            file_was_read = 1
      f.close()

   return file_was_read

def main():
   """
   file listing, sending to load_json (file_name),
   we only receive those detections that have the "visible" state
   """
   list_file_json = os.listdir(detections_path)

   for json_file in range(len(list_file_json)):#file where we have name file which files we have finished reading
      file_was_read = check_file(list_file_json[json_file])

      if file_was_read == 0:
         current_file = detections_path + list_file_json[json_file]
         file_name=list_file_json[json_file].split(".")
         file_name=file_name[0]# [0] - name file, [1] - ".json"
         start_analyze(current_file,file_name)

if __name__ == '__main__':
    main()