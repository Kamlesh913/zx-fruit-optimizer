import pyzx as zx
from qiskit import QuantumCircuit, transpile
import pandas as pd
import matplotlib.pyplot as plt
import os, random

def qiskit_counts(qc):
    counts = qc.count_ops()
    tqc = transpile(qc, basis_gates=['t','tdg','cx','u1','u2','u3'])
    tcounts = tqc.count_ops()
    return counts, tcounts.get('t',0) + tcounts.get('tdg',0)

def make_random_ct(n_qubits=4, depth=12):
    qc = QuantumCircuit(n_qubits)
    for _ in range(depth):
        for q in range(n_qubits):
            r = random.random()
            if r < 0.3: qc.h(q)
            elif r < 0.6: qc.s(q)
            else: qc.t(q)
        qc.cx(0,n_qubits-1)
    return qc

def optimize(qc):
    circ = zx.Circuit.from_qiskit(qc)
    g = circ.to_graph()
    try: g.full_reduce()
    except: zx.simplify.full_reduce(g)
    return zx.Circuit.from_graph(g).to_qiskit()

os.makedirs("banana/banana_outputs", exist_ok=True)

qc = make_random_ct()
b_counts, b_t = qiskit_counts(qc)
opt = optimize(qc)
o_counts, o_t = qiskit_counts(opt)

df = pd.DataFrame([{
    "metric":["T-count","Depth","Total gates"],
    "baseline":[b_t, qc.depth(), sum(b_counts.values())],
    "optimized":[o_t, opt.depth(), sum(o_counts.values())]
}])
df.to_csv("banana/banana_outputs/results.csv")
