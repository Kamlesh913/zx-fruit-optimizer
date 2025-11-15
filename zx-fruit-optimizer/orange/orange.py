import pyzx as zx
from qiskit import QuantumCircuit, transpile
import pandas as pd
import matplotlib.pyplot as plt
import os

def cuccaro_adder():
    qc = QuantumCircuit(9)
    for i in range(4):
        qc.cx(i, i+4)
        qc.cx(i+4, 8)
        qc.ccx(i, i+4, 8)
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

os.makedirs("orange/orange_outputs", exist_ok=True)

qc = cuccaro_adder()
b_counts, b_t = qiskit_counts(qc)
opt = optimize(qc)
o_counts, o_t = qiskit_counts(opt)

df = pd.DataFrame({
    "metric":["T-count","CNOT","Depth"],
    "baseline":[b_t, b_counts.get('cx',0), qc.depth()],
    "optimized":[o_t, o_counts.get('cx',0), opt.depth()]
})
df.to_csv("orange/orange_outputs/results.csv")
