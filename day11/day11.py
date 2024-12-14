import math
def import_input(filename):
    with open(filename, 'r') as f:
        return [int(n) for n in f.readline().rstrip().split()]
    
def slow_stones(stones, runs=25):
    for n in range(runs):
        if n % 5 == 0:
            print(f'run {n}')
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

cache_list = [{} for _ in range(75)]

def fast_stones_helper(stone, run, max_runs = 75):
    if run == 0:
        print(f"stone {stone} at run {run}")
    if stone != 0:
        log_stone = int(math.log10(stone))
    else:
        log_stone = 0
    if run == max_runs-1:
        if log_stone % 2 == 1:
            cache_list[run][stone] = 2
        else:
            cache_list[run][stone] = 1
    else:
        if log_stone % 2 == 1:
            half_exp_stone = 10 ** (log_stone//2 + 1)
            ls, rs = stone // half_exp_stone, stone % half_exp_stone
            if ls not in cache_list[run+1]:
                fast_stones_helper(ls, run+1)
            if rs not in cache_list[run+1]:
                fast_stones_helper(rs, run+1)
            cache_list[run][stone] = cache_list[run+1][ls] + cache_list[run+1][rs]
        else:
            if stone == 0:
                new_stone = stone + 1
            else:
                new_stone = stone * 2024
            if new_stone not in cache_list[run+1]:
                fast_stones_helper(new_stone, run+1)
            cache_list[run][stone] = cache_list[run+1][new_stone]

if __name__ == "__main__":
    stones = import_input("day11.txt")
    stones_initial_result = slow_stones(stones)
    print(f'Length after 25 runs, slow method: {len(stones_initial_result)}')
    print(cache_list)

    stones = import_input("day11.txt")
    print(stones)
    
    for stone in stones:
        fast_stones_helper(stone, 0)

    stones_fast_result = sum(cache_list[0].values())
    print(f'Length after 75 runs, fast method: {stones_fast_result}')

    