from PIL import Image

#Open resources-----------------------------------------------------

mountains = Image.open("mountains.png")
mountains_pix = mountains.load()
mountains_texture = Image.open("mountains_texture.png")
mountains_texture_pix = mountains_texture.load()

hills = Image.open("hills.png")
hills_pix = hills.load()
hills_texture = Image.open("hills_texture.png")
hills_texture_pix = hills_texture.load()

forest = Image.open("forest.png")
forest_pix = forest.load()

#Create image-------------------------------------------------------

terrain_map = Image.new('RGBA',
                        (mountains.size[0], mountains.size[1]),
                        None)
terrain_map_pix = terrain_map.load()

#Apply hill---------------------------------------------------------
print("Applying Hills...")
for x in range(0, terrain_map.size[0]):
    for y in range(0, terrain_map.size[1]):

        if(hills_pix[x,y][1] <= 215 and hills_pix[x,y][1] > 0):
            terrain_map_pix[x,y] = hills_texture_pix[x%10,y%10]
        else:
            terrain_map_pix[x,y] = (0,0,0,0)
            hills_pix[x,y] = (255,255,255,255)

#Apply Mountains-----------------------------------------------------
print("Applying Mountains...")
for x in range(0, terrain_map.size[0]):
    for y in range(0, terrain_map.size[1]):

        if(mountains_pix[x,y][1] <= 127 and mountains_pix[x,y][1] > 0):
            terrain_map_pix[x,y] = mountains_texture_pix[x%10,y%10]

        else:
            mountains_pix[x,y] = (255,255,255,255)

#Apply Forests-------------------------------------------------------
print("Applying Forests...")
for x in range(0, terrain_map.size[0]):
    for y in range(0, terrain_map.size[1]):

        if(forest_pix[x,y][1] <= 191 and forest_pix[x,y][1] > 0):

            if(terrain_map_pix[x,y] == (255,255,255,255) or
               terrain_map_pix[x,y] == (0,0,0,0)):

                terrain_map_pix[x,y] = (0,170,0,255)
        else:
            forest_pix[x,y] = (255,255,255,255)

#Save----------------------------------------------------------------

terrain_map.save("terrain_map.png")
mountains.save("mountains.png")
hills.save("hills.png")
forest.save("forest.png")

print("Done")