#Removing "wrinkles"

#open files/initialize
if(True):
    temp = open("maps.txt","r")
    map_s = temp.read().split("\n")
    temp.close()

    temp = open("mapa1.txt","r")
    map_a1 = temp.read().split("\n")
    temp.close()

    mapl = open("mapl.txt", "w")
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

#unwrinkling
for r in range(0, len(provinces)):

    #closing 1-on-1 wrinkles
    for i in range(0,len(vector_adjacent_provinces[r])):
        if(i < len(vector_adjacent_provinces[r])):
            temp = (i+1)%len(vector_adjacent_provinces[r])
            counter = 0
            if(vector_adjacent_provinces[r][i] != False):
                while(vector_adjacent_provinces[r][temp] == False and counter < 10):
                    counter += 1
                    temp = (temp+1)%len(vector_adjacent_provinces[r])

                if(vector_adjacent_provinces[r][temp] == vector_adjacent_provinces[r][i] and temp != i):
                    temp = (i + 1) % len(vector_adjacent_provinces[r])
                    while(vector_adjacent_provinces[r][temp] == False):
                        vector_adjacent_provinces[r][temp] = None
                        temp = (temp + 1) % len(vector_adjacent_provinces[r])

            #popping
            k = 0
            while (k < len(vector_adjacent_provinces[r])):

                while(k < len(vector_adjacent_provinces[r]) and vector_adjacent_provinces[r][k] == None):
                    vector_adjacent_provinces[r].pop(k)
                    vector_lists[r].pop(k)
                k += 1

    #Stretching 1-on-1 wrinkles
    for i in range(0,len(vector_adjacent_provinces[r])):
        if(i < len(vector_adjacent_provinces[r])):

            temp = (i+1)%len(vector_adjacent_provinces[r])
            counter = 0
            if(vector_adjacent_provinces[r][i] != False):
                while(vector_adjacent_provinces[r][temp] == False and counter < 20):
                    counter += 1
                    temp = (temp+1)%len(vector_adjacent_provinces[r])

                #stretching
                if (vector_adjacent_provinces[r][temp] == vector_adjacent_provinces[r][i] and temp != i and counter > 0):

                    adjacent_index = vector_adjacent_provinces[r][i]
                    flag = False

                    # search for starting vertex in adjacent province
                    for k in range(0, len(vector_lists[adjacent_index])):

                        if(vector_lists[adjacent_index][k][0] == vector_lists[r][i][0] and
                                vector_lists[adjacent_index][k][1] == vector_lists[r][i][1]):
                            flag = True
                            break

                    if(flag):
                        temp = (i + 1) % len(vector_adjacent_provinces[r])
                        while (vector_adjacent_provinces[r][temp] == False):
                            vector_lists[adjacent_index].insert(k, [vector_lists[r][temp][0], vector_lists[r][temp][1]])
                            vector_adjacent_provinces[adjacent_index].insert(k,r)
                            temp = (temp + 1) % len(vector_adjacent_provinces[r])
                    else:
                        print("FAILED AT: ", r, i, "ADJACENT AT: " , adjacent_index, counter)

    # remove duplicates
    for i in range(0, len(vector_lists[r])):
        if (i < len(vector_lists[r])):
            if (vector_lists[r][i][0] == vector_lists[r][(i + 1) % len(vector_lists[r])][0] and
                        vector_lists[r][i][1] == vector_lists[r][(i + 1) % len(vector_lists[r])][1]):
                vector_lists[r].pop((i + 1) % len(vector_lists[r]))
                vector_adjacent_provinces[r].pop((i + 1) % len(vector_lists[r]))

    print("Done unwrinkling")

