import os
import time
import cvsmr, cvsmgmt
import config
import numpy as np
import calculations
import math

class scenario:
    def __init__(self):
        self.map = [None] * config.num_provinces

        self.year = None
        self.month = None
        self.day = None
        self.name = None

        self.description = None

    def set(self):
        self.index = 0
        for i in range(0, len(config.provinces)):
            if (config.provinces[i] != None):
                while (self.map[self.index][0] < config.provinces[i].id):
                    self.index += 1
                if (self.map[self.index][0] == config.provinces[i].id):
                    config.provinces[i].set_nation(self.map[self.index][1])

        config.day = self.day
        config.month = self.month
        config.year = self.year

        config.nation_borders.remove_from_scene()
        draw_nation_borders()
        config.nation_borders.add_to_scene()

        for i in range(0, config.num_nations):
            config.nations[i].add_provinces()
            config.nations[i].draw_label()

        zoom_dependant_update(True)

class save:
    def __init__(self):
        self.map = [None] * config.num_provinces

        self.year = None
        self.month = None
        self.day = None

        self.nation = None
        self.name = None

    def set(self):
        self.index = 0
        for i in range(0, len(config.provinces)):
            if (config.provinces[i] != None):
                while (self.map[self.index][0] < config.provinces[i].id):
                    self.index += 1
                if (self.map[self.index][0] == config.provinces[i].id):
                    config.provinces[i].set_nation(self.map[self.index][1])

        config.day = self.day
        config.month = self.month
        config.year = self.year

        config.nation_borders.remove_from_scene()
        draw_nation_borders()
        config.nation_borders.add_to_scene()

        for i in range(0, config.num_nations):
            config.nations[i].add_provinces()
            config.nations[i].draw_label()

        zoom_dependant_update(True)

