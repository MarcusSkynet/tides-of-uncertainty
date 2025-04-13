from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from math import pi

class QFT:
    def __init__(
        self,
        qft_qubits: int,
        inverse: bool = False,
        do_swaps: bool = False,
        approximation_level: int = 0,
        debug: bool = False,
        insert_barrier: bool = False,
        label: str | None = None
    ):
        """
        Initialize a configurable Quantum Fourier Transform (QFT) generator.

        Parameters:
        - num_qubits (int): Number of qubits the QFT will act on.
        - inverse (bool): If True, builds the inverse QFT (used in algorithms like Quantum Phase Estimation).
        - do_swaps (bool): If True, includes qubit-swapping logic to reverse qubit order at the end (or beginning for inverse).
        - approximation_level (int): Controls how many smallest-angle CP gates to skip to reduce circuit depth.
        - debug (bool): If True, display the constructed circuit diagram after building.
        - insert_barrier (bool): If True, insert visual barriers between logical blocks for better visualization.
        - label (str|None): Optional label for the returned QFT gate.
        """
        if qft_qubits is None or qft_qubits < 1:
            raise ValueError("[!] Number of qubits must be a positive integer.")

        if label is None:
            label = f"QFT ({qft_qubits})" if not inverse else f"QFT† ({qft_qubits})"

        self.qft_qubits = qft_qubits
        self.inverse = inverse
        self.do_swaps = do_swaps
        self.approximation_level = approximation_level
        self.debug = debug
        self.insert_barrier = insert_barrier
        self.label = label

    def _qubit_range(self):
        '''
        Determines the processing order of qubits. For inverse QFT, we apply gates from lowest to highest index.
        For forward QFT, the order is reversed (highest to lowest index), matching standard QFT gate application order.
        '''
        return list(range(self.qft_qubits)) if self.inverse else list(reversed(range(self.qft_qubits)))

    def _target_range(self, control_qubit):
        '''
        Returns the list of target qubits for a given control qubit.
        In the forward QFT, targets are lower-indexed qubits.
        In the inverse QFT, targets are higher-indexed qubits.
        '''
        return (
            list(range(control_qubit + 1, self.qft_qubits))
            if self.inverse else list(range(control_qubit - 1, -1, -1))
        )

    def _should_approximate(self, distance: int) -> bool:
        '''
        Determines whether a controlled-phase gate should be skipped due to approximation.
        If the gate acts between distant qubits (i.e., distance > cutoff), it is skipped.
        This reduces gate count and depth for near-term quantum devices.
        '''
        cutoff = self.qft_qubits - 1 - self.approximation_level
        return distance > cutoff

    def _swap_pairs(self) -> list[tuple[int, int]]:
        '''
        Generates a list of symmetric qubit pairs to swap.
        This is used to reverse qubit order which is necessary
        because the QFT naturally outputs in reverse bit order.
        '''
        return [(i, self.qft_qubits - i - 1) for i in range(self.qft_qubits // 2)]

    def _add_barrier(self, circuit):
        '''
        Adds a barrier after each major step if enabled.
        Barriers help visually separate logical steps in the circuit for debugging and clarity.
        '''
        if self.insert_barrier:
            circuit.barrier()

    def _debug_display(self, circuit):
        '''
        Displays the circuit using matplotlib if debug mode is enabled.
        This is useful for visually verifying circuit structure during development.
        '''
        if self.debug:
            display(circuit.draw('mpl'))

    def _init_circuit(self):
        """
        Initialize the internal QuantumCircuit object.
    
        Creates a new QuantumCircuit with the configured number of qubits.
        This circuit will store the QFT or inverse QFT construction.
        """
        self.qft_circuit = QuantumCircuit(self.qft_qubits)

    def _apply_pre_swaps(self):
        """
        Apply swap operations before the main QFT logic (used in inverse QFT).
    
        If `inverse=True` and `do_swaps=True`, this reverses the qubit order
        before applying the transform. This is necessary to align the
        qubit layout with the expected inverse QFT output.
    
        A barrier is added after the swaps if `insert_barrier=True`.
        """
        if self.inverse and self.do_swaps:
            for q1, q2 in self._swap_pairs():
                self.qft_circuit.swap(q1, q2)
            self._add_barrier(self.qft_circuit)

    def _apply_post_swaps(self):
        """
        Apply swap operations after the QFT logic (used in forward QFT).
    
        If `inverse=False` and `do_swaps=True`, this reverses the qubit order
        after the transform to match classical bit order in typical QFT use.
    
        No barrier is added after post-swaps.
        """
        if not self.inverse and self.do_swaps:
            for q1, q2 in self._swap_pairs():
                self.qft_circuit.swap(q1, q2)

    def _apply_core_transform(self):
        """
        Apply the core sequence of gates for QFT or inverse QFT.
    
        This includes:
        - A Hadamard gate for each qubit
        - Controlled-phase rotations with decreasing angles
        - Optional approximation to skip low-impact CP gates
    
        Barriers are added between each qubit's set of operations if `insert_barrier=True`.
        """
        for control_qubit in self._qubit_range():
            self.qft_circuit.h(control_qubit)  # Apply Hadamard gate to control qubit

            for target_qubit in self._target_range(control_qubit):
                distance = abs(control_qubit - target_qubit)
                if self._should_approximate(distance):
                    continue  # Skip gate if approximation threshold exceeded

                angle = pi / (2 ** distance)  # Calculate CP gate rotation angle
                if self.inverse:
                    angle = -angle  # Negate for inverse QFT
                    self.qft_circuit.cp(angle, target_qubit, control_qubit)
                else:
                    self.qft_circuit.cp(angle, control_qubit, target_qubit)

            self._add_barrier(self.qft_circuit)        

    def build(self):
        """
        Assemble and return the full Quantum Fourier Transform circuit.
    
        The build process follows these steps:
        1. Initialize the quantum circuit.
        2. Apply optional pre-swaps (only for inverse QFT with `do_swaps=True`).
        3. Apply the core QFT logic (Hadamard and controlled-phase gates).
        4. Apply optional post-swaps (only for forward QFT with `do_swaps=True`).
        5. Display the circuit diagram if `debug=True`.
    
        Returns
        -------
        QuantumCircuit
            The constructed (inverse) QFT circuit based on the configuration.
        """
        self._init_circuit()
        self._apply_pre_swaps()
        self._apply_core_transform()
        self._apply_post_swaps()
        self._debug_display(circuit=self.qft_circuit)

        return self.qft_circuit

class QFTGate:
    def __init__(
        self,
        qft_qubits: int,
        inverse: bool = False,
        do_swaps: bool = False,
        approximation_level: int = 0,
        label: str | None = None
    ):

        """
        Wrapper class for converting a QFT circuit into a reusable quantum gate.
    
        This class builds a Quantum Fourier Transform (QFT) or inverse QFT circuit using the `QFT`
        circuit class and converts it into a Qiskit `Gate` object. The resulting gate can be appended
        or composed into larger quantum circuits.
    
        Barriers and debug output are disabled internally to ensure gate compatibility.
    
        Parameters
        ----------
        qft_qubits : int
            Number of qubits the QFT will act on.
    
        inverse : bool, optional (default: False)
            If True, constructs the inverse QFT (QFT†).
    
        do_swaps : bool, optional (default: False)
            If True, includes swap operations to reverse qubit order.
    
        approximation_level : int, optional (default: 0)
            Number of smallest-angle controlled-phase gates to omit, allowing an approximate QFT.
    
        label : str, optional
            Optional name for the resulting gate.
        """

        self.qft = QFT(
            qft_qubits = qft_qubits,
            inverse = inverse,
            do_swaps = do_swaps,
            approximation_level = approximation_level,
            label = label,
            insert_barrier = False, # Barriers not allowed in gates
            debug = False
            
        )

    def build(self) -> Gate:
        """
        Build and return the QFT circuit as a reusable unitary gate.
    
        Internally builds the QFT circuit using the `QFT` class and converts it to a Qiskit `Gate`
        for composition into larger circuits. Barriers and debug rendering are suppressed automatically.
    
        Returns
        -------
        Gate
            A Qiskit Gate object representing the QFT or inverse QFT.
        """
        qft_circuit = self.qft.build()
        return qft_circuit.to_gate(label=self.qft.label)