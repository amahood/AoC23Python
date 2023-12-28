class module:
    def __init__(self, name, type, outputs):
        self.name = name
        self.type = type
        self.output_connections = outputs
        self.flipflop_currentstate = ""
        self.conj_lastseen = []

class pulse:
    def __init__(self, level, destination, origin):
        self.level = level
        self.origin = origin
        self.destination = destination

def process_pulse(inpulse, modules):
    output_pulses = []

    #find module for the pulse
    target_module = list(filter(lambda x: x.name == inpulse.destination, modules))[0]
    #handle flip flops
    if target_module.type == '%':
        """
        Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, 
        it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. 
        If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
        """
        if target_module.flipflop_currentstate == 'OffLow' and inpulse.level == 'L':
            target_module.flipflop_currentstate = "OnHigh"
            for t in target_module.output_connections:
                p = pulse('H', t, target_module.name)
                output_pulses.append(p)
        elif target_module.flipflop_currentstate == 'OnHigh' and inpulse.level == 'L':
            target_module.flipflop_currentstate = "OffLow"
            for t in target_module.output_connections:
                p = pulse('L', t, target_module.name)
                output_pulses.append(p)
    #handle conjunctions
    elif target_module.type == '&':
        """
        Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; 
        they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input.
        Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
        """
        #loop through input states and find/update or add
        input_found = False
        for i in target_module.conj_lastseen:
            if i[0] == inpulse.origin:
                input_found = True
                i[1] = inpulse.level
        if input_found == False:
            target_module.conj_lastseen.append([inpulse.origin,inpulse.level])
        
        #now check all inputs
        all_inputs_high = True
        for i in target_module.conj_lastseen:
            if i[1] == 'L':
                all_inputs_high = False

        #now send all pulses
        if all_inputs_high == True:
            for t in target_module.output_connections:
                p = pulse('L', t, target_module.name)
                output_pulses.append(p)
        else:
            for t in target_module.output_connections:
                p = pulse('H', t, target_module.name)
                output_pulses.append(p)

    return output_pulses

f = open("Day20Test1.txt")
#f = open("Day20Test2.text")
#f = open("Day20.txt")

module_rows_raw = set()
for l in f:
    module_rows_raw.add(l.strip())

broadcast_module = set(filter(lambda x: x.__contains__("broad"),module_rows_raw))
module_rows_raw.difference_update(broadcast_module)

broadcast_connections = broadcast_module.pop().split("->")[1].split(',')
bctemp = []
for bc in broadcast_connections:
    bctemp.append(bc.strip())
bctemp.sort()
broadcast_mod = module("broadcast", "broadcast", bctemp)

modules = set()
for m in module_rows_raw:
    #Parse and sanitize input
    raw_parts = m.split("->")
    module_type = raw_parts[0][0]
    module_name = raw_parts[0][1:].strip()
    raw_connections = raw_parts[1].split(',')
    module_connections = []
    for c in raw_connections:
        c = c.strip()
        module_connections.append(c)
    #Create modules from each of the rows
    new_module = module(module_name, module_type, module_connections)
    if module_type == '%':
        new_module.flipflop_currentstate = "OffLow"
        new_module.conj_lastseen = []
    elif module_type == "&":
        new_module.conj_lastseen = []
        new_module.flipflop_currentstate = ""
    modules.add(new_module)

cycle_count = 0
high_count = 0
low_count = 0
#Might need to traverse and find all input connections too

pulses_to_process = [] #Starting with list as might have duplicates and need ordering
for cycle_count in range(1000):
    #increment low count by one because we always count button push
    low_count += 1
    #fire pulse at broadcast
    for broadcast_output in broadcast_mod.output_connections:
        #loop through output connections and add pulses to process, increment pulses
        pulses_to_process.append(pulse('L',broadcast_output, "broadcast"))
    #process pulses
        #likely need function that takes in pulse object and set of modules/states,l returns pulses to add?
    pulse_iterations = 0
    while pulse_iterations < len(pulses_to_process):
        current_pulse = pulses_to_process[pulse_iterations]
        #increment pulse counter
        if current_pulse.level == 'L': 
            low_count +=1
        elif current_pulse.level == 'H': 
            high_count +=1
        #call pulse function with pulses to process(i) and add to pulses in return 
        pulses_to_add = process_pulse(current_pulse, modules)
        #merge lists
        pulses_to_process = pulses_to_process + pulses_to_add
        pulse_iterations += 1


print("High pulses - " + str(high_count))
print("Low pulses  - " + str(low_count))