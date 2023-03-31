import numpy as np
import sys
import matplotlib.pyplot as plt

def getData(asFileName):
    Data = [[]]
    i = 0
    with open(asFileName, 'r') as file:
        for line in file:
            Data.append(line.split())
            i += 1
    return(Data)

def processData(anData):
    time = []
    cwnd = []
    for i in range(0, len(anData)):
        line = anData[i]
        flag = 1
        try:
            timecandidate = line[2].split("-")[0]
            cwndcandidate = line[9]
            timecandidate = float(timecandidate)
            cwndcandidate = float(cwndcandidate)
        except Exception as e:
            flag = -1
            timecandidate = -1
            cwndcandidate = -1
            #print("except", " ", e) 

        if(isinstance(timecandidate, float) and isinstance(cwndcandidate,float) and flag == 1):
            #print("ok")
            time.append(timecandidate)
            cwnd.append(cwndcandidate)
    
    #print(len(time))
    #print(len(cwnd))
    return(time,cwnd)

def plotCwnd(Cwnd,time,lsFileName):

    lsPlotName = lsFileName[0:len(lsFileName)-3]
    lsPlotName += 'png'
    print(lsPlotName)
    if(len(Cwnd) != len(time)):
        print("Size not the same")
        return()

    plt.plot(time,Cwnd)
    plt.savefig(lsPlotName)


if __name__ == '__main__':
    argv = sys.argv[1:]
    lsFileName = argv[0]
    Data = getData(lsFileName)
    time,cwnd = processData(Data)
    plotCwnd(cwnd,time,lsFileName)
