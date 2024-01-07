class beam:
    def __init__(self, currentx, currenty, last_direction):
        self.currentx = currentx
        self.currenty = currenty
        self.last_direction = last_direction

def find_starting_direction(char, entrydir):
    if char == '.':
        return entrydir
    elif char == '|':
        if entrydir == 'up' or entrydir == 'down':
            return entrydir
        else:
            return 'none'
    elif char == '-':
        if entrydir == 'left' or entrydir == 'right':
            return entrydir
        else:
            return 'none'
    elif char == '\\':
        if entrydir == 'up':
            return 'left'
        elif entrydir == 'right':
            return 'down'
        elif entrydir == 'down':
            return 'right'
        elif entrydir == 'left':
            return 'up'
    elif char == '/':
        if entrydir == 'up':
            return 'right'
        elif entrydir == 'right':
            return 'up'
        elif entrydir == 'down':
            return 'left'
        elif entrydir == 'left':
            return 'down'
    
    return 'none'


#f = open("Day16TestInput.txt")
f = open("Day16Input.txt")

map = []

for l in f:
    templine = l.strip()
    map.append(templine)

"""
Approach for populating starting beams for Part 2:
- for each point across top, bottom, left, right
- Get char from map
- Find starting direction from function by passing in char and entry direction
- if not none, create beam and add to list
"""

starting_beams = []
#Top row starting points
for i in range(len(map[0])):
    starting_char = map[0][i]
    starting_dir = find_starting_direction(starting_char, 'down')
    if starting_dir != 'none':
        starting_beams.append(beam(0, i, starting_dir))
    
#Bottom row starting points
for i in range(len(map[0])):
    starting_char = map[len(map)-1][i]
    starting_dir = find_starting_direction(starting_char, 'up')
    if starting_dir != 'none':
        starting_beams.append(beam(len(map)-1, i, starting_dir))

#Left side starting points
for i in range(len(map)):
    starting_char = map[i][0]
    starting_dir = find_starting_direction(starting_char, 'right')
    if starting_dir != 'none':
        starting_beams.append(beam(i, 0, starting_dir))

#Right side starting points
for i in range(len(map)):
    starting_char = map[i][len(map[0])-1]
    starting_dir = find_starting_direction(starting_char, 'left')
    if starting_dir != 'none':
        starting_beams.append(beam(i, len(map[0])-1, starting_dir))

totals = []
for s in starting_beams:
    print("Starting beam at " + str(s.currentx) + ", " + str(s.currenty) + " with direction " + s.last_direction)

    #EVERYTHING BELOW HERE NEEDS TO BE REPEATED FOR EACH ATTEMPT - STARTING CLEAN FOR NEW ENTRY POINT

    #Populate energized tiles set with '.' first
    energized_tiles = []
    for i in range(len(map)):
        energized_tiles.append([])
        for j in range(len(map[i])):
            energized_tiles[i].append('.')

    #Start out by adding our first beam into the beam set, and set our first tile as '#'
    beams = []
    beams.append(s)
    energized_tiles[s.currentx][s.currenty] = '#'

    #Set up visited set to track visited tiles with direction
    visited = set()
    visited.add((s.currentx, s.currenty, s.last_direction))

    energized_count = 1

    #While there are still beams in the set, take a step for each beam
    while len(beams) > 0 :
        #This cycles through each beam
        for current_beam in beams:
            next_char = ''
            delete_current_beam = False

            #Take step for each beam - current location and direction will be updated after this, and next_char will have the char at the new location to assess for beam splitting
            if current_beam.last_direction == 'right':
                if current_beam.currenty + 1 < len(map[0]):
                    next_char = map[current_beam.currentx][current_beam.currenty + 1]
                    current_beam.currenty = current_beam.currenty + 1
                    current_beam.last_direction = 'right'
                else:
                    delete_current_beam = True
                    

            elif current_beam.last_direction == 'down':
                if current_beam.currentx + 1 < len(map):
                    next_char = map[current_beam.currentx + 1][current_beam.currenty]
                    current_beam.currentx = current_beam.currentx + 1
                    current_beam.last_direction = 'down'
                else:
                    delete_current_beam = True
                    

            elif current_beam.last_direction == 'left':
                if current_beam.currenty - 1 >= 0:
                    next_char = map[current_beam.currentx][current_beam.currenty - 1]
                    current_beam.currenty = current_beam.currenty - 1
                    current_beam.last_direction = 'left'
                else:
                    delete_current_beam = True
                    

            elif current_beam.last_direction == 'up':
                if current_beam.currentx - 1 >= 0:
                    next_char = map[current_beam.currentx - 1][current_beam.currenty]
                    current_beam.currentx = current_beam.currentx - 1
                    current_beam.last_direction = 'up'
                else:
                    delete_current_beam = True

            if ((current_beam.currentx, current_beam.currenty, current_beam.last_direction)) in visited:
                delete_current_beam = True
            else:
                visited.add((current_beam.currentx, current_beam.currenty, current_beam.last_direction))

            #Add new step to energized set
            if delete_current_beam == False:
                if energized_tiles[current_beam.currentx][current_beam.currenty] != '#':
                    energized_tiles[current_beam.currentx][current_beam.currenty] = '#'
                    energized_count += 1
                    
                #Check chars and Create new beams if necessary - will be creating new beams at current location with just different dir of travel
                if next_char == '.':
                    current_beam.last_direction = current_beam.last_direction
                
                elif next_char == '|':
                    if current_beam.last_direction == 'right' or current_beam.last_direction == 'left':
                        #print("Splitting at " + str(current_beam.currentx) + ", " + str(current_beam.currenty))
                        beams.append(beam(current_beam.currentx, current_beam.currenty, 'up'))
                        beams.append(beam(current_beam.currentx, current_beam.currenty, 'down'))
                        delete_current_beam = True
                
                elif next_char == '-':
                    if current_beam.last_direction == 'up' or current_beam.last_direction == 'down':
                        #print("Splitting at " + str(current_beam.currentx) + ", " + str(current_beam.currenty))
                        beams.append(beam(current_beam.currentx, current_beam.currenty, 'right'))
                        beams.append(beam(current_beam.currentx, current_beam.currenty, 'left'))
                        delete_current_beam = True

                elif next_char == '\\':
                    if current_beam.last_direction == 'up':
                        current_beam.last_direction = 'left'
                    elif current_beam.last_direction == 'right':
                        current_beam.last_direction = 'down'
                    elif current_beam.last_direction == 'down':
                        current_beam.last_direction = 'right'
                    elif current_beam.last_direction == 'left':
                        current_beam.last_direction = 'up'

                elif next_char == '/':
                    if current_beam.last_direction == 'up':
                        current_beam.last_direction = 'right'
                    elif current_beam.last_direction == 'right':
                        current_beam.last_direction = 'up'
                    elif current_beam.last_direction == 'down':
                        current_beam.last_direction = 'left'
                    elif current_beam.last_direction == 'left':
                        current_beam.last_direction = 'down'

            if delete_current_beam == True:
                beams.remove(current_beam)
        
    #Do stuff that we need to do at the end of each pass - print out energized tiles and add to totals
    print("Energized Tiles - " + str(energized_count))
    totals.append(energized_count)
    #HEre we have effectively completed what was PArt 1 for a given starting location and direction

print("MAX TOTAL - " + str(max(totals)))
