from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeBrisbane
from math import pi
import matplotlib.pyplot as plt

# Function to define the Deutsch function as a 2-qubit circuit
def deutsch_function(case: int):
    """
    Generate a 2-qubit Deutsch function circuit based on the selected case.
    """
    if case not in [1, 2, 3, 4]:
        raise ValueError('"case" must be 1, 2, 3, or 4.')

    function = QuantumCircuit(2)  # Initialize a 2-qubit circuit for the function
    
    # Case definitions:
    # case 1: Identity (constant)
    # case 2: CNOT (balanced)
    # case 3: CNOT + NOT (balanced)
    # case 4: NOT (constant)
    if case in [2, 3]:
        function.cx(0, 1)  # Apply CNOT for balanced function cases
    if case in [3, 4]:
        function.x(1)  # Apply X gate for case 3 (balanced) and case 4 (constant)
    
    return function

# Visualize all 4 possible Deutsch function circuits
fig, axes = plt.subplots(1, 4, figsize=(10, 2))
for i, ax in enumerate(axes):
    deutsch_function(i+1).draw('mpl', ax=ax)
plt.tight_layout()
plt.show()

# Compile the Deutsch circuit based on the given Deutsch function
def compile_circuit(function: QuantumCircuit):
    """
    Prepare the circuit for Deutsch's algorithm using the provided function.
    """
    num_qubits = function.num_qubits - 1  # Number of qubits in control
    circuit = QuantumCircuit(num_qubits + 1, num_qubits)  # Add auxiliary qubit

    # Step 1: Initialize auxiliary qubit to |1⟩ for phase kickback
    circuit.x(num_qubits)
    circuit.barrier()

    # Step 2: Apply Hadamard gates to create superposition
    circuit.h(range(num_qubits + 1))
    circuit.barrier()

    # Step 3: Insert the Deutsch function
    circuit.compose(function, inplace=True)  # Adds function as a subroutine
    circuit.barrier()

    # Step 4: Apply Hadamard to control qubits
    circuit.h(range(num_qubits))
    circuit.measure(range(num_qubits), range(num_qubits))  # Measure result

    return circuit

# Display the compiled circuit for a sample function
display(compile_circuit(deutsch_function(2)).draw('mpl'))

# Function to run Deutsch's algorithm and determine function type (constant or balanced)
def deutsch_algorithm(function: QuantumCircuit, shots=1, optimization_level=2, use_real_qpu=False):
    """
    Determine if a given Deutsch function is constant or balanced using quantum execution.
    """
    # Prepare the Deutsch circuit
    circuit = compile_circuit(function)

    # Select backend: real QPU or simulator
    if use_real_qpu:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False)
    else:
        backend = FakeBrisbane()  # Default simulator backend if QPU not selected

    # Initialize the Sampler for job execution
    sampler = Sampler(backend=backend)

    # Transpile the circuit using the preset pass manager
    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend)
    transpiled_circuit = pm.run(circuit)

    # Execute the circuit and print job details
    job = sampler.run([transpiled_circuit], shots=shots)
    print(f">>> Job ID: {job.job_id()}")
    print(f">>> Job Status: {job.status()}")

    result = job.result()
    counts = result[0].data.c.get_counts()

    # Determine if function is constant or balanced based on measurement outcome
    if "0" in counts and counts["0"] > counts.get("1", 0):
        return "constant"
    return "balanced"

# Test with case 3 function (balanced)
function = deutsch_function(3)
display(function.draw('mpl'))
display(deutsch_algorithm(function))
