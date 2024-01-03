import copy

class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.incoming_nodes = set()
        self.neighbors = set()

class edge:
    def __init__(self, start_x, start_y, dir_from_start):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = 0
        self.end_y = 0
        self.length = 0
        self.dir_from_start = dir_from_start

class map_point:
    def __init__(self, x,y, mapchar):
        self.x = x
        self.y = y
        self.mapchar = mapchar
        self.direction_of_travel = ''

class path:
    def __init__(self, latest_x, latest_y, current_length):
        self.latest_x = latest_x
        self.latest_y = latest_y
        self.path_length = current_length
        self.visited_points = set()

class xy_point:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.direction_of_travel = dir

class xy_point2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def find_potential_next_steps(current_point):
    #Pass in a Map_Point, not just XY Point (NEed a mapchar)
    potential_next_steps = set()

    down = (list(filter(lambda x: x.x == current_point.x+1 and x.y == current_point.y, hiking_map_set))[0]).mapchar
    if current_point.x > 0:
        up = list(filter(lambda x: x.x == current_point.x-1 and x.y == current_point.y, hiking_map_set))[0].mapchar
    left = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y-1, hiking_map_set))[0].mapchar
    right = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y+1, hiking_map_set))[0].mapchar
    
    #Part 2 - Remove the Ice Logic
    """
    #Handle the icy patches first to make sure we go there
    #Assumption that we are not getting iced off a cliff so not doing bounds checking here
    if current_char == '^':
        potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))
    elif current_char == 'v':
        potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
    elif current_char == '<':
        potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
    elif current_char == '>':
        potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))
    """
    
    #Now handle normal non icy conditions. Checked input, assume we don't need to do bounds checking just # checking
    #else:
    if current_point.direction_of_travel == 'D' or current_point.direction_of_travel == 'S': #means no up option
        if down != '#':
            potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
        if left != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
        if right != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))        
    elif current_point.direction_of_travel == 'U' and current_point.x > 0: #means no down option
        if left != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
        if right != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))
        if up != '#':
            potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))
    elif current_point.direction_of_travel == 'L': #means no right option
        if up != '#':
            potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))
        if down != '#':
            potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
        if left != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
    elif current_point.direction_of_travel == 'R': #means no left option
        if down != '#':
            potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
        if right != '#':
            potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))
        if up != '#':
            potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))

    if len(potential_next_steps) == 0:
        print("Returning no locations, end ofthe LINE BICHES")

    return potential_next_steps

def is_junction(current_point):
    is_junction = False
    
    down = (list(filter(lambda x: x.x == current_point.x+1 and x.y == current_point.y, hiking_map_set))[0]).mapchar
    up = list(filter(lambda x: x.x == current_point.x-1 and x.y == current_point.y, hiking_map_set))[0].mapchar
    left = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y-1, hiking_map_set))[0].mapchar
    right = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y+1, hiking_map_set))[0].mapchar

    if down != '#' and up != '#' and left != '#':
        is_junction = True
    elif down != '#' and up != '#' and right != '#':
        is_junction = True
    elif down != '#' and left != '#' and right != '#':
        is_junction = True
    elif up != '#' and left != '#' and right != '#':
        is_junction = True

    return is_junction

f = open("Day23TestInput.txt")
#f = open("Day23Input.txt")

hiking_map = []
for l in f:
    raw_line = l.strip()
    hiking_map.append(raw_line)

#Turn the input into a set of map points with x, y, char
hiking_map_set = set()
r_counter = 0
for r in hiking_map:
    c_counter = 0
    for c in r:
        hiking_map_set.add(map_point(r_counter,c_counter,c))
        c_counter +=1
    r_counter += 1

starting_x = 0
starting_y = hiking_map[0].find('.')

ending_x = len(hiking_map)-1
ending_y = hiking_map[len(hiking_map)-1].find('.')

starting_pt = list(filter(lambda x: x.x == starting_x and x.y == starting_y, hiking_map_set))[0]
starting_pt.direction_of_travel = 'S'
ending_pt = list(filter(lambda x: x.x == ending_x and x.y == ending_y, hiking_map_set))[0]


#PART 2 WORKING TO BUILD THE MAP
"""
Approach - Do it in two passes.
- First pass - Find the nodes, and find the edges with starting node and ending node
- Second pass - Go through and add the end nodes and lengths to each node

"""
node_set = set()
node_set.add((starting_x, starting_y))
node_set.add((ending_x, ending_y))

# Edge has startx/y, endx/y, length, dir from start
initial_edge = edge(starting_x, starting_y, 'D')

potential_edges = set()
potential_edges.add(initial_edge)

known_edges = set()

visited_set = set()
visited_set.add((starting_x, starting_y))

