from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qutilities.qft import QFT
from math import pi

class QPE:
    """
    Quantum Phase Estimation (QPE) builder class.

    This class constructs a quantum circuit that performs the QPE algorithm,
    using a toy controlled-unitary U = Rz(2πθ), where θ is a known parameter.

    Attributes:
    -----------
    control_qubits : int
        Number of qubits used for phase estimation (counting qubits).
    theta : float
        The phase value encoded in the unitary U = Rz(2πθ).
    phase_qubits : int
        Number of target qubits prepared in eigenstate (default: 1).
    debug : bool
        If True, displays the final circuit using matplotlib.
    insert_barrier : bool
        If True, inserts barriers between major algorithm stages.
    label : str
        Optional label for the quantum circuit.
    init_phase : bool
        If True, initializes the first qubit in the phase register to |1⟩.
    """

    def __init__(
        self,
        control_qubits: int,
        theta: float,
        phase_qubits: int = 1,
        label: str | None = None,
        debug: bool = False,
        insert_barrier: bool = False,
        init_phase: bool = False  # Set to False for general unitary eigenstates
    ):
        if control_qubits < 1 or phase_qubits < 1:
            raise ValueError('[!] Both control and phase register must have at least 1 qubit.')

        self.control_qubits = control_qubits
        self.theta = theta
        self.phase_qubits = phase_qubits
        self.debug = debug
        self.insert_barrier = insert_barrier
        self.label = label or f"QPE ({control_qubits} ⊗ {phase_qubits})"
        self.init_phase = init_phase

    def _create_registers(self):
        """Create and store all quantum/classical registers and the circuit."""
        self.control_reg = QuantumRegister(self.control_qubits, 'control')
        self.phase_reg = QuantumRegister(self.phase_qubits, 'phase')
        self.c_reg = ClassicalRegister(self.control_qubits, 'result')
        self.qpe_circuit = QuantumCircuit(self.control_reg, self.phase_reg, self.c_reg, name=self.label)

    def _init_phase_register(self):
        """
        Optionally initialize the first phase qubit to |1⟩.

        This simulates an eigenstate such that:
        U |1⟩ = e^{2πiθ} |1⟩
        Useful for demonstrations with known phases.
        """
        if self.init_phase:
            self.qpe_circuit.x(self.phase_reg[0])

    def _init_control_register(self):
        """Apply Hadamard gates to put control register into equal superposition."""
        self.qpe_circuit.h(self.control_reg)

    def _add_barrier(self):
        """Insert a global barrier if enabled for visual clarity between steps."""
        if self.insert_barrier:
            self.qpe_circuit.barrier()

    def _apply_controlled_rotations(self):
        """
        Apply controlled phase rotations simulating powers of U = Rz(2πθ).

        For each control qubit i, apply:
        CP(2πθ × 2^i)
        to each qubit in the phase register.
        """
        for control_qubit in range(self.control_qubits):
            angle = 2 * pi * self.theta * (2 ** control_qubit)
            for phase_qubit in range(self.phase_qubits):
                self.qpe_circuit.cp(angle, self.control_reg[control_qubit], self.phase_reg[phase_qubit])
            self._add_barrier()

    def _apply_inverse_qft(self):
        """Apply the inverse QFT to the control register using the imported QFT class."""
        inversed_qft = QFT(num_qubits=self.control_qubits, inverse=True, do_swaps=True)
        self.qpe_circuit.compose(inversed_qft.build(), qubits=self.control_reg, inplace=True)

    def _measure(self):
        """Measure each control qubit into the corresponding classical bit."""
        self.qpe_circuit.measure(self.control_reg, self.c_reg)

    def build(self):
        """
        Assemble and return the full QPE circuit.

        Returns:
        --------
        QuantumCircuit
            Complete QPE circuit, optionally displayed if debug=True.
        """
        self._create_registers()
        self._init_control_register()
        self._init_phase_register()
        self._add_barrier()
        self._apply_controlled_rotations()
        self._apply_inverse_qft()
        self._add_barrier()
        self._measure()

        if self.debug:
            display(self.qpe_circuit.draw('mpl'))

        return self.qpe_circuit

class QPEGate:
    """
    Wrapper class to convert a QPE circuit into a reusable gate.

    Ensures the resulting subcircuit is gate-safe by:
    - Removing measurement operations
    - Excluding classical registers
    - Excluding barriers

    Useful for composing QPE as a subroutine within larger algorithms.
    """

    def __init__(
        self,
        control_qubits: int,
        theta = float,
        phase_qubits: int = 1,
        label: str | None = None
    ):
        self.qpe = QPE(
            control_qubits=control_qubits,
            theta=theta,
            phase_qubits=phase_qubits,
            label=label,
            insert_barrier=False,
            debug=False
        )

    def build(self):
        """
        Build a gate-safe QPE subcircuit by stripping measurements and barriers.

        Returns:
        --------
        Gate
            A reusable Qiskit Gate object for inclusion in larger circuits.
        """
        qpe_circuit = self.qpe.build()
        clean_qpe_circuit = QuantumCircuit(*qpe_circuit.qregs, name=self.qpe.label)

        for instruction in qpe_circuit.data:
            if instruction.operation.name != "measure":
                clean_qpe_circuit.append(instruction.operation, instruction.qubits, [])

        return clean_qpe_circuit.to_gate(label=self.qpe.label)
