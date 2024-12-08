
def import_input(filename):
    output = []
    with open(filename, 'r') as f:
        for line in f:
            output.append(list(line.rstrip()))
        return output
    
def in_bounds(value, limit):
    return value >= 0 and value < limit
if __name__ == "__main__":
    grid = import_input("day8.txt")
    height, width = len(grid), len(grid[0])
    seen = set()
    frequency_lut = {}
    for i in range(height):
        for j in range(width):
            freq = grid[i][j]
            if freq != '.':
                if freq in frequency_lut:
                    frequency_lut[freq].append((i, j))
                else:
                    frequency_lut[freq] = [(i, j)]
    for k, v in frequency_lut.items():
        for pt in v:
            for tgt in v:
                if pt != tgt:
                    seen.add((tgt[0], tgt[1]))
                    seen.add((pt[0], pt[1]))
                    dx, dy = tgt[0]-pt[0], tgt[1]-pt[1]
                    fwd_anti_x, fwd_anti_y = tgt[0] + dx, tgt[1] + dy
                    while in_bounds(fwd_anti_x, width) and in_bounds(fwd_anti_y, height):
                        seen.add((fwd_anti_x, fwd_anti_y))
                        fwd_anti_x, fwd_anti_y = fwd_anti_x + dx, fwd_anti_y + dy

                    bwd_anti_x, bwd_anti_y = pt[0] - dx, pt[1] - dy
                    while in_bounds(bwd_anti_x, width) and in_bounds(bwd_anti_y, height):
                        seen.add((bwd_anti_x, bwd_anti_y))
                        bwd_anti_x, bwd_anti_y = bwd_anti_x - dx, bwd_anti_y - dy
    # grid_new = []
    # for i in range(height):
    #     row = []
    #     for j in range(width):
    #         if (i,j) in seen:
    #             row.append("#")
    #         else:
    #             row.append(".")
    #     grid_new.append(row)
    # for row in grid_new:
    #     print(row)
    print(f"Number of antinodes:{len(seen)}")