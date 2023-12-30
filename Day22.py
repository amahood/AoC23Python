import copy

class Brick():
    def __init__(self, id, startpt, endpt):
        self.id = id
        self.startpt = startpt
        self.endpt = endpt
        self.length = self.calc_length((startpt),(endpt))
        self.orientation = self.calc_orientation((startpt),(endpt))
        self.lowest_z = min(startpt[2], endpt[2])
        self.occupiedpts = self.calc_occupied_points()
        self.supportingbricks = [] #This is bricks that are supporting it, NOT bricks it is supporting
        self.bricks_supported = set()

    def calc_length(self, startpt, endpt):
        length = 0
        if startpt == endpt:
            length = 1
        else:
            xdelta = abs(endpt[0]-startpt[0])
            ydelta = abs(endpt[1]-startpt[1])
            zdelta = abs(endpt[2]-startpt[2])

            if xdelta == 0 and ydelta == 0:
                length = zdelta+1
            elif xdelta == 0 and zdelta == 0:
                length = ydelta+1
            elif ydelta == 0 and zdelta == 0:
                length = xdelta + 1
        return length
    
    def calc_orientation(self, startpt, endpt):
        """
        Orientation is the direction of change, e.g. extends in orientation direction. S if just one block.
        """
        if startpt == endpt:
            orientation = 'Z'
        else:
            orientation = ''
            xdelta = abs(endpt[0]-startpt[0])
            ydelta = abs(endpt[1]-startpt[1])
            zdelta = abs(endpt[2]-startpt[2])

            if xdelta == 0 and ydelta == 0:
                orientation = 'Z'
            elif xdelta == 0 and zdelta == 0:
                orientation = 'Y'
            elif ydelta == 0 and zdelta == 0:
                orientation = 'X'
        return orientation
    
    def calc_occupied_points(self):
        occupied_pts = []

        if self.orientation == 'Z':
            #for z in range(self.startpt[2], self.endpt[2]+1):
            for z in range( min(self.startpt[2], self.endpt[2]), max(self.startpt[2], self.endpt[2])+1):
                occupied_pts.append((self.startpt[0], self.startpt[1], z))

        if self.orientation == 'X':
            #for x in range(self.startpt[0], self.endpt[0]+1):
            for x in range( min(self.startpt[0], self.endpt[0]), max(self.startpt[0], self.endpt[0])+1):
                occupied_pts.append((x, self.startpt[1], self.startpt[2]))
        
        if self.orientation == 'Y':
            #for y in range(self.startpt[1], self.endpt[1]+1):
            for y in range( min(self.startpt[1], self.endpt[1]), max(self.startpt[1], self.endpt[1])+1):
                occupied_pts.append((self.startpt[0], y, self.startpt[2]))
        
        return occupied_pts

    def falldown(self):
        self.startpt = (self.startpt[0], self.startpt[1], self.startpt[2]-1)
        self.endpt = (self.endpt[0], self.endpt[1], self.endpt[2]-1)

        updated_pts = []
        for p in self.occupiedpts:
            temp = (p[0],p[1], p[2]-1)
            updated_pts.append(temp)
        self.occupiedpts = updated_pts    
        self.lowest_z = min(self.startpt[2], self.endpt[2]) 
        return

def find_supports(pts_below, brickset):
    supports = set()
    for p in pts_below:
        for b in brickset:
            # Can further optimize by only looking at bricks that are below, not all bricks
            if p in b.occupiedpts:
                supports.add(b)
    
    if len(supports) == 0:
        print("DEBUG ERROR, SHOULDN:T HAVE NO SUPPORTS")
        if p in all_occupied_pts:
            print("MISMATCH")
    return supports

f = open("Day22TestInput.txt")
#f = open("Day22Input.txt")
#f = open("Day22Test2.txt")

raw_bricks = []

id_counter = 0
for l in f:
    raw = l.strip()
    pts_raw = raw.split('~')
    start = pts_raw[0].split(',')
    end = pts_raw[1].split(',')
    start_int = []
    for s in start:
        start_int.append((int(s)))
    end_int = []
    for e in end:
        end_int.append((int(e)))
    b = Brick(id_counter, start_int, end_int)
    raw_bricks.append(b)
    id_counter += 1

#Populate set of all occupied points
all_occupied_pts = set()
for b in raw_bricks:
    for op in b.occupiedpts:
        all_occupied_pts.add(op)


highest_low_z = 0
for b in raw_bricks:
    local_high_z = min(b.startpt[2], b.endpt[2])
    if local_high_z > highest_low_z:
        highest_low_z = local_high_z

