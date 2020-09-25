"""
Skrypt to create one image with: orginal image and histogram of brightest (value pixels)
you can add hostogram with color mask - but its not god viev
"""
import imageio
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import os
import cv2

SMALL_SIZE = 12
MEDIUM_SIZE = 15
BIGGER_SIZE = 17

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure titl

path = "/media/slawekstu/CREDO1/Api/Skrypty/pyCharm/data_save/detections_analysis/images/examples/todo/"
path_save = "/media/slawekstu/CREDO1/Api/Skrypty/pyCharm/data_save/detections_analysis/images/examples/done/"
def print_images(img_detections,title):
    name = str(img_detections).split(".")
    format = name[1]
    name = name[0]#i.e good2
    type = name[:-1]#good
    image = imageio.imread(path +img_detections)

    fig = plt.figure(figsize=(17, 5))#,linewidth=10, edgecolor="#04253a")#13,6
    gs = gridspec.GridSpec(1, 2,width_ratios=[1,2])#podział 0.3 do 0.6
    fig.suptitle(title, fontsize=24, fontweight='bold')
    fig.subplots_adjust(hspace=0.5, wspace=0.3,top=0.88)

    # visualization of selected cosmic particle exposition
    ax = fig.add_subplot(gs[0])

    #plt.xlabel("X coordinate")
    #plt.ylabel("Y coordinate")
    plt.axis('off')
    #plt.title("Detection image: "+str(type)+" candidate ")

    ax.imshow(image)

    # histogram
    ax = fig.add_subplot(gs[1])
    #ax = fig.add_subplot(1, 3, 2)
    gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
    gray = gray(image)#bez tego jest w barwach koloru
    ax.hist(gray.ravel(),255,[0,256],color="orange")
    #plt.hist(image.ravel(), 256, [0, 256])
    ax.grid()
    plt.yscale("log")
    plt.xlabel("Brightness value (0-255)")
    plt.ylabel("Count (log scale)")
    #plt.title("Value of the brightest - grayscale")

    #color-mask
    #ax = fig.add_subplot(1, 3, 3)
    #plt.xlabel("Value of pixel (0-256)")
    #plt.ylabel("Frequency of occurrence of values")
    #plt.title("The value of the brightest pixel - color mask")
    #color = ('r','g','b')
    #for i,col in enumerate(color):
    #    histr = cv2.calcHist([image],[i],None,[256],[0,256])
    #    maximum = max(histr[30:])
    #    plt.plot(histr,color = col)
    #    ax.grid()
    #    plt.yscale("log")
    os.makedirs(path_save, exist_ok=True)
    #plt.tight_layout()
    plt.savefig(path_save + name+"_conv."+format, pad_inches = 0.1,bbox_inches='tight')#,edgecolor=fig.get_edgecolor())#,bbox_inches='tight'
    plt.clf()
    plt.cla()
    plt.close()


def main():
    list_image = os.listdir(path)
    lista = ["(a)","(b)","(c)","(d)","(e)"]
    i=0
    for img_detections in list_image:
        l = i%5
        i+=1
        title = lista[l]
        print_images(img_detections,title)

if __name__ == "__main__":
    main()
