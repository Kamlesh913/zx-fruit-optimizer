# ZX Fruit Optimizer 
Quantum Circuit Optimization with ZX-Calculus

This repository contains three structured experiments applying ZX-calculus rewrites to reduce the cost of quantum circuits. Each “fruit problem” corresponds to a different quantum circuit class:

| Problem | Description |
|--------|-------------|
| **Banana** | Benchmarking Clifford+T circuits using PyZX optimisations |
| **Orange** | ZX optimisation of a reversible 4-bit Cuccaro Adder |
| **Jackfruit** | ZX optimisation of a 5-qubit Grover iteration |

---

## 🚀 Features  
- ZX-calculus optimisation (spider fusion, gadget fusion, full_reduce)  
- Qiskit → ZX → Qiskit circuit transformation  
- Automatic extraction of T-count, CNOT count, and depth  
- CSV output + plots  
- Ready for GitHub Actions CI  

---

## Installation  
Use Python **3.10** (recommended for PyZX):

```bash
python3.10 -m venv zxenv
source zxenv/bin/activate        # Windows: zxenv\Scripts\activate
pip install qiskit matplotlib pandas
pip install git+https://github.com/Quantomatic/pyzx
