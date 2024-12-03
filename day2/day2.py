
"""
    Return numeric input as a 2d matrix.
"""
def import_input(filename):

    with open(filename, 'r') as f:
        reports = [[int(c) for c in line.split()] for line in f]
    return reports

def diff_fail_check(diff, mode):
    return abs(diff) < 1 or abs(diff) > 3 or diff/mode < 0
"""
    Return if the report is "safe".
"""
def is_report_safe(report) -> bool:
    prev = report[0]
    # Mode will be < 0 if strictly decreasing
    # Mode will be > 0 if strictly increasing
    # In either case, if any diff is not matching sign of mode,
    # return False
    mode = report[1] - report[0]
    # since this check is done w/ division, check if mode=0 to ensure no div by 0 
    # (this shouldn't happen b/c of the first if statement ordering but alas)
    if mode == 0:
        return False
    for n in report[1:]:
        diff = n - prev
        # diff/mode will be < 0 if signs are opposite only
        if diff_fail_check(diff, mode):
            return False
        prev = n
    return True


if __name__ == "__main__":
    safe_reports = 0
    safe_reports_dampened = 0
    reports = import_input("day2.txt")
    for report in reports:
        if is_report_safe(report):
            safe_reports += 1
            safe_reports_dampened += 1
        else:
            # Yes I am aware this is not optimal. LOOK AWAY SANTA
            # I'm on the naughty list this year ig
            for i in range(len(report)):
                new_report = report[:]
                new_report.pop(i)
                if is_report_safe(new_report):
                    safe_reports_dampened += 1
                    break
    print(f'# of safe reports: {safe_reports}')
    print(f'# of safe reports w/ dampening: {safe_reports_dampened}')