from collections import defaultdict
from collections import deque
from math import prod

from utils.utils import split_lines
# Part 2: Watch module rx
# Each module has input queue; processed on activation
#TODO: each processed pulse sends pulse to output's input queue

class Module():

    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

class Broadcaster(Module):

    def receive(self, _, pulse):
        return pulse

class FlipFlop(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on = False

    def receive(self, _,  pulse):
        if pulse:
            return
        self.on = not self.on
        return self.on

class Conjunction(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = {i : False for i in self.inputs}
        self.n_inputs = len(self.inputs)

    def receive(self, name, pulse):
        self.inputs[name] = pulse
        return sum(self.inputs.values()) != self.n_inputs

    def __repr__(self):
        return str(self.inputs)

def parse(lines):
    inputs = defaultdict(list)
    data = []
    end = None
    for line in lines:
        name, outputs = line.split(" -> ")
        kind = FlipFlop if name[0] == "%" else Conjunction if name[0] == "&" else Broadcaster
        name = name.lstrip("&%")
        outputs = outputs.split(", ")
        if outputs == ["rx"]:
            end = name
        for o in outputs:
            inputs[o].append(name)
        data.append((name, kind , outputs))
    return {t[0] : t[1](t[0], inputs[t[0]], t[2]) for t in data}, end

def pulse(data, iterations):
    low = iterations
    high = 0

    for _ in range(iterations):
        # Only one set of pulses in queue at once
        #Separate received pulse queue for each input?
        queue = deque([ ("broadcaster", "", False) ])
        while queue:
            new = deque()
            while queue:
                target, source, pulse = queue.popleft()
                outputs = data[target].outputs
                kind = data[target].receive(source, pulse)
                if kind is not None:
                    sent = len(outputs)
                    if kind:
                        high += sent
                    else:
                        low += sent

                    for o in outputs:
                        if o not in data:
                            continue
                        if o not in new:
                            new.append((o, target,  kind))
            queue = new
    return low, high

def find_targets(data, end):
    result = []
    for t in  data[end].inputs.keys():
        result.append(next(iter(data[t].inputs.keys())))
    return result

def read_number(start, ends, data):
    num = ""
    current = start
    while current is not None :
        digit = "0"
        next = None
        for o in data[current].outputs:
            if o in ends:
                digit = "1"
            else:
                next = o
        num += digit
        #assert next is not None
        current = next

    return int(num[-1::-1], 2)

raw_input = split_lines("inputs/day20.txt")
data, end = parse(raw_input)
low, high = pulse(data, 1000)
print(low * high)

targets = set(find_targets(data, end))
nums = [ read_number(num, targets, data) for num in data["broadcaster"].outputs]
part2 = prod(nums)
print(part2)

# TODO:
    #prod = 1
    # For each broadcast output:
        # For each module in circle:
            # If outputs of final output of circle:
                # Add 1
            # Else
                # Add 0
            # Reverse, read binary, multiply by prod
