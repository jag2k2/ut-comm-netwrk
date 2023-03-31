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

        if(isinstance(timecandidate, float) and isinstance(cwndcandidate,float) and flag == 1):
            time.append(timecandidate)
            cwnd.append(cwndcandidate)
    
    return(time,cwnd)

def plotCwnd(MasterCwnd, MasterTime, PlotTitles, numofPlots, PlotName):

    fig = plt.figure()
    x = np.linspace(0, 2, 100)
    fig, ax = plt.subplots()
    ax.plot(x, x, label='linear')
    ax.plot(x, x**2, label='quadratic')
    ax.plot(x, x**3, label='cubic')
    ax.set_xlabel('x label name')
    ax.set_ylabel('y label name')
    ax.set_title("My Plot")
    ax.legend()

    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_xlabel('time')
    ax.set_ylabel('CWND (KBytes)')
    for i in range(0, int(numofPlots)):
        ax.plot(MasterTime[i], MasterCwnd[i], label = PlotTitles[i])
    ax.set_title(PlotName[0:len(PlotName)-4])
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
    PlotTitles = []
    i = 0
    while(i < 2*int(numofPlots)):
        Data = getData(argv[i+2])
        i += 1
        PltName = argv[i+2]
        i += 1
        time,cwnd = processData(Data)
        MasterTime += [time]
        MasterCwnd += [cwnd]
        PlotTitles += [PltName]
        
    plotCwnd(MasterCwnd, MasterTime, PlotTitles, numofPlots, PlotName)
    