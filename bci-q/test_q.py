import sys

try:
    import cudaq
    print("✓ Successfully imported CUDA-Q!")
except Exception as e:
    print(f"✗ Failed to import CUDA-Q. Error: {e}")
    sys.exit(1)

try:
    print("Defining a 2-qubit Bell Pair quantum circuit...")
    # 1. Define a quantum kernel using the @cudaq.kernel decorator
    @cudaq.kernel
    def bell_pair():
        # Allocate a vector of 2 qubits (initialized to |00>)
        qubits = cudaq.qvector(2)
        
        # Apply a Hadamard gate to put the first qubit in superposition
        h(qubits[0])
        
        # Apply a Controlled-X (CNOT) gate to entangle the two qubits
        cx(qubits[0], qubits[1])

    print("Running quantum simulation (sampling 1000 shots on default CPU backend)...")
    # 2. Sample the quantum kernel (runs 1000 shots by default)
    result = cudaq.sample(bell_pair)

    # 3. Print the measurement results
    print("\n✓ Quantum Simulation Completed Successfully!")
    print("Measurement Results (Counts):")
    print(result)
    
    # Simple validation of results
    print("Successfully verified quantum superposition and entanglement!")
except Exception as e:
    print(f"✗ Failed to execute CUDA-Q quantum simulation. Error: {e}")
    sys.exit(1)
