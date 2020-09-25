from data_tools.read_ping import return_timestamps,read_ping

def check_ping(start :int,stop :int):

    dict=return_timestamps(start, stop)
    dict2 = read_ping(start, stop)

    fa = open("device_ping.txt", "w")
    for id in range (50000):
        if id in dict2:
            if dict2[id]["ping"]>0:
                fa.write("%d\n%s\n%s\n\n"%(id,dict[id],dict2[id]))
    fa.close()


def main():
    start = 1591999200
    stop = 1592092800
    check_ping(start,stop)




if __name__ == "__main__":
    main()
