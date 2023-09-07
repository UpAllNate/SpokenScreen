from typing import Any

class FunReturn:

    def __init__(self, success : bool, result : Any = None) -> None:
        self.success = success
        self.result = result