Shor's Algorithm is a quantum algorithm used to factorize large integers efficiently.
It leverages quantum phase estimation and modular exponentiation to find the period
of a function, which is then used to determine the non-trivial factors of the number N.

Steps of Shor's Algorithm:
1. Choose a random base 'a' such that gcd(a, N) == 1.
2. Build and initialize the quantum circuit.
3. Precompute phase fractions for modular exponentiation.
4. Apply quantum phase estimation.
5. Perform repeated measurements and classical post-processing to find a factor of N.

Example usage:

result = ShorAlgorithm(N=21, a=17).run(attempts=5)

  N : Number to be factored
  
  a : is base for modular exponentiation. Default - chosen on random.
  
  attempts : number of measurement attempts to find factor. Default - 10

NOTE: This version is currently only simulated and does not run on actual quantum hardware.