class nation:
    def __init__(self):
        self.color = None
        self.name = None
        self.adjective = None

        self.id = None  # same as index

        self.borders = []  # 2D, array of array of borders of each body
        self.provinces = []
        self.num_provinces = 0

        self.body_labels = []  # 3D, 1st dimension is for each body, 2nd dimension has index 0 as array of label letters, index 1 as its scale
        self.test_line = None

    def add_provinces(self):
        # populates / refreshes list of provinces and their borders

        self.provinces = []

        # add to province list
        self.index = 0
        for i in range(config.num_provinces):
            if (config.provinces[i].nation != None and config.provinces[i].nation.id == self.id):
                self.provinces.append(config.provinces[i])
                config.provinces[i].nation_index = self.index
                self.index += 1

        self.num_provinces = len(self.provinces)

        self.temp_bodies = [[None] * self.num_provinces,  # secondary body
                            [None] * self.num_provinces]  # whether a province has been seen
        self.bodies = []
        self.bodies_count = [0]

        # make bodies
        for i in range(0, self.num_provinces):

            if (self.temp_bodies[1][i] == None):

                recursive_add_prov(self.provinces[i], self.temp_bodies, self.id, self.bodies_count)

                if (self.bodies_count[0] > 5):
                    self.bodies.append(self.temp_bodies[0])

                self.bodies_count[0] = 0
            self.temp_bodies[0] = [None] * self.num_provinces

        self.temp_bodies = None

    def init_label(self):

        cvsmr.image_init(self.name + "-n")
        self.temp = cvsmr.sprite_object(self.name + "-n", [0, 0], 0)
        self.raw_length = self.temp.sprite.width
        self.raw_height = self.temp.sprite.height
        self.temp = None

    def draw_label(self):
        self.body_labels = []

        # Make a label for each body
        for r in range(0, len(self.bodies)):

            # Make a new label for this body
            self.body_labels.append([cvsmr.sprite_object(self.name + "-n", [0, 0], 5), None])

            # Find bounds for the body
            self.maxx = 0
            self.minx = 99999999
            self.maxy = 0
            self.miny = 99999999
            for i in range(1, len(self.bodies[r])):
                if (self.bodies[r][i] != None):
                    if (self.maxx < self.bodies[r][i].centroid[0]):
                        self.maxx = self.bodies[r][i].centroid[0]
                    elif (self.minx > self.bodies[r][i].centroid[0]):
                        self.minx = self.bodies[r][i].centroid[0]

                    if (self.maxy < self.bodies[r][i].centroid[1]):
                        self.maxy = self.bodies[r][i].centroid[1]
                    elif (self.miny > self.bodies[r][i].centroid[1]):
                        self.miny = self.bodies[r][i].centroid[1]

            self.sumx = 0
            self.sumy = 0
            self.scoresum = 0
            self.body_num = 0
            for i in range(0, len(self.bodies[r])):
                if (self.bodies[r][i] != None):
                    self.sumx += self.bodies[r][i].centroid[0] * self.bodies[r][i].centroid_score
                    self.sumy += self.bodies[r][i].centroid[1] * self.bodies[r][i].centroid_score

                    self.scoresum += self.bodies[r][i].centroid_score

            self.avgx = self.sumx / (self.scoresum)
            self.avgy = self.sumy / (self.scoresum)

            if (self.maxx - self.minx > (self.maxy - self.miny) * 0.8):
                self.leftxsum = 0
                self.rightxsum = 0

                self.leftysum = 0
                self.rightysum = 0

                self.leftxscore = 0
                self.rightxscore = 0

                self.leftyscore = 0
                self.rightyscore = 0

                for i in range(0, len(self.bodies[r])):
                    if (self.bodies[r][i] != None):

                        if (self.bodies[r][i].centroid[0] <= self.avgx):

                            self.leftxsum += self.bodies[r][i].centroid[0] * self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])
                            self.leftxscore += self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])

                            self.leftysum += self.bodies[r][i].centroid[1] * self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])
                            self.leftyscore += self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])

                        else:
                            self.rightxsum += self.bodies[r][i].centroid[0] * self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])
                            self.rightxscore += self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])

                            self.rightysum += self.bodies[r][i].centroid[1] * self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])
                            self.rightyscore += self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])

                self.point1 = [self.leftxsum / self.leftxscore, self.leftysum / self.leftyscore]
                self.point2 = [self.rightxsum / self.rightxscore, self.rightysum / self.rightyscore]
            else:
                self.topxsum = 0
                self.topysum = 0

                self.bottomxsum = 0
                self.bottomysum = 0

                self.topxscore = 0
                self.topyscore = 0

                self.bottomxscore = 0
                self.bottomyscore = 0

                for i in range(0, len(self.bodies[r])):
                    if (self.bodies[r][i] != None):

                        if (self.bodies[r][i].centroid[1] <= self.avgy):

                            self.bottomxsum += self.bodies[r][i].centroid[0] * self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])
                            self.bottomxscore += self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])

                            self.bottomysum += self.bodies[r][i].centroid[1] * self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])
                            self.bottomyscore += self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])

                        else:

                            self.topxsum += self.bodies[r][i].centroid[0] * self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])
                            self.topxscore += self.bodies[r][i].centroid_score * abs(
                                self.avgx - self.bodies[r][i].centroid[0])

                            self.topysum += self.bodies[r][i].centroid[1] * self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])
                            self.topyscore += self.bodies[r][i].centroid_score * abs(
                                self.avgy - self.bodies[r][i].centroid[1])

                self.point1 = [self.topxsum / self.topxscore, self.topysum / self.topyscore]
                self.point2 = [self.bottomxsum / self.bottomxscore, self.bottomysum / self.bottomyscore]

                if (self.point1[0] > self.point2[0]):
                    self.temp = self.point1
                    self.point1 = self.point2
                    self.point2 = self.temp

            self.length = ((self.point2[0] - self.point1[0]) ** 2 + (self.point2[1] - self.point1[1]) ** 2) ** 0.5
            self.line_vec = [(self.point2[0] - self.point1[0]) / self.length,
                             (self.point2[1] - self.point1[1]) / self.length]

            self.angle = math.degrees(math.asin(self.line_vec[1]))

            self.length_scale = self.length / self.raw_length
            self.final_scale = self.length_scale
            self.perp = [self.line_vec[1] * self.raw_height * self.final_scale / 2,
                         -1 * self.line_vec[0] * self.raw_height * self.final_scale / 2]

            # make_label
            self.length_progress = 0

            self.body_labels[r][0].sprite.update(x=self.point1[0] + self.perp[0],
                                                 y=self.point1[1] + self.perp[1],
                                                 scale_x=self.final_scale,
                                                 scale_y=self.final_scale,
                                                 rotation=-1 * self.angle)

            self.body_labels[r][1] = self.final_scale

            '''
            self.test_line.append(cvsmr.line_object(config.line_groups['2/3']))
            self.test_line[r].vertices = [self.point1[0], self.point1[1],
                                          self.point2[0], self.point2[1]]
            self.test_line[r].solid_color_coords(255, 255, 255)
            self.test_line[r].add()
            '''

    def add_labels(self):
        for r in range(0, len(self.body_labels)):
            self.body_labels[r][0].add()

    def remove_labels(self):
        for r in range(0, len(self.body_labels)):
            self.body_labels[r][0].remove()

