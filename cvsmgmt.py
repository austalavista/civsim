#infrastructure for supporting game engine stuff

import config
import time

class scene_object:
    def __init__(self, group_num = 0):
        self.group_num = group_num
        self.checkbox = checkbox(group_num)
        self.render_objects = [] #should be a 2d array
        self.scene_index = None
        self.handlers = [False,False,False,False,False,False,False]

    def default_checkbox(self,source):
        self.checkbox.set_source(source)

    def add_to_scene(self):
        for i in range(0, config.scene_objects_size):
            if(config.scene_objects[i] == None):
                self.scene_index = i
                config.scene_objects[i] = self
                break

        for i in range(0,len(self.render_objects)):
            for j in range(0,len(self.render_objects[i])):
                if(self.render_objects[i][j] != None):
                    self.render_objects[i][j].add()

    def remove_from_scene(self):

        if(self.scene_index != None):
            for i in range(0,len(self.render_objects)):
                for j in range(0,len(self.render_objects[i])):
                    self.render_objects[i][j].remove()

            config.scene_objects[self.scene_index] = None
            self.scene_index = None

    def coords(self,x,y):

        for i in range(0, len(self.render_objects)):
            for j in range(0, len(self.render_objects[i])):
                self.render_objects[i][j].coords(x,y)

        self.checkbox.update_source()

    def nodrag_click_scene(self,x,y):
        self.nodrag_x = x
        self.nodrag_y = y

        self.nodrag = True

    def nodrag_leftdrag_scene(self,x,y):
        config.scene_transformation_group.fcoords((x-self.nodrag_x), (y-self.nodrag_y))

        self.nodrag_x = x
        self.nodrag_y = y

        self.nodrag = False

    def zoom(self,x,y,scroll_y):
        if (scroll_y > 0):
            config.scene_transformation_group.fscale(2, 2)
            config.scene_transformation_group.fcoords(-1*x, -1*y)
        else:
            config.scene_transformation_group.fscale(0.5, 0.5)
            config.scene_transformation_group.fcoords( x/2, y/2)

class checkbox:
    def __init__(self, group = 0):
        self.group = group

        self.source = None

        self.broad_checkbox = None
        self.narrow_checkbox = None

        self.narrow_check = False
        self.triangles = False

    def set_source(self, source):
        #does not support label_object

        self.source = source

        if(source.render_type == "sprite"):
            self.broad_checkbox = [self.source.anchor[0],self.source.anchor[1],
                                   self.source.anchor[0] + self.source.width, self.source.anchor[1] + self.source.height]

        elif(source.render_type == "polygon"):
            self.narrow_check = True
            self.triangles = True

            self.max_x = source.vertices[0]
            self.min_x = source.vertices[0]
            self.max_y = source.vertices[1]
            self.min_y = source.vertices[1]

            for i in range(2, len(source.vertices)):

                if( i % 2 == 0):
                    if(source.vertices[i] < self.min_x):
                        self.min_x = source.vertices[i]
                    elif(source.vertices[i] > self.max_x):
                        self.max_x = source.vertices[i]
                else:
                    if (source.vertices[i] < self.min_y):
                        self.min_y = source.vertices[i]
                    elif (source.vertices[i] > self.max_y):
                        self.max_y = source.vertices[i]

            self.broad_checkbox = [self.min_x, self.min_y,
                                   self.max_x, self.max_y]

            self.narrow_checkbox = source.vertices #dont double dcoords this!

    def update_source(self):
        if (self.source.render_type == "sprite"):
            self.broad_checkbox = [self.source.anchor[0], self.source.anchor[1],
                                   self.source.anchor[0] + self.source.width,
                                   self.source.anchor[1] + self.source.height]

        elif (self.source.render_type == "polygon"):
            self.narrow_check = True
            self.triangles = True

            self.max_x = source.vertices[0]
            self.min_x = source.vertices[0]
            self.max_y = source.vertices[1]
            self.min_y = source.vertices[2]

            for i in range(2, len(source.vertices)):

                if (i % 2 == 0):
                    if (source.vertices[i] < self.min_x):
                        self.min_x = source.vertices[i]
                    elif (source.vertices > self.max_x):
                        self.max_x = source.vertices[i]
                else:
                    if (source.vertices[i] < self.min_y):
                        self.min_y = source.vertices[i]
                    elif (source.vertices > self.max_y):
                        self.max_y = source.vertices[i]

            self.broad_checkbox = [self.min_x, self.min_y,
                                   self.max_x, self.min_y]

            self.narrow_checkbox = source.vertices  # dont double dcoords this!

class update_entry:
    #animation and event entries are executed only on update()

    def __init__(self, function = None, args = None):
        self.function = function
        self.args = args

        self.queued = False
        self.index = None

        self.timer = 0

    def run(self):

        if(self.timer == 0):

            if(self.args != None):
                self.function(self.args)
            else:
                self.function()

            self.remove()

        else:
            self.timer -= 1

    def remove(self):
        self.queued = False
        config.update_queue[self.index] = None
        self.index = None

    def add(self, countdown = 0):
        if(self.queued == False):
            for i in range(0,config.update_queue_size):
                if(config.update_queue[i] == None):
                    self.queued = True
                    self.timer = countdown
                    self.index = i

                    config.update_queue[i] = self
                    break

class release_handler_entry(update_entry):
    def __init__(self, args = None):
        update_entry.__init__(self, args = args)

    def run(self):
        if (self.timer == 0):

            self.function(self.args[0], self.args[1])

            self.remove()

        else:
            self.timer -= 1

class drag_handler_entry(update_entry):
    def __init__(self, args = None):
        update_entry.__init__(self, args=args)

    def run(self):
        if (self.timer == 0):

            self.function(self.args[0], self.args[1], self.args[2], self.args[3])

            self.remove()

        else:
            self.timer -= 1
#-----------------------------------------------------------------------------------------------------------------------
