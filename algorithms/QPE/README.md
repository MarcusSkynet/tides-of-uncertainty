# Quantum Phase Estimation (QPE) - On Tides of Uncertainty

This module provides a clean and configurable implementation of **Quantum Phase Estimation (QPE)**, a key quantum algorithm for extracting eigenphases of unitary operators. It is part of the **on-tides-of-uncertainty** quantum computation toolkit.

---

## 📌 Features

- ✅ Standard QPE implementation with tunable parameters
- 🔁 Supports arbitrary number of counting and target qubits
- 🌀 Parameterized by rotation angle `theta` for toy phase estimation
- 🧱 Modular design for composing into larger quantum algorithms
- 🧪 Built-in support for visualization and measurement

---

## 🧠 What is QPE?

Quantum Phase Estimation is an algorithm that estimates the phase \( \theta \) in the eigenvalue \( e^{2\pi i \theta} \) of a unitary operator \( U \), given a corresponding eigenvector \( |\psi\rangle \).

It is widely used in:
- Shor’s algorithm
- Quantum simulations
- Eigenvalue problems in quantum chemistry

---

## 🚀 Example Usage

```python
from qpe import QPE

# Estimate phase theta = 0.125 using 3 counting qubits and 1 target qubit
circuit = QPE(num_qubits=3, theta=0.125, phase_qubits=1)
circuit.draw('mpl')
```

---

## 🧱 Circuit Structure

1. Apply Hadamards to counting register
2. Prepare target qubit in eigenstate (e.g. |1⟩)
3. Apply controlled-U^{2^j} operations
4. Apply inverse QFT to counting register
5. Measure and extract phase estimate

---

## 🆕 Upcoming Features

- Support for general unitary operators (controlled-U injection)
- Optional use of external QFT modules
- Class-based version for advanced configuration

---

## 📜 License

Licensed under the **Apache 2.0 License**.