class province(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, group_num=1)
        self.render_objects = [[None]]
        self.handlers[0] = True
        self.handlers[3] = True
        self.handlers[4] = True
        self.handlers[5] = True
        self.handlers[8] = True

        self.border = None
        self.label = None
        self.alt_color = (100,100,100)

        self.adjacents_border = []  # list of lists of indexes of adjacents provinces to each border vertice
        self.adjacents = []  # list of indexes of adjacent provinces

        self.name = None
        self.nation = None
        self.id = None
        self.index = None
        self.inside_coord = None

        self.centroid = None
        self.centroid_score = None

        self.nation_index = None

        self.on_screened = False

    def set_nation(self, nation):

        self.prev_nation = self.nation
        if (nation != None):

            self.nation = config.nations_dict[nation]

            self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1],
                                                         self.nation.color[2])
            self.render_objects[0][0].update_color()

            if (config.state == "in_game_menu"):
                self.draw_nation_borders()

                self.nation.add_provinces()
                if (self.prev_nation != None):
                    self.prev_nation.add_provinces()

            self.border.solid_color_coords(255 - self.nation.color[0],
                                           255 - self.nation.color[1],
                                           255 - self.nation.color[2])

            self.alt_color = (int(max(self.nation.color[0]*1.6 % 255, self.nation.color[0]*0.5 % 255)),
                              int(max(self.nation.color[1] * 1.6 % 255, self.nation.color[1] * 0.5 % 255)),
                              int(max(self.nation.color[2] * 1.6 % 255, self.nation.color[2] * 0.5 % 255)))

        else:
            self.render_objects[0][0].solid_color_coords(255, 255, 255)
            self.render_objects[0][0].update_color()

            self.border.solid_color_coords(0,
                                           0,
                                           0)
            self.alt_color = (0,0,0)

    def draw_nation_border(self):

        self.temp_line = cvsmr.line_object(config.line_groups["1/3"])
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

        zoom_dependant_update()

    def set_id(self, id):
        self.id = id
        config.provinces_id[str(id)] = self

    def on_screen(self):

        if (self.inside_coord[0] > config.screen_bound_left and
                    self.inside_coord[0] < config.screen_bound_right and
                    self.inside_coord[1] > config.screen_bound_bottom and
                    self.inside_coord[1] < config.screen_bound_top):

            self.on_screened = True
            return True
        else:
            return False

    def handler_leftclick(self, x, y):
        config.click_selected = self

        self.nodrag_click_scene(x, y)

    def handler_leftdrag(self, x, y, dx, dy):
        self.nodrag_leftdrag_scene(x, y)

        zoom_dependant_update()

    def handler_release(self, x, y):
        if (self.nodrag):
            self.select_self()


            if (config.state == "play_menu"):
                if (self.nation != None):
                    config.menus["play_menu"].elements[7].set_province(self.name)
                    config.menus["play_menu"].elements[7].set_nation(self.nation.name)

            if(config.state == "play_menu" or config.state == "in_game_menu"):
                self.border.add()
                self.render_objects[0][0].solid_color_coords(self.alt_color[0], self.alt_color[1],
                                                             self.alt_color[2])
                self.render_objects[0][0].update_color()

    def handler_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom(x, y, scroll_y)

        zoom_dependant_update(True)

    def handler_deselect(self):
        self.border.remove()
        if(self.nation != None):
            self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1],
                                                         self.nation.color[2])
            self.render_objects[0][0].update_color()
        else:
            self.render_objects[0][0].solid_color_coords(255,255,255)
            self.render_objects[0][0].update_color()

class ocean(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, 0)
        self.handlers[0] = True
        self.handlers[5] = True
        self.handlers[3] = True

        self.render_objects = [[cvsmr.sprite_object("ocean", [0, 0], 0)]]
        self.render_objects[0][0].scale(100, 100)

        self.checkbox.set_source(self.render_objects[0][0])

    def handler_leftclick(self, x, y):
        config.click_selected = self

        self.nodrag_click_scene(x, y)

    def handler_leftdrag(self, x, y, dx, dy):
        self.nodrag_leftdrag_scene(x, y)

        zoom_dependant_update()

    def handler_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom(x, y, scroll_y)

        zoom_dependant_update(True)

