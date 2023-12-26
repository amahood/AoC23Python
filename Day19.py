class workflow_rule:
    def __init__(self, letter, condition, value, next_workflow):
        self.letter = letter
        self.condition = condition
        self.value = value
        self.next_workflow = next_workflow

class workflow:
    def __init__(self, label, rules):
        self.label = label
        self.rules = rules

def parse_workflow_rule(raw_rule):
    """
    In comes a list of rules in a list of strings.  Each string is a rule that needs to be parsed out
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
    return workflow_rule(letter, condition, value, next_workflow)

def parse_workflow(raw_workflow):
    w_label = raw_workflow.split('{')[0]
    w_rules_raw = raw_workflow.split('{')[1].split('}')[0].split(',')
    w_rules_instances = []
    for rr in w_rules_raw:
        w_rules_instances.append(parse_workflow_rule(rr))
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

#f = open("Day19TestInput.txt")
f = open("Day19Input.txt")

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
