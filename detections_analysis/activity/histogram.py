"""
create histogram from summary about activity from dict in file
"""
# Library
import os
import pickle

import matplotlib.pyplot as plt
from math import sqrt


string = "Detections_analysis/activity/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
path_save=back_to_main_path+"data_save/detections_analysis/activity/"


def read_dict_detection():
    infile = infile = open(path_save+"summary", 'rb')
    Dict_detection_all = pickle.load(infile)
    infile.close()


    return Dict_detection_all

def prepere_data(Dict):
    Dict_detect = {"id_days":[],"visible": [], "unvisible": [], "all":[],"device": [], "users": [], "average":[]}
    Dict_detect_norm = {"visible": [], "unvisible": [], "device": [], "users": [],}
    i=0
    for year in Dict:
        for id_day in Dict[year]:
            i+=1
            element = Dict[year][id_day]
            Dict_detect["id_days"].append(i)
            Dict_detect["visible"].append(element["visible"])
            Dict_detect["unvisible"].append(element["unvisible"])
            Dict_detect["device"].append(element["device"])
            Dict_detect["users"].append(element["users"])
            all = element["visible"] + element["unvisible"]
            Dict_detect["all"].append(all)

            if element["visible"]>0:
                Dict_detect["average"].append(element["visible"]/element["device"])
                Dict_detect_norm["visible"].append(element["visible"] / all)
                Dict_detect_norm["unvisible"].append(element["unvisible"] / all)
                Dict_detect_norm["device"].append(element["visible"] / element["device"])
                Dict_detect_norm["users"].append(element["visible"] / element["users"])
            else:
                Dict_detect["average"].append(0)
                Dict_detect_norm["visible"].append(0)
                Dict_detect_norm["unvisible"].append(0)
                Dict_detect_norm["device"].append(0)
                Dict_detect_norm["users"].append(0)




    return Dict_detect,Dict_detect_norm

def print_plot_for_all(Dict):
    """
    Create plot with muons histogram for all devices.
    At the beginning, we check each day of the year if there were any detections,
    if they were, we add to the list of elements for plot.
    :return: only create and save plot
    """
    Dict_detect,Dict_detect_norm = prepere_data(Dict)
    id_days = Dict_detect["id_days"]
    visible = Dict_detect["visible"]
    unvisible = Dict_detect["unvisible"]
    device = Dict_detect["device"]
    users = Dict_detect["users"]
    average = Dict_detect["average"]
    all = Dict_detect["all"]

    visible_norm = Dict_detect_norm["visible"]
    unvisible_norm = Dict_detect_norm["unvisible"]
    device_norm = Dict_detect_norm["device"]#detect for device
    users_norm = Dict_detect_norm["users"]#detect for users

    binsy = id_days
    #ALL Category (dot,worms,line)
    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    ax2 = ax1.twinx()

    #ax1.plot(binsy, all, "b--", label="all")
    ax1.plot(binsy, visible, "g--", label="visible: "+str(sum(visible)))
    ax2.plot(binsy, device, "k-", label="device")
    plt.title("Daily activity in detecting detection days,year: " + str("2018-2020"))
    ax1.set_ylabel('Number of detections')
    ax2.set_ylabel('Number of devices')
    ax1.set_xlabel('Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend(loc=2)
    ax2.legend(loc = 1)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/detection.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    fig, ax1 = plt.subplots(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    ax2 = ax1.twinx()

    #ax1.plot(binsy, unvisible_norm, "ro", label="unvisible")
    ax1.plot(binsy, visible_norm, "-", label="visible")

    #ax2.plot(binsy, device, "b.", label="device")
    plt.title("Daily activity in detecting detection days,year: " + str("2018-2020"))
    ax1.set_ylabel('Number of detections - norm')
    #ax2.set_ylabel('Number of devices')
    ax1.set_xlabel('Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend(loc=1)
    #ax2.legend(loc = 1)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/detection_proc.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()


#2 pod soba
    fig, ax1 = plt.subplots(figsize=(14, 10))

    plt.subplot(211)
    plt.title("Daily activity in detecting detection days,year: " + str("2018-2020"))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.ylabel('Average number of detections per device')
    plt.plot(binsy, device_norm, "g-", label="detection/devices")
    plt.xlabel('(id) Day since 1.01.2018')
    plt.grid(True)
    plt.subplot(212)
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.plot(binsy, users_norm, "k-", label="detection/users")

    plt.ylabel('Average number of detections per users')
    plt.xlabel('(id) Day since 1.01.2018')
    plt.grid(True)
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/detection_norm.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    fig, ax1 = plt.subplots(figsize=(12, 10))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    ax1.plot(binsy, device, "k--", label="device")
    ax1.plot(binsy, users, "b--", label="users")
    plt.title("Daily activity in detecting detection days,year: " + str("2018-2020"))
    ax1.set_ylabel('Number device or users')
    ax1.set_xlabel('(id) Day since 1.01.2018')
    ax1.grid(True)
    ax1.legend()
    os.makedirs(path_save , exist_ok=True)
    plt.savefig(path_save+ "/device_users.png", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(figsize=(12, 7))
    xposition = [366, 731]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.plot(binsy, visible_norm, "g--", label="visible: "+str(sum(visible)))
    plt.plot(binsy, unvisible_norm, "r--", label="unvisible: "+str(sum(unvisible)))
    plt.title("Daily activity in detecting detection days,year: " + str("2018-2020"))
    plt.ylabel('Number of detections - normalize')
    plt.xlabel('(id) Day since 1.01.2018')
    plt.grid(True)
    plt.legend(loc=2)
    os.makedirs(path_save, exist_ok=True)
    plt.savefig(path_save + "/visible_norm.png",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()



def main():
    Dict= read_dict_detection()
    print_plot_for_all(Dict)
    print (Dict)

if __name__ == '__main__':
    main()