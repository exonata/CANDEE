import threading
import time
import csv
import sys


# file setup
filelocation = '\CANDEE\logs\ '
filename = "testfile.csv"
print(filename)
fileheader = ['Time','DIN1','DIN2','DIN3','DIN4','DIN5','DIN6','DIN7','DIN8','DOUT0','DOUT1','DOUT2']
#,DOUT3,AIN0,AIN1,AIN2,AIN3,AOUT0,AOUT1,AOUT2,AOUT3]


raw_data = ['TIME:\t    5344|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.178901 0.211136 0.255458 0.173260|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5344|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.189377 0.226447 0.253846 0.209524|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5344|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.180513 0.213553 0.263516 0.178095|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5345|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.190989 0.229670 0.260293 0.213553|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5345|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.177289 0.208718 0.254652 0.171648|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5345|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.195824 0.235311 0.272381 0.220000|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5345|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.177289 0.208718 0.258681 0.171648|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5345|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.183736 0.299780 0.261099 0.215971|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5346|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.180513 0.213553 0.257875 0.176484|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5346|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.193407 0.232088 0.262711 0.216777|AOUTPUTS:\t0.000000|*\n',
            'TIME:\t    5346|DINPUTS:\t000110000|DOUTPUTS:\t00000000|AINPUTS:\t0.178901 0.211136 0.256264 0.173260|AOUTPUTS:\t0.000000|*\n']


def init_logFile(filename, fileheader):
    f = open('testfile.csv', 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Time','DIN1','DIN2','DIN3','DIN4','DIN5','DIN6','DIN7','DIN8','DOUT0','DOUT1','DOUT2') )
    finally:
        f.close()
    return f


def data_handler(raw_data):
    TIME = []
    DINPUTS = []
    DOUTPUTS = []
    AINPUTS = []
    AOUTPUTS = []

    for i in range(len(raw_data)):
        data = raw_data[i].split('|')
        TIME.append(data[0].split("\t"))
        DINPUTS.append(data[1].split("\t"))
        DOUTPUTS.append(data[2].split("\t"))
        AINPUTS.append(data[3].split("\t"))
        AOUTPUTS.append(data[4].split("\t"))

    return TIME, DINPUTS,  DOUTPUTS, AINPUTS, AOUTPUTS


def fileWriter(time, dinputs, douputs, ainput, aoutputs, file1):
    rows = len(time)
    file = open('testfile.csv', 'wt')
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    outputData = list(zip(time,dinputs, douputs, ainput, aoutputs))
    print(outputData)

    try:
        #for i in range(rows):
        writer.writerows(outputData)
           # print([time[i], dinputs[i], douputs[i], ainput[i], aoutputs[i]])
    finally:
        file.close()



file = init_logFile(filename, fileheader)
a, b, c, d, e = data_handler(raw_data)
fileWriter(a, b, c, d, e, file)