from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

def build_pump_quantum_circuit(S1, S2, S3, S4, S5, S6):
    """
    Build quantum circuit for pump monitoring system.
    
    Qubits:
      q[0..5]  : S1..S6 (sensor inputs)
      q[6]     : S5' (normalized S5)
      q[7]     : S6' (normalized S6)
      q[8..11] : ancilla for multi-input AND (A1 computation)
      q[12]    : A1 (relay output)
      q[13]    : A5 (alarm output)
    
    Classical bits:
      c[0]     : measurement of A1
      c[1]     : measurement of A5
    """
    qc = QuantumCircuit(14, 2)
    
    # === STEP 1: Encode input basis state |S1 S2 S3 S4 S5 S6⟩ ===
    if S1: qc.x(0)
    if S2: qc.x(1)
    if S3: qc.x(2)
    if S4: qc.x(3)
    if S5: qc.x(4)
    if S6: qc.x(5)
    
    qc.barrier()
    
    # === STEP 2: Normalize S5 and S6 ===
    # |S5'⟩ = X|S5⟩  (so S5=0 safe becomes |1⟩)
    # |S6'⟩ = X|S6⟩  (so S6=0 safe becomes |1⟩)
    qc.cx(4, 6)  # Copy S5 to q6
    qc.x(6)      # Invert to get S5'
    
    qc.cx(5, 7)  # Copy S6 to q7
    qc.x(7)      # Invert to get S6'
    
    qc.barrier()
    
    # === STEP 3: Compute A1 = S1 & S2 & S3 & S4 & S5' & S6' ===
    # Use cascaded Toffoli (CCNOT) gates with ancilla qubits
    
    # First level: t1 = S1 & S2
    qc.ccx(0, 1, 8)
    
    # Second level: t2 = t1 & S3
    qc.ccx(8, 2, 9)
    
    # Third level: t3 = t2 & S4
    qc.ccx(9, 3, 10)
    
    # Fourth level: t4 = t3 & S5'
    qc.ccx(10, 6, 11)
    
    # Final: A1 = t4 & S6'
    qc.ccx(11, 7, 12)
    
    qc.barrier()
    
    # === STEP 4: Compute A5 = ~S2 | ~S3 | ~S4 | S5 | S6 ===
    # Using X + CNOT pattern for OR logic
    
    # ~S2: if S2=0, set A5=1
    qc.x(1)
    qc.cx(1, 13)
    qc.x(1)
    
    # ~S3: if S3=0, set A5=1
    qc.x(2)
    qc.cx(2, 13)
    qc.x(2)
    
    # ~S4: if S4=0, set A5=1
    qc.x(3)
    qc.cx(3, 13)
    qc.x(3)
    
    # S5: if S5=1, set A5=1
    qc.cx(4, 13)
    
    # S6: if S6=1, set A5=1
    qc.cx(5, 13)
    
    qc.barrier()
    
    # === STEP 5: Measure A1 and A5 ===
    qc.measure(12, 0)  # A1 → c[0]
    qc.measure(13, 1)  # A5 → c[1]
    
    return qc


def simulate_all_scenarios():
    """
    Simulate all 7 scenarios from truth table and compare with expected outputs.
    """
    scenarios = [
        ("Normal Operation",      1,1,1,1,0,0,  1,0),
        ("Low Pressure",          1,0,1,1,0,0,  0,1),
        ("Low Level",             1,1,0,1,0,0,  0,1),
        ("No Flow",               1,1,1,0,0,0,  0,1),
        ("Overheat",              1,1,1,1,1,0,  0,1),
        ("Abnormal Vibration",    1,1,1,1,0,1,  0,1),
        ("Shutdown/OFF",          0,1,1,1,0,0,  0,1),
    ]
    
    # Use AerSimulator (new API)
    simulator = AerSimulator()
    
    print("=" * 80)
    print("QUANTUM SIMULATION RESULTS - Industrial Pump Monitoring System")
    print("=" * 80)
    print(f"{'Scenario':<25} {'S1 S2 S3 S4 S5 S6':<20} {'A1 A5':<10} {'Expected':<10} {'Status'}")
    print("-" * 80)
    
    for scenario in scenarios:
        name = scenario[0]
        S1, S2, S3, S4, S5, S6 = scenario[1:7]
        expected_A1, expected_A5 = scenario[7:9]
        
        # Build circuit
        qc = build_pump_quantum_circuit(S1, S2, S3, S4, S5, S6)
        
        # Transpile and run (new Qiskit 1.x API)
        qc_transpiled = qc
        result = simulator.run(qc_transpiled, shots=1024).result()
        counts = result.get_counts()
        
        # Get most frequent measurement
        measured_bitstring = max(counts, key=counts.get)
        # Bitstring format: 'A5 A1' (reversed order in Qiskit)
        measured_A5 = int(measured_bitstring[0])
        measured_A1 = int(measured_bitstring[1])
        
        # Check correctness
        status = "✓ PASS" if (measured_A1 == expected_A1 and measured_A5 == expected_A5) else "✗ FAIL"
        
        print(f"{name:<25} {S1} {S2} {S3} {S4} {S5} {S6}           "
              f"{measured_A1} {measured_A5}        {expected_A1} {expected_A5}        {status}")
    
    print("=" * 80)


def draw_circuit_schematic():
    """
    Generate and save quantum circuit schematic for paper.
    """
    # Example: Normal operation scenario
    qc = build_pump_quantum_circuit(1, 1, 1, 1, 0, 0)
    
    # Draw circuit (ASCII)
    print("\n=== Quantum Circuit Schematic ===\n")
    print(qc)
    
    # Save high-resolution image for IEEE paper
    try:
        fig = circuit_drawer(qc, output='mpl', style={'backgroundcolor': '#FFFFFF'})
        plt.savefig('pump_quantum_circuit_schematic.png', dpi=300, bbox_inches='tight')
        print("\n✓ Circuit schematic saved as 'pump_quantum_circuit_schematic.png'")
    except Exception as e:
        print(f"\nWarning: Could not save circuit image: {e}")
        print("Install matplotlib if needed: pip install matplotlib")


if __name__ == "__main__":
    # Run simulation for all 7 scenarios
    simulate_all_scenarios()
    
    # Generate circuit schematic for paper
    draw_circuit_schematic()
