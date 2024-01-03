import copy

class map_point:
    def __init__(self, x,y, mapchar):
        self.x = x
        self.y = y
        self.mapchar = mapchar
        self.direction_of_travel = ''

class path:
    def __init__(self, point, current_length):
        self.latest_location = point
        self.path_length = current_length
        self.visited_points = set()

class xy_point:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.traveldir = dir

def find_potential_next_steps(current_point):
    #Pass in a Map_Point, not just XY Point (NEed a mapchar)
    potential_next_steps = set()
    current_char = current_point.mapchar

    down = (list(filter(lambda x: x.x == current_point.x+1 and x.y == current_point.y, hiking_map_set))[0]).mapchar
    if current_point.x > 0:
        up = list(filter(lambda x: x.x == current_point.x-1 and x.y == current_point.y, hiking_map_set))[0].mapchar
    left = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y-1, hiking_map_set))[0].mapchar
    right = list(filter(lambda x: x.x == current_point.x and x.y == current_point.y+1, hiking_map_set))[0].mapchar
    
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
    
    #Now handle normal non icy conditions. Checked input, assume we don't need to do bounds checking just # checking
    else:
        if current_point.direction_of_travel == 'D' or current_point.direction_of_travel == 'S': #means no up option
            if down != '#' and down != '^':
                potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
            if left != '#' and left != '>':
                potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
            if right != '#' and right != '<':
                potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))        
        elif current_point.direction_of_travel == 'U': #means no down option
            if left != '#' and left != '>':
                potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
            if right != '#' and right != '<':
                potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))
            if up != '#' and up != 'v':
                potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))
        elif current_point.direction_of_travel == 'L': #means no right option
            if up != '#' and up != 'v':
                potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))
            if down != '#' and down != '^':
                potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
            if left != '#' and left != '>':
                potential_next_steps.add(xy_point(current_point.x, current_point.y-1, 'L'))
        elif current_point.direction_of_travel == 'R': #means no left option
            if down != '#' and down != '^':
                potential_next_steps.add(xy_point(current_point.x + 1, current_point.y, 'D'))
            if right != '#'  and right != '<':
                potential_next_steps.add(xy_point(current_point.x, current_point.y +1, 'R'))
            if up != '#'  and up != 'v':
                potential_next_steps.add(xy_point(current_point.x - 1, current_point.y, 'U'))

    if len(potential_next_steps) == 0:
        print("Returning no locations, end ofthe LINE BICHES")

    return potential_next_steps

#f = open("Day23TestInput.txt")
f = open("Day23Input.txt")

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

successful_path_lengths = []
potential_paths = [] #Making this a list as we are going to need to be updating this

initial_path = path(starting_pt, 0)
initial_path.visited_points.add(xy_point(starting_x, starting_y, ''))
potential_paths.append(initial_path)

while len(potential_paths) > 0:
    print("Number of potential paths exploring - " + str(len(potential_paths))) 
    pp = potential_paths[0]
    end_of_current_path = False
    while end_of_current_path == False:
        #First try to handle end here
        #print("Latest location - " + str(pp.latest_location.x) + "," + str(pp.latest_location.y))
        if pp.latest_location.x == ending_x and pp.latest_location.y == ending_y:
            print("Found a path to the end with steps - " + str(pp.path_length))
            successful_path_lengths.append(pp.path_length)
            potential_paths.remove(pp)
            end_of_current_path = True

        if end_of_current_path == False:                
            potential_next_steps = find_potential_next_steps(pp.latest_location)
            potential_step_counter = 1
            
            if len(potential_next_steps) >= 1: 
                while len(potential_next_steps) > 0:
                    # Cretae a map point that represents the next location, including point, char, and direction of travel
                    next_step = potential_next_steps.pop()
                    next_step_for_comparison = copy.deepcopy(next_step)
                    next_step_for_comparison.traveldir = ''
                    
                    if next_step_for_comparison not in pp.visited_points:
                        pp.visited_points.add(next_step_for_comparison)
                        
                        #Populate the point with the data
                        next_step_on_path = map_point(next_step.x, next_step.y, '')
                        char = (list(filter(lambda x: x.x == next_step.x and x.y == next_step.y, hiking_map_set))[0]).mapchar
                        next_step_on_path.mapchar = char
                        next_step_on_path.direction_of_travel = next_step.traveldir
                        
                        #Update the current path if this is the first one we are testing - Update path with this point and increment length
                        if potential_step_counter == 1:
                            pp.latest_location = next_step_on_path #Note to self, already updating the ncurrent paths latest location and length to the first result even though we clone later
                            pp.path_length = pp.path_length + 1
                        #If there is more than one point returned, we won't just update current one, we spawn a new path
                        
                        elif potential_step_counter > 1:
                            print("Starting new path at - " + str(next_step_on_path.x) + "," + str(next_step_on_path.y))
                            new_path_copy = copy.deepcopy(pp)
                            new_path_copy.latest_location = next_step_on_path #Note - This overrides the fishy behavior above of updating fcurrentpath before copying, as we're basiclly getting it for it's length
                            new_path_copy.path_length = new_path_copy.path_length
                            potential_paths.append(new_path_copy)
                    else:
                        print("Next step is in visited set, this path is a dead end - nothing to remove, we are just not doing anythingiwth this next point")    
                    potential_step_counter +=1 
                
for l in successful_path_lengths:
    print(str(l) + " ")
print("Longest - " + str(max(successful_path_lengths)))