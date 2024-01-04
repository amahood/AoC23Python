"""
Day 24 Part 1 Scratch Notes:
Pair of equations:
Finding an x and y that satisy both pairs of equations:
a.px + a.vx*ta = b.px + b.vx*tb
a.py + a.vy*ta = b.py + b.vy*tb
(Times can be different)

Used paper to use variable substitution to solve for ta and tb
"""
class hailstone_path():
    def __init__(self, px, py, pz, vx, vy, vz):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

class intersection():
    def __init__(self, x, y):
        self.x = x
        self.y = y

f = open("Day24TestInput.txt")

UPPERBOUND = 27
LOWERBOUND = 7

#Parse input to populate path classes
hailstones = []

for l in f:
    temp = l.split('@')
    p = temp[0].split(',')
    v = temp[1].split(',')
    p_int = [int(p[0]), int(p[1]), int(p[2])]
    v_int = [int(v[0]), int(v[1]), int(v[2])]
    h_path = hailstone_path(p_int[0], p_int[1], p_int[2], v_int[0], v_int[1], v_int[2])
    hailstones.append(h_path)

intersections = []

for ha in range(0, len(hailstones)):
    for hb in range(ha+1, len(hailstones)):
        a = hailstones[ha]
        b = hailstones[hb]
        
        #TODO CHECK FOR PARALLEL LINES
        slope_a = a.vy/a.vx
        slope_b = b.vy/b.vx
        is_parallel = (slope_a == slope_b)

        if is_parallel == False:
            Ta = (b.vy*(a.px-b.px)/b.vx + b.py - a.py ) / (a.vy - (b.vy*a.vx)/b.vx)
            Tb = ((a.vx*Ta) + a.px - b.px)/b.vx

            int_x = a.px + a.vx*Ta
            int_y = a.py + a.vy*Ta
            if Ta > 0 and Tb > 0 and int_x >= LOWERBOUND and int_x <= UPPERBOUND and int_y >= LOWERBOUND and int_y <= UPPERBOUND:
                intersections.append(intersection(int_x, int_y))

print(str(len(intersections)))