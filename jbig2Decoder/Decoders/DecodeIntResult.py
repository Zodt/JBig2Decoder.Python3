

class DecodeIntResult():
    _intResult: int = int()
    _booleanResult: bool = bool()

    def __int__(self, intResult: int, booleanResult: bool) -> None:
        self._intResult = intResult
        self._booleanResult = booleanResult

    def intResult(self) -> int:
        return self._intResult

    def booleanResult(self) -> bool():
        return self._booleanResult







