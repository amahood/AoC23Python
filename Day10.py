#f = open("Day10TestInput2.txt")
f = open("Day10TestInput1.txt")
#f = open("Day10TestInput.txt")

pipe_maze = []
path = []

#Load the maze
for l in f:
    pipe_maze.append(list(l))

for r in pipe_maze:
    if r.__contains__('\n'):
        r.remove('\n') 

#Find the start
for r in pipe_maze:
    for c in r:
        if c == 'S':
            start_row = pipe_maze.index(r)
            start_col = r.index(c)
            path.append((start_row, start_col))
            break

next_row = start_row
next_col = start_col
next_char = 'Z'
came_from = "Self"
while next_char != 'S':
    pipes_found = 0
    if came_from != "Up" and next_char!= '-' and next_char!= 'F' and next_char!= '7' and pipes_found == 0:
        #VAlid for Up = |, 7, F from not 7, F, -
        if next_row > 0:
            if pipe_maze[next_row-1][next_col] == '|' or pipe_maze[next_row-1][next_col] == '7' or pipe_maze[next_row-1][next_col] == 'F' or pipe_maze[next_row-1][next_col] == 'S':
                pipes_found = pipes_found + 1
                next_char = pipe_maze[next_row-1][next_col]
                next_row = next_row - 1
                next_col = next_col
                came_from = "Down"

    if came_from != "Down" and pipes_found == 0 and next_char!= 'J' and next_char!= 'L' and next_char!= '-':
        #VAlid for Down = |, J, L
        if next_row < len(pipe_maze)-1:
            if pipe_maze[next_row+1][next_col] == '|' or pipe_maze[next_row+1][next_col] == 'J' or pipe_maze[next_row+1][next_col] == 'L' or pipe_maze[next_row+1][next_col] == 'S':
                pipes_found = pipes_found + 1
                next_char = pipe_maze[next_row+1][next_col]
                next_row = next_row + 1
                next_col = next_col
                came_from = "Up"
    
    if came_from != "Left" and pipes_found == 0 and next_char!= '|' and next_char!= 'L' and next_char!= 'F':
        #VAlid for Left = -, L, F
        if next_col > 0:
            if pipe_maze[next_row][next_col-1] == '-' or pipe_maze[next_row][next_col-1] == 'L' or pipe_maze[next_row][next_col-1] == 'F' or pipe_maze[next_row][next_col-1] == 'S':
                pipes_found = pipes_found + 1
                next_char = pipe_maze[next_row][next_col-1]
                next_row = next_row
                next_col = next_col - 1
                came_from = "Right"
        
    if came_from != "Right" and pipes_found == 0 and next_char!= '|' and next_char!= '7' and next_char!= 'J':
        #VAlid for Right = -, 7, J
        if next_col < len(pipe_maze[0])-1:
            if pipe_maze[next_row][next_col+1] == '-' or pipe_maze[next_row][next_col+1] == '7' or pipe_maze[next_row][next_col+1] == 'J' or pipe_maze[next_row][next_col+1] == 'S':
                pipes_found = pipes_found + 1
                next_char = pipe_maze[next_row][next_col+1]
                next_row = next_row
                next_col = next_col + 1
                came_from = "Left"
    
    if pipes_found == 3:
        print("Error - 3 pipes found")
        break

    path.append((next_row, next_col))
