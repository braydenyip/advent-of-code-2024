import math
import time
import numpy as np

offset = 10000000000000

def import_input(filename):
    with open(filename, 'r') as f:
        button_a, button_b, prizes = [], [], []
        for line in f:
            line = line.strip().split(":")
            if len(line) > 1:
                if line[0] == "Button A":
                    coords_list = line[1].strip().split("+")
                    button_a.append((int(coords_list[1].split(',')[0]), int(coords_list[2])))
                elif line[0] == "Button B":
                    coords_list = line[1].strip().split("+")
                    button_b.append((int(coords_list[1].split(',')[0]), int(coords_list[2])))
                elif line[0] == "Prize":
                    coords_list = [l.split("=") for l in line[1].strip().split(',')]
                    prizes.append((int(coords_list[0][1]), int(coords_list[1][1])))
    return (button_a, button_b, prizes)

def is_eligible(prize_loc, da, db):
    da_x, da_y, db_x, db_y = da[0], da[1], db[0], db[1]
    gcd_x = math.gcd(da_x, db_x)
    gcd_y = math.gcd(da_y, db_y)
    return (prize_loc[0] % gcd_x == 0) and (prize_loc[1] % gcd_y == 0)

def get_total_tokens(machines, presses=100):
    total_tokens, skipped = 0, 0
    for machine in machines:
        min_tokens = math.inf
        da, db, prize_loc = machine[0], machine[1], machine[2]
        da_x, da_y, db_x, db_y = da[0], da[1], db[0], db[1]
        # Determine if the location can even be reached...
        if is_eligible(prize_loc, da, db):
            max_a = max(prize_loc[0]//da_x+1, prize_loc[1]//da_y+1)
            max_b = max(prize_loc[0]//db_x+1, prize_loc[1]//db_y+1)
            bound_a, bound_b = min(presses+1, max_a), min(presses+1, max_b)

            for a in range(bound_a):
                for b in range(bound_b):
                    x = da_x*a + db_x*b
                    y = da_y*a + db_y*b
                    if x == prize_loc[0] and y == prize_loc[1]:
                        min_tokens = min(min_tokens, 3*a+b)
            if (min_tokens != math.inf):
                total_tokens += min_tokens
    return total_tokens

# Copping out of writing the algorithm -- use SciPy to quickly do linear programming
def token_optimizer(machines):
    total_tokens = 0
    for machine in machines:
        da, db, prize_loc = machine[0], machine[1], machine[2]
        prize_loc = (prize_loc[0] + offset, prize_loc[1] + offset)
        prize_loc = machine[2]
        da_x, da_y, db_x, db_y = da[0], da[1], db[0], db[1]
        a = np.array([[da_x, da_y], [db_x, db_y]])
        b = np.array([prize_loc[0], prize_loc[1]])
        res = np.linalg.solve(a, b)
        if res[0].is_integer() and res[1].is_integer():
            total_tokens += int(3*res[0] + res[1])
    return total_tokens

if __name__ == "__main__":
    button_a, button_b, prizes = import_input("day13.txt")
    machines = list(zip(button_a, button_b, prizes))
    begin = time.time()
    total_tokens = get_total_tokens(machines, presses=100)
    end = time.time()
    print(f"Total tokens needed: {total_tokens}")
    print(f"Time: {end-begin:.3f}s")
    print(f"--------PART B-------")
    print(f"Total tokens needed: {token_optimizer(machines)}")

