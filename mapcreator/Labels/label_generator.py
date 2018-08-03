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

    #Determine points
    if(True):
        #Determine bounds and average
        sumx = 0
        sumy = 0

        maxx = 0
        maxy = 0
        minx = 900000
        miny = 900000

        for i in range(0, len(vector_lists[r])):
            sumx += vector_lists[r][i][0]
            sumy += vector_lists[r][i][1]

            if(maxx < vector_lists[r][i][0]):
                maxx = vector_lists[r][i][0]
            elif(minx > vector_lists[r][i][0]):
                minx = vector_lists[r][i][0]

            if(maxy < vector_lists[r][i][1]):
                maxy = vector_lists[r][i][1]
            elif(miny > vector_lists[r][i][1]):
                miny = vector_lists[r][i][1]

        avgx = sumx / len(vector_lists[r])
        avgy = sumy / len(vector_lists[r])

        #Determine point1 and point2
        xsum = [0, 0]  # left,right OR top,bottom
        ysum = [0, 0]
        xscore = [0, 0]
        yscore = [0, 0]
        if(maxx - minx > (maxy - miny) * 0.8):

            for i in range(0, len(vector_lists[r])):

                if(vector_lists[r][i][0] <= avgx):
                    side = 0
                else:
                    side = 1

                xsum[side] += vector_lists[r][i][0] * abs(avgx - vector_lists[r][i][0])
                xscore[side] += abs(avgx - vector_lists[r][i][0])

                ysum[side] += vector_lists[r][i][1] * abs(avgy - vector_lists[r][i][1])
                yscore[side] += abs(avgy - vector_lists[r][i][1])

            point1 = [xsum[0]/xscore[0], #left
                      ysum[0]/yscore[0]]

            point2 = [xsum[1]/xscore[1], #right
                      ysum[1]/yscore[1]]
        else:
            for i in range(0, len(vector_lists[r])):

                if(vector_lists[r][i][1] >= avgy):
                    side = 0
                else:
                    side = 1

                xsum[side] += vector_lists[r][i][0] * abs(avgx - vector_lists[r][i][0])
                xscore[side] += abs(avgx - vector_lists[r][i][0])

                ysum[side] += vector_lists[r][i][1] * abs(avgy - vector_lists[r][i][1])
                yscore[side] += abs(avgy - vector_lists[r][i][1])

            point1 = [xsum[0]/xscore[0], #top
                      ysum[0]/yscore[0]]

            point2 = [xsum[1]/xscore[1], #right
                      ysum[1]/yscore[1]]

            if(point1[0] > point2[0]):
                temp = point1
                point1 = point2
                point2 = temp

    #vectors etc
    if(True):
        line_vec = [point2[0] - point1[0],
                    point2[1] - point1[1]]
        distance = (line_vec[0]**2 + line_vec[1]**2)**0.5
        length_vector = line_vec
    #create label
    if(True):

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
        final_scale = distance / raw_length

        height = raw_height * final_scale

        #actually create the image now #scaling everything up by 2 for better resolution
        label_image = Image.new('RGBA', (int(raw_length*final_scale), int(raw_height * final_scale) + 8), None)

        length_progress = 0
        for i in range(0, len(name_letters)):
            size = name_letters[i].size

            #print(size, final_scale)
            temp = name_letters[i].resize((int(size[0]*final_scale + 0.5),
                                          int(size[1]*final_scale + 0.5)), resample = Image.ANTIALIAS)
            label_image.paste(im = temp, box = (int(length_progress),4))

            length_progress += (int(name_letters[i].size[0] * final_scale))

        label_image.save("labels/" + provinces[r] + ".png")

    #write txt
    mag = (length_vector[0]**2 + length_vector[1]**2)**0.5
    perpindicular = [length_vector[1] / mag * (raw_height + 8) * final_scale / 2, length_vector[0] / mag * (raw_height+8) * final_scale / 2 ]

    if(perpindicular[1] < 0):
        perpindicular[1] *= -1
    else:
        perpindicular[0] *= -1

    label_map.write(str(r) + " " + provinces[r] + "\t" +
                    str(point1[0] + perpindicular[0]) + "," +
                    str(point1[1] + perpindicular[1]) + "\t" +
                    str(math.asin(length_vector[1]/mag)) + "\n")

    print(r,"\t", provinces[r])