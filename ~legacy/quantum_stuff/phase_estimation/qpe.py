from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import pi

# Function to create the Quantum Fourier Transform (QFT) circuit
def QFT(num_qubits: int):
    # Initialize a quantum register and circuit for QFT
    q_register = QuantumRegister(num_qubits)
    circuit = QuantumCircuit(q_register)

    # Step 1: Apply SWAP gates to reverse qubit order
    # QFT outputs results in reverse order, so we swap the first half with the last half
    for i in range(num_qubits // 2):
        circuit.swap(i, num_qubits - i - 1)

    # Add a barrier for readability, to separate stages in the circuit
    circuit.barrier()

    # Step 2: Apply Hadamard and controlled phase rotations
    # For each qubit i, apply a Hadamard gate, then apply decreasing controlled phase rotations
    for i in range(num_qubits):
        circuit.h(i)  # Apply Hadamard to start the QFT
        # Apply controlled phase rotations with angles decreasing by powers of 2
        for j in range(i + 1, num_qubits):
            circuit.cp(pi / (2 ** (j - i)), i, j)  # Controlled phase shift by pi/2^(j-i)
        # Barrier for visual clarity
        circuit.barrier()

    # Return the QFT circuit, which can be composed with the main QPE circuit
    return circuit

# Quantum Phase Estimation (QPE) function
def QPE(num_qubits: int, theta: float):
    # Initialize quantum and classical registers
    control_register = QuantumRegister(num_qubits, 'qubit')  # Control qubits for precision
    phase_register = QuantumRegister(1, 'psi')  # Eigenstate register with 1 qubit for |ψ⟩
    classic_register = ClassicalRegister(num_qubits)  # Classical register for measurement
    circuit = QuantumCircuit(control_register, phase_register, classic_register)

    # Step 1: Prepare the eigenstate |ψ⟩ = |1⟩
    # Set the eigenstate register to |1⟩ by applying an X gate
    circuit.x(phase_register[0])
    circuit.barrier()

    # Step 2: Apply Hadamard gates to the control register
    # This puts the control register qubits into a superposition, enabling phase estimation
    for i in range(num_qubits):
        circuit.h(control_register[i]) 
    circuit.barrier()

    # Step 3: Apply controlled powers of the unitary U
    # Each qubit in the control register applies U^(2^n) to the eigenstate |ψ⟩
    # U is represented here as a phase rotation by theta with increasing powers
    for n in range(num_qubits):
        circuit.cp(2 * pi * theta * (2 ** n), control_register[n], phase_register[0])
    circuit.barrier()

    # Step 4: Apply the inverse QFT to the control register
    # Use the QFT function to create an inverse QFT circuit and compose it on control_register
    qft_circuit = QFT(num_qubits)
    circuit.compose(qft_circuit, qubits=control_register[:], inplace=True)

    # (Optional) Measure the control register
    # This measurement would allow testing in a simulator to check if the phase is estimated correctly
    # Uncomment the line below if you wish to use this for simulation
    # circuit.measure(control_register, classic_register)

    # Return the complete QPE circuit
    return circuit

# Example usage: Create a QPE circuit for a 7-qubit control register with theta = 1/5
qpe_circuit = QPE(7, 1/5)

# Display the QPE circuit diagram
display(qpe_circuit.draw('mpl'))
