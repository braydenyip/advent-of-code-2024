def import_input(filename):
    input_grid = True
    grid, movements = [], ""
    with open(filename, 'r') as f:
        for line in f:
            if len(line) < 2:
                input_grid = False
            elif input_grid:
                grid.append(list(line.rstrip()))
            else:
                movements += line.rstrip()
    return (grid, list(movements))

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.last_move = "/"
        self.height = len(grid)
        self.width = len(grid[0])

    def get_grid(self):
        return self.grid
    
    def get_tile(self, x, y):
        return self.grid[y][x]
    
    def set_last_move(self, move):
        self.last_move = move
    
    def get_current_position(self):
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile == "@":
                    return (i, j)
        return (-1, -1)

    def print_grid(self):
        if self.last_move == "/":
            print("--- Initial grid: ---")
        else:
            print(f"------ After last move ({self.last_move}) ------")
        for j, line in enumerate(self.grid):
            print(f'{j:02} ' + ''.join(line))
        print("\n")

class NormalGrid(Grid):

    """
    Get the tile in front of the head of the line of boxes
    Return as coordinates (x, y), which are coords of the tile IN FRONT of the line of boxes
    """
    def get_head(self, x, y, move):
        head_x, head_y = x, y
        curr = self.grid[head_y][head_x]
        while curr == "O":
            if move == "<":
                head_x -= 1
            elif move == "^":
                head_y -= 1
            elif move == ">":
                head_x += 1
            elif move == "v":
                head_y += 1
            curr = self.grid[head_y][head_x]
        return (head_x, head_y)

    def swap(self, cx, cy, next_x, next_y):
        self.grid[cy][cx], self.grid[next_y][next_x] = ".", "@"
    
    def move_boxes(self, tail_x, tail_y, head_x, head_y, move):
        # We just have to move the robot "tail" and the head to the first empty space
        if self.grid[head_y][head_x] != ".":
            return
        self.grid[head_y][head_x] = "O"
        if move == "<":
            self.grid[tail_y][tail_x], self.grid[tail_y][tail_x-1] = ".", "@"
        elif move == "^":
            self.grid[tail_y][tail_x], self.grid[tail_y-1][tail_x] = ".", "@"
        elif move == ">":
            self.grid[tail_y][tail_x], self.grid[tail_y][tail_x+1] = ".", "@"
        elif move == "v":
            self.grid[tail_y][tail_x], self.grid[tail_y+1][tail_x] = ".", "@"

    def move(self, move, x, y):
        next_x, next_y = x, y
        if move == "<":
            next_x = x - 1
        elif move == "^":
            next_y = y - 1
        elif move == ">":
            next_x = x + 1
        elif move == "v":
            next_y = y + 1
        else:
            return (-1, -1)
        # Update grid
        in_front = self.get_tile(next_x, next_y)
        if in_front == ".":
            self.swap(x, y, next_x, next_y)
        elif in_front == "O":
            head_x, head_y = self.get_head(next_x, next_y, move)
            if self.get_tile(head_x, head_y) == ".":
                self.move_boxes(x, y, head_x, head_y, move)
            else:
                next_x, next_y = x, y
        else:
            # Do not move if none of the above conditions are met (assume a wall)
            next_x, next_y = x, y
        self.last_move = move
        return (next_x, next_y)

    def get_score(self):
        score = 0
        for i in range(self.height):
            for j in range(self.width):
                if (self.grid[i][j] == "O"):
                    score += (100*i + j)
        return score

class DoubleWidthGrid(Grid):
    def __init__(self, grid):
        self.grid = DoubleWidthGrid.resize_grid(grid)
        self.height = len(grid)
        self.width = len(grid[0])
        self.last_move = "/"
    
    def resize_grid(grid):
        new_grid = []
        for i in range(len(grid)):
            line = []
            for j in range(len(grid[0])):
                if grid[i][j] == "#" or grid[i][j] == ".":
                    line += [grid[i][j], grid[i][j]]
                elif grid[i][j] == "O":
                    line += ['[', ']']
                else:
                    line += ['@', '.']
            new_grid.append(line)
        return new_grid

    def swap(self, cx, cy, next_x, next_y):
        self.grid[cy][cx], self.grid[next_y][next_x] = ".", "@"

    def get_score(self):
        score = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                h_score = min(i, height-1-i)
                if self.grid[i][j] == "[":
                    # width from ] to RS is width-1-(j+1) = width-j-2
                    w_score = min(j, width-j-2)
                    score += 100*h_score + w_score
        return score

    def move(self, move, x, y):
        next_x, next_y = x, y
        if move == "<":
            next_x = x - 1
        elif move == "^":
            next_y = y - 1
        elif move == ">":
            next_x = x + 1
        elif move == "v":
            next_y = y + 1
        else:
            return (-1, -1)
        
        in_front = self.get_tile(next_x, next_y)
        if in_front == '.':
            self.swap(x, y, next_x, next_y)
        elif in_front == '[' or in_front == ']':
            head_x, head_y = self.get_head(next_x, next_y, move)
            if self.get_tile(head_x, head_y) == '.':
                self.move_boxes(x, y, head_x, head_y, move)
            else:
                next_x, next_y = x, y
        else:
            # Do not move if none of the above conditions are met (assume a wall)
            next_x, next_y = x, y
        self.last_move = move
        return (next_x, next_y)
        
if __name__ == "__main__":
    grid_text, moves = import_input("test.txt")
    height, width = len(grid_text), len(grid_text[0])
    grid = NormalGrid(grid_text)
    
    y, x = grid.get_current_position()
    # Initialize next move to current spot
    next_y, next_x = y, x
    grid.print_grid()
    for move in moves:
        next_x, next_y = grid.move(move, x, y)
        # Update 'cursor' position (x, y)
        x, y = next_x, next_y
    grid.print_grid()
    score = grid.get_score()
    print(f"Total score part A: {score}")


    print("\n----------PART B-----------\n")
    grid_text, moves = import_input("test.txt")
    dw_grid = DoubleWidthGrid(grid_text)
    y, x = dw_grid.get_current_position()
    # Again, initialize next move to current spot
    # next_y, next_x = y, x
    # for move in moves:
    #     next_x, next_y = dw_grid.move(move, x, y)
    #     # Update 'cursor' position (x, y)
    #     x, y = next_x, next_y
    # dw_grid.print_grid()
    # score = dw_grid.get_score()
    # print(f"Total score part B: {score}")