class beam:
    def __init__(self, currentx, currenty, last_direction):
        self.currentx = currentx
        self.currenty = currenty
        self.last_direction = last_direction
            
#f = open("Day16TestInput.txt")
f = open("Day16Input.txt")

map = []

for l in f:
    templine = l.strip()
    map.append(templine)

energized_tiles = []
for i in range(len(map)):
    energized_tiles.append([])
    for j in range(len(map[i])):
        energized_tiles[i].append('.')

beams = []
beams.append(beam(0, 0, 'down'))
#beams.append(beam(0, 0, 'right'))
energized_tiles[0][0] = '#'

energized_count = 1

same_cycle_count = 0
previous_energized_count = 0
repeated_enough = False
while len(beams) > 0 and repeated_enough == False:
    #print("BEAM COUNT - " + str(len(beams)))
    for current_beam in beams: #MIGHT NEED TO TURN THIS INTO A POP BECAUSE I"M GOING TO GET A SET SIZE CHANGE ERROR
        next_char = ''
        delete_current_beam = False
        #Take step for each beam - current location and direction will be updated after this
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
            #print("Deleting beam at " + str(current_beam.currentx) + ", " + str(current_beam.currenty))

        #NEED TO GET TOTAL COUNT OF HASHES IN THE ENERGIZED TILES SET
        if energized_count == previous_energized_count:
            same_cycle_count += 1
        else:
            same_cycle_count = 0
            previous_energized_count = energized_count

        if same_cycle_count == 10000000:
            print("Total hashes: " + str(energized_count))
            repeated_enough = True
            break
    #print("Total hashes: " + str(energized_count))


"""
    print(" ")
    for i in range(len(energized_tiles)):
        temp = ""
        for j in range(len(energized_tiles[i])):
            temp = temp + energized_tiles[i][j]
        print(temp)
        """