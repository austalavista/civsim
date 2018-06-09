#Menu baseclasses and their custom derivatives

import pyglet
import config
import cvsmr, cvsmgmt, cvsms

#---BASE MENU OBJECTS/CLASSES------------------------------------------------------------------------------------------
class base_window():
    def __init__(self, anchor, group_num = config.num_scene_groups, sprite_name = None):

        self.anchor = anchor
        self.group_num = group_num

        if(sprite_name != None):
            self.sprite = cvsmr.sprite_object(sprite_name, anchor, group_num)
        else:
            self.sprite = None

        self.elements = None
        self.elements_index = None

        self.add_to_scene_entry = cvsmgmt.update_entry(self.add_to_scene_1)
        self.remove_from_scene_entry = cvsmgmt.update_entry(self.remove_from_scene_1)

    def add_to_scene(self):
        self.add_to_scene_entry.add()

    def add_to_scene_1(self):
        if(self.sprite != None):
            self.sprite.add()

        for i in range(0,len(self.elements)):
            self.elements[i].add_to_scene(self.elements_index[i])

    def remove_from_scene(self):
        self.remove_from_scene_entry.add()

    def remove_from_scene_1(self):
        if(self.sprite != None):
            self.sprite.remove()

        for i in range(0,len(self.elements)):
            self.elements[i].remove_from_scene()

class base_button(cvsmgmt.scene_object):
    def __init__(self, anchor, sprite_name, clicked_sprite_name, group_num = config.num_scene_groups+1):
        cvsmgmt.scene_object.__init__(self,group_num)

        self.sprite_name = sprite_name
        self.click_sprite_name = clicked_sprite_name
        self.render_objects.append([cvsmr.sprite_object(sprite_name, anchor, group_num)])

        self.click_state = False

        self.checkbox.set_source(self.render_objects[0][0])

        self.handlers[0] = True
        self.handlers[4] = True

    def toggle_sprite(self):
        if(self.click_state):
            self.render_objects[0][0].switch_image(self.sprite_name)
            self.click_state = False
        else:
            self.render_objects[0][0].switch_image(self.click_sprite_name)
            self.click_state = True

class scroll_slider(cvsmgmt.scene_object):
    def __init__(self, scroll_menu, group_num, sprite_name, anchor, height):
        cvsmgmt.scene_object.__init__(self,group_num)

        self.anchor = anchor

        self.height = height

        self.scroll_menu = scroll_menu
        self.handlers[0] = True
        self.handlers[5] = True

        self.render_objects.append([cvsmr.sprite_object(sprite_name, anchor, group_num)])
        self.checkbox.set_source(self.render_objects[0][0])

        self.drag_slider_entry = cvsmgmt.update_entry(self.drag_slider, ["dy"])

    def update_self(self):
        #update sprite position and checkbox
        self.anchor[1] = (self.scroll_menu.max_position - self.scroll_menu.position) /self.scroll_menu.max_position * self.height
        self.render_objects[0][0].coords(self.anchor[0],self.anchor[1])
        self.checkbox.update_source()

    def dpos(self, d):
        self.scroll_menu.dpos(d)

    def handler_leftclick(self,x,y):
        config.click_selected = self

    def handler_leftdrag(self, x,y,dx,dy):
        self.drag_slider_entry.args[0] = (dy)/self.height * self.scroll_menu.max_position
        self.drag_slider_entry.add()

    def drag_slider(self,args):
        self.dpos(args[0])

class scroll_slider_box(cvsmgmt.scene_object):
    def __init__(self, scroll_menu, group_num, anchor, height, width):
        cvsmgmt.scene_object.__init__(self,group_num)
        self.checkbox.broad_checkbox = [anchor[0],anchor[1],
                                        anchor[0] + width,
                                        anchor[1] + height]

        self.handlers[0] = True
        self.scroll_menu = scroll_menu

    def handler_leftclick(self, x,y):
        self.scroll_menu.pos((self.height - (y-self.anchor[1]))/self.height * self.scroll_menu.max_position)

