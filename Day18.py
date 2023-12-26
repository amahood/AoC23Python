import copy
class digging_instruction:
    def __init__(self, direction, spaces, color):
        self.direction = direction
        self.spaces = spaces
        self.color = color

instruction_set = []

f = open("Day18TestInput.txt")
#f = open("Day18Input.txt")

for l in f:
    instruction = l.split()
    # put the 6 characters of the third item in instruction after the hash mark into an object
    temp_instruction = digging_instruction(instruction[0], instruction[1], instruction[2][2:8])
    instruction_set.append(temp_instruction)


#PArt 2 need to reparwsew instruction set
for i in instruction_set:
    #convert i.color to decimal and set to i.spaces
    i.spaces = int(i.color[0:5], 16)
    if i.color[5] == '0':
        i.direction = "R"
        i.color = ''
    elif i.color[5] == '1':
        i.direction = "D"
        i.color = ''
    elif i.color[5] == '2':
        i.direction = "L"
        i.color = ''
    elif i.color[5] == '3':
        i.direction = "U"
        i.color = ''

        
print("Instructions loaded.")

dig_map_not_normalized = set()
dig_map = set()

current_row = 0
current_col = 0

for i in instruction_set:
    if i.direction == "R":
        for j in range(current_col, current_col+int(i.spaces)):
            current_col = current_col + 1
            dig_map_not_normalized.add((current_row,current_col))
            
    elif i.direction == "L":
        for j in range(current_col, current_col+int(i.spaces)):
            current_col = current_col - 1
            dig_map_not_normalized.add((current_row,current_col))
            
    elif i.direction == "U":
        for j in range(current_row, current_row+int(i.spaces)):
            current_row = current_row - 1
            dig_map_not_normalized.add((current_row,current_col))

    elif i.direction == "D":
        for j in range(current_row, current_row + int(i.spaces)):
            current_row = current_row + 1
            dig_map_not_normalized.add((current_row,current_col))

#find the max row and col in dig_map
max_row = 0
max_col = 0
min_row = 0
min_col = 0
for i in dig_map_not_normalized:
    if i[0] > max_row:
        max_row = i[0]
    if i[1] > max_col:
        max_col = i[1]
    if i[0] < min_row:
        min_row = i[0]
    if i[1] < min_col:
        min_col = i[1]

#find the min row and col in dig_map

print("Max row: " + str(max_row))
print("Max col: " + str(max_col))
print("Min row: " + str(min_row))
print("Min col: " + str(min_col))

rows_to_add = abs(min_row)
cols_to_add = abs(min_col)

total_rows = max_row + rows_to_add
total_cols = max_col + cols_to_add

#REminder - dig map is the set of tuples of locaton and character on the path
    #This is shifting them all to nromalize to 0 and then setting them to the char and adding to set
for i in dig_map_not_normalized:
    temp_location = (i[0] + rows_to_add, i[1] + cols_to_add)
    dig_map.add(temp_location)

pts_to_check = set()
vistied_pts = set()
pts_to_check.add((-1,-1))
pts_to_check.add((-1,total_cols+1))
pts_to_check.add((total_rows+1,-1))
pts_to_check.add((total_rows+1,total_cols+1))

length = total_rows + 3
width = total_cols + 3

pts_outside_map = 0

while len(pts_to_check) > 0:
    pt = pts_to_check.pop()
    if pt not in vistied_pts:
        vistied_pts.add(pt)
        if pt not in dig_map:
            pts_outside_map += 1
            if pt[0] > -1:
                pts_to_check.add((pt[0]-1, pt[1]))
            if pt[0] < total_rows+1:
                pts_to_check.add((pt[0]+1, pt[1]))
            if pt[1] > -1:
                pts_to_check.add((pt[0], pt[1]-1))
            if pt[1] < total_cols+1:
                pts_to_check.add((pt[0], pt[1]+1))
print("Dimensions - " + str(length*width))
print("Visited points - " + str(len(vistied_pts)))
print("Dig points - " + str(len(dig_map)))
print("Outside points - " + str(pts_outside_map))

print("Total dug area - " + str(length*width - pts_outside_map))


    
        





