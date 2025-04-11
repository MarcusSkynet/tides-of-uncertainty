# On Tides of Uncertainty 🌊⚛️

*On Tides of Uncertainty* is my personal quantum playground — an evolving space documenting my learning journey, built quantum functions, algorithm implementations, experiments, and more. It blends curiosity-driven research with hands-on development, capturing the beautiful chaos of qubits, superpositions, and algorithms.

In the future, it might evolve into the foundation for a more interactive platform — one that brings the delightful nonsensicality of qubits to a broader audience. After all, everyone should experience the existential absurdity of the quantum world.

Feel free to explore or reverse-engineer anything here — and don’t hesitate to reach out if you have questions or ideas.

---

## 📁 Structure

- `qutilities/`: Low-level reusable components (e.g. controlled gates, register helpers)
- `algorithms/`: Full algorithm implementations (Shor, Grover, etc.)
- `notebooks/`: Educational experiments, proofs-of-concept, and dynamic demos
- `~legacy/`: Earlier code from the beginning of this quantum journey

---

## 🛠 Installation

This repo uses a modern [PEP 517](https://peps.python.org/pep-0517/) `pyproject.toml` layout. You can install the `qutilities` package locally for use in your own notebooks or projects:

```bash
git clone https://github.com/your-username/tides-of-uncertainty.git
cd tides-of-uncertainty
pip install -e .
```

This will install the `qutilities` package in editable mode. You can then import any component like:

```python
from qutilities.qft import QFT
from qutilities.qpe import QPE, QPEGate
```

Requires:
- Python ≥ 3.8
- [Qiskit](https://qiskit.org/) (included in dependencies)

---

## 📜 License

This project is licensed under the Apache 2.0 License. See [LICENSE](./LICENSE) for details.
