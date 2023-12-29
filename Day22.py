class Brick():
    def __init__(self, id, startpt, endpt):
        self.id = id
        self.startpt = startpt
        self.endpt = endpt
        self.length = self.calc_length((startpt),(endpt))
        self.orientation = self.calc_orientation((startpt),(endpt))
        self.lowest_z = min(startpt[2], endpt[2])
        self.occupiedpts = self.calc_occupied_points()

    def calc_length(self, startpt, endpt):
        length = 0
        if startpt == endpt:
            length = 1

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
        if startpt == endpt:
            orientation = 'S'

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
            for z in range(self.startpt[2], self.endpt[2]+1):
                occupied_pts.append((self.startpt[0], self.endpt[1], z))

        if self.orientation == 'X':
            for x in range(self.startpt[0], self.endpt[0]+1):
                occupied_pts.append((x, self.startpt[1], self.startpt[2]))
        
        if self.orientation == 'Y':
            for y in range(self.startpt[1], self.endpt[1]+1):
                occupied_pts.append((self.startpt[0], y, self.startpt[2]))
        
        return occupied_pts

f = open("Day22TestInput.txt")

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

highest_z = 0
for b in raw_bricks:
    local_high_z = max(b.startpt[2], b.endpt[2])
    if local_high_z > highest_z:
        highest_z = local_high_z

#0 = ground, 1 is first layer
#Now do collapsing
"""
Approach to collapsing:
- Iterate through each z plane
- Find bricks whose lowest z is on that z plane

"""

print("Still WIP")