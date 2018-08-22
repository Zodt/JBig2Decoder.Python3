class BinaryOperation:

    _LEFT_SHIFT: int = 0
    RIGHT_SHIFT: int = 1

    LONGMASKL: int = 0xffffffff     # 1111 1111 1111 1111 1111 1111 1111 1111
    _INTMASK: int = 0xff            # 1111 1111

    @staticmethod
    def getInt32(number: list) -> int:
        return number[0] << 24 | number[1] << 16 | number[2] << 8 | number[3]

    @staticmethod
    def getInt16(number: list) -> int:
        return number[0] << 8 | number[1]

    @staticmethod
    def bit32ShiftL(number: int, shift: int) -> int:
        return number << shift

    @staticmethod
    def bit32ShiftR(number: int, shift: int) -> int:
        return number >> shift

    def bit8Shift(self, number: int, shift: int, direction: int) -> int:
        if direction == self._LEFT_SHIFT:
            number <<= shift
        else:
            number >>= shift
        return number & self._INTMASK













