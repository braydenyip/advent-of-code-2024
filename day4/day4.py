
target_word = 'XMAS'

def import_input(filename):
    with open(filename, 'r') as f:
        return [line.rstrip() for line in f]

# def search_letter(grid, i, j, letter):

#     total_found = 0
#     if letter == len(target_word-1):
#         total_found = 1
#     else:
        
#         height, width = len(grid), len(grid[0])
#         target_letter = target_word[letter+1]
#         for i2 in range(max(0, i-1), min(i+1, height-1)):
#             for j2 in range(max(0, j-1), min(j+1, width-1)):
#                 if grid[i2][j2] == target_letter:
#                     total_found += search_letter(grid, i2, j2, letter+1)
#     return total_found

def search_letter(grid, i, j, di, dj, current_letter_idx) -> int:

    if current_letter_idx == (len(target_word)-1):
        return 1
    i_new, j_new = i+di, j+dj
    if (i_new >= 0 and i_new < len(grid) and j_new >= 0 and j_new < len(grid[0]) and grid[i_new][j_new] == target_word[current_letter_idx+1]):
        return search_letter(grid, i_new, j_new, di, dj, current_letter_idx+1)
    else:
        return 0


def search_mas(grid, i, j):
    ul, ur, lr, ll = grid[i-1][j-1], grid[i-1][j+1], grid[i+1][j+1], grid[i+1][j-1]
    c1 = ul + 'A' + lr
    c2 = ur + 'A' + ll
    if (c1 == "SAM" or c1 == "MAS") and (c2 == "SAM" or c2 == "MAS"):
        return 1
    return 0
        
if __name__ == "__main__":
    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
    grid = import_input("day4.txt")
    grand_total = 0
    mas_total = 0
    height, width = len(grid), len(grid[0])
    for i in range(height):
        for j in range(width):
            letter = grid[i][j]
            if letter == target_word[0]:
                for direction in directions:
                    grand_total += search_letter(grid, i, j, direction[0], direction[1], 0)
            # Validate this could be a valid "X-MAS" before entering
            elif letter == 'A' and i > 0 and j > 0 and i < height-1 and j < width-1:
                mas_total += search_mas(grid, i, j)
    print(f"Total XMAS={grand_total}")
    print(f"Total X-MAS={mas_total}")