#removing holes
for r in range(0, len(vector_lists)):
    #Removing 3-point holes
    for i in range(0, len(vector_lists[r])):

        if(vector_adjacent_provinces[r][i] != False and vector_adjacent_provinces[r][(i+1)%len(vector_adjacent_provinces[r])] != False and vector_adjacent_provinces[r][i] != vector_adjacent_provinces[r][(i+1)%len(vector_adjacent_provinces[r])]):
            prov_0 = r
            prov_1 = vector_adjacent_provinces[r][i]
            prov_2 = vector_adjacent_provinces[r][(i+1)%len(vector_adjacent_provinces[r])]

            vec_1 = vector_lists[r][i]
            vec_2 = vector_lists[r][(i+1)%len(vector_adjacent_provinces[r])]
            found = False

            if(abs(vec_1[0] - vec_2[0]) >= 0.1 or abs(vec_1[1] - vec_2[1]) >= 0.1 ):
                #Prov_1 must have vec_1 and vec_3 adjacent to eachother
                #Prov_2 must have vec_2 and vec_3 adjacent to eachother
                #vec_3 is common to prov_1 and prov_2 and is adjacent to vec_1 and vec_2

                for p in range(0, len(vector_lists[prov_1])):
                    if(abs(vector_lists[prov_1][p][0] - vec_1[0]) <= 0.1 and abs(vector_lists[prov_1][p][1] - vec_1[1]) <= 0.1):

                        for u in range(0, len(vector_lists[prov_2])):
                            if (abs(vector_lists[prov_2][u][0] - vec_2[0]) <= 0.1 and abs(vector_lists[prov_2][u][1] - vec_2[1]) <= 0.1):

                                pot_vec_3_1 = vector_lists[prov_2][(u + 1) % len(vector_lists[prov_2])]
                                pot_vec_3_2 = vector_lists[prov_2][(u - 1) % len(vector_lists[prov_2])]

                                pot_vec_3_3 = vector_lists[prov_1][(p + 1) % len(vector_lists[prov_1])]
                                pot_vec_3_4 = vector_lists[prov_1][(p - 1) % len(vector_lists[prov_1])]

                                if(abs(pot_vec_3_1[0] - pot_vec_3_3[0]) <= 0.1 and abs(pot_vec_3_1[1] - pot_vec_3_3[1]) <= 0.1):
                                    found = True
                                    vec_3 = pot_vec_3_3
                                elif(abs(pot_vec_3_2[0] - pot_vec_3_3[0]) <= 0.1 and abs(pot_vec_3_2[1] - pot_vec_3_3[1]) <= 0.1):
                                    found = True
                                    vec_3 = pot_vec_3_3
                                elif(abs(pot_vec_3_1[0] - pot_vec_3_4[0]) <= 0.1 and abs(pot_vec_3_1[1] - pot_vec_3_4[1]) <= 0.1):
                                    found = True
                                    vec_3 = pot_vec_3_4
                                elif(abs(pot_vec_3_2[0] - pot_vec_3_4[0]) <= 0.1 and abs(pot_vec_3_2[1] - pot_vec_3_4[1]) <= 0.1):
                                    found = True
                                    vec_3 = pot_vec_3_4



                if(found):
                    if(abs(vec_1[0] - vec_3[0]) >= 0.1 or abs(vec_1[1] - vec_3[1]) >= 0.1):
                        if(abs(vec_2[0] - vec_3[0]) >= 0.1 or abs(vec_2[1] - vec_3[1]) >= 0.1):

                                temp_1 = (vec_1[0] + vec_2[0] + vec_3[0]) / 3
                                temp_2 = (vec_1[1] + vec_2[1] + vec_3[1]) / 3

                                for w in (vec_1,vec_2,vec_3):
                                    temp_vec_1 = w[0] *2 /2
                                    temp_vec_2 = w[1] *2 / 2

                                    for u in range(0,len(vector_lists)):
                                        for p in range(0,len(vector_lists[u])):

                                            if(abs(vector_lists[u][p][0] - temp_vec_1) <= 1 and abs(vector_lists[u][p][1] - temp_vec_2) <= 1):
                                                vector_lists[u][p][0] = temp_1
                                                vector_lists[u][p][1] = temp_2
                                                #print("mm")

    print("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1])
# write to file
for r in range(0, len(vector_lists)):
    if (True):
        mapl.write(
            "[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1] + "\t" + str(provinces[r][2]) + "," + str(
                provinces[r][3]) + "\n")
        mapa.write("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1] + "\n")

        for i in range(0, len(vector_lists[r])):
            mapl.write(str(vector_lists[r][i][0]) + "," + str(vector_lists[r][i][1]) + "\t")
            mapa.write(str(vector_adjacent_provinces[r][i]) + "\t")

        mapl.write("\n")
        mapa.write("\n")


