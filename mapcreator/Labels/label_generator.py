#open files/initialize
if(True):
    mapl = open("mapl.txt", "r").read().split("\n")
    mapt = open("mapt.txt", "r").read().split("\n")

    label_map = open("./labels/map_label.txt", "w+")

#Load all vector data
if(True):
    provinces = [None]*int((len(stage_one)/2))
    for r in range(0,len(provinces)):
        temp = stage_one[r*2].split("\t")
        provinces[r] = (int(temp[0].split("]")[0][1:]),
                        temp[0].split(" ")[1],
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
        #print(vector_lists[r])
            if(len(vector_lists[r][i]) != 2):
                print("yuh")

    vector_adjacent_provinces = [None] * len(provinces) #stores province index that the vector is shared with
    for r in range(0,len(provinces)):
        #///
        vector_adjacent_provinces[r] = [False] * len(vector_lists[r])