class terrain_map(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, 5)

        self.render_objects = [[cvsmr.sprite_object("terrain_map", [0, 0], 4)]]
        self.render_objects[0][0].scale(3.33, 3.33)
        self.render_objects[0][0].coords(8200,0)

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

# ----------------------------------------------------------------------------------------------------------------------

def calc_screen_bounds(threshold_x=100, threshold_y=100):
    config.screen_bound_left = -1 * config.scene_transformation_group.x - threshold_x
    config.screen_bound_right = abs(
        config.scene_transformation_group.x) + 1920 / config.scene_transformation_group.scale_x + threshold_x
    config.screen_bound_top = abs(
        config.scene_transformation_group.y) + 1080 / config.scene_transformation_group.scale_x + threshold_y
    config.screen_bound_bottom = -1 * config.scene_transformation_group.y - threshold_y

def recursive_add_prov(province, bodies, nation_id, bodies_count):
    for rr in range(0, len(province.adjacents)):
        # see if this adjacents is already in
        if (province.adjacents[rr].nation_index != None and
                    province.adjacents[rr].nation.id == nation_id and
                    bodies[1][province.adjacents[rr].nation_index] == None
            ):
            bodies[0][province.adjacents[rr].nation_index] = province.adjacents[rr]
            bodies[1][province.adjacents[rr].nation_index] = True

            bodies_count[0] += 1

            recursive_add_prov(province.adjacents[rr], bodies, nation_id, bodies_count)

    return

def init_provinces(group):
    mysize = 10

    fileone = open("resources/map/num.txt", "r")
    file = fileone.read()
    fileone.close()
    config.num_provinces = int(file)
    config.provinces = [None] * config.num_provinces

    # polygon
    fileone = open("resources/map/mapt.txt", "r")
    file = fileone.read()
    fileone.close()
    map = file.split("\n")
    for i in range(0, int(len(map) / 2)):
        file = map[i * 2 + 1].split("\t")

        temp_poly = cvsmr.polygon_object(group_num=group)
        temp_poly.vertices = [None] * ((len(file) - 1) * 2)

        for j in range(0, len(file) - 1):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices[j * 2] = (float(temp[0]) / 10.0 + 820.0) * mysize
                temp_poly.vertices[j * 2 + 1] = ((11000 - float(temp[1])) / 10.0) * mysize

        temp_poly.solid_color_coords(255, 255, 255)
        config.provinces[i] = province()
        config.provinces[i].render_objects[0][0] = temp_poly

        config.provinces[i].checkbox.set_source(temp_poly)
        config.provinces[i].set_id(int(map[i * 2].split("]")[0][1:]))
        config.provinces[i].index = i

        config.provinces[i].inside_coord = [(int(map[i * 2].split("\t")[2].split(",")[0]) + 820) * mysize,
                                            (11000 - int(map[i * 2].split("\t")[2].split(",")[1]) * 10) * mysize / 10]

    # province borders
    config.province_borders = cvsmgmt.scene_object()
    config.province_borders.render_objects = [[cvsmr.line_object(config.line_groups["1/" + str(group + 1)])]]
    fileone = open("resources/map/mapl.txt", "r")
    file = fileone.read()
    fileone.close()
    map = file.split("\n")
    for i in range(0, int(len(map) / 2)):  # int(len(map)/2)
        file = map[i * 2 + 1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["3/" + str(group + 3)])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = (((float(temp[0]))) / 10 + 820) * mysize
                temp_poly.vertices_loop[j * 2 + 1] = ((11000 - float(temp[1])) / 10) * mysize

        temp_poly.convert_loop()
        temp_poly.solid_color_coords(70,70,70)
        config.provinces[i].border = temp_poly
        config.provinces[i].name = map[i * 2].split("\t")[1]

        #add the completed province border loop to the uniform thing
        for i in range(0,len(temp_poly.vertices)):
            config.province_borders.render_objects[0][0].vertices.append(temp_poly.vertices[i])

    config.province_borders.render_objects[0][0].solid_color_coords(70,70,70)

    # setting adjacents
    fileone = open("resources/map/mapa.txt", "r")
    file = fileone.read()
    fileone.close()
    adj = file.split("\n")
    for i in range(0, int(len(map) / 2)):
        tempc = adj[i * 2].split('\t')
        temp1 = adj[1 + i * 2].split('\t')

        config.provinces[i].centroid = [((float(tempc[2].split(',')[0])) / 10 + 820) * mysize,
                                        ((11000 - (float(tempc[2].split(',')[1]))) / 10) * mysize]

        config.provinces[i].centroid_score = int(tempc[3])

        for p in range(0, len(temp1) - 1):
            config.provinces[i].adjacents_border.append([])
            temp = temp1[p].split(',')

            for j in range(0, len(temp)):

                if (temp[j] != '' and temp[j] != 'False'):
                    config.provinces[i].adjacents_border[p].append(int(temp[j]))

                    if (int(temp[j]) not in config.provinces[i].adjacents):
                        config.provinces[i].adjacents.append(config.provinces[int(temp[j])])

                elif (temp[j] == 'False'):
                    config.provinces[i].adjacents_border[p].append(-1)

    # labels
    fileone = open("resources/map/map_label.txt", "r")
    file = fileone.read().split("\n")
    fileone.close()

    for i in range(0, len(config.provinces)):
        me = config.provinces[i]
        temp = file[i].split("\t")

        cvsmr.image_init(me.name)
        temp_sprite = cvsmr.sprite_object(me.name, [((float(temp[1].split(",")[0])) / 10.0 + 820.0) * mysize,
                                                    ((11000 - (float(temp[1].split(",")[1]))) / 10.0) * mysize],
                                          group + 4)

        #temp_sprite.sprite.update(scale_x=0.8, scale_y=0.8)
        temp_sprite.sprite.update(rotation=math.degrees(float(temp[2])))
        me.label = temp_sprite

