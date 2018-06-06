import pyglet
import config, cvsmr
import random
import time
import numpy as np
import cvsmgmt

def recursive_river(og_vector, vector,x,y,river_map,height_map,size_x,size_y):
    river_map[x][y] = 1

    if(x == 0 or x == size_x - 1 or y == 0 or y == size_y - 1):
        return

    highest_prob = -100
    highest_index = [0,0]

    for pot_vector in ([-1,-1],[-1.2,0],[-1,1],[0,-1.2],[0,1.2],[1,-1],[1.2,0],[1,1]):

        if(x + int(pot_vector[0]) >= 0 and x + int(pot_vector[0]) < size_x and y + int(pot_vector[1]) >= 0 and y + int(pot_vector[1]) < size_y):
            temp_prob = pot_vector[0] * vector[0] + pot_vector[1] * vector[1] - abs(height_map[x][y] - height_map[x + int(pot_vector[0])][y + int(pot_vector[1])]) + random.randrange(-1,2)/2 - height_map[x + int(pot_vector[0])][y + int(pot_vector[1])]/6 +\
                        (pot_vector[0] * og_vector[0] + pot_vector[1] * og_vector[1])/(4 + random.randrange(1,3)/2)

            if(temp_prob > highest_prob):
                highest_prob = temp_prob
                highest_index[0] = int(pot_vector[0])
                highest_index[1] = int(pot_vector[1])

    new_x = x + highest_index[0]
    new_y = y + highest_index[1]

    recursive_river(og_vector, [highest_index[0],highest_index[1]],new_x,new_y,river_map,height_map,size_x,size_y)

class road_node:
    def __init__(self, coords):
        self.coords = coords
        self.nodes = [None,None,None,None]
        self.nodes_ind = [None,None,None,None]
        self.index = 0

        self.edge = False
        self.town = False
        self.bend = True

