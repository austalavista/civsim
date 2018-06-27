import os
import cvsmr, cvsmgmt
import config

class scenario:
    def __init__(self):
        self.map = [None]*916

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

class save:
    def __init__(self):
        self.map = [None]*916

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

class nation:
    def __init__(self):
        self.color = None
        self.name = None
        self.adjective = None

        self.provinces = []
        self.border = None
        self.id = None

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

    def set_nation(self, nation):
        self.nation = config.nations[nation]
        self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1], self.nation.color[2])
        self.render_objects[0][0].update_color()

    def set_id(self, id):
        self.id = id
        config.provinces_id[str(id)] = self

    def handler_leftclick(self,x,y):
        config.click_selected = self

        self.nodrag_click_scene(x,y)

    def handler_leftdrag(self,x,y,dx,dy):
        self.nodrag_leftdrag_scene(x,y)

    def handler_release(self,x,y):
        if(self.nodrag):
            if(self.nation != None):
                config.menus["play_menu"].elements[7].set_province(self.name)
                config.menus["play_menu"].elements[7].set_nation(self.nation.name)


    def handler_scroll(self,x,y,scroll_x,scroll_y):
        self.zoom(x,y,scroll_y)

class ocean(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self,0)
        self.handlers[0] = True
        self.handlers[5] = True
        self.handlers[3] = True

        self.render_objects = [[cvsmr.sprite_object("ocean", [0,0], 0)]]
        self.checkbox.set_source(self.render_objects[0][0])

    def handler_leftclick(self,x,y):
        config.click_selected = self

        self.nodrag_click_scene(x,y)

    def handler_leftdrag(self,x,y,dx,dy):
        self.nodrag_leftdrag_scene(x,y)

    def handler_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom(x, y, scroll_y)

#----------------------------------------------------------------------------------------------------------------------

def init_provinces(group):
    #polygon
    file = open("resources/map/mapt.txt", "r").read()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.polygon_object(group_num = group)
        temp_poly.vertices = [None] * ((len(file) - 1)*2)

        for j in range(0, len(file) - 1):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices[j*2] = float(temp[0]) / 10.0 + 820.0
                temp_poly.vertices[j*2+1] = (11000 - float(temp[1])) / 10.0

        temp_poly.solid_color_coords(255,255,255)
        config.provinces[i] = province()
        config.provinces[i].render_objects[0][0] = temp_poly

        config.provinces[i].checkbox.set_source(temp_poly)
        config.provinces[i].set_id(int(map[i*2].split("]")[0][1:]))

        config.provinces[i].name = map[i*2].split("\t")[1]

        config.provinces[i].inside_coord = [int(map[i * 2].split("\t")[2].split(",")[0]) + 820, (11000 - int(map[i * 2].split("\t")[2].split(",")[1]) * 10) / 10]

    #province borders
    config.province_borders = cvsmgmt.scene_object()
    config.province_borders.render_objects = [[None]*int(len(map)/2)]
    file = open("resources/map/mapl.txt", "r").read()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):#int(len(map)/2)
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["1/" + str(group+1)])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2
        temp_poly.colors = [50] * (len(file) - 1) * 3 * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = ((float(temp[0]))) / 10 + 820
                temp_poly.vertices_loop[j * 2 + 1] = (11000 - float(temp[1])) / 10

        temp_poly.convert_loop()
        config.provinces[i].border = temp_poly

        config.province_borders.render_objects[0][i] = temp_poly

    #setting adjacents
    file = open("resources/map/mapa.txt", "r").read()
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

def init_nations():
    file = open("resources/map/nationdata.txt", "r").read()
    data = file.split("\n")

    for i in range(0,len(data)):
        temp = data[i].split("\t")

        tempnation = nation()
        tempnation.name = temp[0]
        tempnation.adjective = temp[2]
        tempnation.color = (int(temp[1][0:2],16),int(temp[1][2:4],16),int(temp[1][4:6],16))
        tempnation.id = i

        config.nations[tempnation.name] = tempnation

def init_scenarios():
    for root, dirs, files in os.walk("./scenarios"):
        for name in dirs:
            temp_scenario = scenario()
            config.scenarios.append(temp_scenario)

            #scenario map
            file = open("scenarios/" + name + "/map.txt","r").read().split("\n")
            for i in range(0,len(file)):
                temp = file[i].split("\t")
                temp_scenario.map[i] = (int(temp[0]),temp[1])

            file = open("scenarios/" + name + "/info.txt", "r").read().split("\n")
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
            file = open("saves/" + name + "/map.txt","r").read().split("\n")
            for i in range(0,len(file)):
                temp = file[i].split("\t")
                temp_save.map[i] = (int(temp[0]),temp[1])

            file = open("saves/" + name + "/info.txt", "r").read().split("\n")
            temp_save.name = file[0]
            temp_save.year = int(file[1])
            temp_save.month = file[2]
            temp_save.day = int(file[3])
            temp_save.nation= file[4]

def draw_nation_borders():
    # nation borders
    config.nation_borders = cvsmgmt.scene_object()
    config.nation_borders.render_objects = [[None] * 916]
    index = 0
    for i in range(0, 1500):
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
