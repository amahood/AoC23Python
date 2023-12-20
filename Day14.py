from copy import deepcopy

def listify_column(index, map):
    column_to_list = []
    i = 0
    while i < len(map):
        column_to_list.append(map[i][index])
        i = i + 1
    return column_to_list

def shift_north(rock_map):
    shifted_rock_map_cols = []
    hasShifted = False
    column_to_shift = 0
    while column_to_shift < len(rock_map[0]):
        pre_shift_column = listify_column(column_to_shift, rock_map)
        post_shift_column = deepcopy(pre_shift_column)
        shifter_index = 1
        left_char_index = 0
        while shifter_index < len(pre_shift_column):
            if pre_shift_column[shifter_index] == 'O':
                left_char_index = shifter_index - 1
                left_char = post_shift_column[left_char_index]
                while left_char == '.' and left_char_index >= 0:
                    hasShifted = True
                    left_char_index -= 1
                    left_char = post_shift_column[left_char_index]       
            if hasShifted == True:
                post_shift_column[left_char_index+1] = 'O'
                post_shift_column[shifter_index] = '.'
                hasShifted = False
            shifter_index += 1
        post_shift_column.reverse()
        shifted_rock_map_cols.append(post_shift_column)
        column_to_shift += 1 
    #TODO - NEed to turn back into columns
        
    return shifted_rock_map_cols

def shift_west(rock_map):
    shifted_west_rock_map = []
    #TODO Fleshout
    return shifted_west_rock_map

def shift_east(rock_map):
    shifted_east_rock_map = []
    #TODO FLeshout
    return shifted_east_rock_map

def shift_south(rock_map):
    shifted_south_rock_map = []
    #TODO Fleshout


    return shifted_south_rock_map

CYCLECOUNT = 300

#f = open("Day14TestInput.txt")
f = open("Day14Input.txt")

cycle_sums = []

rock_map = []
shifted_rock_map = []
for line in f:
    rock_map.append(line.strip())

spin_cycle_count = 0
shifted_rock_map = deepcopy(rock_map)
while spin_cycle_count < CYCLECOUNT:
    shifted_rock_map = shift_north(shifted_rock_map)
    shifted_rock_map = shift_north(shifted_rock_map) #west
    shifted_rock_map = shift_north(shifted_rock_map) #south
    shifted_rock_map = shift_north(shifted_rock_map) #east
    spin_cycle_count += 1

    running_sum = 0 
    row_index = 0
    for col in shifted_rock_map:
        i = 0
        while i < len(col):
            if col[i] == 'O':
                running_sum += (len(shifted_rock_map) - row_index)
            i += 1
        row_index += 1
    #if spin_cycle_count % 1000 == 0:
    #print("Cycles - " + str(spin_cycle_count) + " - Load - " + str(running_sum))
    cycle_sums.append(running_sum)

i = 0
while i < len(cycle_sums) - 63:
    print("Cycle - " + str(i) + " - " + str(cycle_sums[i]) + " - Cycle + 63 - " + str(cycle_sums[i+63]))
    i += 1

print("Debug hold")