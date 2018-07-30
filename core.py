import os
import time
import cvsmr, cvsmgmt
import config
import numpy as np
import calculations
import math

class scenario:
    def __init__(self):
        self.map = [None]*config.num_provinces

        self.year = None
        self.month = None
        self.day = None
        self.name = None

        self.description = None

    def set(self):
        self.index = 0
        for i in range(0,len(config.provinces)):
            if(config.provinces[i] != None):
                while(self.map[self.index][0] < config.provinces[i].id):
                    self.index += 1
                if(self.map[self.index][0] == config.provinces[i].id):
                    config.provinces[i].set_nation(self.map[self.index][1])

        config.day = self.day
        config.month = self.month
        config.year = self.year

        config.nation_borders.remove_from_scene()
        draw_nation_borders()
        config.nation_borders.add_to_scene()

        for i in range(0,7):
            s = time.time()
            config.nations[i].add_provinces()
            e = time.time()
            print("YUH: ", e-s)
            config.nations[i].draw_label()
            print(i)

class save:
    def __init__(self):
        self.map = [None]*config.num_provinces

        self.year = None
        self.month = None
        self.day = None

        self.nation = None
        self.name = None

    def set(self):
        self.index = 0
        for i in range(0,len(config.provinces)):
            while(self.map[self.index][0] < config.provinces[i].id):
                self.index += 1
            if(self.map[self.index][0] == config.provinces[i].id):
                config.provinces[i].set_nation(self.map[self.index][1])

        config.day = self.day
        config.month = self.month
        config.year = self.year

        for i in range(0, config.num_provinces):
            if(config.provinces[i].nation != None):
                for j in range(0, config.num_nations):
                    if(config.provinces[i].nation.id == j):
                        config.nations[j].provinces.append(config.provinces[i])
                        break

        config.nation_borders.remove_from_scene()
        draw_nation_borders()
        config.nation_borders.add_to_scene()

        for i in range(0, config.num_nations):
            config.nations[i].add_provinces()
            config.nations[i].draw_label()

