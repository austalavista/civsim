import pyglet

#open files/initialize
if(True):
    mapl = open("mapl.txt", "r").read().split("\n")

    label_map = open("./labels/map_label.txt", "w+")

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