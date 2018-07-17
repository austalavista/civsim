import numpy as np

#open files/initialize
if(True):
    temp = open("mapa1.txt","r")
    map_a1 = temp.read().split("\n")
    temp.close()

    temp = open("mapl.txt", "r")
    map_s = temp.read().split("\n")
    temp.close()

    mapa = open("mapa.txt", "w")

#Load all vector data
if(True):
    provinces = [None]*int((len(map_s)/2))
    for r in range(0,len(provinces)):
        temp = map_s[r*2].split("\t")
        provinces[r] = (int(temp[0].split("]")[0][1:]),
                        temp[1],
                        int(temp[2].split(",")[0]),
                        int(temp[2].split(",")[1]))

    vector_lists = [None] * len(provinces)
    for r in range(0,len(provinces)):
        #load vector data
        temp = map_s[r*2+1].split("\t")
        vector_lists[r] = [None]*(len(temp)-1)
        for i in range(0,len(vector_lists[r])):
            if(temp[i] != ''):
                vector_lists[r][i] = [0,0]
                vector_lists[r][i][0] = (float(temp[i].split(",")[0]))
                vector_lists[r][i][1] = (float(temp[i].split(",")[1]))

    vector_adjacent_provinces = [None] * len(provinces)  # stores province index that the vector is shared with
    for r in range(0,len(provinces)):
        vector_adjacent_provinces[r] = [False] * len(vector_lists[r])

        temp = map_a1[r*2+1].split("\t")
        for i in range(0, len(vector_adjacent_provinces[r])):
            if(temp[i] != "False"):
                vector_adjacent_provinces[r][i] = int(temp[i])

#Ccomprehensive adjacents
for r in range(0, len(vector_lists)):
    for i in range(0, len(vector_lists[r])):
        falsed = False
        counter = 0

        vector_adjacent_provinces[r][i] = []

        for u in range(0, len(vector_lists)):

            if(u != r and np.sqrt((provinces[u][2] - provinces[r][2]) ** 2 + abs(provinces[u][3] - provinces[r][3]) ** 2) <= 100):

                for p in range(0, len(vector_lists[u])):

                    if(abs(vector_lists[r][i][0] - vector_lists[u][p][0]) <= 0.1 and abs(vector_lists[r][i][1] - vector_lists[u][p][1]) <= 0.1):
                        vector_adjacent_provinces[r][i].append(u)
                        counter += 1

        if(counter == 0 and not falsed):
            falsed = True
            vector_adjacent_provinces[r][i].append(False)

    print("Comprehensive Adjacents: [" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1])

#Smoothing the lonelys
for r in range(0,len(vector_lists)):
    for i in range(0, len(vector_lists[r])):

        if(vector_adjacent_provinces[r][i] == False):

            vector_lists[r][i][0] = (vector_lists[r][i][0] * 2 + vector_lists[r][(i - 1 )% len(vector_lists[r])][0] + vector_lists[r][(i + 1) % len(vector_lists[r])][0]) / 4
            vector_lists[r][i][1] = (vector_lists[r][i][1] * 2 + vector_lists[r][(i - 1) % len(vector_lists[r])][1] + vector_lists[r][(i + 1) % len(vector_lists[r])][1]) / 4

    print("SMOOTHING LONELIES: [" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1])

# write to file
for r in range(0, len(vector_lists)):
    if (True):
        mapa.write("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1] + "\n")

        for i in range(0, len(vector_lists[r])):

            for p in range(0, len(vector_adjacent_provinces[r][i])):
                mapa.write(str(vector_adjacent_provinces[r][i][p]) + ",")
            mapa.write("\t")

        mapa.write("\n")