class nation:
    def __init__(self):
        self.color = None
        self.name = None
        self.adjective = None

        self.id = None #same as index

        self.border = []
        self.provinces = []

        self.label = []

    def add_provinces(self):
        #populates / refreshes list of provinces and their borders

        self.bodies = [[]]
        self.border = []
        self.provinces = []

        #add to province list
        for i in range(config.num_provinces):
            if(config.provinces[i].nation != None and config.provinces[i].nation.id == self.id):
                self.provinces.append(config.provinces[i])

        #make bodies
        for i in range(0, config.num_provinces):

            for k in range(0, len(self.bodies)):

                if(len(self.bodies[k]) == 0):
                    self.bodies[k].append(config.provinces[i])

                    #Add its adjacents and its adjacents etc
                    recursive_add_prov(config.provinces[i], k, self.bodies, self.id)

                    self.found = True
                    break
                else:
                    self.found = False
                    for j in range(0, len(self.bodies[k])):
                        if(self.bodies[k][j].index == i):
                            self.found = True
                            break

                    if(self.found):
                        break

            if(not self.found):
                self.bodies.append([])

        #determine largest body
        self.hlen = 0
        for i in range(0, len(self.bodies)):
            if(len(self.bodies[i]) > self.hlen):
                self.hlen = len(self.bodies[i])
                self.body = self.bodies[i]

        #add borders of largest body
        for i in range(0, len(self.body)):
            for j in range(0,len(config.nation_borders.render_objects[0][i].vertices)):
                self.border.append(config.nation_borders.render_objects[0][i].vertices[j])

    def init_label(self):
        self.raw_length = 0
        self.raw_height = 0

        for i in range(0,len(self.name)):
            if(self.name[i] != ' '):
                self.label.append(cvsmr.sprite_object(self.name[i].upper(), [0,0], 5))
            else:
                self.label.append(cvsmr.sprite_object('space', [0,0], 5))
            if(self.label[i].sprite.height > self.raw_height):
                self.raw_height = self.label[i].sprite.height

            self.raw_length += self.label[i].sprite.width

    def draw_label(self):
        if(len(self.provinces) > 0):

            self.max_x = 0
            self.min_x = 9999999
            self.max_y = 0
            self.min_y = 9999999

            #Find bounds
            for i in range(0, int(len(self.border)/2)):
                if(self.border[i*2] > self.max_x):
                    self.max_x = self.border[i*2]
                elif(self.border[i*2] < self.min_x):
                    self.min_x = self.border[i*2]

                if (self.border[i * 2 + 1] > self.max_y):
                    self.max_y = self.border[i * 2 + 1]
                elif (self.border[i * 2 + 1] < self.min_y):
                    self.min_y = self.border[i * 2 + 1]


            #aspect ratio X
            if(abs(self.max_x - self.min_x) > abs(self.max_y - self.min_y) * 0.7 or True):
                self.x_interval = (self.max_x - self.min_x) / 10

                self.points = [None] * 8

                for i in range(1,9):

                    self.sample_x = self.min_x + self.x_interval * i

                    self.intersects = []

                    #look for intersects
                    for j in range(0, int(len(self.border)/4)):
                        self.temp1 = [self.border[j*2], self.border[j*2 + 1]]
                        self.temp2 = [self.border[j*2+2], self.border[j*2+3]]

                        if(self.temp1[0] < self.sample_x and self.temp2[0] > self.sample_x or
                           self.temp1[0] > self.sample_x and self.temp2[0] < self.sample_x):

                            self.intersects.append((self.temp1[1] + self.temp2[1])/2) #y

                    #order_intersects
                    for j in range(0, len(self.intersects)):
                        for tt in range(j+1,len(self.intersects)):
                            if(self.intersects[tt] < self.intersects[j]):
                                self.temp = self.intersects[j]
                                self.intersects[j] = self.intersects[tt]
                                self.intersects[tt] = self.temp

                    #choose which segments to add to path
                    if(len(self.intersects) == 2):
                        self.points[i-1] = [self.sample_x,
                                            (self.intersects[0] + self.intersects[1])/2,
                                            abs(self.intersects[0] - self.intersects[1])]

                    elif(len(self.intersects) >= 4 and i > 1):
                        #take the closest to the previous point
                        self.min_d = 1000000

                        for j in range(0, int(len(self.intersects)/2)):
                            self.temp = (self.intersects[j+1] + self.intersects[j*2+1]) /2

                            if(abs(self.temp - self.points[i-2][1]) < self.min_d):
                                self.min_d = abs(self.temp - self.points[i-2][1])
                                self.best = j

                        self.points[i-1] = [self.sample_x,
                                            (self.intersects[self.best*2] + self.intersects[self.best*2+1])/2,
                                            abs(self.intersects[0] - self.intersects[1])
                                            ]

                    elif(len(self.intersects) >= 4):
                        #take the widest point (heightiest)
                        self.max_d = 0

                        for j in range(0, int(len(self.intersects)/2)):
                            self.temp = abs(self.intersects[j*2] - self.intersects[j*2 + 1])
                            if(self.temp > self.max_d):
                                self.max_d = self.temp
                                self.best = j*2

                        self.points[i - 1] = [self.sample_x,
                                              (self.intersects[self.best] + self.intersects[self.best + 1]) / 2,
                                              abs(self.intersects[0] - self.intersects[1])
                                              ]

                    elif(len(self.intersects) == 0):
                        self.points[i - 1] = [self.sample_x,
                                              self.points[i-2][1],
                                              self.points[i-2][2]
                                              ]

                    else:
                        print("FUCKED: ", len(self.intersects))

            # determine distance, height
            self.distance = 0
            self.height = 100000
            for i in range(1, len(self.points)):
                self.distance += (self.points[i][0] - self.points[i-1][0])**2 + (self.points[i][1] - self.points[i-1][1])**2

                if(self.points[i][2] < self.height):
                    self.height = self.points[i][2]

            #determine_scale
            self.length_scale = self.distance / self.raw_length
            self.height_scale = self.height / self.raw_height
            if(self.length_scale < self.height_scale):
                self.final_scale = self.length_scale
            else:
                self.final_scale = self.height_scale

            #determine spacing
            self.spacing = (self.distance - self.raw_length * self.final_scale) / (len(self.label) - 1)

            #make the label
            self.length_progress = 0
            self.current_point_index = 0
            for i in range(0, len(self.label)):
                self.point1 = self.points[self.current_point_index]
                self.point2 = self.points[self.current_point_index + 1]

                self.point_d = (self.point1[0] - self.point2[0])**2 + (self.point1[1] - self.point2[1])**2

                if(self.length_progress > self.point_d):
                    self.current_point_index += 1
                    self.point1 = self.points[self.current_point_index]
                    self.point2 = self.points[self.current_point_index + 1]

                    self.length_progress -= self.point_d

                self.line_vec = [(self.point2[0] - self.point1[0]) / self.point_d,
                                 (self.point2[1] - self.point1[1]) / self.point_d]

                self.perp = [self.line_vec[1] / self.point_d,
                             self.line_vec[0] / self.point_d * -1]

                if(self.perp[1] > 0):
                    self.perp[0] *= -1
                    self.perp[1] *= -1

                self.label[i].sprite.update(rotation = 0)
                self.label[i].sprite.update(scale_x = self.final_scale, scale_y = self.final_scale,
                                            x = self.point1[0] + self.line_vec[0] * self.length_progress + self.perp[0] * self.raw_height * self.final_scale / 2,
                                            y = self.point1[1] + self.line_vec[1] * self.length_progress + self.perp[0] * self.raw_height * self.final_scale / 2)
                self.label[i].sprite.update(rotation = math.degrees(math.asin(self.line_vec[1])))
                self.label[i].add()


