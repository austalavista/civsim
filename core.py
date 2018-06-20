import os
import cvsmr, cvsmgmt
import config

class scenario:
    def __init__(self):
        self.map = [None]*1500

    def set(self):
        for i in range(0,len(config.provinces)):
            if(config.provinces[i] != None and self.map[i] != None):
                config.provinces[i].set_nation(self.map[i])
            else:
                print(config.provinces[i], self.map[i], i)
                break



class nation:
    def __init__(self):
        self.color = None
        self.name = None
        self.adjective = None

        self.provinces = []

class province(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, group_num = 1)
        self.render_objects=[[None]]
        self.handlers[0] = True
        self.handlers[3] = True
        self.handlers[4] = True
        self.handlers[5] = True

        self.border = None
        self.name = None
        self.nation = None

    def set_nation(self, nation):
        self.nation = config.nations[nation]
        self.render_objects[0][0].solid_color_coords(self.nation.color[0], self.nation.color[1], self.nation.color[2])
        self.render_objects[0][0].remove()
        self.render_objects[0][0].add()

    def handler_leftclick(self,x,y):
        config.click_selected = self

        self.nodrag_click_scene(x,y)

    def handler_leftdrag(self,x,y,dx,dy):
        self.nodrag_leftdrag_scene(x,y)

    def handler_release(self,x,y):
        if(self.nodrag):
            self.remove_from_scene()

    def handler_scroll(self,x,y,scroll_x,scroll_y):
        self.zoom(x,y,scroll_y)

#----------------------------------------------------------------------------------------------------------------------

def init_provinces():
    #polygon
    file = open("resources/map/mapt.txt", "r").read()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):
        file = map[i*2+1].split("\t")

        if(int(map[i*2].split("]")[0][1:]) >= 1400):
            temp_poly = cvsmr.polygon_object(0)
        else:
            temp_poly = cvsmr.polygon_object(1)

        temp_poly.vertices = [None] * ((len(file) - 1)*2)

        for j in range(0, len(file) - 1):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices[j*2] = float(temp[0])
                temp_poly.vertices[j*2+1] = (11000 - float(temp[1]))

        temp_poly.solid_color_coords(0,0,0)
        config.provinces[i] = province()
        config.provinces[i].render_objects[0][0] = temp_poly
        config.provinces[i].checkbox.set_source(temp_poly)

    #borders
    config.province_borders = cvsmgmt.scene_object()
    config.province_borders.render_objects = [[None]*int(len(map)/2)]

    file = open("resources/map/mapl.txt", "r").read()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):#int(len(map)/2)
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["1/1"])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2
        temp_poly.colors = [50] * (len(file) - 1) * 3 * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = ((float(temp[0])))
                temp_poly.vertices_loop[j * 2 + 1] = 11000 - float(temp[1])

        temp_poly.convert_loop()
        config.provinces[i].border = temp_poly
        config.provinces[i].add_to_scene()

        config.province_borders.render_objects[0][i] = temp_poly
    config.province_borders.add_to_scene()

def init_nations():
    file = open("resources/map/nationdata.txt", "r").read()
    data = file.split("\n")

    for i in range(0,len(data)):
        temp = data[i].split("\t")

        tempnation = nation()
        tempnation.name = temp[0]
        tempnation.adjective = temp[2]
        tempnation.color = (int(temp[1][0:2],16),int(temp[1][2:4],16),int(temp[1][4:6],16))

        config.nations[tempnation.name] = tempnation

def init_scenarios():
    for root, dirs, files in os.walk("./scenarios"):
        for name in dirs:
            config.scenarios[name] = scenario()

            #scenario map
            file = open("scenarios/" + name + "/map.txt","r").read().split("\n")
            for i in range(0,len(file)):
                config.scenarios[name].map[i] = file[i].split("\t")[1]


