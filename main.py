import numpy as np
from matplotlib import pyplot as plt
from matplotlib import path as mpath
from matplotlib import animation


class Tiger:
    def __init__(self, x, y, a, b, rot):
        # parameters
        self._xpos = x
        self._ypos = y
        self._a = a
        self._b = b
        self._rot = rot
        self._vector = np.array([-np.sin(self._rot), -np.cos(self._rot)])

        # triangle vertices
        self.h = np.sqrt(self._a**2-(self._b/2)**2)
        p1x = self._xpos
        p2x = (self._xpos - 0.5 * self._b)
        p3x = (self._xpos + 0.5 * self._b)
        p1y = (self._ypos + 0.7 * self.h)
        p2y = (self._ypos - 0.3 * self.h)
        p3y = p2y

        self._colx = p1x
        self._coly = p1y - 0.3 * self.h

        # rotation
        self._p1x, self._p1y = (p1x - self._xpos) * np.cos(self._rot) + (p1y - self._ypos) * np.sin(self._rot) + self._xpos, \
                               -(p1x - self._xpos) * np.sin(self._rot) + (p1y-self._ypos) * np.cos(self._rot) + self._ypos
        self._p2x, self._p2y = (p2x - self._xpos) * np.cos(self._rot) + (p2y - self._ypos) * np.sin(self._rot) + self._xpos, \
                               -(p2x - self._xpos) * np.sin(self._rot) + (p2y-self._ypos) * np.cos(self._rot) + self._ypos
        self._p3x, self._p3y = (p3x - self._xpos) * np.cos(self._rot) + (p3y - self._ypos) * np.sin(self._rot) + self._xpos, \
                               -(p3x - self._xpos) * np.sin(self._rot) + (p3y-self._ypos) * np.cos(self._rot) + self._ypos
        self._colx, self._coly = (self._colx - self._xpos) * np.cos(self._rot) + (self._coly - self._ypos) * np.sin(self._rot) + self._xpos, \
                               -(self._colx - self._xpos) * np.sin(self._rot) + (self._coly-self._ypos) * np.cos(self._rot) + self._ypos

    def getx(self):
        return self._xpos

    def gety(self):
        return self._ypos

    def getx_points(self):
        return self._p1x, self._p2x, self._p3x

    def gety_points(self):
        return self._p1y, self._p2y, self._p3y

    def get_triangle(self):
        return [[self._p1x, self._p1y], [self._p2x, self._p2y], [self._p3x, self._p3y]]

    def move(self):
        collision = False
        # collisions line
        y1 = fenceTigerListY[0:-1]
        y2 = fenceTigerListY[1:]
        x1 = fenceTigerListX[0:-1]
        x2 = fenceTigerListX[1:]
        denominator = ((self._p3y-self._coly)*(x2-x1) - (self._p3x-self._colx)*(y2-y1))
        nom1 = ((self._p3x-self._colx)*(y1-self._coly) - (self._p3y-self._coly)*(x1-self._colx))
        nom2 = ((x2 - x1) * (y1 - self._coly) - (y2 - y1) * (x1 - self._colx))
        nom1 = np.where(denominator == 0, 0, nom1)
        nom2 = np.where(denominator == 0, 0, nom2)
        denominator = np.where(denominator == 0, 1, denominator)
        uA = nom1 / denominator
        uB = nom2 / denominator
        for i in range(len(uA)):
            if (uA[i] >= 0 and uA[i] <= 1 and uB[i] >= 0 and uB[i] <= 1):
                collision = True

        if collision==False:
            denominator = ((self._p2y-self._coly)*(x2-x1) - (self._p2x - self._colx)*(y2-y1))
            nom1 = ((self._p2x-self._colx)*(y1-self._coly) - (self._p2y-self._coly)*(x1-self._colx))
            nom2 = ((x2 - x1) * (y1 - self._coly) - (y2 - y1) * (x1 - self._colx))
            nom1 = np.where(denominator == 0, 0, nom1)
            nom2 = np.where(denominator == 0, 0, nom2)
            denominator = np.where(denominator == 0, 1, denominator)
            uA = nom1 / denominator
            uB = nom2 / denominator
            for i in range(len(uA)):
                if (uA[i] >= 0 and uA[i] <= 1 and uB[i] >= 0 and uB[i] <= 1):
                    collision = True

        # rotate tiger when collision
        if self._p3y >= surface_size or self._p3y <=0 or self._p3x >= surface_size or self._p3x <=0\
                or self._p2y >= surface_size or self._p2y <=0 or self._p2x >= surface_size or self._p2x <=0\
                or collision:
            self.change_direction()

        self._xpos += self._vector[0]
        self._ypos += self._vector[1]
        self._p1x += self._vector[0]
        self._p1y += self._vector[1]
        self._p2x += self._vector[0]
        self._p2y += self._vector[1]
        self._p3x += self._vector[0]
        self._p3y += self._vector[1]
        self._colx += self._vector[0]
        self._coly += self._vector[1]

    def change_direction(self):
        self._vector = -self._vector
        self._p1x, self._p1y = 2 * self._colx - self._p1x, 2 * self._coly - self._p1y
        self._p2x, self._p2y = 2 * self._colx - self._p2x, 2 * self._coly - self._p2y
        self._p3x, self._p3y = 2 * self._colx - self._p3x, 2 * self._coly - self._p3y
        self._xpos, self._ypos = 2 * self._colx - self._xpos, 2 * self._coly - self._ypos

