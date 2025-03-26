from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.primitives import Sampler
from fractions import Fraction
import math
import random
import logging

# Configure Logging
def configure_logging(verbose: bool = False):
    """
    Configure the logging level for Shor's Algorithm.
    Verbose mode enables detailed debug logs.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)
    qiskit_logger = logging.getLogger('qiskit')
    qiskit_logger.setLevel(logging.WARNING if not verbose else logging.DEBUG)
    return logging.getLogger(__name__)

class ShorAlgorithm:
    """
    Shor's Algorithm is a quantum algorithm used to factorize large integers efficiently.
    It leverages quantum phase estimation and modular exponentiation to find the period
    of a function, which is then used to determine the non-trivial factors of the number N.
    
    Steps of Shor's Algorithm:
    1. Choose a random base 'a' such that gcd(a, N) == 1.
    2. Build and initialize the quantum circuit.
    3. Precompute phase fractions for modular exponentiation.
    4. Apply quantum phase estimation.
    5. Perform repeated measurements and classical post-processing to find a factor.
    """
    def __init__(self, N: int, a: int = None, verbose: bool = False):
        """
        Initialize Shor's Algorithm with given N and optional a.
        N: Integer to factorize.
        a: Optional base for modular exponentiation.
        verbose: Enable verbose logging.
        """
        self.logger = configure_logging(verbose)
        self.N = N
        self.a = a if a else self.select_random_base(N)
        self.verbose = verbose
        self.circuit = None
        self.exponent_register = None
        self.result_register = None
        self.phase_fractions = None
        self.logger.info(f"Initialized Shor's Algorithm with N={N}, a={self.a}")
    
    def select_random_base(self, N: int) -> int:
        """
        Select a random base 'a' according to Shor's Algorithm requirements.
        Ensure gcd(a, N) == 1.
        This is crucial because if gcd(a, N) != 1, a factor is trivially found.
        """
        self.logger.info("Choosing a random base 'a'")
        while True:
            a = random.randint(2, N - 1)
            if math.gcd(a, N) == 1:
                self.logger.info(f"Chosen random base a: {a}")
                return a
    
    def initialize_circuit(self):
        """
        Build and initialize the quantum circuit for Shor's Algorithm.
        - Exponent register: Controls the modular exponentiation.
        - Modulo register: Stores the results of modular exponentiation.
        - Result register: Stores the measured output from phase estimation.
        """
        self.logger.info("Building quantum circuit")
        num_exponent_qubits = 2 * math.ceil(math.log2(self.N))
        num_modulo_qubits = math.ceil(math.log2(self.N))
        num_result_bits = num_exponent_qubits

        self.exponent_register = QuantumRegister(num_exponent_qubits, 'Exponent')
        modulo_register = QuantumRegister(num_modulo_qubits, 'Modulo')
        self.result_register = ClassicalRegister(num_result_bits, 'Result')
        
        self.circuit = QuantumCircuit(self.exponent_register, modulo_register, self.result_register)
        self.circuit.h(self.exponent_register)
        self.circuit.x(modulo_register[0])
        self.circuit.barrier()
        self.logger.info("Quantum circuit initialized")
    
    def precompute_phase_fractions(self):
        """
        Precompute phase fractions for modular exponentiation.
        These phase fractions represent the results of modular exponentiation for each exponent qubit.
        They are critical for accurate phase estimation.
        """
        self.logger.info("Calculating phase fractions")
        self.phase_fractions = {}
        for x in range(len(self.exponent_register)):
            mod_exp_result = pow(self.a, 2**x, self.N)
            self.phase_fractions[x] = Fraction(mod_exp_result, 2**len(self.exponent_register))
        self.logger.info("Phase fractions calculated")
    
    def phase_estimation(self):
        """
        Apply phase estimation logic to the quantum circuit.
        Phase estimation determines the period of the modular exponentiation function,
        which is used to find a factor of N.
        """
        self.logger.info("Running phase estimation")
        for index, angle in self.phase_fractions.items():
            for _ in range(2 ** index):
                gate = self.c_amodN(angle, self.exponent_register[index])
                self.circuit.append(gate, [self.exponent_register[index]] + self.circuit.qregs[1][:])
        self.circuit.barrier()
        self.circuit.compose(self.QFT(len(self.exponent_register), inverse=True), qubits=self.exponent_register, inplace=True)
        self.circuit.measure(self.exponent_register, self.result_register)
        self.logger.info("Phase estimation completed")
    
    def c_amodN(self, psi: float, control_qubit: int) -> Gate:
        """
        Create a controlled 'a mod N' gate.
        This gate applies a phase shift based on psi, which represents the phase fraction.
        """
        angle_theta = 2 * math.pi * psi
        amodN_gate = QuantumCircuit(len(self.circuit.qregs[1]))
        for i in range(len(self.circuit.qregs[1])):
            amodN_gate.p(angle_theta, i)
        return amodN_gate.to_gate(label='a mod N').control(1)
    
    def QFT(self, qft_qubits: int, inverse: bool = False) -> Gate:
        """
        Create a Quantum Fourier Transform (QFT) gate.
        The QFT is used in phase estimation to extract the period of the modular function.
        If inverse=True, creates an Inverse QFT.
        """
        self.logger.info(f"Creating {'Inverse ' if inverse else ''}QFT gate")
        qft_register = QuantumRegister(qft_qubits)
        qft_circuit = QuantumCircuit(qft_register)
        
        for i in range(qft_qubits):
            qft_circuit.h(i)
            for j in range(i + 1, qft_qubits):
                angle = math.pi / (2 ** (j - i))
                qft_circuit.cp(-angle if inverse else angle, j, i)
        
        self.logger.info("QFT gate ready")
        return qft_circuit.to_gate(label='QFT⁻¹' if inverse else 'QFT')
    
    def attempt(self):
        """
        Perform measurement and calculate factor.
        The measured phase is converted into a fraction, and its denominator is used
        to compute a potential factor of N.
        """
        self.logger.info("Performing measurement")
        sampler = Sampler()
        measurement = sampler.run(self.circuit, shots=1).result().quasi_dists[0].popitem()[0]
        phase = Fraction(measurement, 2**len(self.exponent_register))
        frac = phase.limit_denominator(self.N)
        r = frac.denominator
        return math.gcd(self.a ** (r // 2) - 1, self.N)
    
    def run(self, attempts=10):
        """
        Run the full Shor's Algorithm.
        """
        self.initialize_circuit()
        self.precompute_phase_fractions()
        self.phase_estimation()
        for attempt in range(attempts):
            self.logger.info(f"Attempt {attempt+1}")
            factor = self.attempt()
            if factor not in [1, self.N] and self.N % factor == 0:
                result = f"Factor Found: {factor}"
                print(result)
                return factor
        self.logger.warning("No valid factors found after all attempts.")
        return None


# Example usage
# result = ShorAlgorithm(N=21).run(attempts=5)