class tactical_map(cvsmgmt.scene_object):
    def __init__(self, groupnum = 0):
        cvsmgmt.scene_object.__init__(self, groupnum)

        self.handlers[0] = True
        self.handlers[5] = True

        self.scene_translate_entry = cvsmgmt.update_entry(self.scene_translate_1, ["x","y"])

        #--------------------------------------------------------------------------------------------------------------

        self.forest_threshold = 1.2
        self.river_threshold = 0.8
        self.towns_threshold = 0.5

    def handler_leftclick(self,x,y):
        config.click_selected = self

    def handler_leftdrag(self,x,y,dx,dy):
        self.scene_translate_entry.args[0] = dx
        self.scene_translate_entry.args[1] = dy
        self.scene_translate_entry.add()

    def interpolate_height(self,x,y):
        pass

    def interpolate_forest(self, x ,y):
        pass

    def interpolate_river(self,x,y):
        pass

    def interpolate_town(self,x,y):
        pass

    def generate(self, size_x, size_y, max_height, mountains, hills, forest, river, towns, roads):
        self.size_x = size_x
        self.size_y = size_y

        self.checkbox.broad_checkbox = [0,0, size_x-1, size_y-1]

        self.max_height = max_height #note minimum max height is 6
        self.forest = forest
        self.river = river

        #Height map
        if(True):
            self.height_map = [None]*size_x
            for i in range(0,size_x):
                self.height_map[i] = [0.0]*self.size_y

            #self.height_map = np.zeros((size_x,size_y))

            #gradual
            for f in range(0,3):
                self.temp = random.randrange(0,11)-5.1
                self.temp_one = random.randrange(0, 11)-5.1


                for i in range(0,size_x):
                    for j in range(0,size_y):
                        self.height_map[i][j] += abs(float((self.temp * i + self.temp_one * j)))/(abs(self.temp*size_x)+abs(self.temp_one*size_y))*2

            #plateau ish
            if(max_height > 4 and random.randrange(0,2) == 0):

                self.i = random.randrange(0,size_x)
                self.j = random.randrange(0,size_y)
                self.height = random.randrange(0,max_height)

                self.temp = random.randrange(i,size_x)
                self.temptemp = random.randrange(j,size_y)
                for y in range(j,self.temptemp):
                    for x in range(0,int((self.temptemp-j)/2)):
                        self.height_map[random.randrange(i,self.temptemp)][y] = self.height

            #generate mountains
            if(mountains > 0):
                for g in range(0,max(int(mountains/6),1)):
                    self.direction_1 = random.randrange(0,2)
                    self.direction_2 = random.randrange(0,2)

                    self.start_x_1 = random.randrange(int(size_x * 0.3), int(size_x * 0.75))
                    self.end_y_1 = random.randrange(int(size_y * 0.3), int(size_y * 0.75))

                    self.start_x_2 = random.randrange(int(size_x * 0.3), int(size_x * 0.75))
                    self.end_y_2 = random.randrange(int(size_y * 0.3), int(size_y * 0.75))

                    self.counter = 0
                    while(self.counter <= mountains):
                        self.counter += 1

                        #first
                        if(True):
                            self.temp_y = random.randrange(self.end_y_1, int(size_y*0.9))

                            if(self.direction_1 == 1):
                                self.temp_x = random.randrange(0,max(int(self.start_x_1-(size_y-self.temp_y)*(self.start_x_1/(size_y-self.end_y_1))), int(size_x*0.3)))
                            else:
                                self.temp_x = random.randrange(min(int(self.start_x_1 + (size_y-1-self.temp_y) * ((size_x-1-self.start_x_1) / (size_y-1-self.end_y_1))), int(size_x*0.75)), size_x)

                            self.height_map[self.temp_x][self.temp_y] = max_height

                        #second
                        if(self.counter > 2):
                            self.temp_y = random.randrange(int(size_y*0.2), self.end_y_2)

                            if (self.direction_2 == 1):
                                self.temp_x = random.randrange(0, max(int(self.start_x_2 - (self.temp_y) * (self.start_x_2 / self.end_y_2)),int(size_y*0.3)))
                            else:
                                self.temp_x = random.randrange(min(int(self.start_x_2 + (self.temp_y) * ((size_x-1-self.start_x_2) / self.end_y_2)),int(size_y*0.75)), size_x)

                            self.height_map[self.temp_x][self.temp_y] = max_height

                        if(self.counter > 5):
                            self.height_map[random.randrange(int(size_x*0.3),int(size_x*0.6))][random.randrange(int(size_y * 0.3), int(size_y * 0.6))] = max_height

            #generate hills
            for i in range(0,hills):
                self.height_map[random.randrange(int(size_x*0.15),int(size_x*0.85))][random.randrange(int(size_y*0.15),int(size_y*0.85))] = max_height * 0.8

            #rough terrain
            for f in range(0,20):
                if (random.randrange(0, 2) == 0):
                    self.flag_hurhur = True
                else:
                    self.flag_hurhur = False

                for x in range(0, size_x-1):
                    for y in range(0, size_y-1):

                        if (self.flag_hurhur):
                            self.i = size_x - 1 - x
                            self.j = size_y - 1 - y
                        else:
                            self.i = x
                            self.j = y

                        self.temp = 0

                        for h in (-1, 0, 1):
                            for k in (-1, 0, 1):
                                try:
                                    self.temp = max(self.temp,self.height_map[self.i+h][self.j+k])
                                except:
                                    pass

                        if(self.temp > self.height_map[self.i][self.j]):
                            self.height_map[self.i][self.j] = self.temp * random.randrange(5,10) / 10

            #smoothing stage 1
            for f in range(0,10):

                if (random.randrange(0, 2) == 0):
                    self.flag_hurhur = True
                else:
                    self.flag_hurhur = False

                for x in range(0,size_x):
                    for y in range(0,size_y):
                        if (self.flag_hurhur):
                            self.i = size_x - 1 - x
                            self.j = size_y - 1 - y
                        else:
                            self.i = x
                            self.j = y

                        self.temp = 0
                        self.temp_one = max_height

                        if(self.height_map[self.i][self.j] != max_height or random.randrange(0,4) == 3):
                            for h in (-1,0,1):
                                for k in (-1,0,1):
                                    #if(self.i+h >= 0 and self.i+h < size_x and self.j+k >0 and self.j+k < size_y):
                                    try:
                                        self.temp = max(self.temp,self.height_map[self.i+h][self.j+k])
                                        self.temp_one = min(self.temp_one,self.height_map[self.i+h][self.j+k] )
                                    except:
                                        pass

                                    if(random.randrange(0,20) > 0):
                                        self.height_map[self.i][self.j] = (self.height_map[self.i][self.j]*3 + self.temp+self.temp_one)/5
                                    else:
                                        self.height_map[self.i][self.j] = self.temp

            #smoothing stage 2
            for f in range(0,4):

                if (random.randrange(0, 2) == 0):
                    self.flag_hurhur = True
                else:
                    self.flag_hurhur = False

                for x in range(0, size_x):
                    for y in range(0, size_y):

                        if (self.flag_hurhur):
                            self.i = size_x - 1 - x
                            self.j = size_y - 1 - y
                        else:
                            self.i = x
                            self.j = y

                        self.temp = 0
                        for h in (-1, 0, 1):
                            for k in (-1, 0, 1):
                                try:
                                    self.temp += self.height_map[self.i + h][self.j + k]
                                except:
                                    pass
                        self.height_map[self.i][self.j] = (self.height_map[self.i][self.j]*4 + self.temp / 9)/5

            #edge smoothing
            for f in range(1,2):

                for i in(0,size_x-1):
                    for j in range(0,size_y):
                        if(i!=0):
                            self.height_map[i][j] = (self.height_map[i-f][j] + self.height_map[i][j])/2
                        else:
                            self.height_map[i][j] = (self.height_map[i+f][j] + self.height_map[i][j])/2

                for j in(0,size_y-1):
                    for i in range(0,size_x):
                        if(j != 0):
                            self.height_map[i][j] = (self.height_map[i][j-f] + self.height_map[i][j])/2
                        else:
                            self.height_map[i][j] = (self.height_map[i][j+f] + self.height_map[i][j])/2

        #Rivers
        if(True):
            self.river_map = [None] * size_x
            for i in range(0, size_x):
                self.river_map[i] = [0.0] * self.size_y
            #self.river_map = np.zeros((size_x,size_y))

            #generate base
            if(river >0):

                for x in range(0,river):

                    self.lowest = 1000
                    self.lowest_coords = [None,None]
                    for g in range(0,15):
                        self.temp_x = random.randrange(int(size_x*0.2),int(size_x*0.7))
                        self.temp_y = random.randrange(int(size_y * 0.2), int(size_y * 0.7))
                        if(self.height_map[self.temp_x][self.temp_y] < self.lowest):
                            self.lowest = self.height_map[self.temp_x][self.temp_y]
                            self.lowest_coords = [self.temp_x,self.temp_y]

                    self.river_map[self.lowest_coords[0]][self.lowest_coords[1]] = 1

                    self.vector= [random.choice((-1,1)),random.choice((-1,0))]

                    recursive_river( [self.vector[0],self.vector[1]],[self.vector[0],self.vector[1]], self.lowest_coords[0] + self.vector[0], self.lowest_coords[1] + self.vector[1], self.river_map, self.height_map,size_x,size_y)
                    recursive_river([-1 * self.vector[0],-1 * self.vector[1]], [-1 * self.vector[0],-1 * self.vector[1]], self.lowest_coords[0] - self.vector[0], self.lowest_coords[1] - self.vector[1], self.river_map, self.height_map,size_x,size_y)

            # river smoothing
            if (river > 0):

                # rough widening
                for f in range(0, 1):
                    if (random.randrange(0, 2) == 0):
                        self.flag_hurhur = True
                    else:
                        self.flag_hurhur = False

                    for x in range(0, size_x):
                        for y in range(0, size_y):
                            if (self.flag_hurhur):
                                self.i = size_x - 1 - x
                                self.j = size_y - 1 - y
                            else:
                                self.i = x
                                self.j = y

                            if (self.river_map[self.i][self.j] < 0.9):
                                self.max = 0
                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):
                                        try:
                                            if (self.river_map[self.i + h][self.j + k] > self.max):
                                                self.max = self.river_map[self.i + h][self.j + k]
                                        except:
                                            pass

                                self.river_map[self.i][self.j] = (self.max + self.river_map[self.i][self.j]) / 2

                # randoming
                for f in range(0, 1):
                    for i in range(0, self.size_x):
                        for j in range(0, self.size_y):

                            if (self.river_map[i][j] != 1):
                                self.river_map[i][j] = self.river_map[i][j] * (random.randrange(7, 13) / 10)

                                # averaging

                # edge widening
                for f in range(0, 0):

                    for i in (0, size_x - 1):
                        for j in range(0, size_y):

                            if (self.river_map[i][j] != 1):
                                self.flag = True

                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):
                                        try:
                                            if (self.river_map[i + h][j + k] == 1 and self.flag):
                                                self.river_map[i][j] = 0.95
                                                self.flag = False
                                        except:
                                            pass

                    for j in (0, size_y - 1):
                        for i in range(0, size_x):

                            if (self.river_map[i][j] != 1):
                                self.flag = True

                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):
                                        try:
                                            if (self.river_map[i + h][j + k] == 1 and self.flag):
                                                self.river_map[i][j] = 0.95
                                                self.flag = False
                                        except:
                                            pass

                # average
                for f in range(0, river * 10 + 20):

                    if (random.randrange(0, 2) == 0):
                        self.flag_hurhur = True
                    else:
                        self.flag_hurhur = False

                    for x in range(0, size_x):
                        for y in range(0, size_y):

                            if (self.flag_hurhur):
                                self.i = size_x - 1 - x
                                self.j = size_y - 1 - y
                            else:
                                self.i = x
                                self.j = y

                            if (self.river_map[self.i][self.j] != 1):

                                self.temp = 0
                                self.count = 0

                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):
                                        if (
                                                            self.i + h > 0 and self.i + h < size_x and self.j + k > 0 and self.j + k < size_y):
                                            self.temp += self.river_map[self.i + h][self.j + k]
                                            self.count += 1

                                self.river_map[self.i][self.j] = (self.temp / self.count)

                # remove bloat
                for f in range(0, 0):

                    for i in range(0, size_x):
                        for j in range(0, size_y):

                            if (self.river_map[i][j] < self.river_threshold):
                                self.flag = True

                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):

                                        if (i + h > 0 and i + h < size_x and j + k > 0 and j + k < size_y):

                                            if (self.river_map[i + h][j + k] > self.river_threshold):
                                                self.flag = False

                                if (self.flag):
                                    self.river_map[i][j] = 0

            # height map smoothing
            if (river > 0):

                # find average
                for f in range(0, 1):
                    self.average = 0
                    self.counter = 0
                    for i in range(0, size_x):
                        for j in range(0, size_y):

                            if (self.river_map[i][j] != 0):
                                self.counter += 1
                                self.average += self.height_map[i][j]

                    if (self.counter != 0):
                        self.average = self.average / self.counter

                # set river locations to average
                for f in range(0, 1):
                    for i in range(0, size_x):
                        for j in range(0, size_y):

                            if (self.river_map[i][j] > self.river_threshold - 0.5):
                                self.height_map[i][j] = self.average

                # smoothing
                for f in range(0, 30):

                    if (random.randrange(0, 2) == 0):
                        self.flag_hurhur = True
                    else:
                        self.flag_hurhur = False

                    for x in range(0, size_x):
                        for y in range(0, size_y):

                            if (self.flag_hurhur):
                                self.i = size_x - 1 - x
                                self.j = size_y - 1 - y
                            else:
                                self.i = x
                                self.j = y

                            if (self.river_map[self.i][self.j] > self.river_threshold - 0.6 and
                                        self.river_map[self.i][self.j] < self.river_threshold):

                                self.temp = 0
                                self.count = 0

                                for h in (-1, 0, 1):
                                    for k in (-1, 0, 1):
                                        if (
                                                            self.i + h > 0 and self.i + h < size_x and self.j + k > 0 and self.j + k < size_y):
                                            self.temp += self.height_map[self.i + h][self.j + k]
                                            self.count += 1

                                self.average_factor = abs(
                                    self.river_map[self.i][self.j] - (self.river_threshold - 0.6)) / (abs(
                                    self.river_map[self.i][self.j] - (self.river_threshold)) + 1)
                                self.height_map[self.i][self.j] = (self.height_map[self.i][
                                                                       self.j] + self.temp / self.count + self.average * self.average_factor) / (
                                                                  2 + self.average_factor)

        # Forests
        if (True):
            self.forest_map = [None] * size_x
            for i in range(0, size_x):
                self.forest_map[i] = [0.0] * self.size_y
            #self.forest_map = np.zeros((size_x,size_y))

            if (forest > 0):
                # setting rough forest
                for x in range(0, forest * 4):
                    flag = True
                    i = random.randrange(0, size_x)
                    j = random.randrange(0, size_y)

                    if (flag):
                        self.forest_map[i][j] = random.randrange(0, 3)

                # height based propagation
                for x in range(0, min(20, forest * 3)):

                    for i in range(0, size_x - 1):
                        for j in range(0, size_y - 1):

                            for h in (-1, 0, 1):
                                for k in (-1, 0, 1):

                                    if (abs(self.height_map[i][j] - self.height_map[i + h][j + k]) < 0.05 and self.forest_map[i + h][j + k] > 0):
                                        self.forest_map[i][j] = self.forest_map[i + h][j + k]

                # normal propagation
                for x in range(0, max(2, int(forest))):

                    for i in range(0, size_x - 1):
                        for j in range(0, size_y - 1):
                            self.temp = 0

                            for h in (-1, 0, 1):
                                for k in (-1, 0, 1):
                                    try:
                                        self.temp = max(self.temp,
                                                        self.forest_map[i + h][j + k])
                                    except:
                                        pass

                            if (self.temp > self.forest_map[i][j]):
                                self.forest_map[i][j] = self.temp * random.randrange(5, 10) / 10

                # smoothing stage 1
                for f in range(0, 5):
                    for i in range(0, size_x):
                        for j in range(0, size_y):
                            self.temp = 0
                            self.temp_one = 100

                            for h in (-1, 0, 1):
                                for k in (-1, 0, 1):
                                    try:
                                        self.temp = max(self.temp,
                                                        self.forest_map[i + h][j + k])
                                        self.temp_one = min(self.temp_one,
                                                            self.forest_map[i + h][j + k])
                                    except:
                                        pass
                            if (random.randrange(0, 20) > 0):
                                self.forest_map[i][j] = (self.forest_map[i][
                                                             j] * 3 + self.temp + self.temp_one) / 5
                            else:
                                self.forest_map[i][j] = self.temp

                # smoothing stage 2
                for f in range(0, 2):
                    for i in range(0, size_x):
                        for j in range(0, size_y):
                            self.temp = 0
                            for h in (-1, 0, 1):
                                for k in (-1, 0, 1):
                                    try:
                                        self.temp += self.forest_map[i + h][j + k]
                                    except:
                                        pass
                            self.forest_map[i][j] = (self.forest_map[i][
                                                         j] * 4 + self.temp / 9) / 5

        #towns
        if(True):
            self.towns_map = [None] * size_x
            for i in range(0, size_x):
                self.towns_map[i] = [0] * self.size_y

            self.town_coords = [None]*towns

            #place towns
            for r in range(0,towns):
                self.i = random.randrange(int(size_x*0.1),int(size_x*0.9))
                self.j = random.randrange(int(size_y*0.1),int(size_y*0.9))

                self.height = self.j + random.randrange(5,13)
                self.width = self.i + random.randrange(5,13)

                for g in range(0,random.randrange(1,4)):

                    self.x = self.i + random.randrange(4,10)
                    self.y = self.j + random.randrange(4,10)
                    self.inner_width = self.x + random.randrange(4,7)
                    self.inner_height = self.y + random.randrange(4,7)

                    if(g == 0):
                        self.town_coords[r] = ((self.x + self.inner_width)/2, (self.y + self.inner_height)/2)

                    for h in range(self.x, self.inner_width):
                        for k in range(self.y, self.inner_height ):

                            if(h >= 0 and h < size_x and k >= 0 and k < size_y and self.river_map[h][k] < self.river_threshold - 0.3):
                                self.towns_map[h][k] = 1

        #roads
        if(True):
            if(roads > 0 or towns > 0):
                self.road_nodes = [None] * (towns + min(roads,3) + int(roads/2))
            else:
                self.road_nodes = []

            #set node locations
            if(True):
                #towns and edge
                self.huh = random.randrange(0,4)
                for r in range(0,len(self.road_nodes)):

                    if(r < towns):
                        self.road_nodes[r] = road_node([self.town_coords[r][0], self.town_coords[r][1]])
                        self.road_nodes[r].town = True

                    else:

                        self.huh = (self.huh + 1) % 4

                        self.flag = False
                        while(self.flag != True):
                            if(self.huh == 0):
                                self.road_nodes[r] = road_node([0,random.randrange(0,size_y)])
                            elif(self.huh == 1):
                                self.road_nodes[r] = road_node([size_x-1, random.randrange(0,size_y)])
                            elif (self.huh == 2):
                                self.road_nodes[r] = road_node([random.randrange(0, size_x),0])
                            elif (self.huh == 3):
                                self.road_nodes[r] = road_node([random.randrange(0, size_x),size_y-1])

                            if(self.river_map[self.road_nodes[r].coords[0]][self.road_nodes[r].coords[1]] < self.river_threshold - 0.3):
                                self.flag = True

                        self.road_nodes[r].edge = True

            # set connections
            if(True):
                for r in range(0, len(self.road_nodes)):
                    if (self.road_nodes[r].edge):

                        self.closest = None
                        self.closest_distance = None

                        # find closest non edge node
                        for f in range(0, len(self.road_nodes)):
                            if (r != f and self.road_nodes[f].index < 3 and self.road_nodes[f].town):

                                if (self.closest == None):
                                    self.closest = self.road_nodes[f]
                                    self.closest_distance = (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (self.road_nodes[f].coords[1] - self.road_nodes[r].coords[1]) ** 2

                                elif (self.closest_distance > (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (self.road_nodes[f].coords[1] - self.road_nodes[r].coords[1]) ** 2):
                                    self.closest = self.road_nodes[f]
                                    self.closest_distance = (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (self.road_nodes[f].coords[1] - self.road_nodes[r].coords[1]) ** 2

                        if (self.closest != None):
                            self.road_nodes[r].nodes[0] = self.closest
                            self.road_nodes[r].nodes_ind[0] = f
                            self.road_nodes[r].index += 1

                            self.closest.nodes[self.closest.index] = self.road_nodes[r]
                            self.closest.nodes_ind[self.closest.index] = r
                            self.closest.index += 1

                # set all other connections
                for r in range(0, len(self.road_nodes)):
                    if (self.road_nodes[r].town and self.road_nodes[r].index < 3):

                        for g in range(0, 2):

                            self.closest = None
                            self.closest_distance = None

                            for f in range(0, len(self.road_nodes)):
                                if (r != f and self.road_nodes[f].town and self.road_nodes[f].index < 4 and f not in self.road_nodes[f].nodes_ind):

                                    if (self.closest == None):
                                        self.closest = self.road_nodes[f]
                                        self.closest_distance = (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (
                                                                                                      self.road_nodes[
                                                                                                          f].coords[
                                                                                                          1] -
                                                                                                      self.road_nodes[
                                                                                                          r].coords[
                                                                                                          1]) ** 2

                                    elif (self.closest_distance > (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (self.road_nodes[f].coords[1] - self.road_nodes[r].coords[1]) ** 2):
                                        self.closest = self.road_nodes[f]
                                        self.closest_distance = (self.road_nodes[f].coords[0] - self.road_nodes[r].coords[0]) ** 2 + (
                                                                                                      self.road_nodes[
                                                                                                          f].coords[
                                                                                                          1] -
                                                                                                      self.road_nodes[
                                                                                                          r].coords[
                                                                                                          1]) ** 2

                            if (self.closest != None):
                                self.road_nodes[r].nodes[self.road_nodes[r].index] = self.closest
                                self.road_nodes[r].nodes_ind[self.road_nodes[r].index] = f
                                self.road_nodes[r].index += 1

                                self.closest.nodes[self.closest.index] = self.road_nodes[r]
                                self.closest.nodes_ind[self.closest.index] = r
                                self.closest.index += 1

    def draw_contours(self):
        self.contour_lines = []
        self.contour_interval = 0.5

        #create array
        for i in range(0, 30):
            if(i%2 == 0):
                self.temp = cvsmr.line_object(config.line_groups["2/3"])
            else:
                self.temp = cvsmr.line_object(config.line_groups["1/3"])

            self.contour_lines.append(self.temp)

        for i in range(0,self.size_x-1):#self.size_x-1
            for j in range(0,self.size_y-1):#self.size_y-1
                self.slope_one = self.height_map[i + 1][j] - self.height_map[i][j]
                self.slope_two = self.height_map[i + 1][j + 1] - self.height_map[i][j + 1]
                self.slope_three = self.height_map[i][j+1] - self.height_map[i][j]
                self.slope_four = self.height_map[i+1][j + 1] - self.height_map[i+1][j]
                self.slope_five = (self.height_map[i+1][j+1]-self.height_map[i][j])/1.414

                #print(self.height_map[i + 1][j],self.height_map[i][j])
                #print(self.slope_one, self.slope_two,self.slope_three,self.slope_four)

                for h in range(0,len(self.contour_lines)):#len(self.contour_lines)
                    self.counter = 0
                    self.test_height = h * self.contour_interval


                    #lower triangle
                    if (self.slope_one != 0):
                        self.test_x = i + (self.test_height - self.height_map[i][j]) / float(self.slope_one)
                        # print(self.test_x,j)
                        if (self.test_x > i and self.test_x <= i + 1):
                            self.contour_lines[h].vertices.append(self.test_x)
                            self.contour_lines[h].vertices.append(j)
                            self.counter += 1
                    elif(self.slope_five != 0 and self.height_map[i][j] == self.test_height):
                        self.contour_lines[h].vertices.append(i)
                        self.contour_lines[h].vertices.append(j)
                        self.contour_lines[h].vertices.append(i+1)
                        self.contour_lines[h].vertices.append(j)

                    if (self.slope_four != 0):
                        self.test_y = j + (self.test_height - self.height_map[i + 1][j]) / float(self.slope_four)
                        # print(i+1, self.test_y)
                        if (self.test_y > j and self.test_y <= j + 1):
                            self.contour_lines[h].vertices.append(i + 1)
                            self.contour_lines[h].vertices.append(self.test_y)
                            self.counter += 1

                    if(self.slope_five != 0):
                        self.test_d = (self.test_height - self.height_map[i][j]) / float(self.slope_five)
                        if(self.test_d >= 0 and self.test_d < 1.4143):
                            self.contour_lines[h].vertices.append(i+self.test_d*0.70711)
                            self.contour_lines[h].vertices.append(j + self.test_d * 0.70711)
                            self.counter += 1
                    elif (self.slope_one != 0 or self.slope_three != 0):
                        if(self.height_map[i][j] == self.test_height):
                            self.contour_lines[h].vertices.append(i)
                            self.contour_lines[h].vertices.append(j)
                            self.contour_lines[h].vertices.append(i + 1)
                            self.contour_lines[h].vertices.append(j+1)

                    if (self.counter % 2 != 0):
                        # print(self.counter)
                        self.contour_lines[h].vertices.pop()
                        self.contour_lines[h].vertices.pop()

                    self.counter = 0

                    #upper triangle
                    if (self.slope_two != 0):
                        self.test_x = i + (self.test_height - self.height_map[i][j + 1]) / float(self.slope_two)
                        # print(self.test_x, j+1)
                        if (self.test_x > i and self.test_x <= i + 1):
                            self.contour_lines[h].vertices.append(self.test_x)
                            self.contour_lines[h].vertices.append(j + 1)
                            self.counter += 1

                    if (self.slope_three != 0):
                        self.test_y = j + (self.test_height - self.height_map[i][j]) / float(self.slope_three)
                        # print(i,self.test_y)
                        if (self.test_y > j and self.test_y <= j + 1):
                            self.contour_lines[h].vertices.append(i)
                            self.contour_lines[h].vertices.append(self.test_y)
                            self.counter += 1
                    elif (self.slope_five != 0 and self.height_map[i][j] == self.test_height):
                        self.contour_lines[h].vertices.append(i)
                        self.contour_lines[h].vertices.append(j)
                        self.contour_lines[h].vertices.append(i)
                        self.contour_lines[h].vertices.append(j+1)

                    if (self.slope_five != 0):
                        self.test_d = (self.test_height - self.height_map[i][j]) / float(self.slope_five)
                        if (self.test_d >= 0 and self.test_d < 1.4143):
                            self.contour_lines[h].vertices.append(i + self.test_d * 0.70711)
                            self.contour_lines[h].vertices.append(j + self.test_d * 0.70711)
                            self.counter += 1

                    if(self.counter % 2 != 0):
                        #print(self.counter,len(self.contour_lines[h].vertices))
                        self.contour_lines[h].vertices.pop()
                        self.contour_lines[h].vertices.pop()

        for h in range(0, len(self.contour_lines)):
            #self.contour_lines[h].colors = [255]*3*int(len(self.contour_lines[h].vertices)/2)
            self.contour_lines[h].solid_color_coords(100,20,30)

        self.render_objects.append(self.contour_lines)

    def draw_forest(self):
        self.forest_polygons = []

        for i in range(0,self.size_x-1):
            for j in range(0,self.size_y-1):
                self.temp = cvsmr.polygon_object(1)
                self.temp.vertices_polygon = []

                if(self.forest_map[i][j] >= self.forest_threshold or
                    self.forest_map[i+1][j] >= self.forest_threshold or
                    self.forest_map[i+1][j+1] >= self.forest_threshold or
                    self.forest_map[i][j+1] >= self.forest_threshold):



                    #solid forest block
                    if(self.forest_map[i][j] >= self.forest_threshold and
                        self.forest_map[i+1][j] >= self.forest_threshold and
                        self.forest_map[i+1][j+1] >= self.forest_threshold and
                        self.forest_map[i][j+1] >= self.forest_threshold):
                        #hghghghghggh
                        self.temp.vertices_polygon=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]]
                        self.temp.convert_to_triangles()
                        self.temp.solid_color_coords(10,150,20)
                        self.forest_polygons.append(self.temp)

                    else:

                        self.slope_one = self.forest_map[i + 1][j] - self.forest_map[i][j]
                        self.slope_two = self.forest_map[i + 1][j + 1] - self.forest_map[i][j + 1]
                        self.slope_three = self.forest_map[i][j + 1] - self.forest_map[i][j]
                        self.slope_four = self.forest_map[i + 1][j + 1] - self.forest_map[i + 1][j]
                        self.slope_five = (self.forest_map[i + 1][j + 1] - self.forest_map[i][j]) / 1.414

                        #UPPER TRIANGLE
                        if(True):
                            self.vertex_counter = 0

                            #side3
                            if(True):
                                if(self.forest_map[i][j] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter,[i,j])
                                    self.vertex_counter+=1
                                elif(self.slope_three != 0):
                                    self.test = j + (self.forest_threshold - self.forest_map[i][j]) / float(self.slope_three)
                                    if(self.test >= j and self.test <= j+1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter+=1

                                if(self.forest_map[i][j+1] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j+1])
                                    self.vertex_counter+=1
                                elif (self.slope_three != 0):
                                    self.test = j + (self.forest_threshold - self.forest_map[i][j]) / float(self.slope_three)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter+=1

                            #side2
                            if(True):
                                if (self.forest_map[i][j+1] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j+1])
                                    self.vertex_counter+=1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.forest_threshold - self.forest_map[i][j+1]) / float(self.slope_two)
                                    if(self.test >= i and self.test <= i+1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j+1])
                                        self.vertex_counter+=1

                                if (self.forest_map[i+1][j + 1] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j + 1])
                                    self.vertex_counter+=1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.forest_threshold - self.forest_map[i][j+1]) / float(self.slope_two)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j+1])
                                        self.vertex_counter+=1

                            #side5
                            if(self.slope_five != 0):
                                self.test = (self.forest_threshold - self.forest_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+self.test*0.70711,j+self.test*0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if(len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(10,150,20)
                                self.forest_polygons.append(self.temp)

                        #LOWER TRIANGLE
                        if(True):
                            self.temp = cvsmr.polygon_object(2)
                            self.temp.vertices_polygon = []

                            self.vertex_counter = 0

                            # side4
                            if (True):
                                if (self.forest_map[i+1][j+1] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j+1])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.forest_threshold - self.forest_map[i+1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, self.test])
                                        self.vertex_counter += 1

                                if (self.forest_map[i+1][j] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.forest_threshold - self.forest_map[i + 1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, self.test])
                                        self.vertex_counter += 1

                            # side1
                            if (True):
                                if (self.forest_map[i+1][j] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.forest_threshold - self.forest_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                                if (self.forest_map[i][j] >= self.forest_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.forest_threshold - self.forest_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                            # side5
                            if (self.slope_five != 0):
                                self.test = (self.forest_threshold - self.forest_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + self.test * 0.70711,
                                                                                            j + self.test * 0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if (len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(10,150,20)
                                self.forest_polygons.append(self.temp)

        self.render_objects.append(self.forest_polygons)

    def draw_river(self):
        self.river_polygons = []

        for i in range(0,self.size_x-1):
            for j in range(0,self.size_y-1):
                self.temp = cvsmr.polygon_object(2)
                self.temp.vertices_polygon = []

                if(self.river_map[i][j] >= self.river_threshold or
                    self.river_map[i+1][j] >= self.river_threshold or
                    self.river_map[i+1][j+1] >= self.river_threshold or
                    self.river_map[i][j+1] >= self.river_threshold):

                    #solid river block
                    if(self.river_map[i][j] >= self.river_threshold and
                        self.river_map[i+1][j] >= self.river_threshold and
                        self.river_map[i+1][j+1] >= self.river_threshold and
                        self.river_map[i][j+1] >= self.river_threshold):
                        #hghghghghggh
                        self.temp.vertices_polygon=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]]
                        self.temp.convert_to_triangles()
                        self.temp.solid_color_coords(0, 100, 150)
                        self.river_polygons.append(self.temp)

                    else:

                        self.slope_one = self.river_map[i + 1][j] - self.river_map[i][j]
                        self.slope_two = self.river_map[i + 1][j + 1] - self.river_map[i][j + 1]
                        self.slope_three = self.river_map[i][j + 1] - self.river_map[i][j]
                        self.slope_four = self.river_map[i + 1][j + 1] - self.river_map[i + 1][j]
                        self.slope_five = (self.river_map[i + 1][j + 1] - self.river_map[i][j]) / 1.414

                        #UPPER TRIANGLE
                        if(True):
                            self.vertex_counter = 0

                            #side3
                            if(True):
                                if(self.river_map[i][j] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter,[i,j])
                                    self.vertex_counter+=1
                                elif(self.slope_three != 0):
                                    self.test = j + (self.river_threshold - self.river_map[i][j]) / float(self.slope_three)
                                    if(self.test >= j and self.test <= j+1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter+=1

                                if(self.river_map[i][j+1] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j+1])
                                    self.vertex_counter+=1
                                elif (self.slope_three != 0):
                                    self.test = j + (self.river_threshold - self.river_map[i][j]) / float(self.slope_three)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter+=1

                            #side2
                            if(True):
                                if (self.river_map[i][j+1] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j+1])
                                    self.vertex_counter+=1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.river_threshold - self.river_map[i][j+1]) / float(self.slope_two)
                                    if(self.test >= i and self.test <= i+1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j+1])
                                        self.vertex_counter+=1

                                if (self.river_map[i+1][j + 1] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j + 1])
                                    self.vertex_counter+=1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.river_threshold - self.river_map[i][j+1]) / float(self.slope_two)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j+1])
                                        self.vertex_counter+=1

                            #side5
                            if(self.slope_five != 0):
                                self.test = (self.river_threshold - self.river_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+self.test*0.70711,j+self.test*0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if(len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(0, 100, 150)
                                self.river_polygons.append(self.temp)

                        #LOWER TRIANGLE
                        if(True):
                            self.temp = cvsmr.polygon_object(2)
                            self.temp.vertices_polygon = []

                            self.vertex_counter = 0

                            # side4
                            if (True):
                                if (self.river_map[i+1][j+1] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j+1])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.river_threshold - self.river_map[i+1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, self.test])
                                        self.vertex_counter += 1

                                if (self.river_map[i+1][j] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.river_threshold - self.river_map[i + 1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, self.test])
                                        self.vertex_counter += 1

                            # side1
                            if (True):
                                if (self.river_map[i+1][j] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i+1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.river_threshold - self.river_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                                if (self.river_map[i][j] >= self.river_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.river_threshold - self.river_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                            # side5
                            if (self.slope_five != 0):
                                self.test = (self.river_threshold - self.river_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + self.test * 0.70711,
                                                                                            j + self.test * 0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if (len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(0,100,150)
                                self.river_polygons.append(self.temp)

        self.render_objects.append(self.river_polygons)

    def draw_towns(self):
        self.towns_polygons = []

        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                self.temp = cvsmr.polygon_object(2)
                self.temp.vertices_polygon = []

                if (self.towns_map[i][j] >= self.towns_threshold or
                            self.towns_map[i + 1][j] >= self.towns_threshold or
                            self.towns_map[i + 1][j + 1] >= self.towns_threshold or
                            self.towns_map[i][j + 1] >= self.towns_threshold):

                    # solid towns block
                    if (self.towns_map[i][j] >= self.towns_threshold and
                                self.towns_map[i + 1][j] >= self.towns_threshold and
                                self.towns_map[i + 1][j + 1] >= self.towns_threshold and
                                self.towns_map[i][j + 1] >= self.towns_threshold):
                        # hghghghghggh
                        self.temp.vertices_polygon = [[i, j], [i + 1, j], [i + 1, j + 1], [i, j + 1]]
                        self.temp.convert_to_triangles()
                        self.temp.solid_color_coords(100, 100, 100)
                        self.towns_polygons.append(self.temp)

                    else:

                        self.slope_one = self.towns_map[i + 1][j] - self.towns_map[i][j]
                        self.slope_two = self.towns_map[i + 1][j + 1] - self.towns_map[i][j + 1]
                        self.slope_three = self.towns_map[i][j + 1] - self.towns_map[i][j]
                        self.slope_four = self.towns_map[i + 1][j + 1] - self.towns_map[i + 1][j]
                        self.slope_five = (self.towns_map[i + 1][j + 1] - self.towns_map[i][j]) / 1.414

                        # UPPER TRIANGLE
                        if (True):
                            self.vertex_counter = 0

                            # side3
                            if (True):
                                if (self.towns_map[i][j] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j])
                                    self.vertex_counter += 1
                                elif (self.slope_three != 0):
                                    self.test = j + (self.towns_threshold - self.towns_map[i][j]) / float(
                                        self.slope_three)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter += 1

                                if (self.towns_map[i][j + 1] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j + 1])
                                    self.vertex_counter += 1
                                elif (self.slope_three != 0):
                                    self.test = j + (self.towns_threshold - self.towns_map[i][j]) / float(
                                        self.slope_three)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i, self.test])
                                        self.vertex_counter += 1

                            # side2
                            if (True):
                                if (self.towns_map[i][j + 1] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j + 1])
                                    self.vertex_counter += 1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.towns_threshold - self.towns_map[i][j + 1]) / float(
                                        self.slope_two)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j + 1])
                                        self.vertex_counter += 1

                                if (self.towns_map[i + 1][j + 1] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, j + 1])
                                    self.vertex_counter += 1
                                elif (self.slope_two != 0):
                                    self.test = i + (self.towns_threshold - self.towns_map[i][j + 1]) / float(
                                        self.slope_two)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j + 1])
                                        self.vertex_counter += 1

                            # side5
                            if (self.slope_five != 0):
                                self.test = (self.towns_threshold - self.towns_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + self.test * 0.70711,
                                                                                            j + self.test * 0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if (len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(100, 100, 100)
                                self.towns_polygons.append(self.temp)

                        # LOWER TRIANGLE
                        if (True):
                            self.temp = cvsmr.polygon_object(2)
                            self.temp.vertices_polygon = []

                            self.vertex_counter = 0

                            # side4
                            if (True):
                                if (self.towns_map[i + 1][j + 1] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, j + 1])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.towns_threshold - self.towns_map[i + 1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, self.test])
                                        self.vertex_counter += 1

                                if (self.towns_map[i + 1][j] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_four != 0):
                                    self.test = j + (self.towns_threshold - self.towns_map[i + 1][j]) / float(
                                        self.slope_four)
                                    if (self.test >= j and self.test <= j + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, self.test])
                                        self.vertex_counter += 1

                            # side1
                            if (True):
                                if (self.towns_map[i + 1][j] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + 1, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.towns_threshold - self.towns_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                                if (self.towns_map[i][j] >= self.towns_threshold):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i, j])
                                    self.vertex_counter += 1
                                elif (self.slope_one != 0):
                                    self.test = i + (self.towns_threshold - self.towns_map[i][j]) / float(
                                        self.slope_one)
                                    if (self.test >= i and self.test <= i + 1):
                                        self.temp.vertices_polygon.insert(self.vertex_counter, [self.test, j])
                                        self.vertex_counter += 1

                            # side5
                            if (self.slope_five != 0):
                                self.test = (self.towns_threshold - self.towns_map[i][j]) / float(self.slope_five)
                                if (self.test >= 0 and self.test < 1.4143):
                                    self.temp.vertices_polygon.insert(self.vertex_counter, [i + self.test * 0.70711,
                                                                                            j + self.test * 0.70711])

                            self.temp.convert_to_triangles_remove_duplicates()
                            if (len(self.temp.vertices_polygon) >= 3):
                                self.temp.convert_to_triangles()
                                self.temp.solid_color_coords(100, 100, 100)
                                self.towns_polygons.append(self.temp)

        self.render_objects.append(self.towns_polygons)

    def draw_roads(self):
        self.roads_lines = []

        for r in range(0, len(self.road_nodes)):
            for f in range(0,(self.road_nodes[r].index)):
                self.temp = cvsmr.line_object(config.line_groups["2/2"])
                self.temp.vertices = [self.road_nodes[r].coords[0], self.road_nodes[r].coords[1],
                                      self.road_nodes[r].nodes[f].coords[0], self.road_nodes[r].nodes[f].coords[1]]
                self.temp.solid_color_coords(0,0,0)
                self.roads_lines.append(self.temp)

        self.render_objects.append(self.roads_lines)

    def draw_background(self):
        self.white_background = cvsmr.polygon_object(0)
        self.white_background.vertices_polygon = [[0,0],[self.size_x-1,0],[self.size_x-1,self.size_y-1],[0,self.size_y-1]]
        self.white_background.convert_to_triangles()
        self.white_background.solid_color_coords(240,240,240)

        #for i in range(0,self.size_x):
        #    for j in range(0, self.size_y):
        #        config.batch.add(1,pyglet.gl.GL_POINTS, config.groups[4], ('v2f',(i,j)), ('c3B',(0,0,0)))

        self.render_objects.append([self.white_background])

    def draw_heatmap(self):
        self.heatmap = []

        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                self.temp = config.batch.add(3, pyglet.gl.GL_TRIANGLES,
                                             config.groups[0],
                                             (('v2i'), (i, j, i, j + 1, i + 1, j + 1)),
                                             ('c3B', (int(self.height_map[i][j] * 200 / self.max_height), 200, 0,
                                                      int(self.height_map[i][j] * 200 / self.max_height), 200, 0,
                                                      int(self.height_map[i][j] * 200 / self.max_height), 200, 0)))
                self.heatmap.append(self.temp)

                self.temp = config.batch.add(3, pyglet.gl.GL_TRIANGLES,
                                             config.groups[0],
                                             (('v2i'), (i, j, i + 1, j, i + 1, j + 1)),
                                             ('c3B', (int(self.height_map[i][j] * 200 / self.max_height), 200, 0,
                                                      int(self.height_map[i][j] * 200 / self.max_height), 200, 0,
                                                      int(self.height_map[i][j] * 200 / self.max_height), 200, 0)))
                self.heatmap.append(self.temp)

    def draw_forest_heatmap(self):
        self.heatmap = []

        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                self.temp = config.batch.add(3, pyglet.gl.GL_TRIANGLES,
                                             config.groups[0],
                                             (('v2i'), (i, j, i, j + 1, i + 1, j + 1)),
                                             ('c3B', (0, int(self.forest_map[i][j] * 255 / self.forest), 100, 0,
                                                      int(self.forest_map[i][j + 1] * 255 / self.forest), 100, 0,
                                                      int(self.forest_map[i + 1][j + 1] * 255 / self.forest), 100)))
                self.heatmap.append(self.temp)

                self.temp = config.batch.add(3, pyglet.gl.GL_TRIANGLES,
                                             config.groups[0],
                                             (('v2i'), (i, j, i + 1, j, i + 1, j + 1)),
                                             ('c3B', (0, int(self.forest_map[i][j] * 255 / self.forest), 100, 0,
                                                      int(self.forest_map[i + 1][j] * 255 / self.forest), 100, 0,
                                                      int(self.forest_map[i + 1][j + 1] * 255 / self.forest), 100)))
                self.heatmap.append(self.temp)
