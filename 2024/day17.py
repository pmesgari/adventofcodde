"""Day 17: Chronospatial Computer"""
import re


with open(0) as f:
    A, B, C, *program = map(int, re.findall(r"\d+", f.read()))


def combo(A, B, C, val):
    """Determine the combo operand"""
    if 0 <= val <= 3: return val
    if val == 4: return A
    if val == 5: return B
    if val == 6: return C
    raise Exception(f'Invalid operand {val}')

def run(A, B, C, program):
    """Run the computer"""
    pc = 0
    output = []
    while pc < len(program):
        opcode, operand = program[pc:pc+2]
        pc += 2
        match opcode:
            case 0: A = A // (2 ** combo(A, B, C, operand))
            case 1: B = B ^ operand
            case 2: B = combo(A, B, C, operand) % 8
            case 3:
                if A: pc = operand
            case 4: B = B ^ C
            case 5: output.append(combo(A, B, C, operand) % 8)
            case 6: B = A // (2 ** combo(A, B, C, operand))
            case 7: C = A // (2 ** combo(A, B, C, operand))
    return output


def find_A(A, B, C, program):
    """Find the A register value such that the program outputs itself"""
    As = {0}
    for char in reversed(range(len(program))):
        tail = program[char:]
        candidates = set()
        for A in As:
            for d in range(8):
                candidates.add((A * 8) + d)
        As = set()
        for cand in candidates:
            if run(cand, B, C, program) == tail:
                As.add(cand)
    return As

print(','.join(str(out) for out in run(A, B, C, program)))
print(min(find_A(A, B, C, program)))
