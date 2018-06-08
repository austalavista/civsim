#Rendering frameworks

import pyglet
import config
import tripy

#---BASE RENDER OBJECTS/CLASSES---
class sprite_object:
    render_type = "sprite"

    def __init__(self, image_name, anchor, group_num):
        self.sprite = pyglet.sprite.Sprite(config.sprite_textures[image_name],
                                           x=anchor[0],
                                           y=anchor[1],
                                           group=config.groups[group_num])

        self.anchor = anchor
        self.group_num = group_num

        self.scale_x = 1
        self.scale_y = 1

        self.height = self.sprite.height
        self.width = self.sprite.width

        #use sprite.position(), sprite.update()

    def switch_image(self, sprite_name):
        self.sprite.image = config.sprite_textures[sprite_name]

    def coords(self, x, y):
        self.sprite.position(x,y)
        self.anchor[0] = x
        self.anchor[1] = y

    def dcoords(self, dx, dy):
        self.anchor[0] += dx
        self.anchor[1] += dy
        self.sprite.position(self.anchor[0],self.anchor)

    def scale(self,scale_x,scale_y):
        #scaling is always wrt original size
        self.sprite.update(scale_x = scale_x, scale_y=scale_y)
        self.scale_x = scale_x
        self.scale_y = scale_y

    def add(self):
        self.sprite.batch = config.batch

    def remove(self):
        self.sprite.delete()
        self.sprite.batch=None

class polygon_object:
    render_type = "polygon"

    def __init__(self, group_num, texture_group=None, ):
        self.vertex_list = None

        self.vertices_polygon = None #comes in format [[x1,y1],[x2,y2]], need to call convert_to_triangles
        self.vertices = None #not changed for simple transformation, in triangle format
        self.vertices_temp = None # used for instantiation of vertex_list

        self.colors = None
        self.texture_coords = None
        self.texture_group = texture_group

        if(texture_group == None):
            self.group_num = 0
        else:
            self.group_num = group_num

        self.anchor = [0, 0]
        self.scale_x = 1
        self.scale_y = 1

    def coords(self, x, y):
        for i in range(0,len(self.vertex_list.vertices)):
            if(i%2 == 0):
                self.vertex_list.vertices[i] = self.vertices[i] + x
            else:
                self.vertex_list.vertices[i] = self.vertices[i] + y

        self.anchor[0] = x
        self.anchor[1] = y

    def dcoords(self, dx, dy):
        for i in range(0,len(self.vertex_list.vertices)):
            if(i%2 == 0):
                self.vertex_list.vertices[i] += dx
            else:
                self.vertex_list.vertices[i] += dy

        self.anchor[0] += dx
        self.anchor[1] += dy

    def scale(self, scale_x, scale_y):
        for i in range(0,len(self.vertex_list.vertices)):
            if(i%2 == 0):
                self.vertex_list.vertices[i] = self.vertices[i]*scale_x + self.anchor[0]
            else:
                self.vertex_list.vertices[i] = self.vertices[i]*scale_y + self.anchor[1]

        self.scale_x = scale_x
        self.scale_y = scale_y

    def convert_to_triangles(self):
        self.temp = tripy.earclip(self.vertices_polygon)
        self.vertices = [None] * (len(self.temp) * 6)
        for h in range(0, len(self.temp)):
            for l in range(0, 3):
                for u in range(0, 2):
                    self.vertices[h * 6 + l * 2 + u] = self.temp[h][l][u]

    def convert_to_triangles_remove_duplicates(self):
        for i in range(0,len(self.vertices_polygon)-1):
            if(i < len(self.vertices_polygon)-1):
                if(self.vertices_polygon[i][0] == self.vertices_polygon[i+1][0] and
                    self.vertices_polygon[i][1] == self.vertices_polygon[i + 1][1]):
                    self.vertices_polygon.pop(i+1)

    def linear_texture_coords(self, tex_anchor=[0,0],tex_xbound=1,tex_ybound=1):
        #takes a linear imprint out of texture
        #xbound and ybound are the UV coordinates to be linearly mapped to the greatest XY valued vertices. The rest of vertices are linearly scaled based on this
        #tex_anchor is in terms of UV space

        pass

    def solid_color_coords(self,red,green,blue):
        self.colors = [red,green,blue]*int(len(self.vertices)/2)

    def add(self):
        if(self.vertices_temp == None):
            self.vertices_temp = self.vertices

        for i in range(0, len(self.vertices)):
            if(i%2 == 0):
                self.vertices_temp[i] = self.vertices[i] * self.scale_x + self.anchor[0]
            else:
                self.vertices_temp[i] = self.vertices[i] * self.scale_y + self.anchor[1]

        if(self.texture_group != None):
            self.vertex_list = config.batch.add(int(len(self.vertices)/2),
                                                pyglet.gl.GL_TRIANGLES,
                                                self.texture_group,
                                                ('v2f',self.vertices_temp),
                                                ('t2f',self.texture_coords))
        else:
            self.vertex_list = config.batch.add(int(len(self.vertices) / 2),
                                                pyglet.gl.GL_TRIANGLES,
                                                config.groups[self.group_num],
                                                ('v2f', self.vertices_temp),
                                                ('c3B', self.colors))

    def remove(self):
        self.vertex_list.delete()

