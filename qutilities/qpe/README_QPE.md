# Quantum Phase Estimation (QPE) Implementation in Qiskit

This module provides a clean, modular implementation of **Quantum Phase Estimation (QPE)** using Qiskit. QPE is a core quantum algorithm used in **Shor’s Algorithm**, **eigenvalue estimation**, and many quantum chemistry and linear algebra applications.

---

## 📌 Features

- ✅ Implements **QPE** for arbitrary numbers of control and target qubits.
- 🔁 Optional initialization of the **target (phase) register** to known eigenstate `|1⟩` (useful for toy examples).
- 🧱 Built as a **class-based implementation (`QPE`)** with internal helper methods for clarity and reuse.
- 📦 Includes a companion **`QPEGate` class** for gate-based usage in larger circuits.
- 🧪 Optional **debug mode** and **barrier insertion** for better visualization (disabled in gates).
- 📐 Fully compatible with Qiskit workflows (`compose`, `append`, `to_gate`).

---

## 🧠 Algorithm Overview

Quantum Phase Estimation estimates the phase \( \theta \) in the eigenvalue:

\[
U |\psi\rangle = e^{2\pi i \theta} |\psi\rangle
\]

It uses:
- A **control register** (initialized in superposition via Hadamard)
- A **target register** containing a known eigenstate \( |\psi\rangle \)
- A sequence of **controlled \( U^{2^k} \)** operations
- An **inverse Quantum Fourier Transform (QFT)** to extract the phase

---

## ⚡ Implementation

This implementation uses:
1. A toy unitary: \( U = R_z(2\pi \theta) \)
2. Controlled phase shifts: `cp(2πθ × 2^k)`
3. Inverse QFT from the modular `QFT` class (imported separately)
4. A final measurement of the control register

---

## 🚀 Usage

### 🔧 1. Build a full QPE circuit

```python
from qpe import QPE

qpe = QPE(
    control_qubits=4,
    theta=0.125,               # Phase in the toy eigenvalue
    phase_qubits=1,            # Size of the eigenstate register
    init_phase=True,           # Initialize first target qubit to |1⟩
    insert_barrier=True,       # Add barriers for visualization
    debug=True                 # Show circuit
)

qc = qpe.build()
```

---

### 🧱 2. Use as a gate

```python
from qpe import QPEGate

gate = QPEGate(control_qubits=4, theta=0.125).build()

qc = QuantumCircuit(5)
qc.append(gate, range(5))
```

---

## 🔁 Optional Features

- `init_phase=True`: apply `X` gate to first target qubit to simulate eigenstate `|1⟩`.
- `insert_barrier=True`: adds visual barriers between stages (not allowed in gates).
- `debug=True`: renders circuit diagram inline using `draw('mpl')`.

---

## 🆕 Changelog

### v1.0
- Modular **class-based QPE implementation**
- Added support for toy unitaries using `theta`
- Support for `QPEGate` class with gate-safe export
- Built-in debug + barrier control
- Integration with external `QFT` module

---

## 🔗 References

- Nielsen & Chuang, *Quantum Computation and Quantum Information*
- IBM Qiskit Documentation: [https://qiskit.org/documentation/](https://qiskit.org/documentation/)
- Quantum Phase Estimation Algorithm: [Wikipedia](https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm)

---

## 💡 Contributions

Contributions and suggestions are welcome. Feel free to open issues or submit PRs!

---

## 📜 License

This project is licensed under the **Apache 2.0 License**.