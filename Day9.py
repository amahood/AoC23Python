def find_next_value(list):
    delta_v = []
    i = len(list)-1
    while i > 0:
        delta_v.insert(0,list[i]-list[i-1])
        i = i - 1
    
    if delta_v.count(0) < len(delta_v)-1:
        next = find_next_value(delta_v)
        next = delta_v[0] - next
        return next
    else:
        return 0

#f = open("Day9TestInput.txt")
f = open("Day9Input.txt")

input_rows = []

for l in f:
	new_row = l.split(" ")
	new_row_int = []
	for i in new_row:
		new_row_int.append(int(i))
	input_rows.append(new_row_int)
	

next_values = []
for r in input_rows:
	next_values.insert(0, r[0] - find_next_value(r))

running_sum = 0
for v in next_values:
	running_sum = running_sum + v
print("running sum - " + str(running_sum))
	