class province(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, group_num = 1)
        self.render_objects=[[None]]
        self.handlers[0] = True
        self.handlers[3] = True
        self.handlers[4] = True
        self.handlers[5] = True

        self.border = None
        self.label = None

        self.adjacents_border = [] #list of lists of indexes of adjacents provinces to each border vertice
        self.adjacents = [] #list of indexes of adjacent provinces

        self.name = None
        self.nation = None
        self.id = None
        self.index = None
        self.inside_coord = None

        self.on_screened = False

    def set_nation(self, nation):
        if(nation != None):
            self.prev_nation = self.nation
            self.nation = config.nations_dict[nation]

            self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1], self.nation.color[2])
            self.render_objects[0][0].update_color()

            if(config.state == "in_game_menu"):
                self.draw_nation_borders()

                self.nation.add_provinces()
                if(self.prev_nation != None):
                    self.prev_nation.add_provinces()

        else:
            self.render_objects[0][0].solid_color_coords(255,255,255)
            self.render_objects[0][0].update_color()

    def draw_nation_border(self):

        self.temp_line = cvsmr.line_object(config.line_groups["2/3"])
        config.nation_borders.render_objects[0][self.index] = temp_line
        if (self.nation != None):

            self.counter = 0

            for j in range(0, len(self.adjacents_border)):
                self.flag = False
                for p in range(0, len(self.adjacents_border[j])):
                    self.tempadj = me.adjacents_border[j][p]

                    if (self.tempadj != -1):
                        self.tempadjprov = config.provinces[tempadj]

                        if (
                                            self.tempadjprov != False and self.tempadjprov.nation == None or
                                            self.tempadjprov != False and self.tempadjprov.nation.id != self.nation.id
                        ):
                            self.flag = True
                            self.counter += 1
                            break
                if (not self.flag):
                    self.counter = 0

                if (self.counter > 1):
                    self.temp_line.vertices.append(me.border.vertices[(j - 1) * 4])
                    self.temp_line.vertices.append(me.border.vertices[(j - 1) * 4 + 1])
                    self.temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 2) % len(me.border.vertices)])
                    self.temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 3) % len(me.border.vertices)])

            self.temp_line.solid_color_coords(40, 40, 40)

    def set_id(self, id):
        self.id = id
        config.provinces_id[str(id)] = self

    def on_screen(self):

        if(self.inside_coord[0] > config.screen_bound_left and
           self.inside_coord[0] < config.screen_bound_right and
           self.inside_coord[1] > config.screen_bound_bottom and
           self.inside_coord[1] < config.screen_bound_top):

            self.on_screened = True
            return True
        else:
            return False

    def handler_leftclick(self,x,y):
        config.click_selected = self

        self.nodrag_click_scene(x,y)

    def handler_leftdrag(self,x,y,dx,dy):
        self.nodrag_leftdrag_scene(x,y)

        if (config.scene_transformation_group.scale_x > 0.7):
            calc_screen_bounds()
            for i in range(0, config.num_provinces):
                if (config.provinces[i].on_screen()):
                    config.provinces[i].label.add()
                    config.provinces[i].on_screened = True

                elif(config.provinces[i].on_screened):
                    config.provinces[i].label.remove()
                    config.provinces[i].on_screened = False

    def handler_release(self,x,y):
        if(self.nodrag):

            if(config.state == "play_menu"):
                if(self.nation != None):
                    config.menus["play_menu"].elements[7].set_province(self.name)
                    config.menus["play_menu"].elements[7].set_nation(self.nation.name)

    def handler_scroll(self,x,y,scroll_x,scroll_y):
        self.zoom(x,y,scroll_y)

        if(config.scene_transformation_group.scale_x > 0.7):
            calc_screen_bounds()
            for i in range(0, config.num_provinces):
                if(config.provinces[i].on_screen()):
                    config.provinces[i].label.add()

        elif(config.scene_transformation_group.scale_x > 0.3):
            for i in range(0, config.num_provinces):
                if(config.provinces[i].on_screened):
                    config.provinces[i].label.remove()
                    config.provinces[i].on_screened = False

