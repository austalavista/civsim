#Menu baseclasses and their custom derivatives

import pyglet
import config
import cvsmr, cvsmgmt, cvsms
import core

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

    def add_to_scene(self):
        if(self.sprite != None):
            self.sprite.add()

        for i in range(0,len(self.elements)):
            self.elements[i].add_to_scene()

    def remove_from_scene(self):
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

#-------------------------------------------

class scroll_slider(cvsmgmt.scene_object):
    def __init__(self, scroll_menu, group_num, sprite_name, anchor, height):
        cvsmgmt.scene_object.__init__(self,group_num)

        self.anchor = anchor

        self.render_objects.append([cvsmr.sprite_object(sprite_name, anchor, group_num)])
        self.checkbox.set_source(self.render_objects[0][0])

        self.anchor_original = anchor[1] - self.render_objects[0][0].sprite.height/2

        self.height = height

        self.scroll_menu = scroll_menu
        self.handlers[0] = True
        self.handlers[5] = True

    def update_self(self):
        #update sprite position and checkbox
        if(self.scroll_menu.max_position > 0):
            self.anchor[1] = (self.scroll_menu.max_position - self.scroll_menu.position) /self.scroll_menu.max_position * self.height + self.anchor_original
            self.render_objects[0][0].coords(self.anchor[0],self.anchor[1])
            self.checkbox.update_source()
        else:
            self.anchor[1] = self.height + self.anchor_original
            self.render_objects[0][0].coords(self.anchor[0], self.anchor[1])
            self.checkbox.update_source()

    def handler_leftclick(self,x,y):
        config.click_selected = self

    def handler_leftdrag(self, x,y,dx,dy):
        self.scroll_menu.pos((self.anchor_original - y + self.height)/self.height * self.scroll_menu.max_position)

class scroll_slider_box(cvsmgmt.scene_object):
    def __init__(self, scroll_menu, group_num, anchor, height, width):
        cvsmgmt.scene_object.__init__(self,group_num)
        self.checkbox.broad_checkbox = [anchor[0],anchor[1],
                                        anchor[0] + width,
                                        anchor[1] + height]
        self.handlers[0] = True
        self.scroll_menu = scroll_menu
        self.height = height
        self.anchor = anchor

    def handler_leftclick(self, x,y):
        self.scroll_menu.pos((self.height - (y-self.anchor[1]))/self.height * self.scroll_menu.max_position)

class scroll_slider_button(base_button):
    def __init__(self, direction, scroll_menu, anchor, sprite_name,clicked_sprite_name, group_num):
        base_button.__init__(self, anchor, sprite_name, clicked_sprite_name,group_num)

        self.scroll_menu = scroll_menu
        self.direction = direction # 1 or -1

    def handler_leftclick(self, x, y):
        config.click_selected = self
        self.toggle_sprite()

        self.scroll_menu.dpos(self.direction)

    def handler_release(self, x, y):
        self.toggle_sprite()

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

class scroll_menu_element(base_button):
    def __init__(self,sprite_name, clicked_sprite_name, group_num):
        base_button.__init__(self,[0,0], sprite_name, clicked_sprite_name, group_num)

        self.checkbox.set_source(self.render_objects[0][0])

    def toggle(self,state):
        if(state):
            self.render_objects[0][0].switch_image(self.click_sprite_name)
        else:
            self.render_objects[0][0].switch_image(self.sprite_name)