# first variant jarvis algorithm
def jarvis_algorithm():
    top_point_index = np.argmax(yTigerArray)
    bottom_point_index = np.argmin(yTigerArray)
    reference_point_index = top_point_index
    fence_index_list = []
    fence_index_list.append(top_point_index)
    top_flag = True
    continue_flag = True

    while(continue_flag):
        if top_flag:
            angle_list = np.arctan2(yTigerArray - yTigerArray[reference_point_index],
                                    xTigerArray - xTigerArray[reference_point_index])
        else:
            angle_list = -np.arctan2(yTigerArray - yTigerArray[reference_point_index],
                                     -xTigerArray + xTigerArray[reference_point_index])

        min_angle_index = np.argmin(angle_list)
        fence_index_list.append(min_angle_index)
        reference_point_index = min_angle_index
        if reference_point_index == bottom_point_index:
            top_flag = False
        elif reference_point_index == top_point_index:
            continue_flag = False
    return fence_index_list

# second variant jarvis algorithm
def new_jarvis():
    bot_point_index = np.argmin(yTigerArray)
    reference_point_index = bot_point_index
    previous_x = -100
    previous_y = yTigerArray[bot_point_index]
    fence_index_list = []
    fence_index_list.append(bot_point_index)
    continue_flag = True
    while(continue_flag):
        angles = np.arctan2(previous_y - yTigerArray[reference_point_index], previous_x - xTigerArray[reference_point_index]) - \
        np.arctan2(yTigerArray[reference_point_index]-yTigerArray, xTigerArray[reference_point_index] - xTigerArray)
        angles = np.where(angles < 0, angles + 2*np.pi, angles)
        max_angle = np.argmax(angles)
        fence_index_list.append(max_angle)
        previous_x = xTigerArray[reference_point_index]
        previous_y = yTigerArray[reference_point_index]
        reference_point_index = max_angle
        if reference_point_index == bot_point_index:
            continue_flag = False

    return fence_index_list


