#f = open("Day10TestInput2.txt")
#f = open("Day10TestInput1.txt")
f = open("Day10Input.txt")

pipe_maze = []
path = []

#Load the maze
for l in f:
    pipe_maze.append(list(l))

for r in pipe_maze:
    if r.__contains__('\n'):
        r.remove('\n') 
start_row = 0
start_col = 0
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

#Need to find what shape S has and replace before going into part 2
start_char = 'S'
#Find if -
if path.__contains__((start_row, start_col-1)) and path.__contains__((start_row, start_col+1)):
    start_char = '-'
#Find if |
if path.__contains__((start_row-1, start_col)) and path.__contains__((start_row+1, start_col)):
    start_char = '|'
#Find if L
if path.__contains__((start_row-1, start_col)) and path.__contains__((start_row, start_col+1)):
    start_char = 'L'
#Find if 7
if path.__contains__((start_row-1, start_col)) and path.__contains__((start_row, start_col-1)):
    start_char = '7'
#Find if J
if path.__contains__((start_row+1, start_col)) and path.__contains__((start_row, start_col-1)):
    start_char = 'J'
#Find if F
if path.__contains__((start_row+1, start_col)) and path.__contains__((start_row, start_col+1)):
    start_char = 'F'

pipe_maze[start_row][start_col] = start_char

numrows = len(pipe_maze)
numcols = len(pipe_maze[0])
contained_cells = 0
r = 0
c = 0
while r < numrows: 
    c = 0
    is_counting = False
    has_seen_partial_L = False
    has_seen_partial_7 = False
    has_seen_partial_J = False
    has_seen_partial_F = False
    while c < numcols:
        pc = pipe_maze[r][c]
        if path.__contains__((r,c)):
            if pc == '|':
                is_counting = not is_counting
            elif pc == 'L':
                has_seen_partial_L = True
            elif pc == '7':
                if has_seen_partial_L == True:
                    has_seen_partial_L = False
                    has_seen_partial_7 = False
                    is_counting = not is_counting
                elif has_seen_partial_F == True:
                    has_seen_partial_F = False
                    has_seen_partial_7 = False
                else:
                    has_seen_partial_7 = True
            elif pc == 'J':
                if has_seen_partial_L == True:
                    has_seen_partial_L = False
                    has_seen_partial_J = False
                elif has_seen_partial_F == True:
                    has_seen_partial_F = False
                    has_seen_partial_J = False
                    is_counting = not is_counting
                else:
                    has_seen_partial_J = True
            elif pc == 'F':
                has_seen_partial_F = True 
        else:
            if is_counting == True:
                contained_cells = contained_cells + 1
        c = c + 1
    r = r + 1            

print("Contained cells - " + str(contained_cells))
            

