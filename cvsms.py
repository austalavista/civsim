#functions that are called for changing the game state

import config
import pyglet
import cvsmr, cvsmm, cvsmgmt
import time

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
    pyglet.resource.path = ['resources', 'resources/UI', 'resources/misc']

    config.gs_entries[0].function = pyglet.resource.reindex
    config.gs_entries[0].add(0)

    #groups
    config.gs_entries[2].function = cvsmr.texture_groups_init
    config.gs_entries[2].add(2)

    config.gs_entries[3].function = cvsmr.line_groups_init
    config.gs_entries[3].add(3)

    config.gs_entries[4].function = cvsmr.sprite_texture_init
    config.gs_entries[4].add(4)

    #open main menu
    config.gs_entries[5].function = open_main_menu
    config.gs_entries[5].add(5)

def open_main_menu():
    config.menus["main_menu"] = cvsmm.main_menu()
    config.menus["main_menu"].add_to_scene()

    config.menus["settings_menu"] = cvsmm.settings_menu()

    global mainscreen
    mainscreen = cvsmr.sprite_object("mainscreen", [0,0],0)
    mainscreen.add()