def animate_frame(i):
    global reference_point_index
    global previous_x
    global previous_y
    global continueFlag
    global fenceTigerListX
    global fenceTigerListY
    global fence_index_list

    # actual tigers position
    xTigerList = [t.getx_points() for t in tigerList]
    yTigerList = [t.gety_points() for t in tigerList]
    xTigerArray = np.array([x for sublist in xTigerList for x in sublist])
    yTigerArray = np.array([y for sublist in yTigerList for y in sublist])

    # fence polygon
    poly_list = []

    if continueFlag:
        are_in = True

        for i in range(len(fenceTigerListX)):
            poly_list.append([fenceTigerListX[i], fenceTigerListY[i]])

        poly_path = mpath.Path(np.array(poly_list))

        # checking tigers in fence
        for t in tigerList:
            are_in = are_in*poly_path.contains_point([t._xpos, t._ypos])

        if are_in:
            continueFlag = False
            fenceTigerListX = np.append(fenceTigerListX, fenceTigerListX[0])
            fenceTigerListY = np.append(fenceTigerListY, fenceTigerListY[0])

    if continueFlag:
        # jarvis step
        angles = np.arctan2(yTigerArray - fenceTigerListY[-1],
                            xTigerArray - fenceTigerListX[-1]) - np.arctan2(
            previous_y - yTigerArray[reference_point_index], previous_x - xTigerArray[reference_point_index])
        angles = np.where(angles < 0, angles + 2 * np.pi, angles)
        max_angle = np.argmax(angles)

        # collide points
        fence_index_list.append(max_angle)
        fenceTigerListX = np.append(fenceTigerListX, xTigerArray[fence_index_list[-1]])
        fenceTigerListY = np.append(fenceTigerListY, yTigerArray[fence_index_list[-1]])
        previous_x = fenceTigerListX[-2]
        previous_y = fenceTigerListY[-2]
        reference_point_index = max_angle

    for t in tigerList:
        t.move()

    # if to long try again
    if len(fenceTigerListX) > 25 and continueFlag:
        bot_point_index = np.argmin(yTigerArray)
        reference_point_index = bot_point_index
        previous_x = -100
        previous_y = yTigerArray[bot_point_index]
        fence_index_list = []
        fence_index_list.append(bot_point_index)
        fenceTigerListX = np.take(xTigerArray, fence_index_list)
        fenceTigerListY = np.take(yTigerArray, fence_index_list)

    fencePlot.set_data(fenceTigerListX, fenceTigerListY)

    triangles = [t.get_triangle() for t in tigerList]

    for i, tr in enumerate(triangles):
        trianglesPlot[i].set_xy(tr)
    tigerPlot.set_data([t.getx() for t in tigerList], [t.gety() for t in tigerList])
    # colPlot.set_data([t._colx for t in tigerList], [t._coly for t in tigerList])


if __name__ == '__main__':
    # initial parameters
    number_of_points = 20
    surface_size = 100
    tigerSize = 5

    # random tigers generation
    tigerList = [Tiger(np.random.uniform(0, surface_size), np.random.uniform(0, surface_size),
                       np.random.uniform(2.5, 5), np.random.uniform(1, 2.5), np.random.uniform(0, np.pi*2))
                 for i in range(number_of_points)]
    # triangle lists
    yTigerList = [t.gety_points() for t in tigerList]    # triangle
    yTigerArray = np.array([y for sublist in yTigerList for y in sublist])
    xTigerList = [t.getx_points() for t in tigerList]    # triangle
    xTigerArray = np.array([x for sublist in xTigerList for x in sublist])

    topPointIndex = np.argmax(yTigerArray)
    bottomPointIndex = np.argmin(yTigerArray)
    referencePointIndex = topPointIndex

    # fence_index_list = jarvis_algorithm()
    # fenceIndexList = new_jarvis()

    # to animation initial
    bot_point_index = np.argmin(yTigerArray)
    reference_point_index = bot_point_index
    previous_x = -100
    previous_y = yTigerArray[bot_point_index]
    fence_index_list = []
    fence_index_list.append(bot_point_index)
    continueFlag = True

    # fence lists
    fenceTigerListX = np.take(xTigerArray, fence_index_list)
    fenceTigerListY = np.take(yTigerArray, fence_index_list)

    # plot
    fig, ax = plt.subplots()
    tigerPlot, = plt.plot([t.getx() for t in tigerList], [t.gety() for t in tigerList], linestyle='None', marker='o', color='tab:orange', markersize=1)
    fencePlot, = plt.plot(fenceTigerListX, fenceTigerListY, color='k', marker='o', markersize=2)
    moatPlot, = plt.plot([0, surface_size, surface_size, 0, 0], [0, 0, surface_size, surface_size, 0], color='b')
    # colPlot, = plt.plot([t._colx for t in tigerList], [t._coly for t in tigerList], linestyle='None', marker='o', color='r', markersize=2)
    triangles = [t.get_triangle() for t in tigerList]
    plt.xlim([-5, surface_size + 5])
    plt.ylim([-5, surface_size + 5])
    trianglesPlot = []

    # triangles polygons to plot
    for tr in triangles:
        triangle = plt.Polygon(tr, fill=False, color='tab:orange')
        trianglesPlot.append(triangle)
        ax.add_patch(triangle)

    animation = animation.FuncAnimation(fig, func=animate_frame, interval=100, repeat=False, frames=1000)
    plt.show()

