from threading import currentThread


#f = open("Day8TestIpu1.txt")
#f = open("Day8TestInpu2.txt")
f = open("Day8Input.txt")

instruction_Set = f.readline()
instructions = []
for c in instruction_Set:
    instructions.append(c)
instructions.pop()

f.readline()

node_list = []
for l in f:
    split = l.split("=")
    paths = split[1]
    paths_split = paths.split(",")
    paths_split_left = paths_split[0].split("(")[1].replace(" ","")
    paths_split_right = paths_split[1].split(")")[0].replace(" ","")
    stripped0 = split[0].replace(" ","")
    node_list.append((stripped0, paths_split_left, paths_split_right))

current_node = node_list[0]
node_text = current_node[0]
instruction_tracker = 0
step_count = 0
while node_text != "ZZZ":

    if instruction_tracker >= len(instructions):
        instruction_tracker = 0
        next_instruction = instructions[instruction_tracker]
        #print("Rollover")
    else:
        next_instruction = instructions[instruction_tracker]
    instruction_tracker = instruction_tracker + 1

    if next_instruction == "R":
        next_node = current_node[2]
    elif next_instruction == "L":
        next_node = current_node[1]
    
    for n in node_list:
        if n[0] == next_node:
            current_node = n
    node_text = current_node[0]
    step_count = step_count + 1
    #print("Next node = " + node_text)
print("NumSteps - " + str(step_count))