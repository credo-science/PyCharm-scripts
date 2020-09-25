"""
if you want install credo_cf from your computer use:
pip install -e /your/path/with/package
i.e
pip install -e /media/CREDO1/Api/Skrypty/CREDO_freamwork/credo-classify-framework/

Aktualizacja 13.08.2020
"""
from credo_cf.commons.grouping import group_by_timestamp_division
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



home = os.path.dirname(os.path.abspath(__file__))+'/'
string = "detections_analysis/data_set/"#part path with name project
back_to_main_path = home[:-len(string)]

scala = "LA"#grayscale we can use also LA and RGB
save_folder = 'data_save/'+string
name_data_set = "CDS_001"
save_path = back_to_main_path+save_folder+name_data_set+"/"
file_end_read = 'file_analysis_completed.txt'

raw_data_set = "raw_dev/"#we read from raw_dev
detections_path = back_to_main_path+save_folder+raw_data_set

def start_analyze(current_file,device_id,year,file_name):
   print(current_file)
   try:
      with open(current_file) as json_file:
         json_load = json.load(json_file)



      number  =   10
      time    =   60000
      """
      too_often(detections,number,time)
      detections  -   dict with detection in one device
      number          -   maximum number of detections over time
      time       -   time window in milliseconds (1s = 1000)
      """

      list_detections = []
      for detection in json_load['detections']:

         records = astropy_analyze(detection)
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
      #print("start save")

      part_of_save = device_id+"/"+year+"/"
      prepare_to_save(yes_no_gray, "too_often", part_of_save,file_name)
      prepare_to_save(good_no_gray, "good", part_of_save,file_name)
      prepare_to_save(bad_no_gray, "bad", part_of_save,file_name)

      f = open(save_path+device_id+"/"+file_end_read, "a")
      f.write(file_name + ".json\n")
      f.close()
      #print("--- %s seconds ---" % (int(datetime.now().timestamp()) - int(start_time)))

   except Exception:
      traceback.print_exc()
      print("error with read file: ",file_name)
      f = open(save_path+device_id+"/error_read_file.txt", "a")
      f.write(file_name + ".json\n")
      f.close()

def prepare_to_save(detections,part,part_of_save,file_name):

   path_save = save_path +part_of_save+"/"+part+"/"

   os.makedirs(path_save, exist_ok=True)
   save_to_json(detections, path_save, file_name)

def delete_gray(detections):
   for record in detections:
      del record["gray"]
   return detections


def save_to_json(detections, path_save, file_name):
   os.makedirs(path_save, exist_ok=True)

   dict_detections = []
   if len(detections) > 0:
      print(path_save + file_name+".json")
      with open(path_save + file_name+".json", 'w') as json_file:  # zapisujemy dobre detekcje do jsona
         dictionary = {'detections': []}
         dictionary['detections'] = detections
         json.dump(dictionary, json_file, indent=4)

def check_file(device_id,year,file_name):
   path_device = save_path+device_id+"/"
   file_was_read = 0 #0 - no, 1 - yes
   if str(os.path.isfile(path_device+file_end_read)) == "True":
      f = open(path_device+file_end_read, "r")
      for line in f:
         line = line.rstrip("\n")
         if str(line) == str(file_name):
            print(line, "was readed, we don't read this file")
            file_was_read = 1
      f.close()

   return file_was_read

def main():
   '''
   file listing, sending to load_json (file_name),
   we only receive those detections that have the "visible" state
   '''

   list_device_id = os.listdir(detections_path)

   for device_id in list_device_id:
      print(device_id, len(list_device_id))
      path_device = detections_path+device_id+"/"
      path_device_vis = path_device+"visible/"
      list_years = os.listdir(path_device_vis)
      for year in list_years:
         path_year = path_device_vis+year+"/"
         list_file = os.listdir(path_year)
         list_json_file=[]
         for file in list_file:
             if ".json" in str(file):
                list_json_file.append(file)

         numer_elements = len(list_json_file)
         if numer_elements >0:
            for json_file in range(numer_elements):#file where we have name file which files we have finished reading
              name_json = list_json_file[json_file]
              file_was_read = check_file(device_id,year,name_json)

              if file_was_read == 0:
                  current_file = path_year + list_json_file[json_file]
                  file_name=list_json_file[json_file].split(".")
                  file_name=file_name[0]# [0] - name file, [1] - ".json"
                  start_analyze(current_file,device_id,year,file_name)

if __name__ == '__main__':
    main()