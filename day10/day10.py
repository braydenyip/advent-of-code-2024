
def import_input(filename):
    output = []
    with open(filename, 'r') as f:
        for line in f:
            output.append([int(h) for h in line.rstrip()])
        return output
    
def hiking_rating_helper(hiking_map, i, j, prev):
    height, width = len(hiking_map), len(hiking_map[0])
    if i < 0 or i >= height or j < 0 or j >= width or hiking_map[i][j] != prev+1:
        return 0
    elif (hiking_map[i][j] == 9):
        return 1
    else:
        return (hiking_rating_helper(hiking_map, i-1, j, hiking_map[i][j]) +
        hiking_rating_helper(hiking_map, i, j+1, hiking_map[i][j]) +
        hiking_rating_helper(hiking_map, i+1, j, hiking_map[i][j]) +
        hiking_rating_helper(hiking_map, i, j-1, hiking_map[i][j]))

if __name__ == "__main__":
    
    hiking_map = import_input("day10.txt")
    width, height = len(hiking_map[0]), len(hiking_map)
    seen = set()
    total_peaks, total_ratings = 0, 0
    def hiking_helper(hiking_map, i, j, prev):
        if i < 0 or i >= height or j < 0 or j >= width or hiking_map[i][j] != prev+1:
            return
        elif (hiking_map[i][j] == 9):
            seen.add((i,j))
        else:
            hiking_helper(hiking_map, i-1, j, hiking_map[i][j])
            hiking_helper(hiking_map, i, j+1, hiking_map[i][j]) 
            hiking_helper(hiking_map, i+1, j, hiking_map[i][j]) 
            hiking_helper(hiking_map, i, j-1, hiking_map[i][j])

    for i, line in enumerate(hiking_map):
        for j, h in enumerate(line):
            if h == 0:
                hiking_helper(hiking_map, i, j, -1)
                total_peaks += len(seen)
                total_ratings += hiking_rating_helper(hiking_map, i, j, -1)
                seen = set()
    print(f"Total peaks: {total_peaks}")
    print(f"Total ratings: {total_ratings}")