def init_nations():
    file = open("resources/map/nationdata.txt", "r")
    data = file.read().split("\n")
    file.close()

    config.num_nations = len(data)
    for i in range(0, len(data)):
        temp = data[i].split("\t")

        tempnation = nation()
        tempnation.name = temp[0]
        tempnation.adjective = temp[2]
        tempnation.color = (int(temp[1][0:2], 16), int(temp[1][2:4], 16), int(temp[1][4:6], 16))
        tempnation.id = i
        tempnation.init_label()

        config.nations.append(tempnation)
        config.nations_dict[tempnation.name] = tempnation

def init_scenarios():
    for root, dirs, files in os.walk("./scenarios"):
        for name in dirs:
            temp_scenario = scenario()
            config.scenarios.append(temp_scenario)

            # scenario map
            fileone = open("scenarios/" + name + "/map.txt", "r")
            file = fileone.read().split("\n")
            fileone.close()
            for i in range(0, len(file)):
                temp = file[i].split("\t")
                temp_scenario.map[i] = (int(temp[0]), temp[1])

            # scenario info
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

            # scenario map
            fileone = open("saves/" + name + "/map.txt", "r")
            file = fileone.read().split("\n")
            fileone.close()
            for i in range(0, len(file)):
                temp = file[i].split("\t")
                temp_save.map[i] = (int(temp[0]), temp[1])

            fileone = open("saves/" + name + "/info.txt", "r")
            file = fileone.read().split("\n")
            fileone.close()
            temp_save.name = file[0]
            temp_save.year = int(file[1])
            temp_save.month = file[2]
            temp_save.day = int(file[3])
            temp_save.nation = file[4]

def init_datastructures():
    fileone = open("resources/universal_data.txt", "r")
    file = fileone.read().split("\n")
    fileone.close()

    config.universal_data = np.zeros((len(file), 1))
    for i in range(0, len(file)):
        config.universal_data[i] = float(file[i])

    config.province_data = np.ones((config.num_provinces, config.num_province_attributes))

    config.owner_mask = np.ones((config.num_provinces, config.num_nations))  # temp for testing

    config.nation_data = np.ones((config.num_nations, config.num_nation_attributes))

# -----------------------------------------------------------------------------------------------------------------------

def zoom_dependant_update(zoom_changed=False):
    # province labels
    if (config.scene_transformation_group.scale_x >= 0.8):
        calc_screen_bounds()
        for i in range(0, config.num_provinces):
            if (config.provinces[i].on_screen()):
                config.provinces[i].label.add()

    elif (zoom_changed):
        for i in range(0, config.num_provinces):
            if (config.provinces[i].on_screened):
                config.provinces[i].label.remove()
                config.provinces[i].on_screened = False



    if (zoom_changed):

        # Labels
        if(config.scene_transformation_group.scale_x < 0.8):
            for j in range(0, config.num_nations):
                config.nations[j].add_labels()
        elif(config.scene_transformation_group.scale_x == 0.8):
            for j in range(0, config.num_nations):
                config.nations[j].remove_labels()
        # province borders
        if (config.scene_transformation_group.scale_x == 0.2):
            config.province_borders.render_objects[0][0].fast_show()
        elif(config.scene_transformation_group.scale_x == 0.1):
            config.province_borders.render_objects[0][0].fast_hide()

