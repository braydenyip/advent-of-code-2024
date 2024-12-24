import heapq

def import_input(filename, n=-1, w=71, h=71):
    grid = [[0]*w for _ in range(h)]
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if n > 0 and i >= n:
                break
            coords = [int(c) for c in line.rstrip().split(',')]
            grid[coords[1]][coords[0]] = 1
    return grid

if __name__ == "__main__":
    # full_grid denotes safe tiles w/ -1 and unsafe tiles with the first turn they become unsafe
    # e.g., if dist=1 (turn 1), then 1 can no longer be added to the open list
    
    # width, height = 7, 7
    # full_grid = import_input("test.txt", n=12, w=width, h=height)
    # print(full_grid)
    width, height = 71, 71
    full_grid = import_input("day18.txt", n=1024)
    dist_grid = [[(width*height*width)]*width for _ in range(height)]
    dist_grid[0][0] = 0
    # Heap tuples are in form (dist,x,y)
    open = [(0,0,0)]
    seen = set()
    heapq.heapify(open)
    while open:
        dist, x, y = heapq.heappop(open)
        # Failsafe: if you run into an unsafe tile, move on
        if full_grid[y][x] == 1:
            continue
        new_dist = dist+1
        # check left
        if x > 0 and full_grid[y][x-1] == 0 and (new_dist) < dist_grid[y][x-1]:
            heapq.heappush(open, (new_dist, x-1, y))
            dist_grid[y][x-1] = new_dist
        # check right
        if x < width-1 and full_grid[y][x+1] == 0 and (new_dist) < dist_grid[y][x+1]:
            heapq.heappush(open, (new_dist, x+1, y))
            dist_grid[y][x+1] = new_dist
        # check up
        if y > 0 and full_grid[y-1][x] == 0 and (new_dist) < dist_grid[y-1][x]:
            heapq.heappush(open, (new_dist, x, y-1))
            dist_grid[y-1][x] = new_dist
        # check down
        if y < height-1 and full_grid[y+1][x] == 0 and (new_dist) < dist_grid[y+1][x]:
            heapq.heappush(open, (new_dist, x, y+1))
            dist_grid[y+1][x] = new_dist
    print(f"Result: {dist_grid[height-1][width-1]}")
        