class scroll_menu_box(cvsmgmt.scene_object):
    #set as same group as scroll elements

    def __init__(self, scroll_menu, group_num, anchor, height, width):
        cvsmgmt.scene_object.__init__(self,group_num)
        self.checkbox.broad_checkbox = [anchor[0],anchor[1],
                                        anchor[0] + width,
                                        anchor[1] + height]

        self.handlers[3] = True
        self.scroll_menu = scroll_menu

    def handler_scroll(self, x,y,scroll_x,scroll_y):
        self.scroll_menu.dpos(-1 * scroll_y)

class scroll_menu(base_window):
    def __init__(self, scene_index, anchor, num_elements, element_height, width, slider_x_offset, slider_name, group_num = config.num_scene_groups + 1, list_of_elements = None):
        base_window.__init__(self=self, anchor=anchor, group_num = group_num)

        self.list = self.list_of_elements

        self.num_elements = num_elements
        self.element_height = element_height
        self.pix_height = element_height * num_elements

        self.posiiton = 0
        self.max_position = 0

        self.scroll_slider = scroll_slider(scroll_menu = self, group_num = group_num, slider_name = slider_name, anchor = [anchor[0] + slider_x_offset, anchor[1]], height =  self.pix_height)
        self.elements = [self.scroll_slider,
                         scroll_slider_box(self, group_num-1, [anchor[0] + slider_x_offset, anchor[1]], self.pix_height, self.scroll_slider.render_objects[0][0].width),
                         scroll_menu_box(self, group_num, anchor, self.pix_height, width)]

        self.elements_index = [scene_index, scene_index+1, scene_index+2]

    def populate(self, list_of_elements = None):
        if(list_of_elements != None):
            self.list = list_of_elements
        self.max_position = len(self.list) - 1 - self.num_elements
        self.position = 0

    def pos(self, p):
        self.position = max(0,min(p,self.max_position))
        self.update_self()

    def dpos(self,d):
        self.position += d
        self.position = max(0, min(self.position, self.max_position))

        self.update_self()

    def update_self(self):
        self.elements[0].update_self()

        for i in range(0, self.max_position):
            if(self.list.scene_index != None):
                self.list.remove_from_scene_1()

        for i in range(0, self.num_elements):
            self.list[i + self.position].coords_1(self.anchor[0],
                                                  self.anchor[1] + self.element_height * (self.num_elements - i))

#---CUSTOM-------------------------------------------------------------------------------------------------------------
class main_menu_play(base_button):
    def __init__(self):
        base_button.__init__(self,[5,420], "main_menu_play", "main_menu_play_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        self.toggle_sprite()

class main_menu_settings(base_button):
    def __init__(self):
        base_button.__init__(self, [5, 300], "main_menu_settings", "main_menu_settings_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):

        self.toggle_sprite()

        config.menus["main_menu"].remove_from_scene()
        config.menus["settings_menu"].add_to_scene()

class main_menu_exitgame(base_button):
    def __init__(self):
        base_button.__init__(self, [5, 100], "main_menu_exitgame", "main_menu_exitgame_c")

    def handler_leftclick(self, x, y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self, x, y):
        self.toggle_sprite()
        pyglet.app.exit()

class main_menu(base_window):
    def __init__(self):
        base_window.__init__(self = self, anchor = [0,0], sprite_name = "main_menu")

        self.elements = [main_menu_play(),main_menu_settings(),main_menu_exitgame()]
        self.elements_index = [1,2,3]

#-----------------------------------------

class settings_menu_back(base_button):
    def __init__(self):
        base_button.__init__(self,[5,420], "settings_menu_back", "settings_menu_back_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        self.toggle_sprite()

        config.menus["settings_menu"].remove_from_scene()
        config.menus["main_menu"].add_to_scene()

class settings_menu_fullscreen(base_button):
    def __init__(self):
        base_button.__init__(self,[200,420], "settings_menu_fullscreen", "settings_menu_fullscreen_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        if(config.fullscreen == 0):
            config.fullscreen = 1
        else:
            config.fullscreen = 0

        cvsms.apply_settings()
        cvsms.write_settings()

class settings_menu(base_window):
    def __init__(self):
        base_window.__init__(self=self, anchor=[0, 0], sprite_name="settings_menu")

        self.elements = [settings_menu_back(),settings_menu_fullscreen()]
        self.elements_index = [4,5]