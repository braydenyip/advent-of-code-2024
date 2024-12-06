
def import_input_rules(filename):
    rules = {}
    with open(filename, 'r') as f:
        for line in f:
            if (line == '\n'):
                break
            else:
                rule = line.rstrip().split('|')
                n1, n2 = int(rule[0]), int(rule[1])
                if n1 in rules:
                    rules[n1].append(n2)
                else:
                    rules[n1] = [n2]
    return rules
def import_input_updates(filename):
    flag = 0
    updates = []
    with open(filename, 'r') as f:
        for line in f:
            if (line == '\n'):
                flag = 1
            elif flag:
                update = line.rstrip().split(",")
                updates.append([int(n) for n in update])
    return updates

def is_compliant(rules, update):
    for i, n in enumerate(update):
        if n in rules:
            rule = rules[n]
            for j in range(0, i):
                if update[j] in rule:
                    return False
    return True


def fix_update(rules, update) -> list[int]:
    fixed_update = update[:]
    for i, n in enumerate(fixed_update[::-1]):
        if n in rules:
            rule = rules[n]
            for x in rule:
                # check if number in rule list is to left of current position
                if x in fixed_update[:i]:
                    j = fixed_update.index(x)
                    fixed_update[i], fixed_update[j] = fixed_update[j], fixed_update[i]
    return fixed_update

if __name__ == "__main__":
    rules = import_input_rules("day5.txt")
    updates = import_input_updates("day5.txt")
    total = 0
    fixed_total = 0
    for update in updates:
        if is_compliant(rules, update):
            total += update[len(update) // 2]
        else:
            fixed_update = fix_update(rules, update)
            fixed_total += fixed_update[len(update) // 2]
    print(f"Total middle page #s: {total}")
    print(f"Part 2; fixed total middle page #s: {fixed_total}")


    