class ocean(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self,0)
        self.handlers[0] = True
        self.handlers[5] = True
        self.handlers[3] = True

        self.render_objects = [[cvsmr.sprite_object("ocean", [0,0], 0)]]
        self.render_objects[0][0].scale(100,100)

        self.checkbox.set_source(self.render_objects[0][0])

    def handler_leftclick(self,x,y):
        config.click_selected = self

        self.nodrag_click_scene(x,y)

    def handler_leftdrag(self,x,y,dx,dy):
        self.nodrag_leftdrag_scene(x, y)

        if (config.scene_transformation_group.scale_x > 0.7):
            calc_screen_bounds()
            for i in range(0, config.num_provinces):
                if (config.provinces[i].on_screen()):
                    config.provinces[i].label.add()
                    config.provinces[i].on_screened = True

                elif (config.provinces[i].on_screened):
                    config.provinces[i].label.remove()
                    config.provinces[i].on_screened = False

    def handler_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom(x, y, scroll_y)

        if (config.scene_transformation_group.scale_x > 0.7):
            calc_screen_bounds()
            for i in range(0, config.num_provinces):
                if (config.provinces[i].on_screen()):
                    config.provinces[i].label.add()

        elif (config.scene_transformation_group.scale_x > 0.3):
            for i in range(0, config.num_provinces):
                if (config.provinces[i].on_screened):
                    config.provinces[i].label.remove()
                    config.provinces[i].on_screened = False

class time_entry(cvsmgmt.update_entry):
    def __init__(self, args=None):
        cvsmgmt.update_entry.__init__(self, args=args)
        self.speed = 0
        self.timer = 60

    def run(self):
        if (self.timer <= 0):

            self.timer = 60
            time_update()

        else:
            self.timer -= self.speed

    def set_speed(self, speed):
        self.speed = speed

