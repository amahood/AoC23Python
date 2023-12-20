import copy

def process_row(input_card_list, starting_index):
    row_score = 1
    num_matches_func = 0
    local_starting_index = copy.deepcopy(starting_index)

    winning_numbers_func = input_card_list[local_starting_index][0]
    
    my_numbers_func = input_card_list[local_starting_index][1]
    
    for w in winning_numbers_func:
        for m in my_numbers_func:
            if w == m:
                num_matches_func = num_matches_func + 1

    if num_matches_func > 0:
        i = 0
        while i < num_matches_func:
            local_starting_index = local_starting_index + 1
            loop_score = process_row(input_card_list, local_starting_index)
            row_score = row_score + loop_score
            i = i + 1
        #print("Temporary loop stop - loop score - " + str(loop_score) + " - Row Score - " + str(row_score))
    #Base Case = process line and no matches
    else:
        row_score = 1
        #print("Got to base case")
    return row_score

#f = open("Day4TestInput.txt")
f = open("Day4Input.txt")

running_sum = 0
game_list = []

for l in f:
    
    #Split by colon
    number_sets = l.split(':')[1]
    
    #Split by bar
    number_sets = number_sets.split('|')
    
    #split into numbers
    winning_numbers_int = []
    my_numbers_int = []
    winning_numbers = number_sets[0].split(' ')
    for w in winning_numbers:
        if w != '':
            winning_numbers_int.append(int(w))
    my_numbers = number_sets[1].split(' ')
    for m in my_numbers:
        if m != '':
            my_numbers_int.append(int(m))
    game_list.append((winning_numbers_int, my_numbers_int))

gl_tracker = 0
for gl in game_list:
    print("Card to process tracker - Original " + str(gl_tracker))
    outer_row_score = process_row(game_list, gl_tracker)
    #print("Processed row for score - " + str(outer_row_score))
    running_sum = running_sum + outer_row_score
    gl_tracker = gl_tracker + 1
    outer_row_score= 0

#running_sum = running_sum + 6
print("Overall card total = " + str(running_sum))