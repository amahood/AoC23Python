import queue

def find_neighbors(row, col, numrows, numcols, last_ten):
    
    neighbs = []

    has_gone_ten = False
    has_gone_four = True

    if last_ten.count("Up") == 10 or last_ten.count("Down") == 10 or last_ten.count("Right") == 10 or last_ten.count("Left") ==10:
        has_gone_ten = True

    last_direction = last_ten[9]
    if last_ten[8] != last_direction or last_ten[7] != last_direction or last_ten[6] != last_direction:
        has_gone_four = False

    if has_gone_four == False:
        if last_direction == "Up":
            neighbs.append((row-1, col))
        if last_direction == "Down":
            neighbs.append((row+1, col))
        if last_direction == "Right":
            neighbs.append((row, col+1))
        if last_direction == "Left":
            neighbs.append((row, col-1))
    else:
        #TODO WIP - redo the logic form last_three below
        if row > 0 and not (has_gone_ten == True and last_ten[9] == "Up") and last_ten[9] != "Down":
            neighbs.append((row-1, col))

        #find same row neighbors
        if col > 0 and not(has_gone_ten == True  and last_ten[9] == "Left") and last_ten[9] != "Right":
            neighbs.append((row,col-1))
        if col < numcols-1 and not(has_gone_ten == True  and last_ten[9] == "Right") and last_ten[9] != "Left":
            neighbs.append((row, col+1))

        #find lower row neighbors
        if row < numrows-1 and not(has_gone_ten == True  and last_ten[9] == "Down") and last_ten[9] != "Up":
            neighbs.append((row+1, col))
        
    return neighbs

#f = open("Day17Input.txt")
f = open("Day17TestInput.txt")
#f = open("Day17TestInput2.txt")
VERYLARGENUMBER = 100000000000000000000

raw_map = []

#Populate map
for l in f:
    temp_row = l
    temp_row = temp_row.strip()
    raw_map.append(temp_row)

number_of_columns = len(raw_map[0]) 
number_of_rows = len(raw_map)
#DONE POPULATING MAP

leadingedge = queue.PriorityQueue()
last_ten = ("Self","Self", "Self", "Self","Self", "Self", "Self","Self", "Self", "Self")
#Format is actual cost/priority, location, last three moves BUT me shoving them all into 1 may break PriorityQueue
visited_and_cost_map = set()

leadingedge.put((0, (0,0), last_ten))
visited_and_cost_map.add(((0,0), last_ten))

while leadingedge.empty() == False:
    current_location = leadingedge.get()
    #print("Visiting Location: " + str(current_location[1]))

    if current_location[1] == (number_of_rows-1,number_of_columns-1):
       break

    #get neighbors
    neighbors = find_neighbors(current_location[1][0], current_location[1][1], number_of_rows, number_of_columns, current_location[2])

    #score neighbors
    for next_location in neighbors:

        #calculate the last three!
        last_movements = []
        for movement in current_location[2]:
            last_movements.append(movement)
        #find direction
        recent_movement = ""
        if next_location[0] < current_location[1][0]:
            recent_movement = "Up"
        elif next_location[0] > current_location[1][0]:
            recent_movement = "Down"
        elif next_location[1] < current_location[1][1]:
            recent_movement = "Left"
        elif next_location[1] > current_location[1][1]:
            recent_movement = "Right"
        else:
            print("ERROR: SHOULDNT NOT FIND THE DIRECTION OF TRAVEL")

        last_ten_list = []
        i = 1
        while i < 10:
            last_ten_list.append(last_movements[i])
            i +=1 
        last_ten_list.append(recent_movement)
        last_ten = tuple(last_ten_list)

        if (next_location, last_ten) in visited_and_cost_map:
            continue
        
        #print("     Assessing Neighbor: " + str(next_candidate[1]))
        new_cost = current_location[0] + int(raw_map[next_location[0]][next_location[1]])
        next_candidate = (new_cost, next_location,last_ten)
        leadingedge.put(next_candidate)
        visited_and_cost_map.add((next_location,last_ten))
        #print("     Updated Path: " + str(next_candidate[1]) + " with cost " + str(next_candidate[0]))
print("Path cost = " + str(current_location[0]))
