"""--- Day 24: Crossed Wires ---"""

with open(0) as f:
    signal_data = {}

    for line in f:
        if line == "\n":
            break
        signal, val = line.strip().split(": ")
        signal_data[signal] = int(val)

    output_data = {}
    gate_data = {}
    for line in f:
        left, right = line.strip().split(" -> ")
        inp1sig, gate_type, inp2sig = left.split(" ")
        gate_data[(inp1sig, inp2sig, gate_type, right)] = right
        output_data[right] = (inp1sig, inp2sig, gate_type, right)


def simulate(signals, gates, outputs):
    signal_cache = {}

    def _evaluate(inp1sig, inp2sig, gate_type):
        if gate_type == "AND":
            return inp1sig and inp2sig
        if gate_type == "OR":
            return inp1sig or inp2sig
        if gate_type == "XOR":
            return inp1sig ^ inp2sig

    def _simulate(gate):
        inp1sig, inp2sig, gate_type, _ = gate
        if inp1sig in signals and inp2sig in signals:
            return _evaluate(signals[inp1sig], signals[inp2sig], gate_type)
        else:
            inp1sigval = signal_cache.get(inp1sig, None)
            inp2sigval = signal_cache.get(inp2sig, None)
            if inp1sigval is None:
                inp1sigval = _simulate(outputs[inp1sig])
                signal_cache[inp1sig] = inp1sigval
            if inp2sigval is None:
                inp2sigval = _simulate(outputs[inp2sig])
                signal_cache[inp2sig] = inp2sigval
            return _evaluate(inp1sigval, inp2sigval, gate_type)

    out = []
    for gate, output in gates.items():
        if output.startswith("z"):
            out.append((output, _simulate(gate)))

    return sorted(out, key=lambda x: x[0], reverse=True)


print(
    int(
        "".join([str(out[1]) for out in simulate(signal_data, gate_data, output_data)]),
        2,
    )
)
