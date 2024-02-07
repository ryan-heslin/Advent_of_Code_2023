import operator
import re
from ast import literal_eval
from math import prod

FIELDS = ("x", "m", "a", "s")


class Interval:
    """Closed endpoints, so [low, high] is true interval"""

    def __init__(self, low, high) -> None:
        self.valid = high - low > 0
        self.low = low
        self.high = high

    def narrow(self, value, sign):
        """Shrink interval"""
        if sign == "<":
            return __class__(self.low, min(value - 1, self.high))
        return __class__(max(value + 1, self.low), self.high)

    def __repr__(self) -> str:
        return (self.low, self.high).__repr__()


def dfs(workflows):
    start = {f: Interval(1, 4000) for f in FIELDS}
    valid = []

    def inner(state, workflow):
        state = dict(state)
        workflow = workflows[workflow]

        # breakpoint()
        for rule in workflow:
            if type(rule) == dict:
                field = rule["field"]
                # Remember < x means x-1 is max value
                new = state[field].narrow(rule["value"], rule["operator"])
                if new.valid:
                    new_state = state | ({field: new})
                    target = rule["target"]
                    # If invalid, reject here
                    if target == "A":
                        valid.append(new_state)
                    elif target != "R":
                        inner(new_state, target)

                # Exclude any state caught by rule
                # breakpoint()
                if rule["operator"] == ">":
                    state[field] = Interval(state[field].low, rule["value"])
                else:
                    # < case
                    state[field] = Interval(rule["value"], state[field].high)

                if not state[field].valid:
                    return
            # Catchall rule, so break
            elif rule == "A":
                valid.append(state)
                return
            elif rule == "R":
                return
            else:
                inner(state, rule)

    inner(start, "in")
    return sum(prod(r.high - r.low + 1 for r in v.values()) for v in valid)


def make_rule(key, value, op, target):
    def result(record):
        if op(record[key], value):
            return target

    return result


def parse_rule(rule, part1=True):
    cutpoint = rule.index("{")
    name = rule[:cutpoint]
    rules = rule[cutpoint + 1 : -1 :].split(",")
    parts = []
    operators = (operator.lt, operator.gt)

    for part in rules:
        if part1:
            if ":" in part:
                directive, target = part.split(":")
                op = operators[directive[1] == ">"]
                parts.append(make_rule(directive[0], int(directive[2:]), op, target))
            # Catchall
            else:
                parts.append(lambda _: part)
        else:
            if ":" in part:
                lhs, target = part.split(":")
                part = {
                    "field": lhs[0],
                    "operator": lhs[1],
                    "value": int(lhs[2:]),
                    "target": target,
                }
            parts.append(part)

    return name, parts


def to_dict(string):
    return re.sub(r"([a-z]+)", r'"\1"', string).replace("=", ":")


def eval_rules(workflows, data):
    part1 = 0
    for record in data:
        current_workflow = "in"
        while current_workflow != "A" and current_workflow != "R":
            for rule in workflows[current_workflow]:
                result = rule(record)
                if result is not None:
                    current_workflow = result
                    break
        if current_workflow == "A":
            part1 += sum(record.values())

    return part1


with open("inputs/day19.txt") as f:
    rules, data = f.read().split("\n\n")

rules = rules.splitlines()
workflows = dict(map(parse_rule, rules))
data = list(map(literal_eval, to_dict(data).splitlines()))
part1 = eval_rules(workflows, data)
print(part1)

workflows = dict(parse_rule(rule, False) for rule in rules)
part2 = dfs(workflows)
print(part2)
