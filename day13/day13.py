import math
import time

def import_input(filename):
    with open(filename, 'r') as f:
        button_a, button_b, prizes = [], [], []
        output = []
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

def get_total_tokens(machines, presses=100, big_prize=True):
    total_tokens, skipped = 0, 0
    for machine in machines:
        min_tokens = math.inf
        da, db, prize_loc = machine[0], machine[1], machine[2]
        da_x, da_y, db_x, db_y = da[0], da[1], db[0], db[1]
        if big_prize:
            prize_loc = (prize_loc[0] + 10000000000000, prize_loc[1] + 10000000000000)
        # Determine if the location can even be reached...
        if (prize_loc[0] % math.gcd(da_x, db_x) != 0 or prize_loc[1] % math.gcd(da_y, db_y) != 0):
            #print("Skipping: prize loc cannot be reached...")
            skipped += 1
            continue
        else:
            for a in range(min(presses+1, max(prize_loc[0]//da_x+1, prize_loc[1]//da_y+1))):
                for b in range(min(presses+1, max(prize_loc[0]//db_x+1, prize_loc[1]//db_y+1))):
                    x = da_x*a + db_x*b
                    y = da_y*a + db_y*b
                    if x == prize_loc[0] and y == prize_loc[1]:
                        min_tokens = min(min_tokens, 3*a+b)
            if (min_tokens != math.inf):
                total_tokens += min_tokens
    print(f"Skipped: {skipped}/{len(machines)}")
    return total_tokens

if __name__ == "__main__":
    button_a, button_b, prizes = import_input("day13.txt")
    machines = list(zip(button_a, button_b, prizes))
    begin = time.time()
    total_tokens = get_total_tokens(machines, big_prize=False)
    end = time.time()
    print(f"Total tokens needed: {total_tokens}")
    print(f"Time: {end-begin:.3f}s")
    print(f"---------------")