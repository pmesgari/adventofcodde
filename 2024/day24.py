"""--- Day 24: Crossed Wires ---"""


def normalize(x, op, y):
    return min(x, y), op, max(x, y)


with open(0) as f:
    device_data = {}
    output_data = {}
    for line in f:
        if line == "\n":
            break
        signal, val = line.strip().split(": ")
        device_data[signal] = int(val)

    for line in f:
        left, right = line.strip().split(" -> ")
        inp1sig, gate_type, inp2sig = left.split(" ")
        device_data[right] = normalize(inp1sig, gate_type, inp2sig)
        output_data[normalize(inp1sig, gate_type, inp2sig)] = right


def evaluate(sig1, gate_type, sig2):
    if gate_type == "AND":
        return sig1 and sig2
    if gate_type == "OR":
        return sig1 or sig2
    if gate_type == "XOR":
        return sig1 ^ sig2


def simulate(gate, device):
    sig1, gate_type, sig2 = gate
    if device[sig1] in [0, 1] and device[sig2] in [0, 1]:
        return evaluate(device[sig1], gate_type, device[sig2])
    else:
        sig1val = simulate(device[sig1], device)
        sig2val = simulate(device[sig2], device)
        return evaluate(sig1val, gate_type, sig2val)


def compute_z(device):
    zgates = {}
    zoutputs = {}
    for wire, out in device.items():
        if out not in [0, 1] and wire.startswith("z"):
            zgates[wire] = out
            zoutputs[out] = wire

    output = []
    for zsig in sorted(zoutputs.values(), reverse=True):
        output.append(str(simulate(zgates[zsig], device)))

    return "".join(output)


print(int(compute_z(device_data), 2))

for i in range(45):
    z = f'z{i:02d}'
    g = (f'x{i:02d}', f'y{i:02d}', f'z{i:02d}')
    x, op, y = device_data[z]
    if op != 'XOR':
        print(z, device_data[z])

def find_next_swap(device):
    num1 = int("".join([str(device[f"x{i:02d}"]) for i in reversed(range(45))]), 2)
    num2 = int("".join([str(device[f"y{i:02d}"]) for i in reversed(range(45))]), 2)
    res = "".join(compute_z(device))
    expected = num1 + num2

    print(f"x: {num1: b}")
    print(f"y: {num2: b}")
    print(f"z: {res}")
    print("e: " + f"{expected:b}")

    e = f"{expected:b}"
    for i in reversed(range(45)):
        if res[i] != e[i]:
            print(f"wrong bit {len(e) - i - 1}, expected {e[i]} got {res[i]}")
            break


def swap(a, b, device):
    device_copy = {k: v for k, v in device.items()}
    device_copy[a], device_copy[b] = device_copy[b], device_copy[a]
    return device_copy



find_next_swap(device_data)
e19 = ("x19", "XOR", "y19")
print(output_data.get(e19))
d1 = swap("nmn", "z19", device_data)

#find_next_swap(d1)

