# Quantum Fourier Transform (QFT) Implementation in Qiskit

This repository provides a flexible and extensible implementation of the **Quantum Fourier Transform (QFT)** and its inverse using Qiskit. The QFT is a foundational quantum algorithm used in various quantum computing applications such as **Shor's Algorithm**, **quantum phase estimation**, and **quantum signal processing**.

---

## 📌 Features

- ✅ Implements **QFT and its inverse (QFT⁻¹)** for arbitrary numbers of qubits.
- 🔁 Optional **qubit swaps** to reverse register order, matching classical output.
- ⚙️ **Approximation control** for reducing circuit depth by skipping smallest-angle CP gates.
- 🧱 Designed as a **class (`QFT`) with reusable configuration** and gate/circuit generation.
- 🧪 Built-in **debug and visualization tools** for easier development.
- 📐 Can output as either a **Qiskit Gate** (for `.append`) or full **QuantumCircuit** (for `.compose`).

---

## 🧠 Mathematical Concept

The **Quantum Fourier Transform** (QFT) is the quantum analogue of the **Discrete Fourier Transform (DFT)**. Given a quantum state:

$$|x\rangle = \sum_{j=0}^{N-1} x_j |j\rangle$$

The QFT maps it to:

$$QFT |x\rangle = \sum_{k=0}^{N-1} y_k |k\rangle$$

where:

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j e^{2\pi i jk / N}$$

This transformation is realized via a sequence of **Hadamard gates** and **controlled phase rotations**.

---

## ⚡ Implementation

The QFT class supports the following configurable options:

1. **Hadamard gates** applied in specified qubit order (depends on inverse flag).
2. **Controlled-phase rotations**, optionally skipping gates via `approximation_level`.
3. **Qubit swaps** at beginning (inverse) or end (forward) to restore register order.
4. **Optional debug visualization** and **barrier insertion** for clarity.
5. Outputs a **Gate or full Circuit**, depending on user needs.

---

## 🚀 Usage

### 🔧 1. Import and Initialize

```python
from QFT import QFT

# Create a 4-qubit QFT gate generator
qft = QFT(
    num_qubits=4,
    inverse=False,               # Optional: build inverse QFT
    do_swaps=True,              # Optional: include swaps
    approximation_level=1,      # Optional: skip small-angle CPs
    debug=True,                 # Optional: show circuit
    insert_barrier=True         # Optional: add barriers for visualization
)
```

### 🧱 2. Use in a QuantumCircuit

#### As a Gate (append):
```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(4)
qc.append(qft.build(as_gate=True), range(4))
```

#### As a Subcircuit (compose):
```python
sub = qft.build(as_gate=False)
qc = QuantumCircuit(4)
qc = qc.compose(sub, qubits=range(4))
```

---

## 🔁 Using Inverse QFT
```python
qft_inv = QFT(num_qubits=4, inverse=True)
qc.append(qft_inv.build(), range(4))
```

---

## 🎯 Applications

- **Shor’s Algorithm** for integer factorization
- **Quantum Phase Estimation**
- **Quantum Signal Processing**

---

## 🆕 Changelog

### v2.0
- Rewritten as a **class-based implementation**
- Added support for **approximation level**
- Support for **debug + barrier visualization**
- Dual-mode return: **Gate** or **QuantumCircuit**
- Modular, extensible design with internal helper methods

---

## 🔗 References
- Nielsen & Chuang, *Quantum Computation and Quantum Information*
- IBM Qiskit Documentation: [https://qiskit.org/documentation/](https://qiskit.org/documentation/)

---

## 💡 Contributions

Feel free to contribute improvements, bug fixes, or ideas!

---

## 📜 License

This project is licensed under the **Apache 2.0 License**.