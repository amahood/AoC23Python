from threading import currentThread
import copy
import numpy as np
import math

def take_step(node, instruction, node_list):
    if next_instruction == "R":
        next_node = node[2]
    elif next_instruction == "L":
        next_node = node[1]
    
    for n in node_list:
        if n[0] == next_node:
            current_node = n
            break
    return current_node

#f = open("Day8TestIpu1.txt")
#f = open("Day8TestInpu2.txt")
#f = open("Day8TestInput3.txt")
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

a_nodes = []
for n in node_list:
    if n[0][2] == "A":
        a_nodes.append(n)

tracking_nodes = copy.deepcopy(a_nodes)
z_rollover_count = set()
foundzs = 0
instruction_tracker = 0
step_counter = 0

while foundzs < len(a_nodes):
    #advance instruction
    if instruction_tracker >= len(instructions):
        instruction_tracker = 0
        next_instruction = instructions[instruction_tracker]
    else:
        next_instruction = instructions[instruction_tracker]
    instruction_tracker = instruction_tracker + 1
    step_counter = step_counter + 1

    #take step for all
    temp_tracking_nodes = []
    for node in tracking_nodes:
        next_node = take_step(node, next_instruction, node_list)
        if next_node[0][2] == "Z":
            foundzs = foundzs + 1
            z_rollover_count.add(step_counter)
            print("Found Z at step " + str(step_counter))
        else:
            temp_tracking_nodes.append(next_node)

    tracking_nodes = copy.deepcopy(temp_tracking_nodes)

#lcm = np.lcm.reduce(list(z_rollover_count))
running_lcm = 1
for i in z_rollover_count:
    running_lcm = math.lcm(running_lcm, i)
print("LCM: " + str(running_lcm))
