from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeBrisbane
import numpy as np
import matplotlib.pyplot as plt

# Deutsch-Jozsa Algorithm Explanation:
# The Deutsch-Jozsa algorithm is one of the first quantum algorithms demonstrating an exponential speedup over classical algorithms.
# It determines whether a given function (oracle) is CONSTANT (same output for all inputs) or BALANCED (equal number of 0s and 1s as output).

# Constant Oracle Function
def constant_oracle(num_qubits, output=1):
    """
    Create a constant oracle circuit.
    The output is always 0 or 1, depending on the `output` parameter.
    CONSTANT means the output does not depend on the input.
    """
    ctrl_reg = QuantumRegister(num_qubits, 'Control')
    ancilla_reg = QuantumRegister(1, 'Ancilla')
    qc = QuantumCircuit(ctrl_reg, ancilla_reg)
    if output == 1:
        qc.x(num_qubits)  # Flip the ancilla qubit to represent a constant 1-output function.
    return qc

# Balanced Oracle Function
def balanced_oracle(num_qubits):
    """
    Create a balanced oracle circuit.
    BALANCED means the output is 0 for half the inputs and 1 for the other half.
    """
    ctrl_reg = QuantumRegister(num_qubits, 'Control')
    ancilla_reg = QuantumRegister(1, 'Ancilla')
    qc = QuantumCircuit(ctrl_reg, ancilla_reg)
    
    on_states = set(np.random.permutation(2**num_qubits)[:2**(num_qubits-1)])
    
    def add_cx(qc, bit_string):
        # Apply X gates based on the binary representation of the state.
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == '1':
                qc.x(qubit)
        return qc
    
    for state in on_states:
        qc.barrier()
        qc = add_cx(qc, f"{state:0{num_qubits}b}")
        qc.mcx(ctrl_reg, ancilla_reg[0])  # Apply a multi-controlled X gate.
        qc = add_cx(qc, f"{state:0{num_qubits}b}")
    
    qc.barrier()
    return qc

# Function to compile the Deutsch-Jozsa circuit
def compile_dj_circuit(num_qubits, oracle):
    """
    Prepare the Deutsch-Jozsa circuit.
    Step 1: Initialize the ancilla qubit to |1> and apply Hadamard gates.
    Step 2: Apply the oracle function.
    Step 3: Apply Hadamard gates again and measure the control qubits.
    """
    ctrl_reg = QuantumRegister(num_qubits, 'Control')
    ancilla_reg = QuantumRegister(1, 'Ancilla')
    classical_reg = ClassicalRegister(num_qubits, 'Result')
    qc = QuantumCircuit(ctrl_reg, ancilla_reg, classical_reg)
    
    qc.x(num_qubits)  # Initialize ancilla qubit to |1>
    qc.barrier()
    qc.h(range(num_qubits + 1))  # Apply Hadamard to all qubits.
    qc.barrier()
    qc.compose(oracle, inplace=True)  # Apply the oracle function.
    qc.barrier()
    qc.h(range(num_qubits))  # Apply Hadamard to control qubits.
    qc.measure(range(num_qubits), range(num_qubits))  # Measure control qubits.
    
    return qc

# Main function to run the Deutsch-Jozsa algorithm
def run_dj_algorithm(num_qubits, oracle_type=None, shots=1, optimization_level=1, use_real_qpu=False):
    """
    Run the Deutsch-Jozsa algorithm.
    """
    if oracle_type == 'constant':
        oracle = constant_oracle(num_qubits)
        oracle_label = 'constant'
    elif oracle_type == 'balanced':
        oracle = balanced_oracle(num_qubits)
        oracle_label = 'balanced'
    else:
        oracle_label = np.random.choice(['constant', 'balanced'])
        oracle = constant_oracle(num_qubits) if oracle_label == 'constant' else balanced_oracle(num_qubits)
    
    circuit = compile_dj_circuit(num_qubits, oracle)
    
    # Display the full circuit before results
    display(circuit.draw('mpl'))
    plt.show()
    
    print("Selected Oracle Type:", oracle_label)
    
    if use_real_qpu:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False)
    else:
        backend = FakeBrisbane()
    
    sampler = Sampler(backend=backend)
    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend)
    transpiled_circuit = pm.run(circuit)
    
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()
    counts = result[0].data.Result.get_counts()
    
    print("Measurement Results:", counts)
    if all(key == '0'*num_qubits for key in counts.keys()):
        print("The function is CONSTANT")
    else:
        print("The function is BALANCED")

# Run Example
run_dj_algorithm(3)
