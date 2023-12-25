import re

def find_set_of_arrangements(spring_set, special_instruction):
    matches_for_row = []
    for r in spring_set:
        running_sum = 0
        num_qs = r[0].count('?')
        binary_qs = []
        total_combos = 2**num_qs
        for i in range(total_combos):
            binary_str = str(bin(i))
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

            sets_to_match = r[1].split(',')
            i = 0
            while i < len(sets_to_match):
                sets_to_match[i] = int(sets_to_match[i])
                i = i + 1

            if len(sets_to_match) == len(length_of_tested_sets):
                #Do comparison
                    if sets_to_match == length_of_tested_sets:
                        if special_instruction == True:
                            if temp_pattern[0] == '#' and temp_pattern[len(temp_pattern)-1] == '#':
                                continue
                            else:
                                running_sum += 1
                        else:
                            running_sum += 1
        matches_for_row.append(running_sum)
    return matches_for_row

f = open("Day12TestInput.txt")
#f = open("Day12Input.txt")

spring_set = []
spring_set_extra_q = []

for l in f:
    spring_row = []
    spring_row = l.split(' ')
    spring_row[1] = spring_row[1].strip('\n')
    #ISSUE - STICKING ON FRONT GIVES RIGHT FOR FIRST 4, STICKING ON END GIVES RIGHT FOR LAST 1 IN SAMPLE
    chars_to_repeat = spring_row[0] + '?'
    nums_to_repeat = spring_row[1]
    spring_set.append(spring_row)
    spring_set_extra_q.append([chars_to_repeat, nums_to_repeat])


row_arrangements_orig = find_set_of_arrangements(spring_set, False)
#Passing in now, but not yet handling the extra ? condiution in the function
row_arrangements_extra_q = find_set_of_arrangements(spring_set_extra_q, True)

row_totals = []
for i in range(len(row_arrangements_orig)):
    row_totals[i] = row_arrangements_orig[i]*(row_arrangements_extra_q[i]**4)

print("running_sum = " + str(sum(row_totals)))