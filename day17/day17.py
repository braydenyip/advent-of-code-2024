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

def run_program_until(regs, program):
    output = []
    ip, opcode, output_ptr = 0, 0, 0
    jumped = False
    while (ip < len(program)-1):
        
        opcode = program[ip]
        operand = get_operand_value(regs, program[ip+1])
        # regs_tuple = (regs[0], regs[1], regs[2], ip)
        # if regs_tuple in program_states[opcode]:
        #     return False
        # else:
        #     program_states[opcode].add(regs_tuple)

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
            if output_ptr > (len(program) - 1) or out_value != program[output_ptr]:
                return False
            else:
                output_ptr += 1
                output.append(out_value)
        elif opcode == 6 or opcode == 7:
            regs[opcode-5] = regs[0] >> operand
        if not jumped:
            ip += 2
        jumped = False
    return output == program

if __name__ == "__main__":
    regs, program = import_input("day17.txt")
    program_literal = ""
    for o in program:
        program_literal += f"{o},"
    program_literal = program_literal[:-1]
    print(f"Program: {program_literal}")
    for i in range(8):
        program_states[i] = set()
    output = run_program(regs, program)
    print(f"Part A: {output}")
    a = 0
    regs = [0,0,0]
    while (a < 99000000) and not run_program_until(regs, program):
        regs[0], regs[1], regs[2] = a, 0, 0
        a += 1
    print("END")
            