#----------------------------------------------------------------------------------------------------------------------

def calc_screen_bounds(threshold_x = 100, threshold_y = 100):
    config.screen_bound_left = -1 * config.scene_transformation_group.x - threshold_x
    config.screen_bound_right = abs(config.scene_transformation_group.x) + 1920/ config.scene_transformation_group.scale_x + threshold_x
    config.screen_bound_top = abs(config.scene_transformation_group.y) + 1080 / config.scene_transformation_group.scale_x + threshold_y
    config.screen_bound_bottom =  -1 * config.scene_transformation_group.y - threshold_y

def recursive_add_prov(province, k, bodies, nation_id):

    for rr in range(0, len(province.adjacents)):
        # see if this adjacents is already in
        if(province. adjacents[rr].nation != None and province.adjacents[rr].nation.id == nation_id):
            found = False
            for j in range(0, len(bodies[k])):

                if (bodies[k][j].index == province.adjacents[rr].index):
                    found = True
                    break

            if(not found):
                bodies[k].append(province.adjacents[rr])
                recursive_add_prov(province.adjacents[rr], k, bodies, nation_id)

    return

def init_provinces(group):
    mysize = 10

    fileone = open("resources/map/num.txt", "r")
    file = fileone.read()
    fileone.close()
    config.num_provinces = int(file)
    config.provinces = [None] * config.num_provinces

    #polygon
    fileone = open("resources/map/mapt.txt", "r")
    file = fileone.read()
    fileone.close()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.polygon_object(group_num = group)
        temp_poly.vertices = [None] * ((len(file) - 1)*2)

        for j in range(0, len(file) - 1):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices[j*2] = (float(temp[0]) / 10.0 + 820.0)*mysize
                temp_poly.vertices[j*2+1] = ((11000 - float(temp[1])) / 10.0)*mysize

        temp_poly.solid_color_coords(255,255,255)
        config.provinces[i] = province()
        config.provinces[i].render_objects[0][0] = temp_poly

        config.provinces[i].checkbox.set_source(temp_poly)
        config.provinces[i].set_id(int(map[i*2].split("]")[0][1:]))
        config.provinces[i].index = i

        config.provinces[i].inside_coord = [(int(map[i * 2].split("\t")[2].split(",")[0]) + 820)*mysize, (11000 - int(map[i * 2].split("\t")[2].split(",")[1]) * 10) *mysize/10 ]

    #province borders
    config.province_borders = cvsmgmt.scene_object()
    config.province_borders.render_objects = [[None]*int(len(map)/2)]
    fileone = open("resources/map/mapl.txt", "r")
    file = fileone.read()
    fileone.close()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):#int(len(map)/2)
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["1/" + str(group+1)])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2
        temp_poly.colors = [50] * (len(file) - 1) * 3 * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = (((float(temp[0]))) / 10 + 820)*mysize
                temp_poly.vertices_loop[j * 2 + 1] = ((11000 - float(temp[1])) / 10)*mysize

        temp_poly.convert_loop()
        config.provinces[i].border = temp_poly
        config.provinces[i].name = map[i * 2].split("\t")[1]

        config.province_borders.render_objects[0][i] = temp_poly

    #setting adjacents
    fileone = open("resources/map/mapa.txt", "r")
    file = fileone.read()
    fileone.close()
    adj = file.split("\n")
    for i in range(0,int(len(map)/2)):

        #if(config.provinces[i] != None):
        #if(config.provinces[i].id < 1400 or config.provinces[i].id >= 1600):
        temp1 = adj[1+i*2].split('\t')

        for p in range(0,len(temp1)-1):
            config.provinces[i].adjacents_border.append([])
            temp = temp1[p].split(',')

            for j in range(0, len(temp)):

                if(temp[j] != '' and temp[j] != 'False'):
                    config.provinces[i].adjacents_border[p].append(int(temp[j]))

                    if(int(temp[j]) not in config.provinces[i].adjacents):
                        config.provinces[i].adjacents.append(config.provinces[int(temp[j])])

                elif(temp[j] == 'False'):
                    config.provinces[i].adjacents_border[p].append(-1)

    #labels
    fileone = open("resources/map/map_label.txt", "r")
    file = fileone.read().split("\n")
    fileone.close()

    for i in range(0,len(config.provinces)):
        me = config.provinces[i]
        temp = file[i].split("\t")

        cvsmr.image_init(me.name)
        temp_sprite = cvsmr.sprite_object(me.name, [((float(temp[1].split(",")[0])) / 10.0 + 820.0) * mysize,
                                                    ((11000- (float(temp[1].split(",")[1]))) / 10.0) * mysize],
                                          group + 1)

        temp_sprite.sprite.update(scale_x = 0.4, scale_y = 0.4)
        temp_sprite.sprite.update(rotation = math.degrees(float(temp[2])))
        me.label = temp_sprite

