from Decoders.ArithmeticDecoderStats import ArithmeticDecoderStats
from Decoders.DecodeIntResult import DecodeIntResult
from Utilities.BinaryOperation import BinaryOperation
from Utilities.StreamReader import Big2StreamReader


class ArithmeticDecoder:
    _reader: Big2StreamReader = Big2StreamReader

    a: int = int()
    c: int = int()
    buffer0: int = int()
    buffer1: int = int()
    previous: int = int()
    counter: int = int()

    contextSize: list = [16, 13, 10, 10]
    referredToContextSize: list = [13, 10]

    iadhStats: ArithmeticDecoderStats = None
    iadwStats: ArithmeticDecoderStats = None
    iaexStats: ArithmeticDecoderStats = None
    iaaiStats: ArithmeticDecoderStats = None
    iadtStats: ArithmeticDecoderStats = None
    iaitStats: ArithmeticDecoderStats = None
    iafsStats: ArithmeticDecoderStats = None
    iadsStats: ArithmeticDecoderStats = None
    iariStats: ArithmeticDecoderStats = None
    iaidStats: ArithmeticDecoderStats = None
    iardxStats: ArithmeticDecoderStats = None
    iardyStats: ArithmeticDecoderStats = None
    iardwStats: ArithmeticDecoderStats = None
    iardhStats: ArithmeticDecoderStats = None
    genericRegionStats: ArithmeticDecoderStats = None
    refinementRegionStats: ArithmeticDecoderStats = None

    qeTable = [0x56010000, 0x34010000, 0x18010000, 0x0AC10000, 0x05210000, 0x02210000,
               0x56010000, 0x54010000, 0x48010000, 0x38010000, 0x30010000, 0x24010000,
               0x1C010000, 0x16010000, 0x56010000, 0x54010000, 0x51010000, 0x48010000,
               0x38010000, 0x34010000, 0x30010000, 0x28010000, 0x24010000, 0x22010000,
               0x1C010000, 0x18010000, 0x16010000, 0x14010000, 0x12010000, 0x11010000,
               0x0AC10000, 0x09C10000, 0x08A10000, 0x05210000, 0x04410000, 0x02A10000,
               0x02210000, 0x01410000, 0x01110000, 0x00850000, 0x00490000, 0x00250000,
               0x00150000, 0x00090000, 0x00050000, 0x00010000, 0x56010000]

    nmpsTable = [1, 2, 3, 4, 5, 38, 7, 8, 9, 10, 11, 12, 13, 29, 15,
                 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                 42, 43, 44, 45, 45, 46]

    nlpsTable = [1, 6, 9, 12, 29, 33, 6, 14, 14, 14, 17, 18, 20, 21,
                 14, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                 38, 39, 40, 41, 42, 43, 46]

    switchTable = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                   0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __int__(self, reader: Big2StreamReader):
        self.genericRegionStats = ArithmeticDecoderStats(1 << 1)
        self.refinementRegionStats = ArithmeticDecoderStats(1 << 1)

        self.iadhStats = ArithmeticDecoderStats(1 << 9)
        self.iadwStats = ArithmeticDecoderStats(1 << 9)
        self.iaexStats = ArithmeticDecoderStats(1 << 9)
        self.iaaiStats = ArithmeticDecoderStats(1 << 9)
        self.iadtStats = ArithmeticDecoderStats(1 << 9)
        self.iaitStats = ArithmeticDecoderStats(1 << 9)
        self.iafsStats = ArithmeticDecoderStats(1 << 9)
        self.iadsStats = ArithmeticDecoderStats(1 << 9)
        self.iardxStats = ArithmeticDecoderStats(1 << 9)
        self.iardyStats = ArithmeticDecoderStats(1 << 9)
        self.iardwStats = ArithmeticDecoderStats(1 << 9)
        self.iardhStats = ArithmeticDecoderStats(1 << 9)
        self.iariStats = ArithmeticDecoderStats(1 << 9)
        self.iaidStats = ArithmeticDecoderStats(1 << 1)

    def resetIntStats(self, symbolCodeLength: int) -> None:
        self.iadhStats.reset()
        self.iadwStats.reset()
        self.iaexStats.reset()
        self.iaaiStats.reset()
        self.iadtStats.reset()
        self.iaitStats.reset()
        self.iafsStats.reset()
        self.iadsStats.reset()
        self.iardxStats.reset()
        self.iardyStats.reset()
        self.iardwStats.reset()
        self.iardhStats.reset()
        self.iariStats.reset()

        if self.iaidStats.getContextSize() == 1 << symbolCodeLength + 1:
            self.iaidStats.reset()
        else:
            self.iaidStats = ArithmeticDecoderStats(1 << symbolCodeLength + 1)

    def resetGenericStats(self, template: int, previousStats: ArithmeticDecoderStats):
        size: int = self.contextSize[template]

        if previousStats is not None and previousStats.getContextSize() == size:
            if self.genericRegionStats.getContextSize() == size:
                self.genericRegionStats.overwrite(previousStats)
            else:
                self.genericRegionStats = previousStats.copy()
        else:
            if self.genericRegionStats.getContextSize() == size:
                self.genericRegionStats.reset()
            else:
                self.genericRegionStats = ArithmeticDecoderStats(1 << size)

    def resetRefinementStats(self, template: int, previousStats: ArithmeticDecoderStats):
        size: int = self.referredToContextSize[template]
        if previousStats is not None and previousStats.getContextSize() == size:
            if self.refinementRegionStats.getContextSize() == size:
                self.refinementRegionStats.overwrite(previousStats)
            else:
                self.refinementRegionStats = previousStats.copy()
        else:
            if self.refinementRegionStats.getContextSize() == size:
                self.refinementRegionStats.reset()
            else:
                self.refinementRegionStats = ArithmeticDecoderStats(1 << size)

    def start(self):
        self.buffer0 = self._reader.readbyte()
        self.buffer1 = self._reader.readbyte()

        self.c = BinaryOperation.bit32ShiftL(self.buffer0 ^ 0xff, 16)
        self.readbyte()
        self.c = BinaryOperation.bit32ShiftL(self.c, 7)
        self.counter -= 7
        self.a = 0x80000000

    def decodeInt(self, stats: ArithmeticDecoderStats) -> DecodeIntResult():
        value = int()

        self.previous = 1
        s = self.decodeIntBit(stats)
        if self.decodeIntBit(stats) != 0:
            if self.decodeIntBit(stats) != 0:
                if self.decodeIntBit(stats) != 0:
                    if self.decodeIntBit(stats) != 0:
                        if self.decodeIntBit(stats) != 0:
                            value = 0
                            for i in range(32):
                                value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                            value += 4436
                        else:
                            value = 0
                            for i in range(12):
                                value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                            value += 340
                    else:
                        value = 0
                        for i in range(8):
                            value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                        value += 84
                else:
                    value = 0
                    for i in range(6):
                        value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                    value += 20
            else:
                value = self.decodeIntBit(stats)
                value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)
                value += 4
        else:
            value = self.decodeIntBit(stats)
            value = BinaryOperation.bit32ShiftL(value, 1) | self.decodeIntBit(stats)

        decodedInt = int()

        if s != 0:
            if value == 0:
                return DecodeIntResult(self, int(value), False)
            decodedInt = int(-value)
        else:
            decodedInt = int(value)

        return DecodeIntResult(self, decodedInt, True)

    def decodeIAID(self, codeLen: int, stats: ArithmeticDecoderStats) -> int:
        self.previous = 1
        for i in range(codeLen):
            bit: int = self.decodeBit(self.previous, stats)
            self.previous = BinaryOperation.bit32ShiftL(self.previous, 1) | bit

        return self.previous - (1 << int(codeLen))

    def decodeBit(self, context: int, stats: ArithmeticDecoderStats) -> int:
        iCX: int = BinaryOperation.bit8Shift(stats.getContextCodingTableValue(int(context)), 1,
                                             BinaryOperation.RIGHT_SHIFT)
        mpsCX: int = stats.getContextCodingTableValue(int(context) & 1)
        qe: int = self.qeTable[iCX]

        self.a -= qe

        bit = int()

        if (self.a & 0x80000000) != 0:
            bit = mpsCX
        else:
            if self.a < qe:
                if self.a < qe:
                    bit = 1 - mpsCX
                    if self.switchTable[iCX] != 0:
                        stats.setContextCodingTableValue(int(context), self.nlpsTable[iCX] << 1 | 1 - mpsCX)
                    else:
                        stats.setContextCodingTableValue(int(context), self.nlpsTable[iCX] << 1 | mpsCX)
                else:
                    bit = mpsCX
                    stats.setContextCodingTableValue(int(context), self.nmpsTable[iCX] << 1 | mpsCX)

                    while True:
                        if self.doWhile(): break
            else:
                self.c -= self.a

                if self.a < qe:
                    bit = mpsCX
                    stats.setContextCodingTableValue(int(context), self.nmpsTable[iCX] << 1 | mpsCX)
                else:
                    bit = 1 - mpsCX
                    if self.switchTable[iCX] != 0:
                        stats.setContextCodingTableValue(int(context), self.nmpsTable[iCX] << 1 | 1 - mpsCX)
                    else:
                        stats.setContextCodingTableValue(int(context), self.nmpsTable[iCX] << 1 | mpsCX)

                self.a = qe

                while True:
                    if self.doWhile(): break

        return bit

    def doWhile(self):
        if (self.a & 0x80000000) == 0:
            if self.counter == 0:
                self.readbyte()
            self.a = BinaryOperation.bit32ShiftL(self.a, 1)
            self.c = BinaryOperation.bit32ShiftL(self.c, 1)
            self.counter -= 1
        else:
            return False

    def readbyte(self):
        if self.buffer0 == 0xff:
            if self.buffer1 > 0x8f:
                self.counter = 8
            else:
                self.buffer0 = self.buffer1
                self.buffer1 = self._reader.readbyte()
                self.c = self.c + 0xfe00 - BinaryOperation.bit32ShiftL(self.buffer0, 9)
                self.counter = 8

    def decodeIntBit(self, stats: ArithmeticDecoderStats):
        bit = int()

        bit = self.decodeBit(self.previous, stats)
        if self.previous < 0x100:
            self.previous = BinaryOperation.bit32ShiftL(self.previous, 1) | bit
        else:
            self.previous = (BinaryOperation.bit32ShiftL(self.previous, 1) | bit) & 0x1ff | 0x100

        return bit





