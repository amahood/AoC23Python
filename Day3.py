#HELPERS



#f = open("Day3testInput.txt")
f = open("Day3Input.txt")


symbols = ['~','!','@','#','$','%','^','&','*','+','-','=','/','?','/','_']

in_memory_copy = []
for l in f:
    in_memory_copy.append(l)
f.seek(0,0)
row_length = len(in_memory_copy[0]) - 1

line_count = 0
running_sum = 0

for l in f:
    row_numbers = []
    part_number = ""
    working_on_number = False
    index_tracker = 0
    for c in l:
        if c.isdigit():
            if working_on_number == False:
                leftmost_index = index_tracker
                working_on_number = True
            part_number = part_number + c
        elif working_on_number == True and c.isdigit() == False:
            #Number is over here
            working_on_number = False
            rightmost_index = index_tracker - 1
            part_number_int = int(part_number)
            row_numbers.append([part_number_int, line_count, leftmost_index, rightmost_index])
            part_number = ""
        index_tracker = index_tracker + 1
    #print("End of Row" + str(line_count))
    #should have all the numbers in the row at this point
    

    #for each number, iterate neighbors, find symbol, set to count or not
    for n in row_numbers:
        valid_number = False
        positions_to_check = []
        #find bounds of round search
        if n[2] == 0:
            left_search_index = 0
        else:
            left_search_index = n[2] - 1
        
        if n[3] == (row_length - 1):
            right_search_index = n[3]
        else:
            right_search_index = n[3] + 1

        if line_count == 0:
            upper_search_index = n[1]
        else:
            upper_search_index = n[1] - 1

        if line_count == len(in_memory_copy) - 1:
            lower_search_index = line_count
        else:
            lower_search_index = line_count + 1

        #find positions to search
        r = upper_search_index
        while r < lower_search_index + 1:
            p = left_search_index
            while p < right_search_index + 1:
                positions_to_check.append([r,p])
                p = p+1
            r = r + 1
        
        #print("Should have all positions to check here")
        #iterate over positions
        is_valid = False
        for pos in positions_to_check:
            if in_memory_copy[pos[0]][pos[1]] in symbols:
                running_sum = running_sum + n[0]
                is_valid = True
        if is_valid == False:
            print("Discarding " + str(n[0]))
            
    #have looked at all the numbers in a row at this point
    line_count = line_count + 1
#done processing a row at this point

print("Total Sum = " + str(running_sum))

#STARTING PART 2 HERE 
f.seek(0,0)

line_count = 0
running_sum = 0

#Find Stars
for l in f:
    index_tracker = 0
    for c in l:
        if c == '*':
            #For each star Find nesighbor cells to check
            numbers_for_current_star = []
            current_number = ""
            adjacent_numbers = 0
            has_more_than_two = False

            positions_to_check = []
            positions_to_check.append((line_count-1,index_tracker-1))
            positions_to_check.append((line_count-1,index_tracker))
            positions_to_check.append((line_count-1,index_tracker+1))
            positions_to_check.append((line_count,index_tracker-1))
            positions_to_check.append((line_count,index_tracker+1))
            positions_to_check.append((line_count+1,index_tracker-1))
            positions_to_check.append((line_count+1,index_tracker))
            positions_to_check.append((line_count+1,index_tracker+1))
            
            ##Check cells / build numbers
            positions_checked = []

            for p in positions_to_check:
                if p not in positions_checked:
                    if in_memory_copy[p[0]][p[1]].isdigit():
                        adjacent_numbers = adjacent_numbers + 1
                        current_number = in_memory_copy[p[0]][p[1]]
                        going_left = True
                        left = p[1]-1
                        right = p[1]+1
                        while going_left == True:
                            test_c = in_memory_copy[p[0]][left]
                            positions_checked.append((p[0],left))
                            if test_c.isdigit():
                                current_number = test_c + current_number
                                left = left - 1
                            else:
                                going_left = False
                                going_right = True
                        while going_right == True:
                            test_c = in_memory_copy[p[0]][right]
                            positions_checked.append((p[0],right))
                            if test_c.isdigit():
                                current_number = current_number + test_c
                                right = right + 1
                            else:
                                going_right = False
                        numbers_for_current_star.append(int(current_number))       
            
            #Decide if there are 2 or more than two
            if adjacent_numbers == 2:
                running_sum = running_sum + numbers_for_current_star[0] * numbers_for_current_star[1]
            #Multiply numbers and add to running sum

        index_tracker = index_tracker + 1
    line_count = line_count + 1

print("Sum of gear ratio = " + str(running_sum))


