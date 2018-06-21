#create triangulated polygon lines

import tripy

#open files/initialize
temp = open("mapl.txt","r")
stage_two = temp.read().split("\n")
temp.close()

stage_T = open("mapt.txt", "w")

for r in range(0,int(len(stage_two)/2)):

    temp = stage_two[r * 2 + 1].split("\t")
    vector_list = [None] * (len(temp) - 1)

    for i in range(0, len(vector_list)):
        if (temp[i] != ''):
            vector_list[i] = [0, 0]
            vector_list[i][0] = int(float(temp[i].split(",")[0]))
            vector_list[i][1] = int(float(temp[i].split(",")[1]))

    #remove duplicates
    for i in range(0,len(vector_list)):
        if(i < len(vector_list)):
            if(vector_list[i][0] == vector_list[(i+1)%len(vector_list)][0]and
                vector_list[i][1] == vector_list[(i + 1) % len(vector_list)][1]):

                vector_list.pop((i + 1) % len(vector_list))

    triangles = tripy.earclip(vector_list)
    stage_T.write(stage_two[r * 2] + "\n")
    for h in range(0, len(triangles)):
        for l in range(0, 3):
            stage_T.write(str(triangles[h][l][0]) + "," + str(triangles[h][l][1]) + "\t")
    stage_T.write("\n")
    print(stage_two[r * 2])

stage_T.close()
