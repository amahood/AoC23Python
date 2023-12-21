import queue

def find_neighbors(row, col, numrows, numcols, last_three):
    
    neighbs = []
    #ONLT FINDING 90 DEGREE ONES #find upper neighbors
    if row > 0 and last_three != ("Up","Up","Up") and last_three[2] != "Down":
        neighbs.append((row-1, col))

    #find same row neighbors
    if col > 0 and last_three != ("Left","Left","Left") and last_three[2] != "Right":
        neighbs.append((row,col-1))
    if col < numcols-1 and last_three != ("Right","Right","Right") and last_three[2] != "Left":
        neighbs.append((row, col+1))

    #find lower row neighbors
    if row < numrows-1 and last_three != ("Down","Down","Down") and last_three[2] != "Up":
        neighbs.append((row+1, col))
        
    return neighbs

"""
def found_in_cost_map(row,col, last_three):
    found = False
    for location in visited_and_cost_map:
        if location[1][0] == row and location[1][1] == col and location[2] == last_three:
            found = True

    return found

def find_in_cost_map(row,col):
    for location in visited_and_cost_map:
        if location[1][0] == row and location[1][1] == col:
            next_location = location
            break
    return next_location
"""

f = open("Day17Input.txt")
#f = open("Day17TestInput.txt")
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
last_three = ("Self","Self", "Self")
#Format is actual cost/priority, location, last three moves BUT me shoving them all into 1 may break PriorityQueue
visited_and_cost_map = set()

leadingedge.put((0, (0,0), last_three))
visited_and_cost_map.add(((0,0), last_three))

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
        last_three = (last_movements[1], last_movements[2], recent_movement)

        if (next_location, last_three) in visited_and_cost_map:
            continue
        
        #print("     Assessing Neighbor: " + str(next_candidate[1]))
        new_cost = current_location[0] + int(raw_map[next_location[0]][next_location[1]])
        next_candidate = (new_cost, next_location,last_three)
        leadingedge.put(next_candidate)
        visited_and_cost_map.add((next_location,last_three))
        #print("     Updated Path: " + str(next_candidate[1]) + " with cost " + str(next_candidate[0]))
print("Path cost = " + str(current_location[0]))
