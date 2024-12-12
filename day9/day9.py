
def import_input(filename):
    with open(filename, 'r') as f:
        return f.readline().rstrip()

"""
Get the sparse disk map representation of the dense disk map
"""
def get_sparse_disk_map(dense_disk_map):
    sparse_disk_map = []
    for i, c in enumerate(dense_disk_map):
        if i % 2 == 0:
            id = i // 2
            for _ in range(int(c)):
                sparse_disk_map.append(id)
        else:
            for _ in range(int(c)):
                sparse_disk_map.append(-1)
    return sparse_disk_map


def display_sparse_disk_map(sparse_disk_map):
    display_str = ""
    for n in sparse_disk_map:
        if n == -1:
            display_str += "."
        else:
            display_str += f"({str(n)})"
    print(display_str)
    
"""
Get the disk ID map mapping id to length
"""
def get_disk_id_map(dense_disk_map):
    disk_id_map = []
    for i in range(0, len(dense_disk_map), 2):
        if int(dense_disk_map[i]) > 0:
            disk_id_map.append(int(dense_disk_map[i]))
    return disk_id_map
    
def get_disk_positions(dense_disk_map):
    disk_positions_list = []
    position = 0
    for i, n in enumerate(dense_disk_map):
        if i%2 == 0 and int(n) > 0:
            disk_positions_list.append(position)
        position += int(n)
    return disk_positions_list

# Get in-order list of spaces and their size 
def get_spaces_list(dense_disk_map):
    spaces_list = []
    for i in range(1, len(dense_disk_map), 2):
        if int(dense_disk_map[i]) > 0:
            spaces_list.append(int(dense_disk_map[i]))
    return spaces_list

"""
Associate positions on the spaces list to positions on the dense_disk_map
"""
def get_spaces_positions(dense_disk_map):
    spaces_positions_list = []
    position = 0
    for i, n in enumerate(dense_disk_map):
        if i%2 == 1 and int(n) > 0:
            spaces_positions_list.append(position)
        position += int(n)
    return spaces_positions_list

def fragment_disk(sparse_disk_map):
    i, j = 0, len(sparse_disk_map)-1
    # start left point at free space.
    # start right point at data segment
    while sparse_disk_map[i] != -1:
        i += 1
    while sparse_disk_map[j] == -1:
        j -= 1
    while i < j:
        sparse_disk_map[i], sparse_disk_map[j] = sparse_disk_map[j], sparse_disk_map[i]
        while sparse_disk_map[i] != -1:
            i += 1
        while sparse_disk_map[j] == -1:
            j -= 1
    print(sparse_disk_map[i])
    print(sparse_disk_map[j])
    return sparse_disk_map

def fragment_disk_intact(sparse_disk_map, dense_disk_map):
    spaces_list = get_spaces_list(dense_disk_map)
    spaces_positions = get_spaces_positions(dense_disk_map)
    disk_lengths = get_disk_id_map(dense_disk_map)
    disk_positions = get_disk_positions(dense_disk_map)
    block_idx = len(disk_lengths) - 1
    # iterate through all file blocks in sparse map
    while block_idx >= 0:
        l = disk_lengths[block_idx]
        # LEFTMOST index of file
        rp = disk_positions[block_idx]
        print(f"block_idx={block_idx}")

        for i, space in enumerate(spaces_list):
            # LEFTMOST index of free space
            lp = spaces_positions[i]
            if lp > rp:
                break
            if space >= l:
                # perform L swaps
                for _ in range(l):
                    sparse_disk_map[lp], sparse_disk_map[rp] = sparse_disk_map[rp], sparse_disk_map[lp]
                    lp += 1
                    rp += 1
                # update spaces_list and spaces_positions
                spaces_list[i] -= l
                spaces_positions[i] += l
                break
        block_idx -= 1
    return sparse_disk_map
def get_checksum(sparse_disk_map):
    checksum = 0
    for i, n in enumerate(sparse_disk_map):
        if n >= 0:
            checksum += i*n
    return checksum

if __name__ == "__main__":
    dense_disk_map = import_input("day9.txt")
    
    sparse_disk_map_intact = get_sparse_disk_map(dense_disk_map)
    sparse_disk_map_intact = fragment_disk_intact(sparse_disk_map_intact, dense_disk_map)
    checksum_intact = get_checksum(sparse_disk_map_intact)
    print(f"Checksum, part 2: {checksum_intact}")