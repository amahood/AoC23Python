import copy
class digging_instruction:
    def __init__(self, direction, spaces, color):
        self.direction = direction
        self.spaces = spaces
        self.color = color

instruction_set = []

#f = open("Day18TestInput.txt")
f = open("Day18Input.txt")

for l in f:
    instruction = l.split()
    # put the 6 characters of the third item in instruction after the hash mark into an object
    temp_instruction = digging_instruction(instruction[0], instruction[1], instruction[2][2:8])
    instruction_set.append(temp_instruction)

print("Instructions loaded.")

dig_map = set()

current_row = 0
current_col = 0

for i in instruction_set:
    if i.direction == "R":
        for j in range(current_col, current_col+int(i.spaces)):
            current_col = current_col + 1
            dig_map.add(((current_row,current_col), i.color))
            
    elif i.direction == "L":
        for j in range(current_col, current_col+int(i.spaces)):
            current_col = current_col - 1
            dig_map.add(((current_row,current_col), i.color))
            
    elif i.direction == "U":
        for j in range(current_row, current_row+int(i.spaces)):
            current_row = current_row - 1
            dig_map.add(((current_row,current_col), i.color))

    elif i.direction == "D":
        for j in range(current_row, current_row + int(i.spaces)):
            current_row = current_row + 1
            dig_map.add(((current_row,current_col), i.color))


#find the max row and col in dig_map
max_row = 0
max_col = 0
for i in dig_map:
    if i[0][0] > max_row:
        max_row = i[0][0]
    if i[0][1] > max_col:
        max_col = i[0][1]

#find the min row and col in dig_map
min_row = 0
min_col = 0
for i in dig_map:
    if i[0][0] < min_row:
        min_row = i[0][0]
    if i[0][1] < min_col:
        min_col = i[0][1]

print("Max row: " + str(max_row))
print("Max col: " + str(max_col))
print("Min row: " + str(min_row))
print("Min col: " + str(min_col))

rows_to_add = abs(min_row)
cols_to_add = abs(min_col)

total_rows = max_row + rows_to_add
total_cols = max_col + cols_to_add

dig_map_list = []
for i in range(total_rows+1):
    temp_dig_row = []
    for j in range(total_cols+1):
        temp_dig_row.append('.')
    dig_map_list.append(temp_dig_row)

for i in dig_map:
    dig_map_list[i[0][0] + rows_to_add][i[0][1]+cols_to_add] = i[1]

temp_string_to_add_top_bottom = []
for i in range(total_cols+1):
    temp_string_to_add_top_bottom.append('.')
dig_map_list.insert(0, copy.deepcopy(temp_string_to_add_top_bottom))
dig_map_list.append(copy.deepcopy(temp_string_to_add_top_bottom))

for r in dig_map_list:
    r.insert(0, '.')
    r.append('.')

print("Map created.")

pts_to_check = set()
vistied_pts = set()
pts_to_check.add((0,0))
pts_to_check.add((0,len(dig_map_list[0])-1))
pts_to_check.add((len(dig_map_list)-1,0))
pts_to_check.add((len(dig_map_list)-1,len(dig_map_list[0])-1))

while len(pts_to_check) > 0:
    pt = pts_to_check.pop()
    if pt not in vistied_pts:
        vistied_pts.add(pt)
        #COP GENERATED BELOW HERE, NEED TO CHECK
        if dig_map_list[pt[0]][pt[1]] == '.':
            dig_map_list[pt[0]][pt[1]] = 'X'
            if pt[0] > 0:
                pts_to_check.add((pt[0]-1, pt[1]))
            if pt[0] < len(dig_map_list)-1:
                pts_to_check.add((pt[0]+1, pt[1]))
            if pt[1] > 0:
                pts_to_check.add((pt[0], pt[1]-1))
            if pt[1] < len(dig_map_list[0])-1:
                pts_to_check.add((pt[0], pt[1]+1))

running_sum = 0
for r in dig_map_list:
    string_to_print = ""
    for c in r:
        if c == '.':
            string_to_print += '.'
            running_sum += 1
        elif c == 'X':
            string_to_print += 'X'
        else:
            string_to_print += '#'
            running_sum += 1
    print(string_to_print)

print("Running sum: " + str(running_sum))


    
        





