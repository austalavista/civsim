#province stitching

import numpy as np

#open files/initialize
if(True):
    temp = open("mapr.txt","r")
    stage_one = temp.read().split("\n")
    temp.close()

    mapl = open("maps.txt", "w")
    mapa = open("mapa1.txt", "w")

#Load all vector data
if(True):
    provinces = [None]*int((len(stage_one)/2))
    for r in range(0,len(provinces)):
        temp = stage_one[r*2].split("\t")
        provinces[r] = (int(temp[0].split("]")[0][1:]),
                        temp[0].split("]")[1][1:],
                        int(temp[1].split(",")[0]),
                        int(temp[1].split(",")[1]))
        #print(provinces[r])

    vector_lists = [None] * len(provinces)
    for r in range(0,len(provinces)):
        #load vector data
        temp = stage_one[r*2+1].split("\t")
        vector_lists[r] = [None]*(len(temp)-1)
        for i in range(0,len(vector_lists[r])):
            if(temp[i] != ''):
                vector_lists[r][i] = [0,0]
                vector_lists[r][i][0] = int(float(temp[i].split(",")[0])*10)
                vector_lists[r][i][1] = int(float(temp[i].split(",")[1])*10)

    vector_adjacent_provinces = [None] * len(provinces) #stores province index that the vector is shared with
    for r in range(0,len(provinces)):
        #///
        vector_adjacent_provinces[r] = [False] * len(vector_lists[r])

#Stitching
for r in range(0,len(provinces)):

    #search through all provinces for 10 closest ones
    if(True):
        #setup array
        if (True):
            potential_adjacents = [None] * 50
            for i in range(0, len(potential_adjacents)):
                potential_adjacents[i] = [0,0,9000] #index, distance

        #check proximity of each province other than itself
        for i in range(0, len(provinces)):
            if(i != r):
                temp_distance = np.sqrt((provinces[i][2] - provinces[r][2])**2 + abs(provinces[i][3] - provinces[r][3])**2)

                #setup array for properly ordered replacement
                indices_to_replace = [None]*len(potential_adjacents)
                for x in range(0, len(potential_adjacents)):
                    #dummm
                    indices_to_replace[x] = False
                ii = 0

                for j in range(0,len(potential_adjacents)):
                    if(temp_distance < potential_adjacents[j][2]):
                        indices_to_replace[ii] = j
                        ii+=1

                index_to_replace = indices_to_replace[0]
                if(ii != 0):
                    for j in range(0,ii):
                        temp = max(potential_adjacents[index_to_replace][2], potential_adjacents[indices_to_replace[j]][2])

                        if(temp == potential_adjacents[indices_to_replace[j]][2]):
                            index_to_replace = indices_to_replace[j]

                    potential_adjacents[index_to_replace][0] = i
                    potential_adjacents[index_to_replace][1] = provinces[i][0]
                    potential_adjacents[index_to_replace][2] = temp_distance

    #Stitching
    if(True):
        #iterate through self vertices
        for j in range(0, len(vector_lists[r])):
            candidate_partner = [0, 0, 9000]  # province index, vector, distance

            # search for and stitch pixels within the 10 closest provinces
            for i in range(0, len(potential_adjacents)):  # iterate through adjacent provinces

                    # iterate through adjacent provinces vertices
                    for k in range(0, len(vector_lists[potential_adjacents[i][0]])):

                        # broad distance check
                        if (abs(vector_lists[r][j][0] - vector_lists[potential_adjacents[i][0]][k][0]) < 15 and
                                    abs(vector_lists[r][j][1] - vector_lists[potential_adjacents[i][0]][k][1]) < 15):

                            temp_distance = np.sqrt(
                                (vector_lists[r][j][0] - vector_lists[potential_adjacents[i][0]][k][0]) ** 2 + (
                                vector_lists[r][j][1] - vector_lists[potential_adjacents[i][0]][k][1]) ** 2)

                            if (temp_distance < candidate_partner[2]):
                                candidate_partner[0] = potential_adjacents[i][0]
                                candidate_partner[1] = k
                                candidate_partner[2] = temp_distance

            # apply stitching
            if (candidate_partner[2] != 9000):
                # start stiching process for this vector if it has not already been stitched
                if (vector_adjacent_provinces[candidate_partner[0]][candidate_partner[1]] == False):

                    vector_adjacent_provinces[r][j] = candidate_partner[0]
                    vector_adjacent_provinces[candidate_partner[0]][candidate_partner[1]] = r

                    temp = [(vector_lists[r][j][0] + vector_lists[candidate_partner[0]][candidate_partner[1]][0]) / 2,
                            (vector_lists[r][j][1] + vector_lists[candidate_partner[0]][candidate_partner[1]][1]) / 2]

                    vector_lists[r][j][0] = temp[0]
                    vector_lists[r][j][1] = temp[1]

                    vector_lists[candidate_partner[0]][candidate_partner[1]][0] = temp[0]
                    vector_lists[candidate_partner[0]][candidate_partner[1]][1] = temp[1]
                else:
                    vector_adjacent_provinces[r][j] = candidate_partner[0]
                    vector_lists[r][j][0] = vector_lists[candidate_partner[0]][candidate_partner[1]][0]
                    vector_lists[r][j][1] = vector_lists[candidate_partner[0]][candidate_partner[1]][1]

    # write to file
    if (True):
        mapl.write("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1] + "\t" + str(provinces[r][2]) + "," + str(provinces[r][3]) + "\n")
        mapa.write("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1] + "\n")

        for i in range(0, len(vector_lists[r])):
            mapl.write(str(vector_lists[r][i][0]) + "," + str(vector_lists[r][i][1]) + "\t")
            mapa.write(str(vector_adjacent_provinces[r][i]) + "\t")

        mapl.write("\n")
        mapa.write("\n")

    print("[" + str(provinces[r][0]) + "]" + "\t" + provinces[r][1])

mapa.close()
mapl.close()