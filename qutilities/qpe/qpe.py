from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qutilities.qft import QFT
from math import pi
from IPython.display import display

class QPE:
    def __init__(
        self,
        control_qubits: int,
        theta: float | None = None,
        unitary: QuantumCircuit | Gate | None = None,
        phase_qubits: int = 1,
        label: str | None = None,
        debug: bool = False,
        insert_barrier: bool = False,
        init_phase: bool = False
    ):

        """
        Quantum Phase Estimation (QPE) circuit builder.
        
        This class supports two use cases:
        1. A toy simulation using a known phase angle `theta`, simulating controlled powers of U = Rz(2πθ)
        2. A fully general implementation using a custom unitary `QuantumCircuit` or `Gate` to estimate its eigenphase
        
        Parameters
        ----------
        control_qubits : int
            Number of qubits in the control register (determines precision of phase estimation).
        
        theta : float, optional
            Phase value for simulated controlled-Rz gates (CP(2πθ · 2^k)). Mutually exclusive with `unitary` argument.
            Mainly, for educational purposes.
            (default: None)
        
        unitary : QuantumCircuit or Gate, optional
            A custom unitary U whose eigenphase is to be estimated. The number of `phase_qubits` must match the unitary's qubit width. Mutually exclusive with `theta` argument.
            (default: None)
        
        phase_qubits : int, optional
            Number of qubits in the phase register (i.e., the target system). Required if using `unitary`.
            If using `theta`, must be 1. (default: 1).
        
        label : str, optional
            Custom name for the circuit.
            (default: None)
        
        debug : bool, optional
            If True, renders the circuit diagram using matplotlib at build time.
            (default: False)
        
        insert_barrier : bool, optional
            If True, inserts barriers between QPE stages (useful for visualization, not suitable for gates).
            (default: False)
        
        init_phase : bool, optional
            If True, initializes the first qubit in the phase register to |1⟩. Required when simulating eigenvalue estimation for known θ.
            Mainly for educational purposes.
            (default: False)
        
        Raises
        ------
        ValueError
            If neither or both of `theta` and `unitary` are provided.
            If `theta` is used with more than 1 phase qubit.
        """
        
        if control_qubits < 1 or phase_qubits < 1:
            raise ValueError('[!] Both control and phase register must have at least 1 qubit.')

        if (theta is None and unitary is None) or (theta is not None and unitary is not None):
            raise ValueError(
                '[!] QPE requires either a phase angle (theta) or a custom unitary circuit (unitary).\n'
                '    Please provide one at a time. '
            )
        
        if theta is not None and phase_qubits > 1:
            raise ValueError(
                "[!] When using a phase angle (theta), the phase register should be a single qubit.\n"
                "    Multiple phase qubits are only valid when using a custom unitary."
            )
    
        self.control_qubits = control_qubits
        self.theta = theta
        self.phase_qubits = phase_qubits
        self.unitary = unitary
        self.debug = debug
        self.insert_barrier = insert_barrier
        self.label = label or f"QPE ({control_qubits} ⊗ {phase_qubits})"
        self.init_phase = init_phase

    def _create_registers(self):
        """Create and store all quantum/classical registers and the circuit."""
        self.control_reg = QuantumRegister(self.control_qubits, 'control')
        self.phase_reg = QuantumRegister(self.phase_qubits, 'phase')
        self.c_reg = ClassicalRegister(self.control_qubits, 'result')

        self.qpe_circuit = QuantumCircuit(self.control_reg, self.phase_reg, self.c_reg, name = self.label)

    def _init_phase_register(self):
        """Optionally initialize first phase qubit to |1⟩. Used in toy models where U |1⟩ = e^{2πiθ} |1⟩ is a known eigenstate."""
        if self.init_phase:
            self.qpe_circuit.x(self.phase_reg[0])

    def _init_control_register(self):
        """Apply Hadamard gates to all qubits in the control register."""
        self.qpe_circuit.h(self.control_reg)

    def _add_barrier(self):
        """Optionally insert a barrier between major QPE steps for clarity."""
        if self.insert_barrier:
            self.qpe_circuit.barrier()

    def _apply_controlled_rotations(self):
        """
        Apply controlled powers of a unitary operation.
    
        If a custom unitary is provided, this method applies controlled-U^(2^k)
        for each control qubit. Otherwise, it applies simulated controlled-phase
        rotations with CP(2πθ × 2^k) for toy QPE cases.
        """
        for control_qubit in range(self.control_qubits):
            if self.unitary is not None:
                # Apply controlled powers of the unitary circuit
                power = 2 ** control_qubit
                try:
                    powered = self.unitary.power(power)
                except:
                    raise ValueError('[!] Provided unitary circuit does not support ".power()"')
    
                # Apply controlled operation
                cu = powered.control()
                self.qpe_circuit.append(cu, [self.control_reg[control_qubit]] + list(self.phase_reg))
    
            else:
                # Use theta-based CP fallback
                angle = 2 * pi * self.theta * (2 ** control_qubit)
                for phase_qubit in range(self.phase_qubits):
                    self.qpe_circuit.cp(angle, self.control_reg[control_qubit], self.phase_reg[phase_qubit])
    
            self._add_barrier()

    def _apply_inverse_qft(self):
        """Apply inverse QFT to the control register using the QFT class."""
        inversed_qft = QFT(num_qubits=self.control_qubits, inverse=True, do_swaps=True)
        self.qpe_circuit.compose(inversed_qft.build(), qubits=self.control_reg, inplace=True)

    def _measure(self):
        """Measure control register qubits into classical bits."""
        self.qpe_circuit.measure(self.control_reg, self.c_reg)

    def build(self):
        """Assemble and return the full Quantum Phase Estimation circuit."""
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
    def __init__(
        self,
        control_qubits: int,
        theta = float,
        unitary: QuantumCircuit | Gate | None = None,
        phase_qubits: int = 1,
        label: str | None = None
    ):
        """
        Wrapper class to construct QPE as a reusable quantum gate.
        
        This class internally uses the `QPE` builder, but strips out all measurement operations and 
        returns the result as a unitary gate that can be composed into larger quantum circuits.
        
        It supports both toy `theta`-based simulations and general QPE with a custom unitary.
        
        Parameters
        ----------
        control_qubits : int
            Number of control (counting) qubits. Determines the precision of the phase estimation.
        
        theta : float, optional
            Phase value for simulated controlled-Rz gates. Mutually exclusive with `unitary` argument.
            Mainly for educational purposes.
            (default: None)
        
        unitary : QuantumCircuit or Gate, optional
            Custom unitary whose eigenphase is to be estimated. Must match `phase_qubits` width. Mutually exclusive with `theta` argument. 
            (default: None)
        
        phase_qubits : int, optional
            Number of target qubits in the phase register. Must match the size of the `unitary` if provided. 
            (default: 1)
        
        label : str, optional
            Optional label for the resulting gate. 
            (default: None)
        
        Raises
        ------
        ValueError
            If neither or both of `theta` and `unitary` are provided.
        """

        if (theta is None and unitary is None) or (theta is not None and unitary is not None):
            raise ValueError(
                "[!] QPE requires either a phase angle (theta) or a custom unitary circuit (unitary). "
                "Please provide one at a time."
            )
    
        self.qpe = QPE(
            control_qubits = control_qubits,
            theta = theta,
            unitary = unitary,
            phase_qubits = phase_qubits,
            label = label,
            insert_barrier = False,
            debug = False
        )

    def build(self):
        """
        Build the internal QPE circuit and return it as a reusable quantum gate.
        
        Returns
        -------
        Gate
            A unitary gate version of the QPE circuit with all measurements removed.
        """
        qpe_circuit = self.qpe.build()

        clean_qpe_circuit = QuantumCircuit(*qpe_circuit.qregs, name=self.qpe.label)
        
        for instruction in qpe_circuit.data:
            if instruction.operation.name != "measure":
                clean_qpe_circuit.append(instruction.operation, instruction.qubits, [])
                
        return clean_qpe_circuit.to_gate(label=self.qpe.label)