while len(potential_edges) > 0:

    #print("Number of potential edges to close - " + str(len(potential_edges))) 
    pe = potential_edges.pop()    
    current_location = xy_point(pe.start_x, pe.start_y, pe.dir_from_start)
    
    #I Change my current location here but haven't updated length
    if pe.dir_from_start == 'D':
        current_location.x += 1
    elif pe.dir_from_start == 'U':
        current_location.x -= 1
    elif pe.dir_from_start == 'L':
        current_location.y -= 1
    elif pe.dir_from_start == 'R':
        current_location.y += 1
    pe.length += 1 #This handles updating length for first step along any new path
    
    closed_current_edge = False

    while closed_current_edge == False:
        
        #Handle the end first
        if current_location.x == ending_x and current_location.y == ending_y:
            #Close current edge - #Already took the first step above so length is correct if we hit first time, need to check below
            closed_current_edge = True
            pe.end_x = current_location.x
            pe.end_y = current_location.y
            known_edges.add(pe)
            print("Found the end, closing edge with length - " + str(pe.length) + " from " + str(pe.start_x) + "," + str(pe.start_y) + " to " + str(pe.end_x) + "," + str(pe.end_y))

        else:  
            potential_next_steps = find_potential_next_steps(current_location)
            #If it's only one step, we can just update location, update, length, and go again
            if len(potential_next_steps) == 1:
                current_location = potential_next_steps.pop()
                visited_set.add((current_location.x, current_location.y)) #We've basically taken the step forward at this point
                pe.length += 1

            #If it's more than one step, we need to create a new node edge for each step, and add it to the potential edges
            elif len(potential_next_steps) > 1:
                #pe.length += 1 #HMMMM not sure we need to do this
                #Create and add new node
                node_set.add((current_location.x, current_location.y))

                #Close current edge - we stepped forward in the previous iteration with one step, updated length there and current location, so we shouldn't need to update anything
                closed_current_edge = True
                pe.end_x = current_location.x
                pe.end_y = current_location.y
                known_edges.add(pe)
                print("Found the end, closing edge with length - " + str(pe.length) + " from " + str(pe.start_x) + "," + str(pe.start_y) + " to " + str(pe.end_x) + "," + str(pe.end_y))
                
                #Create new edges
                for pns in potential_next_steps:
                    #if ((pns.x, pns.y)) in visited_set:
                        #print("Abandoning")
                    if ((pns.x, pns.y)) not in visited_set:
                        new_edge = edge(current_location.x, current_location.y, pns.direction_of_travel)
                        potential_edges.add(new_edge)

#AT THIS POINT I HAVE THE GRAPH of NODES AND EDGES
node_set_objects = set()
for n in node_set:
    node_set_objects.add(node(n[0], n[1]))

for e in known_edges:
    #Attach end to start
    starting_node = list(filter(lambda x: x.x == e.start_x and x.y == e.start_y, node_set_objects))[0]
    starting_node.neighbors.add((e.end_x, e.end_y, e.length))

    #Attach start to end
    ending_node = list(filter(lambda x: x.x == e.end_x and x.y == e.end_y, node_set_objects))[0]
    ending_node.neighbors.add((e.start_x, e.start_y, e.length))
    
print("BUILT THE GRAPH")
#At this point I have nodes with the edges attached in node_set_objects
#Now I need to do the traversal and find the paths

"""
Approach for this part
- Start at the starting node
- Need to basically do the DFS from the starting node again, but already have the neighbors
"""

successful_path_lengths = []
potential_paths = []

initial_path = path(starting_x, starting_y, 0)
initial_path.visited_points.add((starting_x, starting_y))
potential_paths.append(initial_path)

while len(potential_paths) > 0:
    pp = potential_paths[0]
    end_of_current_path = False

    while end_of_current_path == False:
        #First try to handle end here
        if pp.latest_x == ending_x and pp.latest_y == ending_y:
            print("Found a path to the end with steps - " + str(pp.path_length))
            successful_path_lengths.append(pp.path_length)
            potential_paths.remove(pp)
            end_of_current_path = True

        else:
            found_something = False
            neighbor_counter = 0
            #FIND NEIGHBORS - These are already attached to the node objects
            node_neighbors = list(filter(lambda x: x.x == pp.latest_x and x.y == pp.latest_y, node_set_objects))[0].neighbors
            for n in node_neighbors:
                #Check if we've already visited the neighbor
                if (n[0], n[1]) not in pp.visited_points:
                    if neighbor_counter == 0:
                        #Update main path
                        pp.latest_x = n[0]
                        pp.latest_y = n[1]
                        pp.path_length += n[2]
                        pp.visited_points.add((n[0], n[1]))
                        neighbor_counter += 1
                        found_something = True
                    else:
                        #Create new path
                        print("Creating new path at " + str(pp.latest_x) + "," + str(pp.latest_y))
                        new_path = copy.deepcopy(pp)
                        new_path.latest_x = n[0]
                        new_path.latest_y = n[1]
                        new_path.path_length += n[2]
                        new_path.visited_points.add((n[0], n[1]))
                        potential_paths.append(new_path)
                        found_something = True
            #MAYBE I NEED TO HANDLE DISCARDING PATHS IF I CANT GO ANYWHERE
            if found_something == False:
                print("Found nothing, discarding")
                potential_paths.remove(pp)
                end_of_current_path = True

print("Longest path - " + str(max(successful_path_lengths)))

print("Debugging PArt 2")