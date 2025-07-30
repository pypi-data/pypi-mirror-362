
from qiskit.result import Result
from typing import List

class QVecOptResult:
    def __init__(self, data: dict, nqubits: int, job_id: str):
        if data is None:
            raise ValueError("Result data is None")
        self._data = data
        self._nqubits = nqubits
        self._job_id = job_id

    def get_counts(self):
        counts = {}
        for state, value in self._data.items():
            prob = value[0] ** 2 + value[1] ** 2
            bitstring = bin(int(state))[2:].zfill(29)
            counts[bitstring] = round(prob, 6)
        return counts
    
    def get_statevector(self) -> List[complex]:
        dim = 1 << self._nqubits  # 2^nqubits
        statevector = [0j] * dim  # 初始化为全零复数

        for state_str, [real, imag] in self._data.items():
            index = int(state_str)
            statevector[index] = complex(real, imag)

        return statevector

    def to_result(self):
        return Result.from_dict({
            'results': [{
                'success': True,
                'data': {'counts': self.get_counts()}
            }],
            'success': True,
            'backend_name': 'QVecOpt',
            'backend_version': '1.0.0',
            'job_id': self._job_id,
        })
