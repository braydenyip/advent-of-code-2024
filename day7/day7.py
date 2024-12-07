import math

def import_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            trimmed_line = line.rstrip().split(" ")
            trimmed_line[0] = trimmed_line[0].split(":")[0]
            res.append([int(n) for n in trimmed_line])
    return res

# Apply a list of operations to nums
def apply_operations(nums, operators):
    running_total = nums[0]
    for i in range(len(nums)-1):
        if operators[i] == '+':
            running_total += nums[i+1]
        elif operators[i] == '*':
            running_total *= nums[i+1]
        elif operators[i] == '||':
            running_total = int(str(running_total) + str(nums[i+1]))
    return running_total

# Generatre a 'tree' of operators using backtracking-style algo
def generate_op_tree(n_ops):
    op_tree = []
    def gen_helper(combination, ops):
        if (len(combination) == n_ops):
            op_tree.append(combination)
            return
        else:
            for op in ops:
                new_comb = combination[:]
                gen_helper(new_comb + [op], ops)
    gen_helper([], ['+', '*', '||'])
    return op_tree


if __name__ == "__main__":
    eqns = import_input("day7.txt")
    operator_trees = {}
    calibrated_sum = 0
    for eqn in eqns:
        target, numbers = eqn[0], eqn[1:]
        n_ops = len(numbers) - 1
        if (n_ops not in operator_trees):
            tree = generate_op_tree(n_ops)
            operator_trees[n_ops] = tree
        # 'Traverse' the tree using the in-order listing provided by generate_op_tree
        for operator_list in operator_trees[n_ops]:
            res = apply_operations(numbers, operator_list)
            if res == target:
                print(f"Result found {res}, operators {operator_list}")
                calibrated_sum += res
                ## Break because possibility of duplicate solution
                break
    print(f"Calibrated sum is {calibrated_sum}")