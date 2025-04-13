# Quantum Fourier Transform (QFT) Module — Qiskit Implementation

This module provides a composable and extensible implementation of the **Quantum Fourier Transform (QFT)** and its inverse using Qiskit. It is designed for clarity, experimentation, and reuse in larger quantum circuits such as **Shor's algorithm** and **Quantum Phase Estimation (QPE)**.

---

## 📦 Overview

- ✅ Fully class-based design: `QFT` (circuit generator) and `QFTGate` (gate wrapper).
- 🔁 Optional **qubit swaps** to reverse output bit order.
- ⚙️ **Approximation level** support for skipping smallest-angle phase gates.
- 🔍 Built-in visualization and barrier insertion tools.
- 🔧 Easily configurable, composable, and extendable.

---

## 🧠 Mathematical Foundation

The **Quantum Fourier Transform** maps a quantum state from the computational basis into the Fourier basis:

\[
|x\rangle = \sum_{j=0}^{N-1} x_j |j\rangle \quad \longrightarrow \quad QFT |x\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} \left(\sum_{j=0}^{N-1} x_j e^{2\pi i jk/N}\right) |k\rangle
\]

This transformation is implemented through a series of **Hadamard gates** and **controlled phase rotations**.

---

## 🔧 Usage

### 🧱 1. QFT Circuit

```python
from qutilities.qft import QFT

qft = QFT(
    qft_qubits=4,
    inverse=False,
    do_swaps=True,
    approximation_level=1,
    debug=True,
    insert_barrier=True
)

circuit = qft.build()
```

### 🔁 2. QFT Gate

```python
from qutilities.qft import QFTGate
from qiskit import QuantumCircuit

qft_gate = QFTGate(4, inverse=True, do_swaps=True)
gate = qft_gate.build()

qc = QuantumCircuit(4)
qc.append(gate, range(4))
```

---

## 🧪 Configuration Options

| Parameter             | Description                                               |
|----------------------|-----------------------------------------------------------|
| `qft_qubits`         | Number of qubits in the transform                         |
| `inverse`            | If True, builds the inverse QFT                           |
| `do_swaps`           | If True, adds output-swapping operations                  |
| `approximation_level`| Skips lowest-angle CP gates to reduce depth               |
| `debug`              | If True, displays a visual diagram                        |
| `insert_barrier`     | Adds barriers between steps for clarity                   |

---

## 🔁 Typical Applications

- ✅ **Quantum Phase Estimation (QPE)**
- 🔐 **Shor’s Algorithm**
- 📊 **Quantum signal processing**

---

## 🆕 Changelog

### v2.0

- Modular class split: `QFT` (circuit) and `QFTGate` (gate)
- Method-based architecture for each construction step
- Improved visualization, approximation, and flexibility
- `qft_qubits` replaces `num_qubits` for clarity

---

## 🔗 References

- M. Nielsen and I. Chuang — *Quantum Computation and Quantum Information*
- [Qiskit Documentation](https://qiskit.org/documentation/)

---

## 📜 License

Licensed under the **Apache License 2.0**