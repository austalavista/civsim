from PIL import Image

#open files/initialize
if(True):
    mapl = open("mapl.txt", "r").read().split("\n")

    label_map = open("./labels/map_label.txt", "w+")

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
                vector_lists[r][i][0] = int(float(temp[i].split(",")[0])*10)
                vector_lists[r][i][1] = int(float(temp[i].split(",")[1])*10)

#Label Making
for r in range(0,len(provinces)):

    distance = 0
    point1_index = 0
    point2_index = 0

    #find 2 farthest points
    for i in range(0, len(vector_lists[r])):
        temp1 = vector_lists[r][i]

        for p in range(0, int(len(vector_lists[r])/2 + 0.5)):
            temp2 = vector_lists[r][p]
            temp_distance = (temp1[0] - temp2[0])**2 + (temp1[1] - temp2[1])**2

            if(temp_distance > distance):
                distance = temp_distance
                point1_index = i
                point2_index = p

    #take the average of each points surroudning points
    if(True):
        point1 = [(vector_lists[r][point1_index][0] + vector_lists[r][(point1_index + 1) % len(vector_lists[r])][0] + vector_lists[r][(point1_index - 1) % len(vector_lists[r])][0]) / 3,
                  (vector_lists[r][point1_index][1] + vector_lists[r][(point1_index + 1) % len(vector_lists[r])][1] + vector_lists[r][(point1_index - 1) % len(vector_lists[r])][1]) / 3]

        point2 = [(vector_lists[r][point2_index][0] + vector_lists[r][(point2_index + 1) % len(vector_lists[r])][0] + vector_lists[r][(point2_index - 1) % len(vector_lists[r])][0]) / 3,
                  (vector_lists[r][point2_index][1] + vector_lists[r][(point2_index + 1) % len(vector_lists[r])][1] + vector_lists[r][(point2_index - 1) % len(vector_lists[r])][1]) / 3]

    #order the points; point1 is the left point, point2 is the right point
    if(point1[0] < point2[0]):
        temp = point2
        point2 = point1
        point1 = temp

    #find average height
    if(True):
        length_vector = [point2[0] - point1[0],
                         point2[1] - point1[1]]
        sum = 0

        for i in range(1, 10):
            temp_point = [point1[0] + length_vector[0] / 10 * i,
                          point1[1] + length_vector[1] / 10 * i]

            temp_distance = 90000

            for j in range(0,len(vector_lists[r])):
                temp = (temp_point[0] - vector_lists[r][j][0])**2 + (temp_point[1] - vector_lists[r][j][1])**2

                if(temp < temp_distance):
                    temp_distance = temp

            sum += (temp_distance)**0.5

        height = sum / 9

    #create label
    if(True):
        #bounding size
        length = distance**0.5 * 0.8
        height = height * 0.6

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

        #actually create the image now
        label_image = Image.new('RGBA', (int(raw_length*final_scale + spacing*(len(name_letters)-1)), int(height)), None)

        length_progress = 0
        for i in range(0, len(name_letters)):
            size = name_letters[i].size
            temp = name_letters[i].resize((int(size[0]*final_scale),
                                          int(size[1]*final_scale)))
            label_image.paste(im = temp, box = (int(length_progress),0))

            length_progress += int(name_letters[i].size[0] * final_scale) + spacing

        label_image.save("labels/" + provinces[r] + ".png")


        print(r,"\t", provinces[r])