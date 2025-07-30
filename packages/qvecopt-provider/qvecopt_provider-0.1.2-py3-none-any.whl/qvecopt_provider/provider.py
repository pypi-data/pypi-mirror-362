
from .backend import QVecOptBackend

class QVecOptProvider:
    def __init__(self, url="http://127.0.0.1:8080"):
        from .backend import QVecOptBackend
        self._backend = QVecOptBackend(provider=self, url=url)

    def backends(self, name=None, **kwargs):
        if name is None or name == "QVecOpt":
            return [self._backend]
        return []

    def get_backend(self, name=None, **kwargs):
        if name == "QVecOpt":
            return self._backend
        raise ValueError(f"Backend {name} not found")
