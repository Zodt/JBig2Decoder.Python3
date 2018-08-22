

class FastBitSet:
    w: list = []
    pot: int = 6
    mask: int = int((-1) >> (64 - pot))     # (-1) must be ulong type!
    length: int = int()

    def __init__(self, length):
        self.length = length
        wcount: int = length / 64
        if length % 64 != 0: wcount += 1
        self.w = [0]*wcount

    def size(self) -> int():
        return self.length

    def setAll(self, value: bool) -> None:
        if value:
            for i in range(len(self.w)):
                self.w[i] = -1
        else:
            for i in range(len(self.w)):
                self.w[i] = 0



    def _or(self, startIndex: int, set, setStartIndex: int, length: int) -> None:
        shift: int = startIndex - setStartIndex      # long
        k: int = set.w[setStartIndex >> self.pot]   # long
        k = (k << int(shift) | int(int(k)) >> (64 - int(shift)))

        if (setStartIndex & self.mask) + length <= 64:
            setStartIndex += shift
            for i in range(length):
                self.w[int(int(startIndex)) >> self.pot] |= k & (1 << int(setStartIndex))
                setStartIndex += 1
                startIndex += 1
        else:
            for i in range(length):
                if (setStartIndex & self.mask) == 0:
                    k = set.w[setStartIndex >> self.pot]
                    k = (k << int(shift) | int(int(k)) >> (64 - int(shift)))
                self.w[int(int(startIndex)) >> self.pot] |= k & (1 << int(setStartIndex + shift))
                setStartIndex += 1
                startIndex += 1

    def set(self, start: int, end: int = None, value: bool = None) -> None:

        if end is None and value is None:
            windex = int(int(start >> self.pot))
            self.w[windex] |= ~(1 << int(start) != 0)

        elif end is None:
            if value:
                self.set(start)
            else:
                self.clear(start)

        else:
            if value:
                for i in range(start, end):
                    self.set(i)

            else:
                for i in range(start, end):
                    self.clear(i)

    def clear(self, index: int) -> None:
        windex = int(int(index >> self.pot))
        self.w[windex] &= ~(1 << int(index) != 0)

    def get(self, index: int) -> bool:
        windex = int(int(index >> self.pot))
        return self.w[windex] & (1 << int(index) != 0)