# Reminder - 0 = ground, 1 is first layer
#COLLAPSING
"""
Approach to collapsing:
- Iterate through each z plane
    - Start with plane 2, as 0 is ground, and 1 you can't shift down (it's on ground)
- Find bricks whose lowest z is on that z plane
- for each brick, until brick below is true, find points on z, plane, see if there is block on the pts below, if not, adjust points 
"""
for plane in range(2,highest_low_z+1):
    bricks_in_plane = list(filter(lambda x: x.lowest_z == plane, raw_bricks))
    for b in bricks_in_plane:
        print("Falling brick - " + str(b.id))
        fall_plane = plane
        at_low = False
        while at_low == False and fall_plane >1:
            points_on_plane = []
            #find points on z_plane
            if b.orientation != 'Z':
                points_on_plane = list(filter(lambda x: x[2]==fall_plane, b.occupiedpts))
            elif b.orientation == 'Z':
                if b.lowest_z == fall_plane:
                    points_on_plane.append((b.occupiedpts[0][0], b.occupiedpts[0][1], b.lowest_z))
            
            
            #s  ee if all below pts on that plane are occupied
            if len(points_on_plane) != 0:
                all_pts_below_unoccupied = True
                for pp in points_on_plane:
                    pt_below = (pp[0], pp[1], pp[2]-1)
                    if pt_below[2] == 0 or pt_below in all_occupied_pts:
                        all_pts_below_unoccupied = False
                        at_low = True
                        break
                
                if all_pts_below_unoccupied == True:
                    #Need to update global set of all occipied pts
                    for p in b.occupiedpts:
                        all_occupied_pts.remove(p)

                    #Shift down all pts on plane - need to update actual object and the all occupied pts set
                    b.falldown() #This updates object pts itself
                    for p in b.occupiedpts:
                        if p in all_occupied_pts:
                            print("ERror this should not be the case")
                        all_occupied_pts.add(p)
            fall_plane = fall_plane - 1

for b in raw_bricks:
    if b.lowest_z == 0:
        print("SHOULDNT: HAVE ANY")

"""
Temp work to build the visualization grids on the page to compare

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0


 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0

xz_grid = []
for r in range(8):
    row = ['.','.','.']
    xz_grid.append(row)
for b in raw_bricks:
    for p in b.occupiedpts:
        xz_grid[8-p[2]][p[0]] = b.id

yz_grid = []
for r in range(8):
    row = ['.','.','.']
    yz_grid.append(row)
for b in raw_bricks:
    for p in b.occupiedpts:
        yz_grid[8-p[2]][p[1]] = b.id
"""

#NOW JENGA-ING
"""
Approach to Jenga-ing
- Find all bricks each brick is touching in z direction
    - Find points below (HAve this logic from falldown)
    - Find which brick each of these bricks belongs to - this may be a gap in occupied pts set or can filter them
    - Assign touching bricks
- go trhough bricks and find bricks that are the supports of bricks only supported by one brick, remove everything else
"""
for b in raw_bricks:
    pts_below = []
    if b.orientation != 'Z':
        for op in b.occupiedpts:
            pts_below.append((op[0],op[1],op[2]-1))
    elif b.orientation == 'Z':
        pts_below.append((b.occupiedpts[0][0], b.occupiedpts[0][1], b.lowest_z-1))
    
    if pts_below[0][2] != 0:
        blocks_supporting = find_supports(pts_below, raw_bricks)
        if len(blocks_supporting) == 0:
            print("ERROR, SHOULDN'T NOT BE SUPPORTED BY ANYTHING")
        for bs in blocks_supporting:
            b.supportingbricks.append(bs.id)
    print("Brick - " + str(b.id) + " - # of Supports - " + str(len(b.supportingbricks)))

bricks_cant_remove = set()
for b in raw_bricks:  
    if len(b.supportingbricks) == 0:
        if b.lowest_z !=1:
            print("ERRORRRRRRRR")
    if len(b.supportingbricks) == 1:
        bricks_cant_remove.add(b.supportingbricks[0])

num_bricks_to_remove = len(raw_bricks) - len(bricks_cant_remove)

print("Bricks can remove - " + str(num_bricks_to_remove))

