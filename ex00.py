from qiskit_ibm_runtime import QiskitRuntimeService
from dotenv import load_dotenv
import os

load_dotenv()

service = QiskitRuntimeService('ibm_quantum', os.getenv('API_KEY'))
backends = service.backends()

print("\n=== Available Quantum Simulators ===")
for backend in backends:
    if backend.simulator:
        print(f"\nSimulator: {backend.name}")
        print(f"Status: {backend.status().status_msg}")
        print(f"Queue Length: {backend.status().pending_jobs}")

print("\n=== Available Quantum Computers ===")
for backend in backends:
    if not backend.simulator:
        print(f"\nQuantum Computer: {backend.name}")
        print(f"Number of Qubits: {backend.num_qubits}")
        print(f"Status: {backend.status().status_msg}")
        print(f"Queue Length: {backend.status().pending_jobs}")