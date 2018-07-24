from PIL import Image
import math

#open files/initialize
if(True):
    mapl = open("mapl.txt", "r").read().split("\n")

    label_map = open("map_label.txt", "w+")

    #letters
    letters = {}

    for letter in ("A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","-","."):
        letters[letter] = Image.open("letters/" + letter + ".png")

#Load all vector data
if(True):
    provinces = [None]*int((len(mapl)/2))
    for i in range(0, len(provinces)):
        provinces[i] = mapl[i*2].split("\t")[1]

    vector_lists = [None] * len(provinces)
    for r in range(0,len(provinces)):
        #load vector data
        temp = mapl[r*2+1].split("\t")
        vector_lists[r] = [None]*(len(temp)-1)
        for i in range(0,len(vector_lists[r])):
            if(temp[i] != ''):
                vector_lists[r][i] = [0,0]
                vector_lists[r][i][0] = int(float(temp[i].split(",")[0]))
                vector_lists[r][i][1] = int(float(temp[i].split(",")[1]))

#Label Making
for r in range(0,len(provinces)):

    distance = 0
    point1_index = 0
    point2_index = 0

    if(True):
        scores = [None] * len(vector_lists[r])
        indices = [None] * len(vector_lists[r]) #index of point the path is shared with
        distances = [None] * len(vector_lists[r])
        heights = [None] * len(vector_lists[r])

        for i in range(0, len(vector_lists[r])):
            temp1 = vector_lists[r][i]
            distances[i] = 0

            #f
            for p in range(0, int(len(vector_lists[r]) / 2 + 0.5)):
                temp2 = vector_lists[r][p]
                temp_distance = (temp1[0] - temp2[0]) ** 2 + (temp1[1] - temp2[1]) ** 2

                if (temp_distance > distances[i]):
                    distances[i] = temp_distance
                    indices[i] = p

            #score the path
            loc_point1 = [vector_lists[r][i][0],
                      vector_lists[r][i][1]]

            loc_point2 = [vector_lists[r][indices[i]][0],
                      vector_lists[r][indices[i]][1]]

            loc_length_vector = [loc_point2[0] - loc_point1[0],
                                 loc_point2[1] - loc_point1[1]]
            sum = 0

            #height
            min_height = 90000
            for c in range(4, 17):
                temp_point = [loc_point1[0] + loc_length_vector[0] / 20 * i,
                              loc_point1[1] + loc_length_vector[1] / 20 * i]

                temp_distance = 90000

                for j in range(0, len(vector_lists[r])):
                    temp = (temp_point[0] - vector_lists[r][j][0]) ** 2 + (temp_point[1] - vector_lists[r][j][1]) ** 2

                    if (temp < temp_distance):
                        temp_distance = temp

                if(temp_distance < min_height):
                    min_height = temp_distance

                sum += (temp_distance) ** 0.5

            heights[i] = sum / 9

            scores[i] = distances[i] * (min_height**4) * heights[i]

    #pick the path with the highest score
    hscore = 0
    chosen = None
    for i in range(0,len(vector_lists[r])):
        if(scores[i] > hscore):
            point1_index = i
            point2_index = indices[i]
            distance = distances[i]
            hscore = scores[i]
            height = heights[i]

    #points
    point1 = [vector_lists[r][point1_index][0],
              vector_lists[r][point1_index][1]]

    point2 = [vector_lists[r][point2_index][0],
              vector_lists[r][point2_index][1]]

    #order the points; point1 is the left point, point2 is the right point
    if(point1[0] > point2[0]):
        temp = point2
        point2 = point1
        point1 = temp

    #length vector
    length_vector = [point2[0] - point1[0],
                     point2[1] - point1[1]]

    #create label
    if(True):
        #bounding size
        length = (distance**0.5) * 0.7
        height = height * 0.5

        #find raw name size
        raw_length = 0
        raw_height = 0
        name_letters = [None] * len(provinces[r])

        for i in range(0,len(provinces[r])):
            if(provinces[r][i] != ' ' or i != len(provinces[r])-1):
                if(provinces[r][i] != ' '):
                    name_letters[i] = letters[provinces[r][i].upper()]
                    temp1, temp2 = letters[provinces[r][i].upper()].size
                else:
                    name_letters[i] = letters['space']
                    temp1, temp2 = letters['space'].size

                raw_length += temp1
                if(temp2 > raw_height):
                    raw_height = temp2


            else:
                name_letters.pop()



        #determine scaling factor and word spacing
        length_scale = length / raw_length
        height_scale = height / raw_height

        final_scale = None
        spacing = None

        if(length_scale <= height_scale):
            #length limit hit, no letter spacing
            spacing = 1
            final_scale = length_scale
        else:
            #height limit hit, add letter spacing
            spacing = (length - raw_length * height_scale) / (len(name_letters) - 1)
            final_scale = height_scale
        height = raw_height * final_scale




        #actually create the image now #scaling everything up by 2 for better resolution
        label_image = Image.new('RGBA', (int(raw_length*final_scale + spacing*(len(name_letters)-1)) * 2, int(raw_height * final_scale) * 2 + 6), None)

        length_progress = 0
        for i in range(0, len(name_letters)):
            size = name_letters[i].size
            temp = name_letters[i].resize((int(size[0]*final_scale) * 2,
                                          int(size[1]*final_scale) * 2), resample = Image.ANTIALIAS)
            label_image.paste(im = temp, box = (int(length_progress),3))

            length_progress += (int(name_letters[i].size[0] * final_scale) + spacing) * 2

        label_image.save("labels/" + provinces[r] + ".png")

    #write txt
    mag = (length_vector[0]**2 + length_vector[1]**2)**0.5
    perpindicular = [length_vector[1] / mag * raw_height * final_scale, length_vector[0] / mag * raw_height * final_scale ]

    if(perpindicular[1] < 0):
        perpindicular[1] *= -1
    else:
        perpindicular[0] *= -1

    label_map.write(str(r) + " " + provinces[r] + "\t" +
                    str(point1[0] + length_vector[0] * 0.15 + perpindicular[0]) + "," +
                    str(point1[1] + length_vector[1] * 0.15 + perpindicular[1]) + "\t" +
                    str(math.asin(length_vector[1]/mag)) + "\n")

    print(r,"\t", provinces[r])