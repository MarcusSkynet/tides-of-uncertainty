from qiskit import QuantumCircuit, QuantumRegister
from numpy import pi

def QFT(qft_qubits: int, inverse: bool = False, do_swaps: bool = False, debug: bool = False):
    """
    Implements the Quantum Fourier Transform (QFT) or its inverse (QFT⁻¹) on a given number of qubits.

    Parameters:
    -----------
    qft_qubits : int
        The number of qubits in the QFT circuit.
    inversed : bool, optional (default=False)
        If True, implements the Inverse Quantum Fourier Transform (QFT⁻¹).
    do_swaps : bool, optional (default=False)
        If True, applies final swap operations to match standard QFT output ordering.
    debug : bool, optional (default=False)
        If True, displays the circuit for visual analysis.

    Returns:
    --------
    qiskit.circuit.Instruction
        A gate representation of the (inverse) QFT circuit.

    Notes:
    ------
    - The QFT applies Hadamard and controlled phase shifts to transform the input basis states.
    - The inverse QFT negates the angles in the controlled phase gates.
    - The final swap operations (optional) reorder the qubits for standard QFT output format.
    - If `debug=True`, the circuit will be displayed using text-based visualization.
    """
    
    # Create a quantum register and quantum circuit
    qft_register = QuantumRegister(qft_qubits)
    qft_circuit = QuantumCircuit(qft_register)
    
    # If performing the inverse QFT, apply swaps at the beginning
    if do_swaps and inverse:
        for i in range(qft_qubits // 2):
            qft_circuit.swap(i, qft_qubits - i - 1)
    
    # Determine the order of applying operations (standard vs inverse QFT)
    qubit_range = reversed(range(qft_qubits)) if not inverse else range(qft_qubits)

    for i in qubit_range:
        # Apply Hadamard gate to create superposition
        qft_circuit.h(i)

        # Determine phase shift direction
        target_range = range(i-1, -1, -1) if not inverse else range(i+1, qft_qubits)

        for j in target_range:
            # Compute controlled-phase shift angle
            angle = pi / (2 ** (i - j)) if not inverse else -pi / (2 ** (i - j))
            
            # Apply controlled phase rotation
            qft_circuit.cp(angle, j, i)  # Ensure correct control-target order
    
    # If performing the forward QFT, apply swaps at the end
    if do_swaps and not inverse:
        for i in range(qft_qubits // 2):
            qft_circuit.swap(i, qft_qubits - i - 1)
    
    # Assign a description label
    label = f"QFT ({qft_qubits})" if not inverse else f"QFT⁻¹ ({qft_qubits})"
    
    # If debugging, display the circuit
    if debug:
        display(qft_circuit.draw('mpl'))
    
    return qft_circuit.to_gate(label=label)