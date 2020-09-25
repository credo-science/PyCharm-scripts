import base64
import os
from datetime import datetime

home =os.path.dirname(os.path.abspath(__file__)) + '/'
def print_img(images,name : str = "detection_image",path_to_save: str = home,convert:int = 0):
    """

    :param image: element "frame_content" from record of detection
    :param path_to_save: path to save
    :param name - name image , use to save
    :param convert - if is 1, convert name (timestamp to datatime))
    :return: save img as png
    """
    if convert == 1:
        names =datetime.fromtimestamp(int(int(name)/1000)).strftime("%Y-%m-%d_%H_%M_%S")
        name =names+"_"+str(int(name)%1000)
    os.makedirs(path_to_save, exist_ok=True)
    obrazek = images.encode('ascii')
    adres=path_to_save+ str(name)+".png"
    print(adres)
    with open(adres, "wb") as fh:
        fh.write(base64.decodebytes(obrazek))