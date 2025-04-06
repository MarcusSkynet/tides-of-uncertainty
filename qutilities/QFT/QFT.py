from qiskit import QuantumCircuit
from math import pi

class QFT:
    def __init__(
        self,
        num_qubits: int,
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
        if num_qubits is None or num_qubits < 1:
            raise ValueError("Number of qubits must be a positive integer.")

        if label is None:
            label = f"QFT ({num_qubits})" if not inverse else f"QFT† ({num_qubits})"

        self.num_qubits = num_qubits
        self.inverse = inverse
        self.do_swaps = do_swaps
        self.approximation_level = approximation_level
        self.debug = debug
        self.insert_barrier = insert_barrier
        self.label = label

    def _qubit_range(self):
        # Determines the processing order of qubits. For inverse QFT, we apply gates from lowest to highest index.
        # For forward QFT, the order is reversed (highest to lowest index), matching standard QFT gate application order.
        return list(range(self.num_qubits)) if self.inverse else list(reversed(range(self.num_qubits)))

    def _target_range(self, control_qubit):
        # Returns the list of target qubits for a given control qubit.
        # In the forward QFT, targets are lower-indexed qubits.
        # In the inverse QFT, targets are higher-indexed qubits.
        return (
            list(range(control_qubit + 1, self.num_qubits))
            if self.inverse else list(range(control_qubit - 1, -1, -1))
        )

    def _should_approximate(self, distance: int) -> bool:
        # Determines whether a controlled-phase gate should be skipped due to approximation.
        # If the gate acts between distant qubits (i.e., distance > cutoff), it is skipped.
        # This reduces gate count and depth for near-term quantum devices.
        cutoff = self.num_qubits - 1 - self.approximation_level
        return distance > cutoff

    def _swap_pairs(self) -> list[tuple[int, int]]:
        # Generates a list of symmetric qubit pairs to swap.
        # This is used to reverse qubit order which is necessary
        # because the QFT naturally outputs in reverse bit order.
        return [(i, self.num_qubits - i - 1) for i in range(self.num_qubits // 2)]

    def _add_barrier(self, circuit):
        # Adds a barrier after each major step if enabled.
        # Barriers help visually separate logical steps in the circuit for debugging and clarity.
        if self.insert_barrier:
            circuit.barrier()

    def _debug_display(self, circuit):
        # Displays the circuit using matplotlib if debug mode is enabled.
        # This is useful for visually verifying circuit structure during development.
        if self.debug:
            display(circuit.draw('mpl'))

    def _init_circuit(self):
        # Initializes and returns a QuantumCircuit with the correct number of qubits.
        return QuantumCircuit(self.num_qubits)

    def build(self, as_gate: bool = True):
        """
        Constructs the (approximate) QFT or inverse QFT circuit.

        Parameters:
        - as_gate (bool): If True, return the circuit as a Qiskit Gate for reuse and composition.
                          If False, return a QuantumCircuit instance instead.

        Returns:
        - Gate or QuantumCircuit: The constructed QFT or inverse QFT as per the configuration.

        The build process includes optional pre-swaps (for inverse), main QFT logic with controlled-phase gates,
        optional post-swaps (for forward QFT), optional barriers for visualization, and debug rendering.
        """
        circuit = self._init_circuit()

        # Apply pre-swaps before inverse QFT to reverse output order
        if self.inverse and self.do_swaps:
            for q1, q2 in self._swap_pairs():
                circuit.swap(q1, q2)
            self._add_barrier(circuit)

        # Apply the QFT gate sequence
        for control_qubit in self._qubit_range():
            circuit.h(control_qubit)  # Apply Hadamard gate to control qubit

            for target_qubit in self._target_range(control_qubit):
                distance = abs(control_qubit - target_qubit)
                if self._should_approximate(distance):
                    continue  # Skip gate if approximation threshold exceeded

                angle = pi / (2 ** distance)  # Calculate CP gate rotation angle
                if self.inverse:
                    angle = -angle  # Negate for inverse QFT
                    circuit.cp(angle, target_qubit, control_qubit)
                else:
                    circuit.cp(angle, control_qubit, target_qubit)

            self._add_barrier(circuit)

        # Apply post-swaps for forward QFT to reverse output order
        if not self.inverse and self.do_swaps:
            for q1, q2 in self._swap_pairs():
                circuit.swap(q1, q2)

        self._debug_display(circuit)

        # Clean up barriers before returning as gate, if required
        if self.insert_barrier:
            clean_circuit = QuantumCircuit(self.num_qubits)
            for instr in circuit.data:
                if instr.operation.name != "barrier":
                    clean_circuit.append(instr.operation, instr.qubits, instr.clbits)
            circuit = clean_circuit

        return circuit.to_gate(label=self.label) if as_gate else circuit