class line_object:
    render_object_type = "line"

    def __init__(self,line_group):
        #line type can be either 1 for line, or 0 for loop
        self.vertex_list = None

        self.vertices_loop = [] #add loop format vertices to this, then call convert_loop
        self.vertices = [] #not changed for simple transformations such as translation or scaling
        self.vertices_temp = None #used to initialize vertex_list, applies scale and translation to vertices

        self.colors = None
        self.line_group = line_group

        self.scene_object_index = None

        self.anchor = [0, 0]
        self.scale_x = 1
        self.scale_y = 1

    def coords(self, x, y):
        for i in range(0,len(self.vertex_list.vertices)):
            if(i%2 == 0):
                self.vertex_list.vertices[i] = self.vertices[i] + x
            else:
                self.vertex_list.vertices[i] = self.vertices[i] + y

        self.anchor[0] = x
        self.anchor[1] = y

    def dcoords(self, dx, dy):
        for i in range(0, len(self.vertex_list.vertices)):
            if (i % 2 == 0):
                self.vertex_list.vertices[i] += dx
            else:
                self.vertex_list.vertices[i] += dy

        self.anchor[0] += dx
        self.anchor[1] += dy

    def scale(self, scale_x, scale_y):
        for i in range(0,len(self.vertex_list.vertices)):
            if(i%2 == 0):
                self.vertex_list.vertices[i] = self.vertices[i]*scale_x + self.anchor[0]
            else:
                self.vertex_list.vertices[i] = self.vertices[i]*scale_y + self.anchor[1]

        self.scale_x = scale_x
        self.scale_y = scale_y

    def convert_loop(self):
        self.loop_size = (len(self.vertices_loop)*2)
        self.vertices = [None]* self.loop_size

        self.vertices[0] = self.vertices_loop[0]
        self.vertices[1] = self.vertices_loop[1]

        self.vertices[self.loop_size-2] = self.vertices_loop[0]
        self.vertices[self.loop_size-1] = self.vertices_loop[1]

        for i in range(1,int(len(self.vertices_loop)/2)):
            #iterates through vector pairs

            self.vertices[i * 4 - 2] = self.vertices_loop[i * 2]
            self.vertices[i * 4 - 1] = self.vertices_loop[i * 2 + 1]

            self.vertices[i * 4] = self.vertices[i * 4 - 2]
            self.vertices[i * 4 + 1] = self.vertices[i * 4 - 1]

    def solid_color_coords(self,red,green,blue):
        self.colors = [red,green,blue]*int(len(self.vertices)/2)

    def add(self):
        if(self.vertices_temp == None):
            self.vertices_temp = self.vertices

        for i in range(0, len(self.vertices)):
            if(i%2 == 0):
                self.vertices_temp[i] = self.vertices[i] * self.scale_x + self.anchor[0]
            else:
                self.vertices_temp[i] = self.vertices[i] * self.scale_y + self.anchor[1]

        self.vertex_list = config.batch.add(int(len(self.vertices)/2),
                                            pyglet.gl.GL_LINES,
                                            self.line_group,
                                            ('v2f',self.vertices_temp),
                                            ('c3B', self.colors))

    def remove(self):
        self.vertex_list.delete()