def init_nations():
    file = open("resources/map/nationdata.txt", "r")
    data = file.read().split("\n")
    file.close()

    config.num_nations = len(data)
    for i in range(0,len(data)):
        temp = data[i].split("\t")

        tempnation = nation()
        tempnation.name = temp[0]
        tempnation.adjective = temp[2]
        tempnation.color = (int(temp[1][0:2],16),int(temp[1][2:4],16),int(temp[1][4:6],16))
        tempnation.id = i
        tempnation.init_label()

        config.nations.append(tempnation)
        config.nations_dict[tempnation.name] = tempnation

def init_scenarios():
    for root, dirs, files in os.walk("./scenarios"):
        for name in dirs:
            temp_scenario = scenario()
            config.scenarios.append(temp_scenario)

            #scenario map
            fileone = open("scenarios/" + name + "/map.txt","r")
            file = fileone.read().split("\n")
            fileone.close()
            for i in range(0,len(file)):
                temp = file[i].split("\t")
                temp_scenario.map[i] = (int(temp[0]),temp[1])

            #scenario info
            fileone = open("scenarios/" + name + "/info.txt", "r")
            file = fileone.read().split("\n")
            fileone.close()
            temp_scenario.name = file[0]
            temp_scenario.year = int(file[1])
            temp_scenario.month = file[2]
            temp_scenario.day = int(file[3])
            temp_scenario.description = file[4]

def init_saves():
    for root, dirs, files in os.walk("./saves"):
        for name in dirs:
            temp_save = save()
            config.saves.append(temp_save)

            #scenario map
            fileone = open("saves/" + name + "/map.txt","r")
            file = fileone.read().split("\n")
            fileone.close()
            for i in range(0,len(file)):
                temp = file[i].split("\t")
                temp_save.map[i] = (int(temp[0]),temp[1])

            fileone = open("saves/" + name + "/info.txt", "r")
            file = fileone.read().split("\n")
            fileone.close()
            temp_save.name = file[0]
            temp_save.year = int(file[1])
            temp_save.month = file[2]
            temp_save.day = int(file[3])
            temp_save.nation= file[4]

def init_datastructures():

    fileone = open("resources/universal_data.txt", "r")
    file = fileone.read().split("\n")
    fileone.close()

    config.universal_data = np.zeros((len(file), 1))
    for i in range(0, len(file)):
        config.universal_data[i] = float(file[i])

    config.province_data = np.ones((config.num_provinces,config.num_province_attributes))

    config.owner_mask = np.ones((config.num_provinces,config.num_nations)) # temp for testing

    config.nation_data = np.ones((config.num_nations,config.num_nation_attributes))

#-----------------------------------------------------------------------------------------------------------------------

