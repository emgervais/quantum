from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt

def create_diffuser(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    return qc

def oracle3(num_qubits):
    oracle = QuantumCircuit(num_qubits)
    oracle.x([0, 2])
    oracle.h(2)
    oracle.ccx(0, 1, 2)
    oracle.h(2)
    oracle.x([0, 2])
    return oracle

def oracle4(num_qubits):
    oracle = QuantumCircuit(num_qubits)
    oracle.x([1, 3])
    oracle.h(3)
    oracle.mcx([0, 1, 2], 3)
    oracle.h(3)
    oracle.x([1, 3])
    return oracle

def grovers_algorithm(num_qubits, oracle):
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))

    num_iterations = int(np.floor(np.pi / 4 * np.sqrt(2**num_qubits)))

    for _ in range(num_iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(create_diffuser(num_qubits), inplace=True)

    qc.measure_all()
    return qc

num_qubits = 4
oracle = oracle4(num_qubits)
qc = grovers_algorithm(num_qubits, oracle)
result = AerSimulator().run([transpile(qc, AerSimulator())], shots=1024).result()
counts = result.get_counts()
print(counts)

