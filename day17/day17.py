import time
import math

def import_input(filename):
    regs = []
    with open(filename, 'r') as f:
        for line in f:
            if len(line) < 2:
                continue
            if line.rstrip().split()[0] == "Register":
                regs.append(int(line.rstrip().split()[2]))
            else:
                program = [int(i) for i in line.rstrip().split()[1].split(',')]
    return (regs, program)

program_states = {}

def get_operand_value(regs, operand):
    if operand < 4:
        return operand
    elif operand < 7:
        return regs[operand-4]
    else:
        return 0
    
def run_program(regs, program):
    output = ""
    ip, opcode, output_ptr = 0, 0, 0
    jumped = False
    while (ip < len(program)-1):
        
        opcode = program[ip]
        operand = get_operand_value(regs, program[ip+1])
        # regs_tuple = (regs[0], regs[1], regs[2], ip)
        # if regs_tuple in program_states[opcode]:
        #     return "0,"
        # else:
        #     program_states[opcode].add(regs_tuple)
        
        if output_ptr >= len(program)-1:
            return output
        # print(f"perform opcode {opcode} with regs {regs} and combo operand {operand}")
        if opcode == 0:
            # ad
            regs[0] = regs[0] >> operand
        elif opcode == 1:
            regs[1] = regs[1] ^ program[ip+1]
        elif opcode == 2:
            regs[1] = operand % 8
        elif opcode == 3 and regs[0] != 0:
            ip = program[ip+1]
            jumped = True
        elif opcode == 4:
            regs[1] = regs[1] ^ regs[2]
        elif opcode == 5:
            out_value = operand%8
            output += f"{out_value},"
            output_ptr += 1
        elif opcode == 6 or opcode == 7:
            regs[opcode-5] = regs[0] >> operand
        if not jumped:
            ip += 2
        jumped = False
    return output[:-1]

def run_fast_until(a, program):
    # Note that since the regs[0] is modified only after regs[1] is extracted from it,
    # we can just divide it by 8 every loop...
    # Working backwards:
    # the last operation before output is regs[1] = regs[1] xor regs[2]
    # regs[2] = regs[0] / 2^regs[1] after the first step
    # i.e., regs[2] = regs[0] / 2^(regs[0]%8 xor 1) = regs[0] >> (regs[0]%8 xor 1)
    # regs[1] = (regs[0]) % 8 xor 1 xor 4
    # This means on every pass regs[1] = (regs[0]) % 8 xor 1 xor 4
    # Thus, regs[1] = [(regs[0]) % 8 xor 1 xor 4] xor [regs[0] >> (regs[0]%8 xor 1)]
    res = []
    index = 0
    while a > 0:
        m8 = a%8
        print_num = (m8 ^ 1 ^ 4) ^ (a >> (m8 ^ 1))
        if print_num == program[index]:
            res.append(print_num)
            index += 1
        else:
            break
        a = a >> 3
    return res


def search_space_helper(i, current_a, program):
    if i == -1:
        print(f"final a={current_a}")
        return -1
    current_a = current_a << 3    
    for j in range(8):
        new = current_a + j
        res = run_program([new, 0, 0], program).split(",")[0]
        if int(res) == program[i]:
            dfs_res = search_space_helper(i-1, new, program)
            if dfs_res >= 0:
                return current_a
    return -1
if __name__ == "__main__":
    regs, program = import_input("day17.txt")
    program_literal = ""
    for o in program:
        program_literal += f"{o},"
    program_literal = program_literal[:-1]
    print(f"Program: {program_literal}")

    output = run_program(regs, program)
    print(f"Part A: {output}")

    a = search_space_helper(len(program)-1, 0, program)
    print(a)
    print("END")
            
