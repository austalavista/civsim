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

    if(True):
        sumx = 0
        sumy = 0

        minx = 900000
        miny = 900000

        maxx = 0
        maxy = 0
        for i in range(0, len(vector_lists[r])):
            sumx += vector_lists[r][i][0]
            sumy += vector_lists[r][i][1]

            if(minx > vector_lists[r][i][0]):
                minx = vector_lists[r][i][0]
            elif(maxx < vector_lists[r][i][0]):
                maxx = vector_lists[r][i][0]

            if (miny > vector_lists[r][i][1]):
                miny = vector_lists[r][i][1]
            elif (maxy < vector_lists[r][i][1]):
                maxy = vector_lists[r][i][1]

        avgx = sumx / i
        avgy = sumy / i

        #determine boundaries
        xindex = 0
        yindex = 0

        xbound = []
        ybound = []

            #solve for intersections
        for i in range(0, len(vector_lists)):
            now = vector_lists[r][i]
            next = vector_lists[r][(i+1)%len(vector_lists[r])]

            if(now[1] > avgy and next[1] < avgy or
               now[1] < avgy and next[1] > avgy):

                xbound.append((now[0] + next[0]) / 2)

            if (now[0] > avgx and next[0] < avgx or
                now[0] < avgx and next[0] > avgx):

                ybound.append((now[1] + next[1]) / 2)

            #order the boundary lists, small to large
        for i in range(0, len(xbound) - 1):
            for p in range(i+1,len(xbound)):
                if(xbound[p] < xbound[i]):
                    temp = xbound[i]
                    xbound[i] = xbound[p]
                    xbound[p] = temp

        for i in range(0, len(ybound) - 1):
            for p in range(i+1,len(ybound)):
                if(ybound[p] < ybound[i]):
                    temp = ybound[i]
                    ybound[i] = ybound[p]
                    ybound[p] = temp

            #determine segments that will be searched for COM
        length_x = xbound[1] - xbound[0]
        start_x = ybound[0]
        if(len(xbound) > 2):
            for i in range(0,len(xbound)/2):
                temp_distance = xbound[i*2+1] - xbound[i*2]
                if(length_x < temp_distance):
                    length_x = temp_distance
                    start_x = xbound[i*2]

        length_y = ybound[1] - ybound[0]
        start_y = ybound[0]
        if (len(ybound) > 2):
            for i in range(0, len(ybound) / 2):
                temp_distance = ybound[i * 2 + 1] - ybound[i * 2]
                if (length_y < temp_distance):
                    length_y = temp_distance
                    start_y = xbound[i * 2]


            #find most appropriaet almost-COM within the segments
        min_distance_x = 0
        min_distance_y = 0
        almostcomx = None
        almostcomy = None

        for x in range(1,5):
            temp_point_x = [start_x + length_x / 5 * i,avgy]
            temp_point_y = [avgx, start_y + length_y / 5 * i]

            for i in range(0,len(vector_lists[r])):
                temp_distance_x = (temp_point_x[0] - vector_lists[r][i][0])**2 + (temp_point_x[1] - vector_lists[r][i][1])**2

                if(min_distance_x > temp_distance_x):
                    min_distance_x = temp_distance_x
                    almostcomx = temp_point_x[0]

                temp_distance_y = (temp_point_y[0] - vector_lists[r][i][0]) ** 2 + (temp_point_y[1] - vector_lists[r][i][1]) ** 2

                if (min_distance_y > temp_distance_y):
                    min_distance_y = temp_distance_y
                    almostcomy = temp_point_y[0]

            #determien the COM as the average of those two points
        COM = [(almostcomx + avgx) / 2,
               (almostcomy + avgy) / 2]

        

    #points and vectors
    if(True):
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