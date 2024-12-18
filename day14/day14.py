import sys
from functools import reduce

class Robot:
    map_width, map_height = 101, 103
    def __init__(self, position, velocity):
        self.vx, self.vy = velocity[0], velocity[1]    
        self.x, self.y = position[0], position[1]


    def __repr__(self):
        return f"Robot at position {self.x},{self.y} with velocity of {self.vx},{self.vy}"
    def __str__(self):
        return f"Robot at position {self.x},{self.y} with velocity of {self.vx},{self.vy}"
    
    def move(self):
        new_x = (self.x + self.vx) % (Robot.map_width)
        new_y = (self.y + self.vy) % (Robot.map_height)
        self.x = new_x
        self.y = new_y
    
    """
    Return the quadrant of the robot:
    0, 1, 2, 3 indicate upper left, upper right, lower left, and lower right, respectively.
    Return -1 if the robot is in the middle on any axis.
    """
    def get_quadrant(self):
        middle_width = Robot.map_width // 2
        middle_height = Robot.map_height // 2
        if self.x == middle_width or self.y == middle_height:
            return -1
        else:
            return 2*int(self.y > middle_height) + int(self.x > middle_width)
        
    def get_position(self):
        return (self.x, self.y)
    

def import_input(filename):
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip().split()
            pos, vel = [int(i) for i in line[0][2:].split(',')], [int(i) for i in line[1][2:].split(',')]
            robots.append(Robot(pos, vel))
    return robots

def print_robots(robots, file=sys.stdout):
    positions = {}
    for robot in robots:
        pos = robot.get_position()
        if pos in positions:
            positions[pos] += 1
        else:
            positions[pos] = 1
    for i in range(Robot.map_height):
        line = ""
        for j in range(Robot.map_width):
            if (i, j) in positions:
                line += str(positions[(i, j)])
            else:
                line += '.'
        print(line, file=file)

if __name__ == "__main__":
    robots = import_input("day14.txt")
    for _ in range(100):
        for robot in robots:
            robot.move()
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        q = robot.get_quadrant()
        if q >= 0:
            quadrants[q] += 1
    print(f"Quads: {quadrants}")
    print(f"Safety factor: {reduce(lambda x, y: x*y, quadrants)}")

    print("---")
    print("Part B: Movement check")
    print("---")

    robots = import_input("day14.txt")
    with open("output.txt", 'w') as f:
        for i in range(10000):
            print(f"\n\n----- {i+1} seconds -----\n\n", file=f)
            for robot in robots:
                robot.move()
            print_robots(robots, file=f)
            print("\n\n-----------\n\n", file=f)