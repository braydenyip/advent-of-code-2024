import math
def import_input(filename):
    with open(filename, 'r') as f:
        return [int(n) for n in f.readline().rstrip().split()]
    
def slow_stones(stones, runs=25):
    for _ in range(runs):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            else:
                log_stone = int(math.log10(stone))
                half_exp_stone = 10 ** (log_stone//2 + 1)
                if log_stone % 2 == 1:
                    ls, rs = stone // half_exp_stone, stone % half_exp_stone
                    new_stones.append(ls)
                    new_stones.append(rs)
                else:
                    new_stones.append(stone * 2024)
        stones = new_stones
    return stones

if __name__ == "__main__":
    stones = import_input("day11.txt")
    print(f'Length after 25 runs, slow method: {len(slow_stones(stones))}')