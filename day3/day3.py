import re
def import_input(filename):
    with open(filename, 'r') as f:
        return f.read()

if __name__ == "__main__":
    raw_input = import_input("day3.txt")
    
    pruned_input = re.findall('mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)', raw_input)
    print(pruned_input)
    sum = 0
    is_on = True
    for cmd in pruned_input:
        if cmd == 'do()':
            is_on = True
        elif cmd == 'don\'t()':
            is_on = False
        elif is_on:
            pair = re.findall('\d{1,3},\d{1,3}', cmd)[0].split(',')
            sum += int(pair[0]) * int(pair[1])
    print(f"Sum: {sum}")