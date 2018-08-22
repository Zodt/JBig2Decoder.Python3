from Utilities.BinaryOperation import BinaryOperation
from Utilities.StreamReader import Big2StreamReader

class MMRDecoder:
    _reader: Big2StreamReader

    buffer: int = 0
    bufferLength: int = 0
    noOfbytesRead: int = 0
    twoDimensionalPass: int = 0

    ccittEndOfLine = -2
    twoDimensionalVertical0 = 2
    twoDimensionalHorizontal = 1
    twoDimensionalVerticalR1 = 3
    twoDimensionalVerticalL1 = 4
    twoDimensionalVerticalR2 = 5
    twoDimensionalVerticalL2 = 6
    twoDimensionalVerticalR3 = 7
    twoDimensionalVerticalL3 = 8

    twoDimensionalTable1 = [[-1, -1],            [-1, -1], [7, twoDimensionalVerticalL3], [7, twoDimensionalVerticalR3],
                            [6, twoDimensionalVerticalL2], [6, twoDimensionalVerticalL2], [6, twoDimensionalVerticalR2],
                            [6, twoDimensionalVerticalR2], [4, twoDimensionalPass],       [4, twoDimensionalPass],
                            [4, twoDimensionalPass],       [4, twoDimensionalPass],       [4, twoDimensionalPass],
                            [4, twoDimensionalPass],       [4, twoDimensionalPass],       [4, twoDimensionalPass],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal], [3, twoDimensionalHorizontal],
                            [3, twoDimensionalHorizontal], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1],
                            [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1],
                            [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1],
                            [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1],
                            [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1],
                            [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalL1], [3, twoDimensionalVerticalR1],
                            [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1],
                            [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1],
                            [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1],
                            [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1],
                            [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1], [3, twoDimensionalVerticalR1],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],  [1, twoDimensionalVertical0],
                            [1, twoDimensionalVertical0]]

    whiteTable1 = [[-1, -1], [12, ccittEndOfLine], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
                   [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [11, 1792], [11, 1792],
                   [12, 1984], [12, 2048], [12, 2112], [12, 2176], [12, 2240], [12, 2304], [11, 1856], [11, 1856],
                   [11, 1920], [11, 1920], [12, 2368], [12, 2432], [12, 2496], [12, 2560]]

    whiteTable2 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [8, 29], [8, 29], [8, 30], [8, 30], [8, 45], [8, 45],
                   [8, 46], [8, 46], [7, 22], [7, 22], [7, 22], [7, 22], [7, 23], [7, 23], [7, 23], [7, 23], [8, 47],
                   [8, 47], [8, 48], [8, 48], [6, 13], [6, 13], [6, 13], [6, 13], [6, 13], [6, 13], [6, 13], [6, 13],
                   [7, 20], [7, 20], [7, 20], [7, 20], [8, 33], [8, 33], [8, 34], [8, 34], [8, 35], [8, 35], [8, 36],
                   [8, 36], [8, 37], [8, 37], [8, 38], [8, 38], [7, 19], [7, 19], [7, 19], [7, 19], [8, 31], [8, 31],
                   [8, 32], [8, 32], [6, 1], [6, 1], [6, 1], [6, 1], [6, 1], [6, 1], [6, 1], [6, 1], [6, 12], [6, 12],
                   [6, 12], [6, 12], [6, 12], [6, 12], [6, 12], [6, 12], [8, 53], [8, 53], [8, 54], [8, 54], [7, 26],
                   [7, 26], [7, 26], [7, 26], [8, 39], [8, 39], [8, 40], [8, 40], [8, 41], [8, 41], [8, 42], [8, 42],
                   [8, 43], [8, 43], [8, 44], [8, 44], [7, 21], [7, 21], [7, 21], [7, 21], [7, 28], [7, 28], [7, 28],
                   [7, 28], [8, 61], [8, 61], [8, 62], [8, 62], [8, 63], [8, 63], [8, 0], [8, 0], [8, 320], [8, 320],
                   [8, 384], [8, 384], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10],
                   [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 10], [5, 11], [5, 11], [5, 11], [5, 11],
                   [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11], [5, 11],
                   [5, 11], [7, 27], [7, 27], [7, 27], [7, 27], [8, 59], [8, 59], [8, 60], [8, 60], [9, 1472],
                   [9, 1536], [9, 1600], [9, 1728], [7, 18], [7, 18], [7, 18], [7, 18], [7, 24], [7, 24], [7, 24],
                   [7, 24], [8, 49], [8, 49], [8, 50], [8, 50], [8, 51], [8, 51], [8, 52], [8, 52], [7, 25], [7, 25],
                   [7, 25], [7, 25], [8, 55], [8, 55], [8, 56], [8, 56], [8, 57], [8, 57], [8, 58], [8, 58], [6, 192],
                   [6, 192], [6, 192], [6, 192], [6, 192], [6, 192], [6, 192], [6, 192], [6, 1664], [6, 1664],
                   [6, 1664], [6, 1664], [6, 1664], [6, 1664], [6, 1664], [6, 1664], [8, 448],
                   [8, 448], [8, 512], [8, 512], [9, 704], [9, 768], [8, 640], [8, 640], [8, 576], [8, 576], [9, 832],
                   [9, 896], [9, 960], [9, 1024], [9, 1088], [9, 1152], [9, 1216], [9, 1280], [9, 1344], [9, 1408],
                   [7, 256], [7, 256], [7, 256], [7, 256], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2],
                   [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2],
                   [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2], [4, 2],
                   [4, 2], [4, 2], [4, 2], [4, 2], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3],
                   [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3],
                   [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3],
                   [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128],
                   [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 128], [5, 8],
                   [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8],
                   [5, 8], [5, 8], [5, 8], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9],
                   [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [6, 16], [6, 16], [6, 16], [6, 16], [6, 16],
                   [6, 16], [6, 16], [6, 16], [6, 17], [6, 17], [6, 17], [6, 17], [6, 17], [6, 17], [6, 17], [6, 17],
                   [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4],
                   [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4],
                   [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4],
                   [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5],
                   [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5],
                   [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5],
                   [6, 14], [6, 14], [6, 14], [6, 14], [6, 14], [6, 14], [6, 14], [6, 14], [6, 15], [6, 15], [6, 15],
                   [6, 15], [6, 15], [6, 15], [6, 15], [6, 15], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64],
                   [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [5, 64], [4, 6],
                   [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6],
                   [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6],
                   [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 6], [4, 7],
                   [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7],
                   [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7],
                   [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7]]

    blackTable1 = [[-1, -1], [-1, -1], [12, ccittEndOfLine], [12, ccittEndOfLine], [-1, -1], [-1, -1], [-1, -1],
                   [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
                   [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
                   [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [11, 1792], [11, 1792], [11, 1792], [11, 1792],
                   [12, 1984], [12, 1984], [12, 2048], [12, 2048], [12, 2112], [12, 2112],
                   [12, 2176], [12, 2176], [12, 2240], [12, 2240], [12, 2304], [12, 2304], [11, 1856], [11, 1856],
                   [11, 1856], [11, 1856], [11, 1920], [11, 1920], [11, 1920], [11, 1920], [12, 2368], [12, 2368],
                   [12, 2432], [12, 2432], [12, 2496], [12, 2496], [12, 2560], [12, 2560], [10, 18], [10, 18], [10, 18],
                   [10, 18], [10, 18], [10, 18], [10, 18], [10, 18], [12, 52], [12, 52], [13, 640], [13, 704],
                   [13, 768], [13, 832], [12, 55], [12, 55], [12, 56], [12, 56], [13, 1280], [13, 1344],
                   [13, 1408], [13, 1472], [12, 59], [12, 59], [12, 60], [12, 60], [13, 1536], [13, 1600], [11, 24],
                   [11, 24], [11, 24], [11, 24], [11, 25], [11, 25], [11, 25], [11, 25], [13, 1664], [13, 1728],
                   [12, 320], [12, 320], [12, 384], [12, 384], [12, 448], [12, 448], [13, 512], [13, 576], [12, 53],
                   [12, 53], [12, 54], [12, 54], [13, 896], [13, 960], [13, 1024], [13, 1088], [13, 1152], [13, 1216],
                   [10, 64], [10, 64], [10, 64], [10, 64], [10, 64], [10, 64], [10, 64], [10, 64]]

    blackTable2 = [[8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [8, 13],
                   [8, 13], [8, 13], [8, 13], [8, 13], [8, 13], [11, 23], [11, 23], [12, 50], [12, 51], [12, 44],
                   [12, 45], [12, 46], [12, 47], [12, 57], [12, 58], [12, 61], [12, 256], [10, 16], [10, 16], [10, 16],
                   [10, 16], [10, 17], [10, 17], [10, 17], [10, 17], [12, 48], [12, 49], [12, 62], [12, 63], [12, 30],
                   [12, 31], [12, 32], [12, 33], [12, 40], [12, 41], [11, 22],
                   [11, 22], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14],
                   [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [8, 14], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10],
                   [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10],
                   [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10],
                   [7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 11], [7, 11],
                   [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11],
                   [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11],
                   [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [7, 11], [9, 15], [9, 15], [9, 15],
                   [9, 15], [9, 15], [9, 15], [9, 15], [9, 15], [12, 128], [12, 192], [12, 26], [12, 27], [12, 28],
                   [12, 29], [11, 19], [11, 19], [11, 20], [11, 20], [12, 34], [12, 35],
                   [12, 36], [12, 37], [12, 38], [12, 39], [11, 21], [11, 21], [12, 42], [12, 43], [10, 0], [10, 0],
                   [10, 0], [10, 0], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12],
                   [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12],
                   [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12], [7, 12],
                   [7, 12]]

    blackTable3 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [6, 9], [6, 8], [5, 7], [5, 7], [4, 6], [4, 6], [4, 6],
                   [4, 6], [4, 5], [4, 5], [4, 5], [4, 5], [3, 1], [3, 1], [3, 1], [3, 1], [3, 1], [3, 1], [3, 1],
                   [3, 1], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [2, 3], [2, 3], [2, 3],
                   [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3],
                   [2, 3], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2],
                   [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2]]

    def __init__(self, reader=None):
        if reader is not None:
            self._reader = reader

    def reset(self) -> None:
        self.buffer = 0
        self.bufferLength = 0
        self.noOfbytesRead = 0

    def skipTo(self, length: int) -> None:
        while self.noOfbytesRead < length:
            self._reader.readbyte()
            self.noOfbytesRead += 1

    def get24Bits(self):
        while self.bufferLength < 24:
            self.buffer = ((BinaryOperation.bit32ShiftL(self.buffer, 8)
                            ) | (self._reader.readbyte() & 0xff))
            self.bufferLength += 8
            self.noOfbytesRead += 1

        return (BinaryOperation.bit32ShiftR(self.buffer, int(self.bufferLength - 24)
                                            )) & 0xffffff

    def get2DCode(self) -> int:
        tuple0: int = int()
        tuple1: int = int()

        if self.bufferLength == 0:
            self.buffer = (self._reader.readbyte() & 0xff)
            self.bufferLength = 8
            self.noOfbytesRead += 1

            lookup: int = int((BinaryOperation.bit32ShiftR(self.buffer, 1)) & 0x7f)
            tuple0 = self.twoDimensionalTable1[lookup][0]
            tuple1 = self.twoDimensionalTable1[lookup][1]

        elif self.bufferLength == 8:
            lookup = int((BinaryOperation.bit32ShiftR(self.buffer, 1)) & 0x7f)
            tuple0 = self.twoDimensionalTable1[lookup][0]
            tuple1 = self.twoDimensionalTable1[lookup][1]

        else:
            lookup = int((BinaryOperation.bit32ShiftL(self.buffer, int(7 - self.bufferLength))) & 0x7f)
            tuple0 = self.twoDimensionalTable1[lookup][0]
            tuple1 = self.twoDimensionalTable1[lookup][1]

            if tuple0 < 0 or tuple0 > int(self.bufferLength):
                right: int = (self._reader.readbyte() & 0xff)
                left: int = (BinaryOperation.bit32ShiftL(self.buffer, 8))

                self.buffer = left | right
                self.bufferLength += 8
                self.noOfbytesRead += 1

                lookup = int((BinaryOperation.bit32ShiftL(self.buffer, int(7 - self.bufferLength))) & 0x7f)
                tuple0 = self.twoDimensionalTable1[lookup][0]
                tuple1 = self.twoDimensionalTable1[lookup][1]

        if tuple0 < 0:
            return 0

        self.bufferLength -= tuple0

        return tuple1

    def getWhiteCode(self):
        tuple0: int = int()
        tuple1: int = int()
        code: int = int()

        if self.bufferLength == 0:
            self.buffer = (self._reader.readbyte() & 0xff)
            self.bufferLength = 8
            self.noOfbytesRead += 1

        while True:
            if (self.bufferLength >= 7 and
                    ((BinaryOperation.bit32ShiftR(self.buffer,
                                                  int(self.bufferLength - 7))) & 0x7f) == 0):

                code = self.returnCode(12)
                tuple0 = self.whiteTable1[int(code & 0x1f)][0]
                tuple1 = self.whiteTable1[int(code & 0x1f)][1]

            else:
                code = self.returnCode(9)

                lookup = int(code & 0x1ff)

                tuple0, tuple1 = self.returnTuples(lookup, self.whiteTable2)

                if 0 < tuple0 <= int(self.bufferLength):
                    self.bufferLength -= tuple0
                    return tuple1

                if self.bufferLength >= 12:
                    break

                self.buffer = ((BinaryOperation.bit32ShiftL(self.buffer, 8)) | self._reader.readbyte() & 0xff)
                self.bufferLength += 8
                self.noOfbytesRead += 1

        self.bufferLength -= 1
        return 1

    def getBlackCode(self):
        tuple0: int = int()
        tuple1: int = int()
        code: int = int()

        if self.bufferLength == 0:
            self.buffer = (self._reader.readbyte() & 0xff)
            self.bufferLength = 8
            self.noOfbytesRead += 1

        while True:

            if (self.bufferLength >= 6 and
                    ((BinaryOperation.bit32ShiftR(self.buffer, int(self.bufferLength - 6))) & 0x3f) == 0):

                code = self.returnCode(13)
                tuple0 = self.blackTable1[int(code & 0x7f)][0]
                tuple1 = self.blackTable1[int(code & 0x7f)][1]

            elif (self.bufferLength >= 4 and
                  ((BinaryOperation.bit32ShiftR(self.buffer, int(self.bufferLength - 4))) & 0x0f) == 0):

                code = self.returnCode(12)
                lookup = int((code & 0xff) - 64)
                tuple0, tuple1 = self.returnTuples(lookup, self.blackTable2)

            else:
                code = self.returnCode(6)
                lookup = int(code & 0x3f)
                tuple0, tuple1 = self.returnTuples(lookup, self.blackTable2)

            if 0 < tuple0 <= int(self.bufferLength):
                self.bufferLength -= tuple0
                return tuple0

            if self.bufferLength >= 13:
                break

            self.buffer = ((BinaryOperation.bit32ShiftL(self.buffer, 8)) | (self._reader.readbyte() & 0xff))
            self.bufferLength += 8
            self.noOfbytesRead += 1

        self.bufferLength -= 1
        return 1

    def returnCode(self, number: int) -> int:
        if self.bufferLength <= number:
            return BinaryOperation.bit32ShiftL(self.buffer, int(number - self.bufferLength))
        else:
            return BinaryOperation.bit32ShiftR(self.buffer, int(self.bufferLength - number))

    @staticmethod
    def returnTuples(lookup, array):

        if lookup >= 0:
            tuple0 = array[lookup][0]
            tuple1 = array[lookup][1]

        else:
            tuple0 = array[len(array) + lookup][0]
            tuple1 = array[len(array) + lookup][1]

        return tuple0, tuple1

















