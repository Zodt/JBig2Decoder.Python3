
class Big2StreamReader:

    _data: bytearray = bytearray()
    _bitPointer: int = 7
    _bytePointer: int = 0

    def __init__(self, data: bytearray):
        self._data: bytearray = data

    def readbyte(self, buf=None) -> int:  # must return a short value
        if buf is None:
            bite: int = int(self._data[self._bytePointer + 1])   # must be a short value
            return bite
        else:
            for i in range(len(buf)):
                buf[i] = int(self._data[self._bytePointer + 1] & 255)   # must be a short value

    def readBit(self) -> int:
        buf: int = self.readbyte()               # must be a short value
        mask: int = int(1 << self._bitPointer)   # must be a short value

        bit = ((buf & mask) >> self._bitPointer)

        self._bitPointer -= 1

        if self._bitPointer == -1:
            self._bitPointer = 7
        else:
            self.movePointer(-1)

        return bit

    def readBits(self, num: int) -> int:   # num must be a short value
        result: int = 0

        for i in range(num):
            result = (result << 1) | self.readBit()

        return result

    def movePointer(self, ammount: int) -> None:
        self._bytePointer += ammount

    def consumeRemainingBits(self) -> None:
        if self._bitPointer != 7:
            self.readBits(self._bitPointer + 1)

    def isFinished(self) -> bool:
        return self._bytePointer == len(self._data)
















