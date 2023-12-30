class map_point:
    def __init__(self, x,y, mapchar):
        self.x = x
        self.y = y
        self.mapchar = mapchar

f = open("Day23TestInput.txt")

hiking_map = []
for l in f:
    raw_line = l.strip()
    hiking_map.append(raw_line)

hiking_map_set = set()
r_counter = 0
for r in hiking_map:
    c_counter = 0
    for c in r:
        hiking_map_set.add(map_point(r_counter,c_counter,c))
        c_counter +=1
    r_counter += 1

print("STILLWIP")