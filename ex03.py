from qiskit_ibm_runtime import QiskitRuntimeService
from dotenv import load_dotenv
import os
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import SamplerV2 as Sampler
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import time

load_dotenv()

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()
service = QiskitRuntimeService('ibm_quantum', os.getenv('API_KEY'))
backend = service.least_busy(operational=True, simulator=False)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)
sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1000)
start = time.time()
print(f">>> Job ID: {job.job_id()}")
while job.status() == "RUNNING":
    print(f"Been {time.time() - start:.2f}: Job {job.job_id()} is {job.status()}")
    time.sleep(5)
res = job.result()
pub_result = res[0].data.meas.get_counts()
figure = plot_histogram(pub_result)
 
try:
    plt.savefig('assets/result_real.png')
except Exception as e:
    print(f"Error saving visualization: {e}")
finally:
    plt.close()