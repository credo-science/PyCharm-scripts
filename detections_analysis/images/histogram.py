import cv2
import os
from matplotlib import pyplot as plt

def hist (image,path_save, name):
    plt.xlabel("value of pixel")
    plt.ylabel("frequency of events")
    plt.title("The value of the brightest pixel for the detection id: " + str(name))
    plt.hist(image.ravel(),256,[0,256])
    plt.xlim([30, 256])
    plt.ylim([0, 15])
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + name + ".png")
    plt.clf()
    plt.cla()
    plt.close()

def color_hist(image,path_save, name):
    plt.xlabel("value of pixel")
    plt.ylabel("frequency of events")
    plt.title("The value of the brightest pixel for the detection id: " + str(name))
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([image],[i],None,[256],[0,256])
        maximum = max(histr[30:])
        plt.plot(histr,color = col)
        plt.xlim([30,256])
        #plt.yscale("log")
    plt.xlim([30, 256])
    plt.ylim([0, maximum + 2])
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + name + ".png")
    plt.clf()
    plt.cla()
    plt.close()
