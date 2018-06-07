#Menu baseclasses and their custom derivatives

import pyglet
import config
import cvsmr, cvsmgmt

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

#---CUSTOM-------------------------------------------------------------------------------------------------------------
class main_menu_play(base_button):
    def __init__(self):
        base_button.__init__(self,[0,100], "main_menu_play", "main_menu_play_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        self.toggle_sprite()

class main_menu(base_window):
    def __init__(self):
        base_window.__init__(self = self, anchor = [0,0], sprite_name = "main_menu")

        self.elements = [main_menu_play()]
        self.elements_index = [1, 2]