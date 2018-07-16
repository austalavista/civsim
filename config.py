import pyglet

#---CORE----

num_provinces = 958
provinces = None
provinces_id = {}

num_nations = -1
nations = {}

scenarios = []
saves = []

init = False #have the saves, provinces, scenarios etc been initialized?
state = "main_menu"

time_entry = None
day = 1
month = "January"
year = 1444

#---BIG DATA---
num_province_attributes = 10
province_data = None

num_nation_attributes = 10
nation_data = None
owner_mask = None

universal_data = None

#---MISC GRAPHICS---

province_borders = None
nation_borders = None
ocean = None

screen_bound_left = None
screen_bound_right = None
screen_bound_top = None
screen_bound_bottom = None

#---SETTINGS---
fullscreen = 1
resolution = 0

#---COMMON-------------------------------------------------------------------------------------------------------------

#---UI---
selected = None
click_selected = None

prev_menu = None
menus = {}

#---SWITCHING GAME STATE---
gs_entries = [None] * 20

#---COLLISIONBOXES, EVENT HANDLING---
scene_objects_size = 2000
scene_objects = [None] * scene_objects_size #objects that are on screen are added to this list for box checks and event handling

update_queue_size = 50
update_queue = [None] * update_queue_size

#---RESOURCES---
sprite_textures = {}

# ---WINDOWING---
aa = None
window = None

#---BATCHES AND GROUPS---
batch = pyglet.graphics.Batch()

global_transformation_group = None
scene_ordered_group = None
scene_transformation_group = None
menu_ordered_group = None

num_scene_groups = 7
num_menu_groups = 6
groups = []

texture_groups = {}
line_groups = {}
layouttop_groups = []
layout_groups = []

