import queue

def find_neighbs(current_location, numrows, numcols):
    neighbor_set = set()
    if current_location[1][0] > 0 and is_in_rockset((current_location[1][0]-1, current_location[1][1])) == False:
        neighbor_set.add((current_location[0] + 1, (current_location[1][0]-1, current_location[1][1])))
    
    if current_location[1][0]<(numrows-1) and is_in_rockset((current_location[1][0]+1, current_location[1][1])) == False:
        neighbor_set.add((current_location[0] + 1, (current_location[1][0]+1, current_location[1][1])))

    if current_location[1][1]>0 and is_in_rockset((current_location[1][0], current_location[1][1]-1)) == False:
        neighbor_set.add((current_location[0] + 1, (current_location[1][0], current_location[1][1]-1)))
    
    if current_location[1][1]<numcols-1 and is_in_rockset((current_location[1][0], current_location[1][1]+1)) == False:
        neighbor_set.add((current_location[0] + 1, (current_location[1][0], current_location[1][1]+1)))
    return neighbor_set

def is_in_rockset(location):
    is_rock = False
    for r in rock_set:
        if r[0] == location[0] and r[1] == location[1]:
            is_rock = True
    return is_rock

#f = open("Day21TestInput.txt")
f = open("Day21Input.txt")

STEPS = 64

input_lines = []
for l in f:
    l = l.strip()
    input_lines.append(l)

numrows = len(input_lines)
numcols = len(input_lines[0])

starting_point = (0,0)
visited_set = set()
rock_set = set()
frontier = queue.PriorityQueue()

r_tracker = 0
for r in input_lines:
    c_counter = 0
    for c in r:
        if c == 'S':
            starting_point = (r_tracker, c_counter)
        elif c == '#':
            rock_set.add((r_tracker, c_counter))
        c_counter += 1
    r_tracker += 1

still_walking = True #Will set this to if nothing in frontier set has <STEPS
frontier.put((0,(starting_point)))

while still_walking == True:
    current_patch = frontier.get()
    visited_set.add(current_patch)
    neighbs = find_neighbs(current_patch, numrows, numcols)
    for n in neighbs:
        if n not in visited_set:
            frontier.put(n)
    
    still_walking = False
    for f in frontier.queue:
        if f[0] <= STEPS:
            still_walking = True
            break

patch_counter = 0
for v in visited_set:
    if v[0] == STEPS:
        patch_counter += 1

print("Patch Counter = " + str(patch_counter))
    