class label_object:
    render_object_type = "label"

    def __init__(self, text, anchor, group_num):
        self.label = pyglet.text.Label(text,
                                       x = anchor[0],
                                       y = anchor[1],
                                       group = config.groups[group_num])
        self.anchor = anchor
        self.group_num = group_num
        self.scene_object_index = None

        self.handlers = [False, False, False, False, False, False, False]

    def coords(self, x, y):
        self.Label.x = x
        self.Label.y = y
        self.anchor[0] = x
        self.anchor[1] = y

    def dcoords(self, dx, dy):
        self.Label.x += dx
        self.Label.y += dy
        self.anchor[0] += dx
        self.anchor[1] += dy

    def settings(self, font_name, font_size,color):
        self.Label.font_name = font_name
        self.Label.font_size = font_size
        self.Label.color = color

    def add(self):
        self.label.batch = config.batch

    def remove(self):
        self.Label.batch = None

#---GROUPS---
class line_group(pyglet.graphics.Group):
    def __init__(self, thickness,group_num):
        super(line_group, self).__init__(parent=config.groups[group_num])
        self.thickness = thickness

    def set_state(self):
        pyglet.gl.glLineWidth(self.thickness)

class transformation_group(pyglet.graphics.Group):
    def __init__(self,parent = None):
        super(transformation_group, self).__init__(parent=parent)

        self.x = 0.0
        self.y = 0.0

        self.scale_x = 1.0
        self.scale_y = 1.0

    def set_state(self):
        pyglet.graphics.glPushMatrix()#relative to absolute

        pyglet.graphics.glScalef(self.scale_x,self.scale_y,1)
        pyglet.graphics.glTranslatef(self.x,self.y,0)

    def unset_state(self):
        pyglet.graphics.glPopMatrix()

    def coords(self,x,y):
        self.x = x
        self.y = y

    def dcoords(self,dx,dy):
        self.x += dx
        self.y += dy

    def fcoords(self,dx,dy):
        self.x += dx / self.scale_x
        self.y += dy / self.scale_y

    def scale(self, scale_x, scale_y):
        self.scale_x = scale_x
        self.scale_y = scale_y

    def dscale(self,dscale_x,dscale_y):
        self.scale_x += dscale_x
        self.scale_y += dscale_y

    def fscale(self, fscale_x,fscale_y):
        self.scale_x = self.scale_x * fscale_x
        self.scale_y = self.scale_y * fscale_y

#---INITIALIZATION---
def ordered_transformation_groups_init():
    config.global_transformation_group = transformation_group()

    config.scene_ordered_group = pyglet.graphics.OrderedGroup(0, parent = config.global_transformation_group)
    config.menu_ordered_group = pyglet.graphics.OrderedGroup(1, parent = config.global_transformation_group)

    config.scene_transformation_group = transformation_group(parent = config.scene_ordered_group)

    for i in range(0,config.num_scene_groups):
        config.groups.append(pyglet.graphics.OrderedGroup(i,parent=config.scene_transformation_group))

    for i in range(config.num_scene_groups,config.num_scene_groups + config.num_menu_groups):
        config.groups.append(pyglet.graphics.OrderedGroup(i,parent=config.menu_ordered_group))

def line_groups_init():
    #config.line_groups[name] = line_group(thickness,group_num)
    config.line_groups["2/3"] = line_group(2, 3)
    config.line_groups["1/3"] = line_group(1, 3)
    config.line_groups["2/2"] = line_group(2, 2)

def texture_groups_init():
    #config.texture_groups[name] = pyglet.graphics.TextureGroup(pyglet.image.load(file).get_texture(),parent=config.groups[group_num])
    pass

def sprite_texture_init():
    config.sprite_textures["main_menu"] = pyglet.resource.image("main_menu.png")
    config.sprite_textures["main_menu_play"] = pyglet.resource.image("main_menu_play.png")
    config.sprite_textures["main_menu_play_c"] = pyglet.resource.image("main_menu_play_c.png")
    config.sprite_textures["main_menu_settings_c"] = pyglet.resource.image("main_menu_settings_c.png")
    config.sprite_textures["main_menu_settings"] = pyglet.resource.image("main_menu_settings.png")
    config.sprite_textures["main_menu_exitgame_c"] = pyglet.resource.image("main_menu_exitgame_c.png")
    config.sprite_textures["main_menu_exitgame"] = pyglet.resource.image("main_menu_exitgame.png")
    config.sprite_textures["mainscreen"] = pyglet.resource.image("mainscreen.png")

#---CUSTOM---