class scroll_menu(base_window):
    def __init__(self, scene_index, anchor, num_elements, element_height, width, slider_x_offset, slider_name, group_num = config.num_scene_groups + 1, list_of_elements = None, slider_y_clip = 34, slider_y_offset = 5):
        base_window.__init__(self=self, anchor=anchor, group_num = group_num)

        self.list = list_of_elements

        self.num_elements = num_elements
        self.element_height = element_height
        self.pix_height = element_height * num_elements

        self.position = 0
        self.max_position = 0

        self.scroll_slider = scroll_slider(scroll_menu = self, group_num = group_num+1, sprite_name = slider_name, anchor = [anchor[0] + slider_x_offset, anchor[1] + slider_y_clip + slider_y_offset], height =  self.pix_height - slider_y_clip * 2 - slider_y_offset * 2)
        self.elements = [self.scroll_slider,
                         scroll_slider_box(self, group_num, [anchor[0] + slider_x_offset, anchor[1] + slider_y_clip + slider_y_offset], self.pix_height - slider_y_clip * 2, self.scroll_slider.render_objects[0][0].width),
                         scroll_menu_box(self, group_num, anchor, self.pix_height, width),
                         scroll_slider_button(-1, self, [anchor[0] + slider_x_offset, anchor[1] + self.pix_height - slider_y_clip - slider_y_offset], "scroll_button_up", "scroll_button_up_c", group_num),
                         scroll_slider_button(1, self, [anchor[0] + slider_x_offset, anchor[1] + slider_y_offset], "scroll_button_down", "scroll_button_down_c",group_num)]

        self.scene_index = scene_index
        if(scene_index != None):
            self.elements_index = [scene_index, scene_index+1, scene_index+2]
        else:
            self.elements_index = [None,None,None]

    def populate(self, list_of_elements = None):
        if(list_of_elements != None):
            self.list = list_of_elements
        self.max_position = max(len(self.list) - self.num_elements, 0)
        self.position = 0

    def pos(self, p):
        if(self.max_position > 0):
            self.position = max(0,min(p,self.max_position))
            self.update_self()

    def dpos(self,d):
        if(self.max_position > 0):
            self.position += d
            self.position = max(0, min(self.position, self.max_position))

            self.update_self()

    def update_self(self):
        self.elements[0].update_self()

        for i in range(0, len(self.list)):
            if(self.list[i].scene_index != None):
                self.list[i].remove_from_scene()

        if(self.scene_index != None):
            for i in range(0, min(self.num_elements, len(self.list))):
                self.list[i + int(self.position)].coords(self.anchor[0],self.anchor[1] + self.element_height * (self.num_elements - i-1))
                self.list[i + int(self.position)].add_to_scene()
        else:
            for i in range(0, min(self.num_elements, len(self.list))):
                self.list[i + int(self.position)].coords(self.anchor[0],self.anchor[1] + self.element_height * (self.num_elements - i-1))
                self.list[i + int(self.position)].add_to_scene()

    def add_to_scene(self):
        for i in range(0, 5):
            self.elements[i].add_to_scene()

        self.populate()
        self.update_self()

    def remove_from_scene(self):
        for i in range(0, len(self.elements)):
            self.elements[i].remove_from_scene()

        for i in range(0,len(self.list)):
            self.list[i].remove_from_scene()

    def toggle(self):
        for i in range(0, len(self.list)):
                self.list[i].toggle(False)

#-------------------------------------------

