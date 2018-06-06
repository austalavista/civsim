file = open("resources/map/mapt.txt", "r").read()
map = file.split("\n")
for i in range(0,int(len(map)/2)):
    file = map[i*2+1].split("\t")

    if(int(map[i*2].split("]")[0][1:]) >= 1400):
        print(int(map[i*2].split("]")[0][1:]))
        temp_poly = cvsmr.polygon_object(0)
    else:
        temp_poly = cvsmr.polygon_object(1)

    temp_poly.vertices = [None] * ((len(file) - 1)*2)

    for j in range(0, len(file) - 1):
        if (file[j] != ''):
            temp = file[j].split(",")
            temp_poly.vertices[j*2] = float(temp[0])*10
            temp_poly.vertices[j*2+1] = (1000 - float(temp[1]))*10

    temp_poly.solid_color_coords((i*100)%101,(i*5)%16 + 50, 100+ (i*13) % 23)
    temp_poly.add_to_scene()

file = open("resources/map/mapl.txt", "r").read()
map = file.split("\n")
for i in range(0,int(len(map)/2)):#int(len(map)/2)
    try:
        file = map[i*2+1].split("\t")

        temp_poly = cvsmr.line_object(config.line_groups["1/1"])
        temp_poly.vertices_loop = [0] * (len(file) - 1) * 2
        temp_poly.colors = [255] * (len(file) - 1) * 3 * 2

        for j in range(0, len(file)):
            if (file[j] != ''):
                temp = file[j].split(",")
                temp_poly.vertices_loop[j * 2] = int((float(temp[0])) * 10)
                temp_poly.vertices_loop[j * 2 + 1] = int(((1000 - float(temp[1]))) * 10)

        temp_poly.convert_loop()
        temp_poly.add_to_scene()
    except:
        print("shit")
