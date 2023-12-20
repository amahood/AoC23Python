import queue


def still_has_unvisited(map):
    has_unvisited = False
    for r in map:
        for c in r:
            if c == 'U':
                has_unvisited = True
    return has_unvisited

def find_neighbors(row, col, numrows, numcols, last_three):
    
    neighbs = []
    #ONLT FINDING 90 DEGREE ONES #find upper neighbors
    if row > 0 and last_three != ("Up","Up","Up"):
        neighbs.append((row-1, col))

    #find same row neighbors
    if col > 0 and last_three != ("Left","Left","Left"):
        neighbs.append((row,col-1))
    if col < numcols-1 and last_three != ("Right","Right","Right"):
        neighbs.append((row, col+1))

    #find lower row neighbors
    if row < numrows-1 and last_three != ("Down","Down","Down"):
        neighbs.append((row+1, col))
        
    return neighbs

def found_in_cost_map(row,col):
    found = False
    for location in visited_and_cost_map:
        if location[1][0] == row and location[1][1] == col:
            found = True

    return found

def find_in_cost_map(row,col):
    for location in visited_and_cost_map:
        if location[1][0] == row and location[1][1] == col:
            next_location = location
            break
    return next_location


#f = open("Day17TestInput.txt")
f = open("Day17TestInput2.txt")
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

###UPDATED APPROACH BASED ON ARTICLES
leadingedge = queue.PriorityQueue()
last_three = ("Self","Self", "Self")
#Format is location, priority, actual cost, last three moves BUT me shoving them all into 1 may break PriorityQueue
#now priority, location, actual cost, last three moves
#WIP - Attempting to swap to get priority working
visited_and_cost_map = []

leadingedge.put((0, (0,0),  0, last_three))
visited_and_cost_map.append((0, (0,0),  0, last_three))

while leadingedge.empty() == False:
    current_location = leadingedge.get()
    print("Visiting Location: " + str(current_location[1]))

   # if current_location[1] == (number_of_rows-1,number_of_columns-1):
    #    break

    #get neighbors
    neighbors = find_neighbors(current_location[1][0], current_location[1][1], number_of_rows, number_of_columns, current_location[3])

    #score neighbors
    for next_location in neighbors:

        if found_in_cost_map(next_location[0], next_location[1]) == True:
            next_candidate = find_in_cost_map(next_location[0], next_location[1])
        else:
            next_candidate = ( 0, next_location, VERYLARGENUMBER, "")
        
        print("     Assessing Neighbor: " + str(next_candidate[1]))
        new_cost = current_location[2] + int(raw_map[next_candidate[1][0]][next_candidate[1][1]])
        if next_candidate[2] == VERYLARGENUMBER or new_cost < next_candidate[2]:

            #Use manhattan distance to the end as the priority
            #TODO - Not getting good weighting on small test input, need to try to update weighting
            manhattan_x = number_of_rows - next_candidate[1][0]-1
            manhattan_x_adder = 0
            if manhattan_x > 3:
                manhattan_x_adder = 3*((number_of_rows - next_candidate[1][0]-1)-3)//3
            manhattan_y_adder = 0
            manattan_y = number_of_columns - next_candidate[1][1]-1


            if manattan_y > 3:
                manhattan_y_adder = 3*((number_of_columns - next_candidate[1][1]-1)-3)//3
            priority = new_cost + manhattan_x + manhattan_x_adder + manattan_y + manhattan_y_adder

            #calculate the last three!
            last_movements = []
            for movement in current_location[3]:
                last_movements.append(movement)
            #find direction
            recent_movement = ""
            if next_candidate[1][0] < current_location[1][0]:
                recent_movement = "Up"
            elif next_candidate[1][0] > current_location[1][0]:
                recent_movement = "Down"
            elif next_candidate[1][1] < current_location[1][1]:
                recent_movement = "Left"
            elif next_candidate[1][1] > current_location[1][1]:
                recent_movement = "Right"
            else:
                print("ERROR: SHOULDNT NOT FIND THE DIRECTION OF TRAVEL")
            last_three = (last_movements[1], last_movements[2], recent_movement)
            
            next_candidate = (priority, next_location,  new_cost, last_three)
            leadingedge.put(next_candidate)
            visited_and_cost_map.append(next_candidate)
            print("     Updated Path: " + str(next_candidate[1]) + " with cost " + str(next_candidate[2]) + " and priority " + str(next_candidate[0]))

print("Hold")
