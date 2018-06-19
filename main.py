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
    global mouse_release_entry

    if(config.click_selected != None):
        if(config.click_selected.handlers[4]):
            mouse_release_entry.args[0] = x / config.global_transformation_group.scale_x
            mouse_release_entry.args[1] = y / config.global_transformation_group.scale_y

            mouse_release_entry.function = config.click_selected.handler_release

            mouse_release_entry.add()
        config.click_selected = None

@config.window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    global mouse_drag_entry

    if(config.click_selected != None):
        if(buttons & pyglet.window.mouse.LEFT):
            if(config.click_selected.handlers[5]):
                mouse_drag_entry.args[0] = x/config.global_transformation_group.scale_x
                mouse_drag_entry.args[1] = y/config.global_transformation_group.scale_y
                mouse_drag_entry.args[2] = dx/config.global_transformation_group.scale_x
                mouse_drag_entry.args[3] = dy/config.global_transformation_group.scale_y

                mouse_drag_entry.function = config.click_selected.handler_leftdrag

                mouse_drag_entry.add()

        elif(buttons & pyglet.window.mouse.RIGHT):
            if (config.click_selected.handlers[6]):
                mouse_drag_entry.args[0] = x / config.global_transformation_group.scale_x
                mouse_drag_entry.args[1] = y / config.global_transformation_group.scale_y
                mouse_drag_entry.args[2] = dx / config.global_transformation_group.scale_x
                mouse_drag_entry.args[3] = dy / config.global_transformation_group.scale_y

                mouse_drag_entry.function = config.click_selected.handler_rightdrag

                mouse_drag_entry.add()

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

    trans_x = (args[0] ) / config.scene_transformation_group.scale_x - config.scene_transformation_group.x
    trans_y = (args[1] ) / config.scene_transformation_group.scale_y - config.scene_transformation_group.y

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

                for j in range(0,int(len(broadcheck_hits[i].checkbox.narrow_checkbox)/6)):

                    temp = j*6

                    v0 = numpy.array([broadcheck_hits[i].checkbox.narrow_checkbox[temp] - broadcheck_hits[i].checkbox.narrow_checkbox[temp+2],
                          broadcheck_hits[i].checkbox.narrow_checkbox[temp + 1] - broadcheck_hits[i].checkbox.narrow_checkbox[temp + 3]])

                    v1 = numpy.array([broadcheck_hits[i].checkbox.narrow_checkbox[temp] - broadcheck_hits[i].checkbox.narrow_checkbox[temp + 4],
                          broadcheck_hits[i].checkbox.narrow_checkbox[temp + 1] - broadcheck_hits[i].checkbox.narrow_checkbox[temp + 5]])

                    v2 = numpy.array([broadcheck_hits[i].checkbox.narrow_checkbox[temp] - x,broadcheck_hits[i].checkbox.narrow_checkbox[temp + 1] - y])

                    dot00 = numpy.dot(v0, v0)
                    dot01 = numpy.dot(v0, v1)
                    dot02 = numpy.dot(v0, v2)
                    dot11 = numpy.dot(v1, v1)
                    dot12 = numpy.dot(v1, v2)

                    invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
                    u = (dot11 * dot02 - dot01 * dot12) * invDenom
                    v = (dot00 * dot12 - dot01 * dot02) * invDenom

                    if( (u >= 0) and (v >= 0) and (u + v < 1)):
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
mouse_drag_entry = cvsmgmt.drag_handler_entry(args = ["x","y","dx","dy"])
mouse_release_entry = cvsmgmt.release_handler_entry(args = ["x", "y"])

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



