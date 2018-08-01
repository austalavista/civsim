from PIL import Image

#nation names
file = open("nationdata.txt", "r").read().split("\n")
nations = [None] * len(file)
for i in range(0,len(file)):
    nations[i] = file[i].split('\t')[0]

#letters
letters = {}

for letter in ("A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","-","."):
    letters[letter] = Image.open("letters/" + letter + ".png")

for r in range(0, len(nations)):
    name_letters = [None] * len(nations[r])

    raw_length = 0
    raw_height = 0
    for i in range(0, len(nations[r])):
        if (nations[r][i] != ' ' or i != len(nations[r]) - 1):
            if (nations[r][i] != ' '):
                name_letters[i] = letters[nations[r][i].upper()]
                temp1, temp2 = letters[nations[r][i].upper()].size
            else:
                name_letters[i] = letters['space']
                temp1, temp2 = letters['space'].size

            raw_length += temp1
            if (temp2 > raw_height):
                raw_height = temp2


        else:
            name_letters.pop()

    label_image = Image.new('RGBA', (raw_length,raw_height + 8), None)

    length_progress = 0
    for i in range(0, len(name_letters)):
        size = name_letters[i].size

        label_image.paste(im=name_letters[i], box=(int(length_progress), 4))

        length_progress += (int(name_letters[i].size[0]))

    label_image.save("nation_labels/" + nations[r] + ".png")
    print(r, nations[r])