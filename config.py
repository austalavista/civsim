import pyglet

#---CUSTOM-------------------------------------------------------------------------------------------------------------


#---COMMON-------------------------------------------------------------------------------------------------------------

#---UI---
global selected
global click_selected #cleared on mouse release

selected = None
click_selected = None

#---COLLISIONBOXES, EVENT HANDLING---
global scene_objects
global scene_objects_size

global update_queue
global update_queue_size

scene_objects_size = 2000
scene_objects = [None] * scene_objects_size #objects that are on screen are added to this list for box checks and event handling

update_queue_size = 100
update_queue = [None] * update_queue_size

#---RESOURCES---
global sprite_textures

sprite_textures = {}

# ---WINDOWING---
global window
global window_size
global scale_factor_y
global scale_factor_x
global zoom_factor_y
global zoom_factor_x

aa = pyglet.gl.Config(sample_buffers=1,samples=3) #ANTIALIASING
window = pyglet.window.Window(config = aa, resizable=True)
window_size = [window.height, window.width] #needs to be updated in program

scale_factor_y = window_size[0]/1080
scale_factor_x = window_size[1]/1920
zoom_factor_y = 1
zoom_factor_x = 1

#---BATCHES AND GROUPS---
global batch
global groups
global front_group_index

batch = pyglet.graphics.Batch()

scene_ordered_group = None
scene_transformation_group = None
menu_ordered_group = None

num_scene_groups = 7
num_menu_groups = 6
groups = []

texture_groups = {}
line_groups = {}

