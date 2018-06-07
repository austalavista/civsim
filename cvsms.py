#functions that are called for changing the game state

import config
import pyglet
import cvsmr, cvsmm, cvsmgmt

def initialize():

    #init startup entries for all other game state update things
    for i in range(0, len(config.gs_entries)):
        config.gs_entries[i] = cvsmgmt.update_entry(None)


    # ---RESOURCE INITIALIZATION---
    pyglet.resource.path = ['resources', 'resources/UI']

    config.gs_entries[0].function = pyglet.resource.reindex
    config.gs_entries[0].add(0)

    # ---GROUP INITIALIZATION---

    config.gs_entries[1].function = cvsmr.ordered_transformation_groups_init
    config.gs_entries[1].add(1)

    config.gs_entries[2].function = cvsmr.texture_groups_init
    config.gs_entries[2].add(2)

    config.gs_entries[3].function = cvsmr.line_groups_init
    config.gs_entries[3].add(3)

    config.gs_entries[4].function = cvsmr.sprite_texture_init
    config.gs_entries[4].add(4)

    config.gs_entries[5].function = open_main_menu
    config.gs_entries[5].add(5)


def open_main_menu():
    global main_menu

    main_menu = cvsmm.main_menu()
    main_menu.add_to_scene()