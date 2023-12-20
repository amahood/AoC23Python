from ast import Num
from asyncore import loop
from locale import locale_alias


def insert_column(index, matrix):
    matrix_expanded = []

    for r in matrix:
        build_row = ""
        build_row = r[:index] + '.' + r[index:]
        matrix_expanded.append(build_row)
    return matrix_expanded

FACTOR = 999999

#f = open("Day11TestInput.txt")
f = open ("Day11Input.txt")

universe = []
universe_stripped = []
universe_row_emptiness = []
universe_column_fullness = []

for l in f:
    universe.append(l)

for r in universe:
    r = r.strip()
    universe_stripped.append(r)


row_counter = 0
column_counter = 0

for row in universe:
    column_counter = 0
    if row.__contains__('#')==False:
        universe_row_emptiness.append(row_counter)
    for column in row:
        if column == '#' and universe_column_fullness.__contains__(column_counter) == False:
            universe_column_fullness.append(column_counter)
        column_counter = column_counter + 1
    row_counter = row_counter + 1 

universe_column_emptiness = []

i = 0
while i < len(row):
    if universe_column_fullness.__contains__(i) == False:
        universe_column_emptiness.append(i)
    i = i+1

universe_column_emptiness.sort()
universe_row_emptiness.sort()


####TRY WITHOUT THIS NEW METHOD###
"""
i = 0
temp_row = ""
while i < len(universe_stripped[0]):
    temp_row = temp_row + '.'
    i = i + 1

#insert rows
rows_inserted = 0
for i in universe_row_emptiness:
    t = 0
    while t < FACTOR-1:
        universe_stripped.insert(i + rows_inserted, temp_row)
        rows_inserted = rows_inserted + 1
        t = t + 1

cols_inserted = 0
for c in universe_column_emptiness:
    i = 0
    while i < FACTOR-1: 
        universe_stripped = insert_column(c + cols_inserted, universe_stripped)
        cols_inserted = cols_inserted + 1
        i = i + 1
"""
#print("Updated matrix dimensions - Rows - " + str(len(universe_stripped)) + " - Columns - " + str(len(universe_stripped[0])))


galaxy_locations= []
galaxy_tracker = 0
i_row = 0
for r in universe_stripped:
    i_col = 0
    for c in r:
        if c == '#':
            galaxy_locations.append((galaxy_tracker, (i_row, i_col)))
            galaxy_tracker = galaxy_tracker + 1
        i_col = i_col + 1
    i_row = i_row + 1

###NOW FIND MANHATTAN DISTANCE BETWEEN EACH
galaxy_tracker = 0
horiz_dist = 0
vert_dist = 0
looping_index = 0
running_sum = 0
for g in galaxy_locations:
    galaxy_looper = looping_index + 1
    while galaxy_looper < len(galaxy_locations):
      
        horiz_distance = 0
        num_x_gaps = 0
        lowerx = min(galaxy_locations[galaxy_looper][1][0], g[1][0])
        higherx = max(galaxy_locations[galaxy_looper][1][0], g[1][0])
        #find number of blank rows in between
        for x in universe_row_emptiness:
            if x >= lowerx and x < higherx:
                num_x_gaps = num_x_gaps +1
        horiz_distance = abs(galaxy_locations[galaxy_looper][1][0] - g[1][0]) + FACTOR*num_x_gaps

        vert_distance = 0
        num_y_gaps = 0
        lowery = min(galaxy_locations[galaxy_looper][1][1],g[1][1])
        highery = max((galaxy_locations[galaxy_looper][1][1],g[1][1]))
        for y in universe_column_emptiness:
            if y >= lowery and y < highery:
                num_y_gaps = num_y_gaps + 1
        vert_distance = abs(galaxy_locations[galaxy_looper][1][1] - g[1][1]) + FACTOR*num_y_gaps

        shortest_distance = vert_distance + horiz_distance
        running_sum = running_sum + shortest_distance
        print("Distance between - " + str(looping_index+1) + " and " + str(galaxy_looper+1) + " = " + str(shortest_distance))
        galaxy_looper = galaxy_looper + 1
    looping_index = looping_index + 1
print("Part 1 Solution = " + str(running_sum))