def time_update():
    month_transition = False
    year_transition = False

    # Update date
    if (True):
        config.day += 1
        if (config.day == 29 and config.month == "February"):
            config.month = "March"
            config.day = 1
            month_transition = True
        elif (config.day == 31):
            if (config.month == "April"):
                config.day = 1
                config.month = "May"
                month_transition = True
            elif (config.month == "June"):
                config.day = 1
                config.month = "July"
                month_transition = True
            elif (config.month == "September"):
                config.day = 1
                config.month = "October"
                month_transition = True
            elif (config.month == "November"):
                config.day = 1
                config.month = "December"
                month_transition = True
        elif (config.day == 32):
            config.day = 1
            month_transition = True

            if (config.month == "January"):
                config.month = "February"
            elif (config.month == "March"):
                config.month = "April"
            elif (config.month == "May"):
                config.month = "June"
            elif (config.month == "July"):
                config.month = "August"
            elif (config.month == "August"):
                config.month = "September"
            elif (config.month == "October"):
                config.month = "November"
            elif (config.month == "December"):
                config.month = "January"
                year_transition = True

        config.menus["in_game_menu"].elements[0].render_objects[0][0].label.text = str(
            config.day) + "/" + config.month + "/" + str(config.year)

    calculations.demographics()
    calculations.agriculture()
    calculations.population()

def draw_nation_borders():
    # nation borders
    config.nation_borders = cvsmgmt.scene_object()
    config.nation_borders.render_objects = [[None] * config.num_provinces]

    # internal nation borders
    for i in range(0, config.num_provinces):
        me = config.provinces[i]

        temp_line = cvsmr.line_object(config.line_groups["1/4"])
        config.nation_borders.render_objects[0][i] = temp_line
        if (me.nation != None):

            counter = 0

            for j in range(0, len(me.adjacents_border)):
                flag = False
                for p in range(0, len(me.adjacents_border[j])):
                    tempadj = me.adjacents_border[j][p]

                    if (tempadj != -1):
                        tempadjprov = config.provinces[tempadj]

                        if (
                                            tempadjprov != False and tempadjprov.nation == None or
                                            tempadjprov != False and tempadjprov.nation.id != me.nation.id
                        ):
                            flag = True
                            counter += 1
                            break
                if (not flag):
                    counter = 0

                if (counter > 1):
                    temp_line.vertices.append(me.border.vertices[(j - 1) * 4])
                    temp_line.vertices.append(me.border.vertices[(j - 1) * 4 + 1])
                    temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 2) % len(me.border.vertices)])
                    temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 3) % len(me.border.vertices)])

        #temp_line.solid_color_coords(40, 40, 40)

    # lonely border, always a nation border, stored as a single line_object in render_objects[1][0]
    for i in range(0, config.num_provinces):
        me = config.provinces[i]
        temp_line = config.nation_borders.render_objects[0][i]

        for j in range(0, len(me.adjacents_border)):
            nflag = False
            pflag = False

            for p in range(0, len(me.adjacents_border[(j + 1) % len(me.adjacents_border)])):

                if (me.adjacents_border[(j + 1) % len(me.adjacents_border)][p] == -1):
                    nflag = True

            for p in range(0, len(me.adjacents_border[(j - 1) % len(me.adjacents_border)])):

                if (me.adjacents_border[(j - 1) % len(me.adjacents_border)][p] == -1):
                    pflag = True

            if (nflag):
                temp_line.vertices.append(me.border.vertices[(j) * 4 % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[(j * 4 + 1) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j) * 4 + 2) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j) * 4 + 3) % len(me.border.vertices)])

            elif (pflag):
                temp_line.vertices.append(me.border.vertices[(j - 1) * 4 % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 1) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 2) % len(me.border.vertices)])
                temp_line.vertices.append(me.border.vertices[((j - 1) * 4 + 3) % len(me.border.vertices)])

        temp_line.solid_color_coords(10, 10, 10)

    zoom_dependant_update()