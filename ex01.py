from qiskit.visualization import plot_histogram
from qiskit_aer.primitives import SamplerV2
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

circuit = QuantumCircuit(1)
circuit.h(0)
circuit.measure_all()
 
result_ideal = SamplerV2().run([circuit], shots=500).result()
res = result_ideal[0].data.meas.get_counts()
for key in res:
    res[key] = res[key] / 500
print(res)
figure = plot_histogram(res)
try:
    plt.savefig('assets/quantum_circuit.png')
    print("Circuit visualization saved to quantum_circuit.png")
except Exception as e:
    print(f"Error saving visualization: {e}")
finally:
    plt.close()