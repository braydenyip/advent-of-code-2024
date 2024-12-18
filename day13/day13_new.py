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

if __name__ == "__main__":
    button_as, button_bs, prizes = import_input("day13.txt")
    machines = list(zip(button_as, button_bs, prizes))
    total_tokens = 0
    for machine in machines:
        da, db, prize = machine
        if is_eligible(prize, da, db):
            prize = [prize[0], prize[1]]
            mat = ([da[0], db[0]], [da[1], db[1]])
            det_m = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
            a = (prize[0] * mat[1][1] - mat[0][1] * prize[1]) / det_m
            b = (mat[0][0] * prize[1] - prize[0] * mat[1][0]) / det_m
            if a >= 0 and a <= 100 and b >= 0 and b <= 100 and a.is_integer() and b.is_integer():
                total_tokens += 3*int(a) + int(b)
    print(f"Min. total tokens: {total_tokens}")

    # Condition for validity changes due to fp-rounding issues
    total_tokens = 0
    for machine in machines:
        da, db, prize = machine
        prize = [prize[0] + offset, prize[1] + offset]
        mat = ([da[0], db[0]], [da[1], db[1]])
        det_m = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        a = (prize[0] * mat[1][1] - mat[0][1] * prize[1]) / det_m
        b = (mat[0][0] * prize[1] - prize[0] * mat[1][0]) / det_m
        if a.is_integer() and b.is_integer():
            total_tokens += 3*int(a) + int(b)
    print(f"Min. total tokens: {total_tokens}")