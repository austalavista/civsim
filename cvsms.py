#functions that are called for changing the game state

import config
import pyglet
import cvsmr, cvsmm, cvsmgmt
import time
import core
import numpy as np

def apply_settings():
    #fullscreen
    if(True):
        if(config.fullscreen == 1):
            config.window.set_fullscreen(True)

            temp = config.window.get_size()
            config.global_transformation_group.scale(temp[0]/1920, temp[1]/1080)
        else:
            config.window.set_fullscreen(False)

    #resolution
    if(config.fullscreen == 0):
        if(config.resolution == 0):
            config.window.set_fullscreen(fullscreen=False, width=1920, height=1080)
        elif(config.resolution == 1):
            config.window.set_fullscreen(fullscreen=False, width=1400, height=900)
        elif (config.resolution == 2):
            config.window.set_fullscreen(fullscreen=False, width=1200, height=900)
        elif (config.resolution == 3):
            config.window.set_fullscreen(fullscreen=False, width=1200, height=700)
        elif (config.resolution == 4):
            config.window.set_fullscreen(fullscreen=False, width=900, height=400)
        elif (config.resolution == 5):
            config.window.set_fullscreen(fullscreen=False, width=600, height=250)

        temp = config.window.get_size()
        config.global_transformation_group.scale(temp[0] / 1920, temp[1] / 1080)

def write_settings():
    settings = open('settings', 'w+')

    settings.write("fullscreen=" + str(config.fullscreen) + "\n")
    settings.write("resolution=" + str(config.resolution) + "\n")

    settings.close()

def clear_scene():
    for i in range(0, config.scene_objects_size):
        if(config.scene_objects[i] != None):
            config.scene_objects[i].remove_from_scene()

def clear_menus():
    for key in config.menus:
        config.menus[key].remove_from_scene()
#-----------------------------------------------------------------------------------------------------------------------

def initialize():
    cvsmr.ordered_transformation_groups_init()

    #init startup entries for all other game state update things
    for i in range(0, len(config.gs_entries)):
        config.gs_entries[i] = cvsmgmt.update_entry(None)

    #settings
    try:
        settings = open('settings', 'r')
        settings_list = settings.read().split("\n")

        config.fullscreen = int(settings_list[0].split('=')[1])
        config.resolution = int(settings_list[1].split('=')[1])

    except:
        settings = open('settings', 'w+')

        settings.write("fullscreen=1\n")
        settings.write("resolution=0\n")

    settings.close()
    apply_settings()

    # resources
    pyglet.resource.path = ['resources', 'resources/UI/main_menu','resources/UI/in_game_menu', 'resources/UI/settings_menu','resources/UI/play_menu', 'resources/UI', 'resources/map']

    config.gs_entries[0].function = pyglet.resource.reindex
    config.gs_entries[0].add(0)

    #groups
    config.gs_entries[2].function = cvsmr.texture_groups_init
    config.gs_entries[2].add(2)

    config.gs_entries[3].function = cvsmr.line_groups_init
    config.gs_entries[3].add(3)

    config.gs_entries[4].function = cvsmr.sprite_texture_init
    config.gs_entries[4].add(4)

    cvsmr.layout_groups_init()

    #open main menu
    config.gs_entries[5].function = open_main_menu
    config.gs_entries[5].add(5)

def open_main_menu():
    config.state = "main_menu"
    config.menus["main_menu"] = cvsmm.main_menu()
    config.menus["main_menu"].add_to_scene()

    config.menus["settings_menu"] = cvsmm.settings_menu()

def open_play_menu():
    config.state = "play_menu"
    config.menus["main_menu"].remove_from_scene()

    if(not config.init):
        core.init_provinces(2)
        core.init_nations()
        core.init_scenarios()
        core.init_saves()
        config.init = True

        config.ocean = core.ocean()
        core.draw_nation_borders()

    config.menus["play_menu"] = cvsmm.play_menu()
    config.menus["play_menu"].add_to_scene()

    for i in range(0,config.num_provinces):
        if(config.provinces[i] != None):
            if(config.provinces[i].id < 1400 or config.provinces[i].id >= 1600):
                config.provinces[i].add_to_scene()

    config.province_borders.add_to_scene()



    config.ocean.add_to_scene()
    config.scene_transformation_group.scale(0.1,0.1)
    config.scene_transformation_group.coords(0,0)

def start():
    config.state = "in_game_menu"

    config.menus["play_menu"].remove_from_scene()
    config.menus["main_menu"] = None
    config.menus["play_menu"] = None

    config.time_entry = core.time_entry()
    config.time_entry.speed = 0
    config.time_entry.add()

    config.menus["in_game_menu"] = cvsmm.in_game_menu()
    config.menus["in_game_menu"].add_to_scene()

    core.init_datastructures()