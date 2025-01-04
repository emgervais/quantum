from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

def add_cx(qc, bit_string):
    for qubit, bit in enumerate(reversed(bit_string)):
        if bit == "1":
            qc.x(qubit)
    return qc

def create_oracle(type):
    oracle = QuantumCircuit(3 + 1)
    if type == 'constant':
        if 1 == np.random.randint(2):
            oracle.x(3)
    if type == 'balanced':
        on_states = np.random.choice(
        range(2**3),
        2**3 // 2,
        replace=False,
    )
        for state in on_states:
            oracle.barrier()
            oracle = add_cx(oracle, f"{state:0b}")
            oracle.mcx(list(range(3)), 3)
            oracle = add_cx(oracle, f"{state:0b}")
    oracle.name = f"{type}"
    oracle.draw(output='mpl')
    plt.savefig('assets/oracle.png')
    return oracle

circuit = QuantumCircuit(4, 3)
circuit.x(3)
circuit.h(range(4))
circuit.append(create_oracle('constant'), range(4))
circuit.h(range(3))
circuit.measure(range(3), range(3))
circuit.draw(output='mpl')
plt.savefig('assets/Deutsch-Jozsa.png')
 
result_ideal = AerSimulator().run([transpile(circuit, AerSimulator())], shots=500, memory=True).result()
res = result_ideal.get_memory()[0]
print(res)
if "1" in res:
    print("balanced")
else:
    print("constant") 
try:
    plt.savefig('assets/result_Deutsch-Jozsa.png')
except Exception as e:
    print(f"Error saving visualization: {e}")
finally:
    plt.close()