def time_update():
    month_transition = False
    year_transition = False

    #Update date
    if(True):
        config.day += 1
        if(config.day == 29 and config.month == "February"):
            config.month = "March"
            config.day = 1
            month_transition = True
        elif(config.day == 31):
            if(config.month == "April"):
                config.day = 1
                config.month = "May"
                month_transition = True
            elif(config.month == "June"):
                config.day = 1
                config.month = "July"
                month_transition = True
            elif(config.month == "September"):
                config.day = 1
                config.month = "October"
                month_transition = True
            elif(config.month == "November"):
                config.day = 1
                config.month = "December"
                month_transition = True
        elif(config.day == 32):
            config.day = 1
            month_transition = True

            if(config.month == "January"):
                config.month = "February"
            elif(config.month == "March"):
                config.month = "April"
            elif(config.month == "May"):
                config.month = "June"
            elif(config.month == "July"):
                config.month = "August"
            elif(config.month == "August"):
                config.month = "September"
            elif(config.month == "October"):
                config.month = "November"
            elif(config.month == "December"):
                config.month = "January"
                year_transition = True

        config.menus["in_game_menu"].elements[0].render_objects[0][0].label.text = str(config.day) + "/" + config.month + "/" + str(config.year)

    calculations.demographics()
    calculations.agriculture()
    calculations.population()

def draw_nation_borders():
    # nation borders
    config.nation_borders = cvsmgmt.scene_object()
    config.nation_borders.render_objects = [[None] * config.num_provinces]

    #internal nation borders
    for i in range(0, config.num_provinces):
        me = config.provinces[i]

        temp_line = cvsmr.line_object(config.line_groups["2/3"])
        config.nation_borders.render_objects[0][i] = temp_line
        if(me.nation != None):

            counter = 0

            for j in range(0, len(me.adjacents_border)):
                flag = False
                for p in range(0, len(me.adjacents_border[j])):
                    tempadj = me.adjacents_border[j][p]

                    if(tempadj != -1):
                        tempadjprov = config.provinces[tempadj]

                        if(
                           tempadjprov != False and tempadjprov.nation == None or
                           tempadjprov != False and tempadjprov.nation.id != me.nation.id
                        ):

                            flag = True
                            counter += 1
                            break
                if(not flag):
                    counter = 0

                if(counter > 1):
                    temp_line.vertices.append(me.border.vertices[(j-1)*4])
                    temp_line.vertices.append(me.border.vertices[(j-1) * 4 + 1])
                    temp_line.vertices.append(me.border.vertices[((j-1)*4 + 2) % len(me.border.vertices)])
                    temp_line.vertices.append(me.border.vertices[((j-1) * 4 + 3) % len(me.border.vertices)])

        temp_line.solid_color_coords(40, 40, 40)

    #lonely border, always a nation border, stored as a single line_object in render_objects[1][0]
    for i in range(0, config.num_provinces):
        me = config.provinces[i]
        temp_line = config.nation_borders.render_objects[0][i]

        for j in range(0,len(me.adjacents_border)):
            nflag = False
            pflag = False

            for p in range(0, len(me.adjacents_border[(j+1)%len(me.adjacents_border)])):

                if(me.adjacents_border[(j+1)%len(me.adjacents_border)][p] == -1):
                    nflag = True

            for p in range(0, len(me.adjacents_border[(j-1)%len(me.adjacents_border)])):

                if(me.adjacents_border[(j-1)%len(me.adjacents_border)][p] == -1):
                    pflag = True

            if(nflag):
                temp_line.vertices.append(me.border.vertices[(j) * 4       % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[(j * 4 + 1)   % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j) * 4 + 2) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j) * 4 + 3) % len(me.border.vertices)])

            elif(pflag):
                temp_line.vertices.append(me.border.vertices[(j-1) * 4 % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j-1) * 4 + 1) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 2) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 3) % len(me.border.vertices)])

        temp_line.solid_color_coords(40, 40, 40)
