def process_map_input(input_num, map):
    output_nunm = 0
    found_range = False
    for m in map:
        if input_num >= m[1] and input_num <= (m[1]+m[2]):
            found_range = True
            break

    if found_range == False:
        output_nunm = input_num
    elif found_range == True:
        output_nunm = m[0] + (input_num - m[1])

    return output_nunm



def process_map(dest_source_map):
    full_map = []
    for mapping_instruction in dest_source_map:
        temp_dest = mapping_instruction[0]
        temp_source = mapping_instruction[1]
        instruction_length = mapping_instruction[2]

        mapping_tracker = temp_source
        while mapping_tracker < temp_source + instruction_length:
            full_map.append((mapping_tracker, temp_dest))
            temp_dest = temp_dest + 1
            #temp_source = temp_source + 1
            mapping_tracker = mapping_tracker + 1
    
    #find the highest number in full_map
    highest_number = 0
    for m in full_map:
        if m[0] > highest_number:
            highest_number = m[0]
        if m[1] > highest_number:
            highest_number = m[1]
    #print("Highest number in full_map - " + str(highest_number))

    remaining_builder = 0
    while remaining_builder < highest_number:
        #find if an element exists in full_map with remaining_builder as the source
        found = False
        for m in full_map:
            if m[0] == remaining_builder:
                found = True
                break
        if found == False:
            full_map.append((remaining_builder, remaining_builder))
        remaining_builder = remaining_builder + 1

    return full_map



#open the file Day5TestInput.txt
#f = open("Day5TestInput.txt")
f = open("Day5Input.txt")

#copy the list of numbers after "seeds: " from the file into a new list called seeds
l = f.readline()

seeds = l.split("seeds: ")[1].split(" ")
seeds_int = []
for s in seeds:
    seeds_int.append(int(s))

seeds_int_pt2_start = []
seeds_int_pt2_length = []

#extract every other value from seeds_int and put it into seeds_int_pt2_start and seeds_int_pt2_length
i = 0
while i < len(seeds_int):
    seeds_int_pt2_start.append(seeds_int[i])
    seeds_int_pt2_length.append(seeds_int[i+1])
    i = i + 2



#SEED TO SOIL MAP
#read the lines of the file f from the line that says seed-to-soil map: until a line of blank space is reached
#copy the lines into a list called soil_map
l = f.readline()
temp_seed_to_soil_map = []   
l = f.readline()
l = f.readline()
#Now reading seed-to-soil map
while l != "\n":
    temp_seed_to_soil_map.append(l)
    l = f.readline()
#convert seed_to_soil_map into a list of lists where each list is a row of the map and each element of the list is a number in the row
seed_to_soil_map = []
for s in temp_seed_to_soil_map:
    seed_to_soil_map.append(s.split(" "))
for s in seed_to_soil_map:
    for i in range(len(s)):
        s[i] = int(s[i])  

#SOIL TO FERTILIZER MAP        
l = f.readline()
temp_soil_to_fertilizer_map = []   
l = f.readline()

while l != "\n":
    temp_soil_to_fertilizer_map.append(l)
    l = f.readline()

soil_to_fertilizer_map = []
for s in temp_soil_to_fertilizer_map:
    soil_to_fertilizer_map.append(s.split(" "))
for s in soil_to_fertilizer_map:
    for i in range(len(s)):
        s[i] = int(s[i])   

#FERTILIZER_TO_WATER MAP   - SPINS HERE
l = f.readline()
temp_fertilizer_map_to_water = []   
l = f.readline()

while l != "\n":
    temp_fertilizer_map_to_water.append(l)
    l = f.readline()

fertilizer_to_water_map = []
for s in temp_fertilizer_map_to_water:
    fertilizer_to_water_map.append(s.split(" "))
for s in fertilizer_to_water_map:
    for i in range(len(s)):
        s[i] = int(s[i])   

#WATER to light
l = f.readline()
temp_water_to_light_map = []   
l = f.readline()

while l != "\n":
    temp_water_to_light_map.append(l)
    l = f.readline()

water_to_light_map = []
for s in temp_water_to_light_map:
    water_to_light_map.append(s.split(" "))
for s in water_to_light_map:
    for i in range(len(s)):
        s[i] = int(s[i])   

#LIGHT TO TEMP
l = f.readline()
temp_light_to_temp_map = []   
l = f.readline()

while l != "\n":
    temp_light_to_temp_map.append(l)
    l = f.readline()

light_to_temp_map = []
for s in temp_light_to_temp_map:
    light_to_temp_map.append(s.split(" "))
for s in light_to_temp_map:
    for i in range(len(s)):
        s[i] = int(s[i]) 
   
#TEMP TO HUMIDITY
l = f.readline()
temp_temp_to_humidity_map = []   
l = f.readline()

while l != "\n":
    temp_temp_to_humidity_map.append(l)
    l = f.readline()

temp_to_humidity_map = []
for s in temp_temp_to_humidity_map:
    temp_to_humidity_map.append(s.split(" "))
for s in temp_to_humidity_map:
    for i in range(len(s)):
        s[i] = int(s[i]) 

#TEMP TO HUMIDITY
l = f.readline()
temp_humidity_to_location_map = []   
l = f.readline()

#read in lines of the file until the end of the file is reached
while l != "":
    temp_humidity_to_location_map.append(l)
    l = f.readline()

humidity_to_location_map = []
for s in temp_humidity_to_location_map:
    humidity_to_location_map.append(s.split(" "))
for s in humidity_to_location_map:
    for i in range(len(s)):
        s[i] = int(s[i]) 


print("TRYING JUST 2")
loop = 0
map_outputs = []
smallest_outputs = []
local_smallest_output = []
for s in seeds_int_pt2_start:
    seeds_int_pt2_full = []
    i = s
    while i < (s + seeds_int_pt2_length[loop]):
        #seeds_int_pt2_full.append(i)
        #tryo to find and compare here
        next_thing_to_map = process_map_input(i, seed_to_soil_map)
        next_thing_to_map = process_map_input(next_thing_to_map, soil_to_fertilizer_map)
        next_thing_to_map = process_map_input(next_thing_to_map, fertilizer_to_water_map)
        next_thing_to_map = process_map_input(next_thing_to_map, water_to_light_map)
        next_thing_to_map = process_map_input(next_thing_to_map, light_to_temp_map)
        next_thing_to_map = process_map_input(next_thing_to_map, temp_to_humidity_map)
        next_thing_to_map = process_map_input(next_thing_to_map, humidity_to_location_map)
        if len(local_smallest_output) == loop:
            local_smallest_output.append(next_thing_to_map)
        else:
            if next_thing_to_map < local_smallest_output[loop]:
                local_smallest_output[loop] = next_thing_to_map
        i = i + 1
    smallest_outputs.append(local_smallest_output[loop])

    print("Done processing seed entries for seed  - " + str(s)) 
    print("Smallest output for seed - " + str(s) + " - " + str(local_smallest_output[loop]))
    loop = loop + 1

#find the smallest number in smallest_outputs
output_to_comare = smallest_outputs[0]
#compare each element of smallest_outputs to output_to_compare and find the smallest one
for m in smallest_outputs:
    if m < output_to_comare:
        output_to_comare = m
    
print("smallest mapped location - " + " " + str(output_to_comare))