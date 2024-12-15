
def import_input(filename):
    with open(filename, 'r') as f:
        return [list(line.rstrip()) for line in f]

def isOutOfBounds(i, j, farm_map, region):
    height, width = len(farm_map), len(farm_map[0])
    return i < 0 or i >= height or j < 0 or j >= width or farm_map[i][j] != region


if __name__ == "__main__":
    farm_map = import_input("day12.txt")

    height, width = len(farm_map), len(farm_map[0])
    def area_helper(i, j, region, seen):
        if isOutOfBounds(i, j, farm_map, region) or (i, j) in seen:
            return 0
        else:
            area = 1
            seen.add((i, j))
            for (x, y) in [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]:
                area += area_helper(x, y, region, seen)
            return area
    
    def perimeter_helper(i, j, region, seen):
        if isOutOfBounds(i, j, farm_map, region):
            return 0
        else:
            perimeter = 0
            seen.add((i, j))
            for (x, y) in [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]:
                if isOutOfBounds(x, y, farm_map, region):
                    perimeter += 1
                elif (x, y) not in seen:
                    perimeter += perimeter_helper(x, y, region, seen)
            return perimeter
    
    """
    Prevent duplicate calculation of regions
    Kept separate in order to decouple from calculation methods
    """
    def clear_region(i, j, region):
        if isOutOfBounds(i, j, farm_map, region):
            return
        farm_map[i][j] = '#'
        for (x, y) in [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]:
            clear_region(x, y, region)
        
    
    total_price = 0
    for i in range(height):
        for j in range(width):
            cur_tile = farm_map[i][j]
            if cur_tile != "#":
                # region_perimeter = perimeter_helper(i, j, cur_tile, farm_map.copy())
                region_area = area_helper(i, j, cur_tile, set())
                region_perimeter = perimeter_helper(i, j, cur_tile, set())
                clear_region(i, j, cur_tile)
                total_price += region_area * region_perimeter
    print(f"Total price: {total_price}")

