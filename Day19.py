import copy
class workflow_rule:
    def __init__(self, workflow_label, letter, condition, value, next_workflow):
        self.workflow_label = workflow_label
        self.letter = letter
        self.condition = condition
        self.value = value
        self.next_workflow = next_workflow
        self.pt2result = 'F'

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

    for r in input_workflow.rules:
        if r.next_workflow == 'A':
            if r.letter != "def":
                local_rsf_success = copy.deepcopy(local_rsf)
                #append failure to main tracker
                failure_rule = copy.deepcopy(r)
                failure_rule.pt2result = 'F'
                local_rsf.append(failure_rule)
                #Append pass to path and return as path
                success_rule = copy.deepcopy(r)
                success_rule.pt2result = 'T'

                local_rsf_success.append(success_rule)
                paths_to_a.append(local_rsf_success)
            if r.letter == "def":
                #append pass to path and return as path
                success_rule = copy.deepcopy(r)
                success_rule.pt2result = 'T'
                local_rsf_success = copy.deepcopy(local_rsf)
                local_rsf_success.append(success_rule)
                paths_to_a.append(local_rsf_success)
        elif (r.next_workflow == 'R' and r.letter != "def"): #Handles conditions for R that we don't meet and move past
            #Add to path but don't call find As?
            r.pt2result = 'F'
            local_rsf.append(r)
        elif r.next_workflow != 'R' and next_workflow != 'A': #handles workflows that go to different location BUG but we are always assumign they fail / tracking they fail
            local_rsf_success = copy.deepcopy(local_rsf)
            #append failure to main tracker
            failure_rule = copy.deepcopy(r)
            failure_rule.pt2result = 'F'
            local_rsf.append(failure_rule)
            #Append pass, find, and pass ot recusion
            success_rule = copy.deepcopy(r)
            success_rule.pt2result = 'T'

            local_rsf_success.append(success_rule)
            nw = find_workflow(r.next_workflow, workflow_set)
            next_layer_paths_to_a = find_paths_to_a(nw, local_rsf_success, workflow_set)
            for path in next_layer_paths_to_a:
                paths_to_a.append(path)
        
    return paths_to_a

#PART 2 CORE LOGIC STARTS HERE
empty_list = []
paths_from_inpoint = find_paths_to_a(inpoint, empty_list, workflows)


def process_path_for_ranges(path):
    letter_ranges = []
    x_range = range(1,4001)
    m_range = range(1,4001)
    a_range = range(1,4001)
    s_range = set(range(1,4001))

    #DO STUFF
    condition_tracker = 0
    for p in path:
        if p.letter == 'x':
            if p.condition == '<':
                if p.pt2result == 'F':
                    x_range =set(filter(lambda x: x>=int(p.value), x_range))
                elif p.pt2result == 'T':
                    x_range =set(filter(lambda x: x<int(p.value), x_range))
            elif p.condition == '>':
                if p.pt2result == 'F':
                    x_range =set(filter(lambda x: x<=int(p.value), x_range))
                elif p.pt2result == 'T':
                    x_range =set(filter(lambda x: x>int(p.value), x_range))
        elif p.letter == 'm':
            if p.condition == '<':
                if p.pt2result == 'F':
                    m_range =set(filter(lambda x: x>=int(p.value), m_range))
                elif p.pt2result == 'T':
                    m_range =set(filter(lambda x: x<int(p.value), m_range))
            elif p.condition == '>':
                if p.pt2result == 'F':
                    m_range =set(filter(lambda x: x<=int(p.value), m_range))
                elif p.pt2result == 'T':
                    m_range =set(filter(lambda x: x>int(p.value), m_range))
        elif p.letter == 'a':
            if p.condition == '<':
                if p.pt2result == 'F':
                    a_range =set(filter(lambda x: x>=int(p.value), a_range))
                elif p.pt2result == 'T':
                    a_range =set(filter(lambda x: x<int(p.value), a_range))
            elif p.condition == '>':
                if p.pt2result == 'F':
                    a_range =set(filter(lambda x: x<=int(p.value), a_range))
                elif p.pt2result == 'T':
                    a_range =set(filter(lambda x: x>int(p.value), a_range))
        elif p.letter == 's':
            if p.condition == '<':
                if p.pt2result == 'F':
                    s_range =set(filter(lambda x: x>=int(p.value), s_range))
                elif p.pt2result == 'T':
                    s_range =set(filter(lambda x: x<int(p.value), s_range))
            elif p.condition == '>':
                if p.pt2result == 'F':
                    s_range =set(filter(lambda x: x<=int(p.value), s_range))
                elif p.pt2result == 'T':
                    s_range =set(filter(lambda x: x>int(p.value), s_range))

        condition_tracker += 1

    letter_ranges.append(x_range)
    letter_ranges.append(m_range)
    letter_ranges.append(a_range)
    letter_ranges.append(s_range)
    return letter_ranges

running_sum = 0
for p in paths_from_inpoint:
    path = ""
    labels = ""
    for w in p:
            labels = labels + " " + w.workflow_label
            if w.letter != "def":
                rule_text = w.letter + w.condition + w.value
                path = path + " " + rule_text + " " + w.pt2result
            elif w.letter == "def" and w.next_workflow == 'A':
                path = path + " def"
            
    print(labels)
    print(path)

    #Start attempt at calculation here
    #CANT ASSUME IT"S ONLY THE LAST THAT IS OPPOSITE< NEED TO TRACK ALONG THE WAY
    # MAYBE HAVE PATHS RIGH TNOW< BUT NEED TO UPDATE THE RANG CALC FUNCTIONS TO UYSE TRUE/FALSE
    output_ranges = process_path_for_ranges(p)
    
    length = ""
    for r in output_ranges:
        length = length + " " + str(len(r))
    print(length)
    combos_for_row = len(output_ranges[0])*len(output_ranges[1])*len(output_ranges[2])*len(output_ranges[3])
    print(str(combos_for_row))
    running_sum = running_sum + combos_for_row
    print(" \n")
print("running sum " + str(running_sum))


