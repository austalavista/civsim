import pyglet
import math
import random
import numpy
import config, cvsmr, cvsmgmt, cvsmm, cvsms
import tactical
import time

#Create window
config.aa = pyglet.gl.Config(sample_buffers=1, samples=3)  # ANTIALIASING
config.window = pyglet.window.Window(config=config.aa, resizable=False)

#EVENTS----------------------------------------------------------------------------------------------------------------
@config.window.event
def on_mouse_motion(x,y, dx, dy):
    pass

@config.window.event
def on_mouse_press(x, y, button,modifiers):
    event = None
    if(button == pyglet.window.mouse.LEFT):
        event = 0
    elif(button == pyglet.window.mouse.MIDDLE):
        event = 1
    elif (button == pyglet.window.mouse.RIGHT):
        event = 2

    coordinate_box_check(x/config.global_transformation_group.scale_x ,y/config.global_transformation_group.scale_y,event)

@config.window.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):

    coordinate_box_check(x/config.global_transformation_group.scale_x ,y/config.global_transformation_group.scale_y,3,scroll_x,scroll_y)

@config.window.event
def on_mouse_release(x,y,buttons,modifiers):

    if(config.click_selected != None):
        if(config.click_selected.handlers[4]):
            config.click_selected.handler_release(x/config.global_transformation_group.scale_x ,y/config.global_transformation_group.scale_y)
        config.click_selected = None

@config.window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):

    if(config.click_selected != None):
        if(buttons & pyglet.window.mouse.LEFT):
            if(config.click_selected.handlers[5]):
                config.click_selected.handler_leftdrag(x/config.global_transformation_group.scale_x ,y/config.global_transformation_group.scale_y,
                                                       dx/config.global_transformation_group.scale_x ,
                                                       dy/config.global_transformation_group.scale_y)

        elif(buttons & pyglet.window.mouse.RIGHT):
            if (config.click_selected.handlers[6]):
                config.click_selected.handler_rightdrag(x/config.global_transformation_group.scale_x ,y/config.global_transformation_group.scale_y,
                                                        dx / config.global_transformation_group.scale_x,
                                                        dy / config.global_transformation_group.scale_y)

@config.window.event
def on_key_press(symbol,modifiers):
    pass
config.window.on_key_press = on_key_press

@config.window.event
def on_draw():
    config.window.clear()
    config.batch.draw()

#OTHER-----------------------------------------------------------------------------------------------------------------
def coordinate_box_check_1(args):
    object = None
    relevance = False

    menu_x = args[0]
    menu_y = args[1]

    trans_x = (args[0] - config.scene_transformation_group.x) / config.scene_transformation_group.scale_x
    trans_y = (args[1] - config.scene_transformation_group.y) / config.scene_transformation_group.scale_y

    broadcheck_hits = [False] * 10
    index = 0
    peakgroup = -1

    #broad checks
    for i in range(0, config.scene_objects_size):

        if(config.scene_objects[i] != None and config.scene_objects[i].handlers[args[2]] and index < 10):

            if(config.scene_objects[i].group_num >= config.num_scene_groups):
                x = menu_x
                y = menu_y
            else:
                x = trans_x
                y = trans_y

            if(x > config.scene_objects[i].checkbox.broad_checkbox[0] and
               x < config.scene_objects[i].checkbox.broad_checkbox[2] and
               y > config.scene_objects[i].checkbox.broad_checkbox[1] and
               y < config.scene_objects[i].checkbox.broad_checkbox[3]):

                broadcheck_hits[index] = config.scene_objects[i]
                index += 1

    #narrow checks
    for i in range(0, index):
        if(broadcheck_hits[i].group_num > peakgroup):
            if(not broadcheck_hits[i].checkbox.narrow_check):
                object = broadcheck_hits[i]
                peakgroup = object.group_num

            elif(broadcheck_hits[i].checkbox.triangles):

                if (config.scene_objects[i].group_num >= config.num_scene_groups):
                    x = menu_x
                    y = menu_y
                else:
                    x = trans_x
                    y = trans_y

                for j in range(0,int(len(broadcheck_hits[i].checkbox.narrow_checkbox)/3)):

                    temp = j*3

                    ba = (broadcheck_hits[i].checkbox.narrow_checkbox[temp + 2] - broadcheck_hits[i].checkbox.narrow_checkbox[temp],
                          broadcheck_hits[i].checkbox.narrow_checkbox[temp + 3] - broadcheck_hits[i].checkbox.narrow_checkbox[temp + 1])

                    ca = (broadcheck_hits[i].checkbox.narrow_checkbox[temp + 4] - broadcheck_hits[i].checkbox.narrow_checkbox[temp],
                          broadcheck_hits[i].checkbox.narrow_checkbox[temp + 5] - broadcheck_hits[i].checkbox.narrow_checkbox[temp + 1])

                    d = ba[0] * ca[0] - ba[1] * ca[0]

                    temp = (y * ba[0] - x * ba[1]) / d
                    if(temp > 0 and temp < 1):
                        temp = (x * ca[1] - y * ca[0]) / d
                        if(temp > 0 and temp < 1):
                            temp = (x * (ba[1] - ca[1]) + y * (ca[0] - ba[0]) + ba[0] * ca[1] - ba[1] * ca[0]) / d
                            if(temp > 0 and temp < 1):
                                object = broadcheck_hits[i]
                                peakgroup = object.group_num
                                break

    #call handlers
    if(object != None):
        if (config.selected != None):
            if (args[2] == 0 and object.handlers[0]):
                relevance = config.selected.handler_leftclick(x, y, object = object)
            elif (args[2] == 1 and object.handlers[1]):
                relevance = config.selected.handler_rightclick(x, y, object = object)
            elif (args[2] == 2 and object.handlers[2]):
                relevance = config.selected.handler_middleclick(x, y, object = object)
            elif (args[2] == 3 and object.handlers[3]):
                relevance = config.selected.handler_scroll(x, y, args[3], args[4], object = object)

        if(not relevance):
            if(args[2] == 0 and object.handlers[0]):
                object.handler_leftclick(x = x,y = y)
            elif(args[2] == 1 and object.handlers[1]):
                object.handler_rightclick(x = x,y = y)
            elif(args[2] == 2 and object.handlers[2]):
                object.handler_middleclick(x = x,y = y)
            elif(args[2] == 3 and object.handlers[3]):
                object.handler_scroll(x = x,y = y, scroll_x = args[3],scroll_y = args[4])
    else:
        config.selected = None

coordinate_box_check_entry = cvsmgmt.update_entry(coordinate_box_check_1,["x", "y", "event_type", "scroll_x", "scroll_y"] )

def coordinate_box_check(x, y, event_type, scroll_x = 0, scroll_y = 0):
    global coordinate_box_check_entry

    coordinate_box_check_entry.args[0] = x
    coordinate_box_check_entry.args[1] = y
    coordinate_box_check_entry.args[2] = event_type
    coordinate_box_check_entry.args[3] = scroll_x
    coordinate_box_check_entry.args[4] = scroll_y

    coordinate_box_check_entry.add()

def update(dt):
    for i in range(0, config.update_queue_size):
        if (config.update_queue[i] != None):

            config.update_queue[i].run()

#RUN-------------------------------------------------------------------------------------------------------------------
cvsms.initialize()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()



