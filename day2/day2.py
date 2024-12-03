
def import_input(filename):
    with open(filename, 'r') as f:
        reports = f.readlines()
    return reports

if __name__ == "__main__":
    reports = import_input("day2.txt")