from copy import deepcopy
import math
import readline

def listify_column(index, map):
    column_to_list = []
    i = 0
    while i < len(map):
        column_to_list.append(map[i][index])
        i = i + 1
    return column_to_list

def find_reflection_axis(map):
    
    midpoints = []
    result = 0
    col_or_row = ''

    found_vert_axis = False
    found_horiz_axis = False
    max_horiz_window_size_cols = int(len(map[0])//2)
    max_vert_window_size_rows = int(len(map)//2)

    # THERE WILL ALWAYS BE ONE LINE of 1->N rows of symmetry

    column_fold_index = 1

    while column_fold_index < len(map[0]):
        if column_fold_index <= int(len(map[0])//2):
            max_horiz_window_size_cols = column_fold_index
            c_pointer = column_fold_index  - max_horiz_window_size_cols
        elif column_fold_index > int(len(map[0])//2):
            max_horiz_window_size_cols = len(map[0]) - column_fold_index
            c_pointer = column_fold_index - max_horiz_window_size_cols

        num_matches = 0
        #compare sets of previous c_window_size and next
        mirror_offset = 2*max_horiz_window_size_cols-1
        compare1_offset = 0
        while mirror_offset >= max_horiz_window_size_cols:
            compare1 = listify_column(c_pointer + compare1_offset, map)
            compare2 = listify_column(c_pointer + mirror_offset, map)
            #compare
            if compare1 == compare2:
                num_matches = num_matches + 1    
            #if equal, add to list
            compare1_offset = compare1_offset + 1
            mirror_offset = mirror_offset - 1
        if num_matches == max_horiz_window_size_cols:
            #midpoint_cols.append(column_fold_index)
            result = column_fold_index
            col_or_row = 'c'
            midpoints.append((col_or_row, result))
            found_vert_axis = True
        column_fold_index = column_fold_index + 1
    
    if found_vert_axis == False or found_vert_axis:
        row_fold_index = 1
        while row_fold_index < len(map):
            if row_fold_index <= int(len(map)//2):
                max_vert_window_size_rows = row_fold_index
                r_pointer = row_fold_index  - max_vert_window_size_rows
            elif row_fold_index > int(len(map)//2):
                max_vert_window_size_rows = len(map) - row_fold_index
                r_pointer = row_fold_index - max_vert_window_size_rows

            num_matches = 0
            #compare sets of previous c_window_size and next
            mirror_offset = 2*max_vert_window_size_rows-1
            compare1_offset = 0
            while mirror_offset >= max_vert_window_size_rows:
                compare1 = map[r_pointer + compare1_offset]
                compare2 = map[r_pointer + mirror_offset]
                #compare
                if compare1 == compare2:
                    num_matches = num_matches + 1    
                #if equal, add to list
                compare1_offset = compare1_offset + 1
                mirror_offset = mirror_offset - 1
            if num_matches == max_vert_window_size_rows:
                #midpoint_rows.append(row_fold_index)
                result = row_fold_index
                col_or_row = 'r'
                midpoints.append((col_or_row, result))
                found_horiz_axis = True
            row_fold_index = row_fold_index + 1     

    return midpoints

def swap_char(c):
    if c == '.':
        return '#'
    if c == '#':
        return '.'

#f = open("Day13TestInput1.txt")
f = open("Day13Input.txt")

mirror_map = []
midpoint_cols = []
midpoint_rows = []
l = f.readline()
while l:
    temp_map = []
    while l != "\n" and l != "":
        temp = l.strip()
        temp_map.append(temp)
        l = f.readline()
    mirror_map.append(temp_map)
    l = f.readline()

old_reflections = []
new_reflections = []

for map in mirror_map:
    found_swap = False
    old_reflections = find_reflection_axis(map)
    row_index = 0
    for r in map:
        column_index = 0
        for c in r:
            swapped_map = deepcopy(map)
            swapped_char = swap_char(map[row_index][column_index])
            temp_row = r[:column_index] + swapped_char + r[(column_index+1):]
            swapped_map.pop(row_index)
            swapped_map.insert(row_index,temp_row)

#TODO: Still getting same c on first test input, need to see of there may be more than one and confirm a different one?
            new_reflections = find_reflection_axis(swapped_map)
            for ref in new_reflections:
                if ref == old_reflections[0]:
                    found_swap = False
                elif ref != old_reflections[0]:
                    if ref[0] == 'c':
                        midpoint_cols.append(ref[1])
                    elif ref[0] == 'r':
                        midpoint_rows.append(ref[1])
                    found_swap = True
                    break
            column_index = column_index + 1
            if found_swap == True:
                break
        if found_swap == True:
                break
        row_index = row_index + 1   
    if found_swap == False:
        assert("HALT")



running_sum = 0
for c in midpoint_cols:
    running_sum = running_sum + (c)
for r in midpoint_rows:
    running_sum = running_sum + (r)*100

print("running sum - " + str(running_sum))

#for each map
#find original line
#for each cell
    #swap
    #find new line
    #check if different
        #if different, mark position

