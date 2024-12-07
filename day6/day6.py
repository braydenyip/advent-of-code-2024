import sys

# use '-c' to do part b

def import_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            grid.append(list(line.rstrip()))
    return grid


def rotate_guard(guard):
    if guard == '^':
        return '>'
    elif guard == '>':
        return 'v'
    elif guard == 'v':
        return '<'
    else:
        return '^'


if __name__ == "__main__":
    grid = import_input("day6.txt")
    mirror_grid = import_input("day6.txt")
    
    height, width = len(grid), len(grid[0])

    for i in range(height):
        for j in range(width):
            if grid[i][j] == '^':
                starting_position = (i, j)
                break

    i, j = starting_position
    
    if len(sys.argv) < 2:
        while True:
            guard = grid[i][j]
            # Calculate next forward positions
            if guard == '^':
                next = (i-1, j)
            elif guard == '>':
                next = (i, j+1)
            elif guard == 'v':
                next = (i+1, j)
            else:
                next = (i, j-1)
            next_i, next_j = next
            if next_i < 0 or next_i >= height or next_j < 0 or next_j >= width:
                mirror_grid[i][j] = 'X'
                break
            elif grid[next_i][next_j] == '#':
                cycle_grid[i][j].add(guard)
                guard = rotate_guard(guard)
                grid[i][j] = guard
            else:
                mirror_grid[i][j] = 'X'
                grid[i][j] = '.'
                i, j = next_i, next_j
                grid[i][j] = guard

        total_traversed = 0
        for i in range(height):
            for j in range(width):
                if mirror_grid[i][j] == 'X':
                    total_traversed += 1

        print(f'Total squares: {total_traversed}')
    
    elif sys.argv[1] == "-c":
        cycles_detected = 0
        for ii in range(height):
            for jj in range(width):
                
                temp = [row[:] for row in grid]
                if grid[ii][jj] == '.':
                    temp[ii][jj] = '#'
                    print(f"Run: {ii}, {jj}")
                else:
                    continue
                cycle_grid = [[set() for _ in range(width)] for _ in range(height)]
                i, j = starting_position
                while True:
                    guard = temp[i][j]
                    # Calculate next forward positions
                    if guard == '^':
                        next = (i-1, j)
                    elif guard == '>':
                        next = (i, j+1)
                    elif guard == 'v':
                        next = (i+1, j)
                    else:
                        next = (i, j-1)
                    next_i, next_j = next
                    if next_i < 0 or next_i >= height or next_j < 0 or next_j >= width:
                        break
                    elif temp[next_i][next_j] == '#':
                        # If I run into an obstacle, I should note what orientation the guard was in
                        # If the orientation was the same as one previously seen, this must be a cycle...
                        if guard in cycle_grid[i][j]:
                            cycles_detected += 1
                            break
                        else:
                            cycle_grid[i][j].add(guard)
                            guard = rotate_guard(guard)
                            temp[i][j] = guard
                    else:
                        temp[i][j] = '.'
                        i, j = next_i, next_j
                        temp[i][j] = guard

        print(f'Total positions: {cycles_detected}')