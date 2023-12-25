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

print("Map created.")

running_sum = 0
rt = 0
for r in dig_map_list:
    is_counting = False
    waiting_for_opening_hash = True
    waiting_for_closing_hash = False
    waiting_for_closing_dot = False
    ct = 0
    for c in r:
        #Case for finding first hash in a line
        if c != '.' and (waiting_for_opening_hash == True and is_counting == False and waiting_for_closing_hash == False and waiting_for_closing_dot == False):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = False
            waiting_for_closing_dot = False
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #Case for handling continuing hashes
        elif c != '.' and (is_counting == True and waiting_for_closing_hash == False and waiting_for_closing_hash == False and waiting_for_closing_dot == False):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = False
            waiting_for_closing_dot = False
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #Case for first handling counted dots
        elif c == '.' and (is_counting == True and waiting_for_opening_hash == False and waiting_for_closing_hash == False and waiting_for_closing_dot == False):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = True
            waiting_for_closing_dot = False
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #case for handling n counted dots
        elif c == '.' and (is_counting == True and waiting_for_opening_hash == False and waiting_for_closing_hash == True and waiting_for_closing_dot == False):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = True
            waiting_for_closing_dot = False
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #Case for handling first hash in closing Hash string
        elif c != '.' and (is_counting == True and waiting_for_opening_hash == False and waiting_for_closing_hash == True and waiting_for_closing_dot == False):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = False
            waiting_for_closing_dot = True
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #case for handling continued hashes in closing hash string
        elif c != '.' and (is_counting == True and waiting_for_opening_hash == False and waiting_for_closing_hash == False and waiting_for_closing_dot == True):
            is_counting = True
            waiting_for_opening_hash = False
            waiting_for_closing_hash = False
            waiting_for_closing_dot = True
            running_sum += 1
            dig_map_list[rt][ct] = 'X'
        #case for handling transition to stop counting finding dot after closing hashes
        elif c == '.' and (is_counting == True and waiting_for_opening_hash == False and waiting_for_closing_hash == False and waiting_for_closing_dot == True):
            is_counting = False
            waiting_for_opening_hash = True
            waiting_for_closing_hash = False
            waiting_for_closing_dot = False
        else:
            is_counting = False
            waiting_for_opening_hash = True
            waiting_for_closing_hash = False
            waiting_for_closing_dot = False
        ct += 1
    rt += 1

print("Running sum: " + str(running_sum))
for r in dig_map_list:
    string_to_print = ""
    for c in r:
        if c == '.':
            string_to_print += '.'
        else:
            string_to_print += c
    print(string_to_print)



        





