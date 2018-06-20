import cvsmr, cvsmgmt
import config

class province(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self, group_num = 1)
        self.render_objects=[[None],[None]]
        self.handlers[0] = True
        self.handlers[3] = True
        self.handlers[4] = True
        self.handlers[5] = True

        self.name = None
        self.nation = None

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

def init_provinces():
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

        temp_poly.solid_color_coords((i*100)%101,(i*5)%16 + 50, 100+ (i*13) % 23)
        config.provinces[i] = province()
        config.provinces[i].render_objects[0][0] = temp_poly
        config.provinces[i].checkbox.set_source(temp_poly)

    file = open("resources/map/mapl.txt", "r").read()
    map = file.split("\n")
    for i in range(0,int(len(map)/2)):#int(len(map)/2)
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["1/1"])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2
        temp_poly.colors = [255] * (len(file) - 1) * 3 * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = ((float(temp[0])))
                temp_poly.vertices_loop[j * 2 + 1] = 11000 - float(temp[1])

        temp_poly.convert_loop()
        config.provinces[i].render_objects[1][0] = temp_poly
        config.provinces[i].add_to_scene()
