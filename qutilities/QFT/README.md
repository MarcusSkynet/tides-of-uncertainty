# Quantum Fourier Transform (QFT) Implementation in Qiskit

This repository provides an implementation of the **Quantum Fourier Transform (QFT)** and its inverse using Qiskit. The QFT is a crucial quantum algorithm used in many quantum computing applications, including **Shor's Algorithm**, quantum phase estimation, and quantum signal processing.

## 📌 Features

- Implements **QFT and its inverse** (QFT⁻¹) on a specified number of qubits.
- Allows optional **swap operations** for standard output ordering.
- Can be applied **as a gate** on existing quantum circuits.
- Debug mode available for **visualizing the QFT circuit**.

---

## 🧠 Mathematical Concept

The **Quantum Fourier Transform** (QFT) is the quantum analogue of the **Discrete Fourier Transform (DFT)**. Given an input quantum state:

$|x\rangle = \sum_{j=0}^{N-1} x_j |j\rangle$

QFT transforms it as follows:

$QFT |x\rangle = \sum_{k=0}^{N-1} y_k |k\rangle$

where the new coefficients are computed as:

$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j e^{2\pi i jk / N}$

This transformation is achieved in quantum circuits using a combination of **Hadamard gates** and **controlled phase shift gates**.

The inverse QFT (QFT⁻¹) negates the phase angles, reversing the transformation.

---

## ⚡ Implementation

The implementation follows these steps:

1. **Apply Hadamard gate** on each qubit.
2. **Apply controlled phase shift gates** between qubits.
3. (Optional) **Apply swap gates** to reorder qubits in standard QFT output format.
4. Convert the constructed circuit into a **Qiskit gate**.

---

## 🚀 Usage

### 1️⃣ Import and Create QFT Gate

```python
from QFT import QFT
from qiskit import QuantumCircuit

# Define number of qubits
num_qubits = 4

# Create QFT gate
qft_gate = QFT(num_qubits)
```

### 2️⃣ Apply QFT as a Gate on an Existing Circuit

```python
qc = QuantumCircuit(num_qubits)
qc.append(qft_gate, range(num_qubits))
qc.draw('mpl')  # Display circuit
```

### 3️⃣ Apply QFT to a Subset of Qubits in a Larger Circuit

If your circuit has more qubits than QFT requires, you can specify a subset:

```python
larger_qc = QuantumCircuit(6)  # Circuit with 6 qubits
qft_subset = QFT(3)  # QFT on only 3 qubits
larger_qc.append(qft_subset, [1, 2, 3])  # Apply to qubits 1,2,3
larger_qc.draw('mpl')
```

### 4️⃣ Using the Inverse QFT (QFT⁻¹)

To apply the inverse QFT, pass `inverse=True`:

```python
qft_inv_gate = QFT(num_qubits, inverse=True)
qc.append(qft_inv_gate, range(num_qubits))
qc.draw('mpl')
```

### 5️⃣ Debug Mode

If `debug=True`, the circuit diagram will be displayed:

```python
QFT(4, debug=True)
```

---

## 🎯 Applications

- **Shor’s Algorithm** for integer factorization.
- **Quantum Phase Estimation** to estimate eigenvalues.
- **Quantum Signal Processing** for wave function analysis.

---

## 🔗 References

- Nielsen & Chuang, *Quantum Computation and Quantum Information*
- IBM Qiskit Documentation: [https://qiskit.org/documentation/](https://qiskit.org/documentation/)

---

## 💡 Contributions

Feel free to contribute by improving the implementation or adding new features!

---

## 📜 License

This project is licensed under the MIT License.

