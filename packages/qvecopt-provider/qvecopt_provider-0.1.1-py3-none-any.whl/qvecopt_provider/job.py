
import time
import requests
from qiskit.providers import JobV1
from qiskit.providers.jobstatus import JobStatus
from .result import QVecOptResult

class QVecOptJob(JobV1):
    def __init__(self, backend, job_id, nqubits, url):
        super().__init__(backend, job_id)
        self._backend = backend
        self._job_id = job_id
        self._nqubits = nqubits
        self._status = JobStatus.INITIALIZING
        self._result = None
        self._url = url
        # 你自己的初始化，比如调用模拟器后端的接口获取job_id

    def job_id(self):
        return self._job_id

    def submit(self):
        # 提交作业的具体逻辑，比如发送HTTP请求等
        # 提交成功后更新状态
        self._status = JobStatus.RUNNING
        # 你可以用线程或异步处理来异步查询结果

    def status(self):
        # 返回当前作业状态，比如
        # 查询你的模拟器接口，更新 self._status
        return self._status

    def result(self):
        url = f"{ self._url }/result?id={self.job_id()}"
        while True:
            resp = requests.get(url).json()
            if resp["code"] == -2:
                time.sleep(0.2)
                continue
            return QVecOptResult(resp["data"], self._nqubits, self._job_id)