#---CUSTOM-------------------------------------------------------------------------------------------------------------
class main_menu_play(base_button):
    def __init__(self):
        base_button.__init__(self,[5,420], "main_menu_play", "main_menu_play_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

        config.gs_entries[0].function = cvsms.open_play_menu
        config.gs_entries[0].add(2)

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
        self.elements_index = [None,None,None]

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

class settings_menu_resolution_element(scroll_menu_element):
    def __init__(self, scroll_menu, resolution_value, text, group_num):
        scroll_menu_element.__init__(self,"settings_menu_resolution_element","settings_menu_resolution_element_c",group_num)

        self.scroll_menu = scroll_menu

        self.render_objects[0].append(cvsmr.label_object(text, [0,0], group_num+1, anchor_offset = [5,5]))

        self.resolution_value = resolution_value

    def handler_leftclick(self, x, y):
        config.resolution = self.resolution_value

        cvsms.apply_settings()
        cvsms.write_settings()

        self.scroll_menu.toggle()
        self.toggle(True)

class settings_menu_resolution(scroll_menu):
    def __init__(self):
        scroll_menu.__init__(self, None,[250,200],4,30,200,205,"scroll_slider", config.num_scene_groups + 2)

        self.list = [settings_menu_resolution_element(self, 0, "1920x1080",self.group_num),
                     settings_menu_resolution_element(self, 1, "1400x900", self.group_num),
                     settings_menu_resolution_element(self, 2, "1200x900", self.group_num),
                     settings_menu_resolution_element(self, 3, "1200x700", self.group_num),
                     settings_menu_resolution_element(self, 4, "900x400", self.group_num),
                     settings_menu_resolution_element(self, 5, "600x250", self.group_num)]

class settings_menu(base_window):
    def __init__(self):
        base_window.__init__(self=self, anchor=[0, 0], sprite_name="settings_menu")

        self.elements = [settings_menu_back(),settings_menu_fullscreen(),settings_menu_resolution()]

#-----------------------------------------

class play_saves_toggle(cvsmgmt.scene_object):
    def __init__(self,menu):
        base_button.__init__(self,[400,100], "play_saves_toggle", None)
        self.menu = menu

    def handler_leftclick(self, x,y):
        self.menu.list[0].add_to_scene()
        self.menu.list[1].remove_from_scene()
        self.menu.list[7].add_to_scene()
        self.remove_from_scene()

class play_scenarios_toggle(base_button):
    def __init__(self,menu):
        base_button.__init__(self,[400,100], "play_scenarios_toggle", None)
        self.menu = menu

    def handler_leftclick(self, x,y):
        self.menu.list[1].add_to_scene()
        self.menu.list[2].remove_from_scene()
        self.menu.list[6].add_to_scene()
        self.remove_from_scene()

class play_start(base_button):
    def __init__(self):
        base_button.__init__(self,[400,100], "play_menu_start", "play_menu_start_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        self.toggle_sprite()

class play_back(base_button):
    def __init__(self):
        base_button.__init__(self,[400,10], "play_menu_back", "play_menu_back_c")

    def handler_leftclick(self, x,y):
        config.click_selected = self
        self.toggle_sprite()

    def handler_release(self,x,y):
        self.toggle_sprite()

        cvsms.clear_scene()
        cvsms.clear_menus()
        cvsms.open_main_menu()
        for i in range(0, config.num_provinces):
            config.provinces[i].set_nation(None)
        config.menus["play_menu"] = None

class play_saves_element(scroll_menu_element):
    def __init__(self, scroll_menu, save, group_num):
        scroll_menu_element.__init__(self,"play_menu_scroll_element","play_menu_scroll_element_c",group_num)

        self.scroll_menu = scroll_menu

        self.save = save
        self.render_objects[0].append(cvsmr.label_object(save.name,[0,0],group_num+1, anchor_offset = [10,80]))
        self.render_objects[0].append(cvsmr.label_object(str(save.month) + " " + str(save.day) + ", " + str(save.year),[0, 0], group_num + 1, anchor_offset = [10,10]))

    def handler_leftclick(self, x, y):
        self.save.set()
        config.nation_borders.remove_from_scene()
        core.draw_nation_borders()
        config.nation_borders.add_to_scene()

        self.scroll_menu.toggle()
        self.toggle(True)

class play_saves(scroll_menu):
    def __init__(self):
        scroll_menu.__init__(self, None,[18,15],6,104,342,350,"scroll_slider", config.num_scene_groups+1)

        self.list = []
        for i in range(0, len(config.saves)):
            self.list.append(play_saves_element(self,config.saves[i], self.group_num))

class play_saves_toggle(base_button):
    def __init__(self):
        base_button.__init__(self,[193,638], "play_menu_saves_toggle", "play_menu_saves_toggle_c")
        self.handlers[4] = False
        self.state = False

    def handler_leftclick(self, x,y):


        if (not self.state):
            self.state = True
            self.toggle_sprite()
            config.menus["play_menu"].elements[1].remove_from_scene()
            config.menus["play_menu"].elements[5].toggle_sprite()
            config.menus["play_menu"].elements[5].state = False
            config.menus["play_menu"].elements[0].add_to_scene()
            config.menus["play_menu"].elements[0].toggle()

class play_scenarios_element(scroll_menu_element):
    def __init__(self, scroll_menu, scenario, group_num):
        scroll_menu_element.__init__(self,"play_menu_scroll_element","play_menu_scroll_element_c",group_num)

        self.scroll_menu = scroll_menu

        self.scenario = scenario
        self.render_objects[0].append(cvsmr.label_object(scenario.name ,[0,0],group_num+1, anchor_offset = [10,80]))
        self.render_objects[0].append(cvsmr.label_object(str(scenario.month) + " " + str(scenario.day) + ", " + str(scenario.year), [0, 0], group_num + 1, anchor_offset=[10, 10]))

    def handler_leftclick(self, x, y):
        self.scenario.set()
        config.nation_borders.remove_from_scene()
        core.draw_nation_borders()
        config.nation_borders.add_to_scene()

        self.scroll_menu.toggle()
        self.toggle(True)

        config.menus["play_menu"].elements[6].set_name(self.scenario.name)
        config.menus["play_menu"].elements[6].set_description(self.scenario.description)

class play_scenarios(scroll_menu):
    def __init__(self):
        scroll_menu.__init__(self, None,[18,15],6,104,342,350,"scroll_slider", config.num_scene_groups+1)

        self.list = []
        for i in range(0, len(config.scenarios)):
            self.list.append(play_scenarios_element(self, config.scenarios[i], self.group_num))

class play_scenarios_toggle(base_button):
    def __init__(self):
        base_button.__init__(self,[23,638], "play_menu_scenarios_toggle_c", "play_menu_scenarios_toggle")
        self.handlers[4] = False
        self.state = True

    def handler_leftclick(self, x,y):

        if(not self.state):
            self.state = True
            self.toggle_sprite()
            config.menus["play_menu"].elements[0].remove_from_scene()
            config.menus["play_menu"].elements[4].toggle_sprite()
            config.menus["play_menu"].elements[4].state = False
            config.menus["play_menu"].elements[1].add_to_scene()
            config.menus["play_menu"].elements[1].toggle()

class scenario_info(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self)

        self.render_objects = [[cvsmr.label_object("Select a scenario/save", [20,1020],config.num_scene_groups+1),
                                cvsmr.layout_object("Times New Roman", 15, [20,600],350,400, config.num_scene_groups+1)
                                ]]
        self.render_objects[0][1].set_text("")

    def set_description(self, description):
        self.render_objects[0][1].remove()
        self.render_objects[0][1].set_text(description)

        self.render_objects[0][1].add()

    def set_name(self,name):
        self.render_objects[0][0].label.text = name

class nation_info(cvsmgmt.scene_object):
    def __init__(self):
        cvsmgmt.scene_object.__init__(self)

        self.render_objects = [[cvsmr.label_object("", [500, 1020], config.num_scene_groups + 1),
                                cvsmr.label_object("", [500, 620], config.num_scene_groups + 1)
                                ]]

    def set_province(self,province):
        self.render_objects[0][0].label.text = "province: " + province

    def set_nation(self,nation):
        self.render_objects[0][1].label.text = "nation: " + nation

class play_menu(base_window):
    def __init__(self):
        base_window.__init__(self=self, anchor=[0, 0], sprite_name="play_menu")

        self.elements = [play_saves(), play_scenarios(), play_start(), play_back(), play_saves_toggle(),play_scenarios_toggle(), scenario_info(),nation_info()]

    def add_to_scene(self):
        if(self.sprite != None):
            self.sprite.add()

        #load scenarios scroll menu first
        for i in range(1,len(self.elements)):
            self.elements[i].add_to_scene()