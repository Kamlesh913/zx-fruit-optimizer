import pyzx as zx
from qiskit import QuantumCircuit, transpile
import pandas as pd
import matplotlib.pyplot as plt
import os

def grover5(marked=3):
    qc = QuantumCircuit(4)
    qc.h(range(4))
    b = format(marked,"04b")
    for i,bit in enumerate(b):
        if bit=="0": qc.x(i)
    qc.h(3)
    qc.mcx([0,1,2],3)
    qc.h(3)
    for i,bit in enumerate(b):
        if bit=="0": qc.x(i)
    qc.h(range(4)); qc.x(range(4))
    qc.h(3); qc.mcx([0,1,2],3); qc.h(3)
    qc.x(range(4)); qc.h(range(4))
    return qc

def qiskit_counts(qc):
    counts = qc.count_ops()
    tqc = transpile(qc, basis_gates=['t','tdg','cx'])
    tcounts = tqc.count_ops()
    return counts, tcounts.get('t',0) + tcounts.get('tdg',0)

def optimize(qc):
    g = zx.Circuit.from_qiskit(qc).to_graph()
    try: g.full_reduce()
    except: zx.simplify.full_reduce(g)
    return zx.Circuit.from_graph(g).to_qiskit()

os.makedirs("jackfruit/jackfruit_outputs", exist_ok=True)

qc = grover5()
b_counts, b_t = qiskit_counts(qc)
opt = optimize(qc)
o_counts, o_t = qiskit_counts(opt)

df = pd.DataFrame({
    "metric":["T-count","CNOT","Depth"],
    "baseline":[b_t, b_counts.get('cx',0), qc.depth()],
    "optimized":[o_t, o_counts.get('cx',0), opt.depth()]
})
df.to_csv("jackfruit/jackfruit_outputs/results.csv")
