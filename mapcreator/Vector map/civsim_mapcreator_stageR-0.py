#converts png province map into vector lists

from PIL import Image

def position_to_coords(position):
    global pix
    global previous
    global current

    if(position == 0):
        return [current[0]-1,current[1]]
    elif(position == 1):
        return [current[0]-1,current[1]+1]
    elif (position == 2):
        return [current[0], current[1] + 1]
    elif (position == 3):
        return [current[0] + 1, current[1] + 1]
    elif (position == 4):
        return [current[0]+1, current[1]]
    elif (position == 5):
        return [current[0] +1, current[1] -1]
    elif (position == 6):
        return [current[0], current[1] -1]
    elif (position == 7):
        return [current[0] - 1, current[1] - 1]

def get_previous_position():
    global current
    global previous

    if(previous[0]-current[0] == -1 and previous[1]-current[1] == 0):
        return 0
    elif(previous[0]-current[0] == -1 and previous[1]-current[1] == 1):
        return 1
    elif (previous[0] - current[0] == 0 and previous[1] - current[1] == 1):
        return 2
    elif (previous[0] - current[0] == 1 and previous[1] - current[1] == 1):
        return 3
    elif (previous[0] - current[0] == 1 and previous[1] - current[1] == 0):
        return 4
    elif (previous[0] - current[0] == 1 and previous[1] - current[1] == -1):
        return 5
    elif (previous[0] - current[0] == 0 and previous[1] - current[1] == -1):
        return 6
    elif (previous[0] - current[0] == -1 and previous[1] - current[1] == -1):
        return 7

def get_next_ccw():
    global current
    global previous
    global border
    global size
    global straight_indicator

    initial_position = get_previous_position()
    position = initial_position + 1

    if(position > 7):
        position = 0

    temp = position_to_coords(position)
    while(pix[temp[0],temp[1]] != border):
        position += 1
        if (position > 7):
            position = 0

        temp = position_to_coords(position)

    if(pix[temp[0],temp[1]] == border):
        return temp, False
    else:
        return temp, True

file = open("provinces.txt", "r")
provinces = file.read().split("\n")

im = Image.open("map.png")
pix = im.load()
size = im.size

new = open("mapr.txt","w+")

first_time = True
for i in range(0,len(provinces)):
    temp = provinces[i].split("\t")
    print(temp)

    new.write("[" + temp[0] + "]" +" " + temp[1] + "\t" + temp[2] + "," + temp[3] + "\n")

    x = int(temp[2])
    y = int(temp[3])

    border = 0
    straight_indicator = 1

    #move right until border is contacted
    while(pix[x,y] == pix[int(temp[2]),int(temp[3])]):
        x += 1
        if(x == size[0]):
            x-=1
            break

    start = [x,y]
    previous = [x-1,y]
    current = [x,y]

    new.write(str(current[0]) + "," + str(current[1]) + "\t")
    temp_coords, straight_line = get_next_ccw()

    previous = current
    current = temp_coords

    while(current != start):
        if(straight_line != True):
            new.write(str(current[0]) + "," + str(current[1]) + "\t")
        temp_coords, straight_line = get_next_ccw()
        previous = current
        current = temp_coords

    new.write("\n")



new.close()

file.close()

