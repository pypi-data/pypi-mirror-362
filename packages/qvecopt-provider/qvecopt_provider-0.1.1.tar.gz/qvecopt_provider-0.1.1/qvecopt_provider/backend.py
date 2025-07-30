
import json
import requests
from qiskit import transpile
from qiskit.providers import BackendV2, Options
from qiskit.transpiler import Target
from qiskit.transpiler import InstructionProperties
from qiskit.transpiler import Layout
from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate, HGate, SGate, SdgGate, TGate, TdgGate, RXGate, RYGate, RZGate, U1Gate, U2Gate, U3Gate, CXGate, CYGate, CZGate, SwapGate
from .job import QVecOptJob

class QVecOptBackend(BackendV2):
    def __init__(self, url, provider=None):
        self._options = Options()  # 一定要先定义
        super().__init__(provider=provider, name="QVecOpt")
        self._target = self._build_target()
        self._url = url

    @property
    def max_circuits(self):
        return 1
    
    def _default_options(self):
        return self._options

    @property
    def target(self):
        return self._target

    def _build_target(self):
        n_qubits = 29
        target = Target(num_qubits=n_qubits)

        target.add_instruction(XGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="x")
        target.add_instruction(YGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="y")
        target.add_instruction(ZGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="z")
        target.add_instruction(HGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="h")
        target.add_instruction(SGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="s")
        target.add_instruction(SdgGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="sdg")
        target.add_instruction(TGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="t")
        target.add_instruction(TdgGate(), {(q,): InstructionProperties() for q in range(n_qubits)}, name="tdg")
        target.add_instruction(RXGate(0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="rx")
        target.add_instruction(RYGate(0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="ry")
        target.add_instruction(RZGate(0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="rz")
        target.add_instruction(U1Gate(0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="u1")
        target.add_instruction(U2Gate(0.0, 0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="u2")
        target.add_instruction(U3Gate(0.0, 0.0, 0.0), {(q,): InstructionProperties() for q in range(n_qubits)}, name="u3")

        cx_qargs = {
            (q1, q2): InstructionProperties()
            for q1 in range(n_qubits)
            for q2 in range(n_qubits)
            if q1 != q2
        }
        target.add_instruction(CXGate(), cx_qargs, name="cx")
        target.add_instruction(CYGate(), cx_qargs, name="cy")
        target.add_instruction(CZGate(), cx_qargs, name="cz")
        target.add_instruction(SwapGate(), cx_qargs, name="swap")
        
        return target

    def run(self, run_input, **kwargs):
        # Extract parameters
        initial_state = kwargs.get("initial_state", 0)
        wipedisk = kwargs.get("wipedisk", True)
        circuit = run_input

        # Build gate list
        gates = []
        for instr, qargs, _ in circuit.data:
            gates.append({
                "name": instr.name,
                "qubits": [qubit._index for qubit in qargs],
                "params": [float(p) for p in instr.params]
            })

        payload = {
            "nqubits": circuit.num_qubits,
            "initial_state": initial_state,
            "gates": gates
        }

        response = requests.post(
            f"{ self._url }/initialize?wipedisk={'true' if wipedisk else 'false'}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=None
        )
        job_id = response.json()["data"]["id"]
        return QVecOptJob(self, job_id, circuit.num_qubits, self._url)
    
    def transpile(self, qc, optimization_level=1):
        """将量子线路编译为目标 backend 支持的门集，且保持逻辑 qubit 编号不变。"""
        qr = qc.qregs[0]
        initial_layout = Layout({qr[i]: i for i in range(qc.num_qubits)})

        compiled = transpile(
            qc,
            backend=self,
            initial_layout=initial_layout,
            optimization_level=optimization_level
        )
        return compiled