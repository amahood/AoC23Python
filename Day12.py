import re
#f = open("Day12TestInput.txt")
f = open("Day12Input.txt")

spring_set = []

for l in f:
    spring_row = []
    spring_row = l.split(' ')
    spring_row[1] = spring_row[1].strip('\n')
    spring_set.append(spring_row)

running_sum = 0
for r in spring_set:
    num_qs = r[0].count('?')
    binary_qs = []
    total_combos = 2**num_qs
    for i in range(total_combos):
        binary_str = str(bin(i))
        #binary_str = binary_str.strip('0b')
        binary_str = binary_str[2:]
        binary_qs.append(binary_str)
    max_length = len(binary_qs[len(binary_qs)-1])
    for i in range(len(binary_qs)):
        while len(binary_qs[i]) < max_length:
            binary_qs[i] = '0' + binary_qs[i]
    #Now have possible combos to test
    #for each possible combo, replace the ?s with the binary and see if it matches the pattern
    for b in binary_qs:
        #replace the ?s with the binary
        temp_pattern = r[0]
        for i in range(len(b)):
        #replace 0s with '.' and 1s with '#'
            temp_pattern = temp_pattern.replace('?', b[i], 1)
        temp_pattern = temp_pattern.replace('0', '.')
        temp_pattern = temp_pattern.replace('1', '#')
        #now check if it matches the pattern
        
        p = re.compile('#+')
        combo_matches = p.findall(temp_pattern)
        #Now need to check against sets
        length_of_tested_sets = []
        for m in combo_matches:
            length_of_tested_sets.append(len(m))
        #sort length_of_tested_sets in ascending order
        #length_of_tested_sets.sort()
        sets_to_match = r[1].split(',')
        i = 0
        while i < len(sets_to_match):
            sets_to_match[i] = int(sets_to_match[i])
            i = i + 1
        #sets_to_match.sort()

        if len(sets_to_match) == len(length_of_tested_sets):
            #Do comparison
                if sets_to_match == length_of_tested_sets:
                    running_sum += 1
    
print("running_sum = " + str(running_sum))