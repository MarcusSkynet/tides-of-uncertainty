def QFT(qft_qubits: int, inversed: bool = False, do_swaps: bool = False):

    qft_register = QuantumRegister(qft_qubits)
    qft_circuit = QuantumCircuit(qft_register)

    qubit_range = reversed(range(qft_qubits)) if not inversed else range(qft_qubits)
    for i in qubit_range:
        qft_circuit.h(i)
        target_range = range(i-1, -1, -1) if not inversed else range(i+1, qft_qubits)

        for j in target_range:
            angle = pi / (2 ** abs(j-i)) if not inversed else -pi / (2 ** abs(j-i))
            
            qft_circuit.cp(angle, i, j)
    if do_swaps:
        for i in range(qft_qubits // 2):
            qft_circuit.swap(i, qft_qubits - i -1) 

    label = f"QFT ({qft_qubits})" if not inversed else f"QFT⁻¹ ({qft_qubits})"

    return qft_circuit.to_gate(label=label)
    
    display(qft_circuit.draw('mpl'))