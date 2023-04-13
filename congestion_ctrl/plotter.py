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

def getModifier(name):
    if(name == "bits/sec"): return(1/1000000)
    if(name == "Bytes" or name == "Kbits/sec"): return(1/1000)
    if(name == "KBytes" or name == "Mbits/sec"): return(1)
    if(name == "MBytes" or name == "Gbits/sec"): return(1000)
    else:
        print("Name not Found :", name)
        return(0)

def processData(anData, time_shift):
    # TODO, Add support to reive information regarding Throughput
    # TODO, Add support to change CWND data to amount of packets - looks good so far
    # TODO, Add support to do Unit Conversion - looks good so far
    pktSize = 1500
    ByteUnit = ["bytes", "KBytes", "MBytes"]
    BitUnit = ["bits/sec", "Kbits/sec", "Mbits/sec"]
    time = []
    band = []
    cwnd = []
    for i in range(0, len(anData)):
        line = anData[i]
        flag = 1
        try:
            timecandidate = line[2].split("-")[0]
            bandcandidate = line[6]
            bandUnit = line[7]
            cwndcandidate = line[9]
            cwndUnit = line[10]
            timecandidate = float(timecandidate)
            bandcandidate = float(bandcandidate) * getModifier(bandUnit)
            cwndcandidate = (1000*(float(cwndcandidate) * getModifier(cwndUnit))/pktSize)
        except Exception as e:
            flag = -1
            timecandidate = -1
            bandcandidate = -1
            cwndcandidate = -1

        if(isinstance(timecandidate, float) and isinstance(cwndcandidate,float) and flag == 1 and bandcandidate > 0 and cwndcandidate > 0):
            time.append(timecandidate + time_shift)
            band.append(bandcandidate)
            cwnd.append(cwndcandidate)
    
    return(time,cwnd,band)

# TODO Add a function that adds support to plot the throughput.

def plotThroughput(MasterTHPT, MasterTime, PlotTitles, numofPlots, PlotName):
    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_xlabel('Time')
    ax.set_ylabel('Throughput MBits/sec')
    for i in range(0, int(numofPlots)):
        ax.plot(MasterTime[i], MasterTHPT[i], label = PlotTitles[i])
    #ax.set_title(PlotName[0:len(PlotName)-4])
    ax.set_title("Throughput for Cubic Algorithm, delay = 162ms")
    ax.legend()
    plt.savefig(PlotName)
    

def plotCwnd(MasterCwnd, MasterTime, PlotTitles, numofPlots, PlotName):

    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_xlabel('Time')
    ax.set_ylabel('CWND (Packets)')
    for i in range(0, int(numofPlots)):
        ax.plot(MasterTime[i], MasterCwnd[i], label = PlotTitles[i])
    #ax.set_title(PlotName[0:len(PlotName)-4])
    ax.set_title("CWND for Cubic Algorithm, delay = 162ms")
    ax.legend()
    plt.savefig(PlotName)

if __name__ == '__main__':
    """
    usage :
    python3 plotter.py plotNameImg numOfPlots file1 file1_Title file2 file2_Title ... fileN fileN_Title
    example: 
    python3 plotter.py test1 2 file1.txt dat-1 file2.txt dat-2
    """
    argv = sys.argv[1:]

    PlotName = argv[0]
    numofPlots = argv[1]
    MasterTime = []
    MasterCwnd = []
    MasterBAND = []
    PlotTitles = []
    i = 0
    Data1 = getData(argv[2])
    PltName1 = argv[3]
    time1,cwnd1,band1 = processData(Data1,0)
    MasterTime += [time1]
    MasterCwnd += [cwnd1]
    MasterBAND += [band1]
    PlotTitles += [PltName1]
    Data2 = getData(argv[4])
    PltName2 = argv[5]
    time2,cwnd2,band2 = processData(Data2,100)
    MasterTime += [time2]
    MasterCwnd += [cwnd2]
    MasterBAND += [band2]
    PlotTitles += [PltName2]
        
    plotCwnd(MasterCwnd, MasterTime, PlotTitles, numofPlots, "Cubic-CWND-162")
    plotThroughput(MasterBAND, MasterTime, PlotTitles, numofPlots, "Cubic-THPT-162")
