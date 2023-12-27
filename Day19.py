import copy
class workflow_rule:
    def __init__(self, workflow_label, letter, condition, value, next_workflow):
        self.workflow_label = workflow_label
        self.letter = letter
        self.condition = condition
        self.value = value
        self.next_workflow = next_workflow

class workflow:
    def __init__(self, label, rules):
        self.label = label
        self.rules = rules

def parse_workflow_rule(containing_workflow, raw_rule):
    """
    In comes in the label of containing node and a list of rules in a list of strings.  Each string is a rule that needs to be parsed out
    """
    if raw_rule.__contains__(">") == False and raw_rule.__contains__("<")==False:
        #this is a default next workflow
        letter = "def"
        condition = "def"
        value = "def"
        next_workflow = raw_rule
    else:
        letter = raw_rule[0]
        condition = raw_rule[1]
        value = raw_rule.split(":")[0][2:]
        next_workflow = raw_rule.split(":")[1]
    return workflow_rule(containing_workflow, letter, condition, value, next_workflow)

def parse_workflow(raw_workflow):
    w_label = raw_workflow.split('{')[0]
    w_rules_raw = raw_workflow.split('{')[1].split('}')[0].split(',')
    w_rules_instances = []
    for rr in w_rules_raw:
        w_rules_instances.append(parse_workflow_rule(w_label, rr))
    return workflow(w_label, w_rules_instances)

def execute_workflow(part, workflow):
    result = ""
    for r in workflow.rules:
        if r.letter == "def":
            result = r.next_workflow
            break
        elif r.letter == "x":
            if r.condition == ">":
                if int(part[0]) > int(r.value):
                    result = r.next_workflow
                    break
            elif r.condition == "<":
                if int(part[0]) < int(r.value):
                    result = r.next_workflow
                    break
        elif r.letter == "m":
            if r.condition == ">":
                if int(part[1]) > int(r.value):
                    result = r.next_workflow
                    break
            elif r.condition == "<":
                if int(part[1]) < int(r.value):
                    result = r.next_workflow
                    break
        elif r.letter == "a":
            if r.condition == ">":
                if int(part[2]) >int(r.value):
                    result = r.next_workflow
                    break
            elif r.condition == "<":
                if int(part[2]) < int(r.value):
                    result = r.next_workflow
                    break
        elif r.letter == "s":
            if r.condition == ">":
                if int(part[3]) > int(r.value):
                    result = r.next_workflow
                    break
            elif r.condition == "<":
                if int(part[3]) <int(r.value):
                    result = r.next_workflow
                    break
    
    """
    REturn either R, A, or next label
    """
    return result

def find_workflow(label, workflow_set):
    found = False
    for w in workflow_set:
        if w.label == label:
            found = True
            return w
    
    if found == False:
        print("ERROR")
        

f = open("Day19TestInput.txt")
#f = open("Day19Input.txt")

#read in workflow lines
raw_workflows = []
l = f.readline()
while l != "\n":
    raw_workflows.append(l)
    l = f.readline()

#parse out workflows
workflows = []
for w in raw_workflows:
    workflows.append(parse_workflow(w))

#read in parts lines
parts_raw = []
l = f.readline()
while l != "":
    parts_raw.append(l)
    l = f.readline()

#parse out parts
parts = []
for p in parts_raw:
    p = p.strip("{}\n")
    p_parts = p.split(",")
    p_parts[0] = p_parts[0][2:]
    p_parts[1] = p_parts[1][2:]
    p_parts[2] = p_parts[2][2:]
    p_parts[3] = p_parts[3][2:]
    parts.append(p_parts)

for w in workflows:
    if w.label == "in":
        inpoint = w
        break

running_sum = 0
result = "" 
for p in parts:
    result = ""
    next_workflow = inpoint
    while result != 'A' and result != 'R':
        result = execute_workflow(p, next_workflow)
        if result != 'A' and result != 'R':
            for w in workflows:
                if w.label == result:
                    next_workflow = w
                    break
    if result == 'A':
        running_sum = running_sum + int(p[0]) + int(p[1]) + int(p[2]) + int(p[3])

print(str(running_sum))

def find_paths_to_a(input_workflow, rules_so_far, workflow_set):
    paths_to_a = []
    local_rsf = copy.deepcopy(rules_so_far)

    #parse workflow rules
    #BUG - But not sure it matters, if a workflow only has rules that end in A, you will get paths for each rule of that node (the lnx bug)
    print("at " + input_workflow.label)
    for r in input_workflow.rules:
        if r.next_workflow == 'A':
            #new_path = copy.deepcopy(local_rsf)
            #new_path.append(r)
            local_rsf.append(r)
            paths_to_a.append(local_rsf)
        elif r.next_workflow != 'R':   
            #temp_path = copy.deepcopy(local_rsf)
            #temp_path.append(r)
            local_rsf.append(r)
            nw = find_workflow(r.next_workflow, workflow_set)
            next_layer_paths_to_a = find_paths_to_a(nw, local_rsf, workflow_set)
            for path in next_layer_paths_to_a:
                paths_to_a.append(path)
        
    return paths_to_a

empty_list = []
paths_from_inpoint = find_paths_to_a(inpoint, empty_list, workflows)

# I NOW HAVE ALL THE CONDITIONS BUT NOT WHETHER THEY PASSED OR FAILED TO GET TO THE NEXT STEP


for p in paths_from_inpoint:
    path = ""
    labels = ""
    for w in p:
            labels = labels + " " + w.workflow_label
            if w.letter != "def":
                rule_text = w.letter + w.condition + w.value
                path = path + " " + rule_text
            
    print(labels)
    print(path)


print("Hold")


