import numpy as np
import random
from operator import attrgetter
from matplotlib import pyplot as plt
from matplotlib import animation


class Tiger:
    def __init__(self, x, y):
        self._xpos = x
        self._ypos = y

    def getXpos(self):
        return self._xpos

    def getYpos(self):
        return self._ypos


def animation_frame(i):
    display.append(fenceList[i])
    fencePlot.set_xdata([x.getXpos() for x in display])
    fencePlot.set_ydata([y.getYpos() for y in display])
    return fencePlot,


if __name__ == '__main__':
    numberOfPoints = 50
    surfaceSize = 100
    tigersList = [Tiger(np.random.uniform(-surfaceSize, surfaceSize), np.random.uniform(-surfaceSize, surfaceSize))
                  for i in range(numberOfPoints)]

    # xposList = [x.getXpos() for x in tigersList]
    # yposList = [y.getYpos() for y in tigersList]

    # plt.show()

    # Jarvis
    # startPoint = np.argmin(yposList)
    # stopPoint = np.argmax(yposList)
    startPointIndex = tigersList.index(max(tigersList, key=attrgetter('_ypos')))
    stopPointIndex = tigersList.index(min(tigersList, key=attrgetter('_ypos')))
    referencePointIndex = startPointIndex
    continueFlag = True
    fenceIndexes = [startPointIndex]
    sign = True    # orientation
    while(continueFlag):
        if sign:
            angleList = [np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), (t.getXpos() - tigersList[referencePointIndex].getXpos()))
                         for t in tigersList]
        else:
            angleList = [-np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), -t.getXpos() + tigersList[referencePointIndex].getXpos())
                         for t in tigersList]
        minAngleIndex = np.argmin(angleList)
        fenceIndexes.append(minAngleIndex)
        referencePointIndex = minAngleIndex
        if referencePointIndex == stopPointIndex:
            sign = False
        elif referencePointIndex == startPointIndex:
            continueFlag = False
    # left side of the fence
    # while (referencePointIndex != stopPointIndex):
    #     angleList = [np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), t.getXpos()-tigersList[referencePointIndex].getXpos())
    #                  for t in tigersList]
    #     minAngleIndex = np.argmin(angleList)
    #     fenceIndexes.append(minAngleIndex)
    #     referencePointIndex = minAngleIndex
    #
    # # right side of the fence
    # # referencePointIndex = stopPointIndex
    # while (referencePointIndex != startPointIndex):
    #     angleList = [-np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), -t.getXpos() + tigersList[referencePointIndex].getXpos())
    #                  for t in tigersList]
    #     # angleList.remove(0.0)
    #     minAngleIndex = np.argmin(angleList)
    #     fenceIndexes.append(minAngleIndex)
    #     referencePointIndex = minAngleIndex

    # while(continueFlag):
    #     if sign:
    #         angleList = [np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), (t.getXpos() - tigersList[referencePointIndex].getXpos()))
    #                      for t in tigersList]
    #     else:
    #         angleList = [-np.arctan2(t.getYpos()-tigersList[referencePointIndex].getYpos(), -t.getXpos() + tigersList[referencePointIndex].getXpos())
    #                      for t in tigersList]
    #     minAngleIndex = np.argmin(angleList)
    #     fenceIndexes.append(minAngleIndex)
    #     referencePointIndex = minAngleIndex
    #     if referencePointIndex == stopPointIndex:
    #         sign = False
    #     elif referencePointIndex == startPointIndex:
    #         continueFlag = False

    fig, ax = plt.subplots()
    tigerPlot, = ax.plot([x.getXpos() for x in tigersList], [y.getYpos() for y in tigersList], linestyle='None', color='tab:orange', marker='o')
    fenceList = np.take(tigersList, fenceIndexes)
    display = []
    fencePlot, = ax.plot(0, 0)
    animation = animation.FuncAnimation(fig, func=animation_frame, frames=len(fenceList), interval=500, repeat=False)
    # fencePlot, = ax.plot([x.getXpos() for x in fenceList], [y.getYpos() for y in fenceList])
    plt.show()