print("Farthest point - " + str((len(path)-1)//2))

#PArt 2 reattempt 
"""
| L
| F
| |

7 |
7 F
7 L

J F
J |
J L
"""

contained_cells = 0
row = 0
for r in pipe_maze:
    column = 0
    counting_cells = False
    on_path = False
    for c in r:
        if counting_cells == True:
            if path.__contains__((row,column))==False:
                contained_cells = contained_cells + 1
                pipe_maze[row][column] = 'Z'
            elif  (c == 'L' or c == 'F' or c == '|' and path.__contains__((row,column))==True):
                counting_cells = False

        elif (c == '7' or c == '|' or c == 'J') and path.__contains__((row,column))==True and on_path == False:
                counting_cells = True
                on_path = False
        elif path.__contains__((row,column))==True and on_path == False:
            on_path = True
        elif path.__contains__((row,column))==True and on_path == True:
            on_path = True
        else:
            pipe_maze[row][column] = '0'
        column = column + 1 
    row = row + 1


"""
#Part 2
contained_cells = 0
keep_filling = True
while keep_filling == True:
    keep_filling = False
    row = 0
    for r in pipe_maze:      
        column = 0
        for c in r:          
            changed_char = False
            if path.__contains__((row,column))==True:
                changed_char = True
            if c != 'Z':

                #Start with corners
                # if it's a top left corner and lower right is not path or Z, make Z
                if c == 'F' or c == 'S':
                    if row+1 < len(pipe_maze) and column+1 < len(r) and pipe_maze[row+1][column+1] != 'Z' and path.__contains__((row+1,column+1))==False and path.__contains__((row,column))==True:
                        pipe_maze[row+1][column+1] = 'Z'
                        contained_cells = contained_cells + 1
                        keep_filling = True
                        changed_char = True
                    elif path.__contains__((row,column))==False:
                        pipe_maze[row][column] = '0'
                        changed_char = True
                elif c == '7' or c == 'S':
                    if row+1 < len(pipe_maze) and pipe_maze[row+1][column-1] != 'Z' and path.__contains__((row+1,column-1))==False and path.__contains__((row,column))==True:
                        pipe_maze[row+1][column-1] = 'Z'
                        contained_cells = contained_cells + 1
                        keep_filling = True
                        changed_char = True
                    elif path.__contains__((row,column))==False:
                        pipe_maze[row][column] = '0'
                        changed_char = True
                elif c == 'J' or c == 'S':
                    if pipe_maze[row-1][column-1] != 'Z' and path.__contains__((row-1,column-1))==False and path.__contains__((row,column))==True:
                        pipe_maze[row-1][column-1] = 'Z'
                        contained_cells = contained_cells + 1
                        keep_filling = True
                        changed_char = True
                    elif path.__contains__((row,column))==False:
                        pipe_maze[row][column] = '0'
                        changed_char = True
                elif c == 'L' or c == 'S':
                    if  column+1 < len(r) and pipe_maze[row-1][column+1] != 'Z' and path.__contains__((row-1,column+1))==False and path.__contains__((row,column))==True:
                        pipe_maze[row-1][column+1] = 'Z'
                        contained_cells = contained_cells + 1
                        keep_filling = True
                        changed_char = True
                    
                    elif path.__contains__((row,column))==False:
                        pipe_maze[row][column] = '0'
                        changed_char = True
                
                #If not in path, path on left, Z above
                elif path.__contains__((row,column)) == False and column >0 and path.__contains__((row,column-1)) == True and pipe_maze[row-1][column] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True
                    
                #If not in path, path on right, Z above
                elif path.__contains__((row,column)) == False and column < len(r)-1 and path.__contains__((row,column+1)) == True and pipe_maze[row-1][column] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True
                
                #If not in path, Z on left, path above
                elif path.__contains__((row,column)) == False and column >0 and path.__contains__((row-1,column)) == True and pipe_maze[row][column-1] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True
                    
                #if not in path, Z on left, Z above
                elif path.__contains__((row,column)) == False and column >0 and pipe_maze[row-1][column] == 'Z' and pipe_maze[row][column-1] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True

                # if not in path, Z on right, path above
                elif path.__contains__((row,column)) == False and column < len(r)-1 and path.__contains__((row-1,column)) == True and pipe_maze[row][column+1] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True

                # if not in path, Z on right, Z above
                elif path.__contains__((row,column)) == False and column < len(r)-1 and pipe_maze[row-1][column] == 'Z' and pipe_maze[row][column+1] == 'Z':
                    pipe_maze[row][column] = 'Z'
                    contained_cells = contained_cells + 1
                    keep_filling = True
                    changed_char = True
                
                if changed_char == False and path.__contains__((row,column)) == False:
                    pipe_maze[row][column] = '0'
            column = column + 1
        row = row + 1
"""
print("Contained cells - " + str(contained_cells))               