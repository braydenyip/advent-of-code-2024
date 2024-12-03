from collections import Counter
def import_input(filename):
    l1, l2 = [], []
    with open(filename, 'r') as f:
        for line in f:
            t = line.split()
            l1.append(int(t[0]))
            l2.append(int(t[1]))
    return (l1, l2)

if __name__ == '__main__':
    dist = 0
    similarity = 0
    l1, l2 = import_input("day1.txt")
    l1.sort()
    l2.sort()
    freq_l1 = Counter(l1)
    freq_l2 = Counter(l2)
    print(freq_l1)
    print(freq_l2)
    for i, n1 in enumerate(l1):
        dist += abs(n1 - l2[i])
        f_match = freq_l2.get(n1)
        if f_match:
            similarity += n1 * f_match
    print(f'Similarity: {similarity}') 
    print(f'Dist: {dist}') 