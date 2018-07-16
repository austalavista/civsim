import os
import time
import cvsmr, cvsmgmt
import config
import numpy as np

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
            if(config.provinces[i] != None):
                while(self.map[self.index][0] < config.provinces[i].id):
                    self.index += 1
                if(self.map[self.index][0] == config.provinces[i].id):
                    config.provinces[i].set_nation(self.map[self.index][1])

        config.day = self.day
        config.month = self.month
        config.year = self.year

class nation:
    def __init__(self):
        self.color = None
        self.name = None
        self.adjective = None

        self.border = None
        self.id = None

        self.owner_mask = None

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

        self.adjacents_border = []
        self.adjacents = []
        self.name = None
        self.nation = None
        self.id = None
        self.inside_coord = None

        self.on_screened = False

    def set_nation(self, nation):
        if(nation != None):
            self.nation = config.nations[nation]
            self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1], self.nation.color[2])
            self.render_objects[0][0].update_color()
        else:
            self.nation = None
            self.render_objects[0][0].solid_color_coords(255,255,255)
            self.render_objects[0][0].update_color()

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
        self.nodrag_leftdrag_scene(x,y)

    def handler_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom(x, y, scroll_y)

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

        config.provinces[i].name = map[i*2].split("\t")[1]

        config.provinces[i].inside_coord = [(int(map[i * 2].split("\t")[2].split(",")[0]) + 820)*mysize, (11000 - int(map[i * 2].split("\t")[2].split(",")[1]) * 10) *mysize/10 ]
        config.provinces[i].label = (cvsmr.label_object(config.provinces[i].name,config.provinces[i].inside_coord,3 ))
        config.provinces[i].label.set_style(font_size = 11)

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

        config.province_borders.render_objects[0][i] = temp_poly

    #setting adjacents
    fileone = open("resources/map/mapa.txt", "r")
    file = fileone.read()
    fileone.close()
    adj = file.split("\n")
    for i in range(0,int(len(map)/2)):
        if(config.provinces[i] != None):
            if(config.provinces[i].id < 1400 or config.provinces[i].id >= 1600):
                temp = adj[1+i*2].split('\t')

                for j in range(0,len(temp)):
                    if(temp[j] != '' and temp[j] != 'False'):
                        config.provinces[i].adjacents_border.append(int(temp[j]))

                        if(int(temp[j]) not in config.provinces[i].adjacents):
                            config.provinces[i].adjacents.append(int(temp[j]))

                    elif(temp[j] == 'False'):
                        config.provinces[i].adjacents_border.append(-1)

    #province data
    config.province_data = np.zeros((config.num_provinces, config.num_province_attributes))

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

        config.nations[tempnation.name] = tempnation

        #owner mask
        tempnation.owner_mask  = np.zeros((config.num_provinces,1))

    #nation data
    config.nation_data = np.zeros((config.num_nations, config.num_nation_attributes))

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

def draw_nation_borders():
    # nation borders
    config.nation_borders = cvsmgmt.scene_object()
    config.nation_borders.render_objects = [[None] * config.num_provinces]
    index = 0
    for i in range(0, config.num_provinces):
        if(config.provinces[i] != None and config.provinces[i].nation != None):
            temp_line = cvsmr.line_object(config.line_groups["2/3"])
            config.nation_borders.render_objects[0][index] = temp_line
            #config.provinces[i].nation.border = temp_line

            for j in range(0, len(config.provinces[i].adjacents_border)):

                if (config.provinces[i].adjacents_border[j] == -1 or config.provinces[(config.provinces[i].adjacents_border[j])].nation == None or config.provinces[(config.provinces[i].adjacents_border[j])].nation.id != config.provinces[i].nation.id):
                    if(config.provinces[i].adjacents_border[(j+1)%len(config.provinces[i].adjacents_border)] == -1 or config.provinces[(config.provinces[i].adjacents_border[(j+1)%len(config.provinces[i].adjacents_border)])].nation == None or config.provinces[(config.provinces[i].adjacents_border[(j+1)%len(config.provinces[i].adjacents_border)])].nation.id != config.provinces[i].nation.id):

                        temp_line.vertices.append(config.provinces[i].border.vertices[j*4])
                        temp_line.vertices.append(config.provinces[i].border.vertices[j * 4 + 1])
                        temp_line.vertices.append(config.provinces[i].border.vertices[(j*4 + 2) % len(config.provinces[i].border.vertices)])
                        temp_line.vertices.append(config.provinces[i].border.vertices[(j * 4 + 3) % len(config.provinces[i].border.vertices)])

            temp_line.solid_color_coords(40, 40, 40)

            index += 1