def find_number_supported_bricks(target_brick):
    supported_bricks = 0

    #for bricks I'm supporting, call function 
    if len(target_brick.bricks_supported) != 0:
        for sb in target_brick.bricks_supported:
            #find full brick
            next_brick = list(filter(lambda x: x.id == sb, raw_bricks))[0]
            if len(next_brick.supportingbricks) == 1: #Only go down the path if there is only one brick holding it up, but this isn't working
                local_chain_result = find_number_supported_bricks(next_brick)
                supported_bricks = supported_bricks + local_chain_result 

    #base case - no bricks supported
    elif len(target_brick.bricks_supported) == 0:
        supported_bricks = 1
    
    print("Incoming brick - " + str(target_brick.id) + " - Number of bricks in chain - " + str(supported_bricks))
    return supported_bricks

#Working on Part 2
"""
Overall approach to PArt 2
- Take a pass and flip to find bricks each brick supports (add a member to the class) - SHOULD BE DONE
- Build recursive function that is finding number of bricks supported in chain  
    - LOGIC IS BROKEN HERE, NEEDTO RETHINK
        - Maybe try seeing how many bricks would fall down if we removed these as occupied pts
- ADd result to running sum and call function
"""

""""
This approach didn't work to Part 2 because bricks won't be counted as falling if they ahve more than one support even though they would.

total_chain_reaction = 0
print("Part 2 - Reversing List to Find Bricks Each Brick Supports")
for b in raw_bricks:
    for rb in raw_bricks:
        if b.id in rb.supportingbricks:
            b.bricks_supported.add(rb.id)
    print("Brick - " + str(b.id) + " - # of Bricks Supported - " + str(len(b.bricks_supported)))

for b in raw_bricks:
    local_chain_reaction = find_number_supported_bricks(b)
    total_chain_reaction = total_chain_reaction + local_chain_reaction
"""
def collapse_and_count(plane_to_start, local_raw_bricks, local_all_occupied_pts):
    bricks_moved_downward = 0
    bricks_moved_down = set()
    for plane in range(plane_to_start,highest_low_z+1):
        bricks_in_plane = list(filter(lambda x: x.lowest_z == plane, local_raw_bricks))

        for b in bricks_in_plane:
            fall_plane = plane
            at_low = False
            while at_low == False and fall_plane >1:
                points_on_plane = []
                #find points on z_plane
                if b.orientation != 'Z':
                    points_on_plane = list(filter(lambda x: x[2]==fall_plane, b.occupiedpts))
                elif b.orientation == 'Z':
                    if b.lowest_z == fall_plane:
                        points_on_plane.append((b.occupiedpts[0][0], b.occupiedpts[0][1], b.lowest_z))
                
                
                #s  ee if all below pts on that plane are occupied
                if len(points_on_plane) != 0:
                    all_pts_below_unoccupied = True
                    for pp in points_on_plane:
                        pt_below = (pp[0], pp[1], pp[2]-1)
                        if pt_below[2] == 0 or pt_below in local_all_occupied_pts:
                            all_pts_below_unoccupied = False
                            at_low = True
                            break
                    
                    if all_pts_below_unoccupied == True:
                        bricks_moved_down.add(b.id)
                        #Need to update global set of all occipied pts
                        for p in b.occupiedpts:
                            local_all_occupied_pts.remove(p)

                        #Shift down all pts on plane - need to update actual object and the all occupied pts set
                        b.falldown() #This updates object pts itself
                        for p in b.occupiedpts:
                            if p in local_all_occupied_pts:
                                print("ERror this should not be the case")
                            local_all_occupied_pts.add(p)
                fall_plane = fall_plane - 1

    return len(bricks_moved_down)

"""
Updated approach - 
- for each brick, make deep copy of occupied pts, make deep copy of raw bricks
    - remove this brick's pts from occupied pts
    - encapsulate all of the collapsing part of part 1 into a function that returns how many bricks went downard (conts not num spaces) 
    - add that number to the sum
"""
total_chain_reaction = 0
for b in raw_bricks:
    raw_bricks_copy = copy.deepcopy(raw_bricks)
    all_occupied_pts_copy = copy.deepcopy(all_occupied_pts)
    to_remove = list(filter(lambda x: x.id==b.id, raw_bricks_copy))[0]
    raw_bricks_copy.remove(to_remove)
    for op in b.occupiedpts:
        all_occupied_pts_copy.remove(op)
    print("TEsting collapse for brick - " + str(b.id))
    #BUG AT 5 in SAMPLE MAY NEED TO PASS IN PLANE + 1, doesn't work for first brick though, need to look at how function is setup
    local_reaction = collapse_and_count(b.lowest_z+1, raw_bricks_copy, all_occupied_pts_copy)
    print("Collapse count - " + str(local_reaction))
    total_chain_reaction = total_chain_reaction + local_reaction


print("Total chain reaction sum - " + str(total_chain_reaction))