from Decoders.ArithmeticDecoder import ArithmeticDecoder
from Decoders.HuffmanDecoder import HuffmanDecoder
from Decoders.MMRDecoder import MMRDecoder
from Utilities.FastBitSet import FastBitSet
from  Utilities.BinaryOperation import BinaryOperation
from Image.BitmapPointer import BitmapPointer
from JBIG2StreamDecoder import JBIG2StreamDecoder



class JBIG2Bitmap:

    _width: int = int()
    _height: int = int()
    _line: int = int()
    _bitmapNumber: int = int()

    _arithmeticDecoder: ArithmeticDecoder = None
    _huffmanDecoder: HuffmanDecoder = None
    _mmrDecoder: MMRDecoder = None
    debug = False
    data: FastBitSet = None

    def __init__(self, width: int, height: int,
                 arithmeticDecoder: ArithmeticDecoder,
                 huffmanDecoder: HuffmanDecoder,
                 mmrDecoder: MMRDecoder):
        self._width = width
        self._height = height
        self._arithmeticDecoder = arithmeticDecoder
        self._huffmanDecoder = huffmanDecoder
        self._mmrDecoder = mmrDecoder

        self._line = (width+7) >> 3
        self.data: FastBitSet = FastBitSet(width * height)


    def readBitmap(self, useMMR: bool, template: int,
            typicalPredictionGenericDecodingOn:bool, useSkip:bool,
            skipBitmap, adaptiveTemplateX: list,
            adaptiveTemplateY: list, mmrDataLength: int) -> None:   # skipBitmap: JBIG2Bitmap

        if useMMR:
            self._mmrDecoder.reset()

            referenceLine: list = [0] * (self._width + 2)
            codingLine: list = [0] * (self._width + 2)
            codingLine[0] = codingLine[1] = self._width

            for row in range(self._height):

                i: int = int()
                while codingLine[i] < self._width:
                    referenceLine[i] = codingLine[i]
                    i += 1
                codingLine[i] = codingLine[i + 1] = self._width

                referenceI: int = int()
                codingI: int = int()
                a0: int = int()

                while True:
                    tmp = self.DoWhile(a0, referenceLine, referenceI, codingI, codingLine)
                    if not tmp[0]:
                        break
                    else: codingLine, codingI = tmp[1], tmp[2]
                codingLine[codingI + 1] = self._width

                j: int = int()
                while codingLine[j] < self._width:
                    for col in range(codingLine[j], codingLine[j+1]):
                        self.setPixel(col, row, 1)
                    j += 2
            if mmrDataLength >= 0:
                self._mmrDecoder.skipTo(mmrDataLength)
            else:
                if self._mmrDecoder.get24Bits() != 0x001001:
                    if self.debug:
                        print("Missing EOFB in JBIG2 MMR bitmap data")

        else:
            cxPtr0: BitmapPointer = BitmapPointer(self)
            cxPtr1: BitmapPointer = BitmapPointer(self)

            atPtr0: BitmapPointer = BitmapPointer(self)
            atPtr1: BitmapPointer = BitmapPointer(self)
            atPtr2: BitmapPointer = BitmapPointer(self)
            atPtr3: BitmapPointer = BitmapPointer(self)

            ltpCX: int = 0      # long

            if typicalPredictionGenericDecodingOn:
                if template == 0:
                    ltpCX = 0x3953
                elif template == 1:
                    ltpCX = 0x079a
                elif template == 2:
                    ltpCX = 0x0e3
                elif template == 3:
                    ltpCX = 0x18a

            ltp: bool = bool()

            # long values
            cx = int()
            cx0 = int()
            cx1 = int()
            cx2 = int()
            #

            for row in range(self._height):
                if typicalPredictionGenericDecodingOn:
                    bit = self._arithmeticDecoder.decodeBit(ltpCX, self._arithmeticDecoder.genericRegionStats)
                    if bit != 0:
                        ltp = not ltp
                    if ltp:
                        self.duplicateRow(row, row - 1)
                        continue

                pixel: int = int()

                if template == 0:
                    cxPtr0.setPointer(0, row - 2)
                    cx0 = (cxPtr0.nextPixel() << 1)
                    cx0 |= cxPtr0.nextPixel()

                    cxPtr1.setPointer(0, row - 1)
                    cx1 = (cxPtr1.nextPixel() << 2)
                    cx1 |= (cxPtr1.nextPixel() << 1)
                    cx1 |= (cxPtr1.nextPixel())

                    cx2 = int()
                    atPtr0.setPointer(adaptiveTemplateX[0], row + adaptiveTemplateY[0])
                    atPtr1.setPointer(adaptiveTemplateX[1], row + adaptiveTemplateY[1])
                    atPtr2.setPointer(adaptiveTemplateX[2], row + adaptiveTemplateY[2])
                    atPtr3.setPointer(adaptiveTemplateX[3], row + adaptiveTemplateY[3])
                    for col in range(self._width):
                        cx = (BinaryOperation.bit32ShiftL(cx0, 13)) | (BinaryOperation.bit32ShiftL(cx1, 8)) | \
                             (BinaryOperation.bit32ShiftL(cx2, 4)) | (atPtr0.nextPixel() << 3) | \
                             (atPtr1.nextPixel() << 2) | (atPtr2.nextPixel() << 1) | atPtr3.nextPixel()

                        if useSkip and skipBitmap.getPixel(col, row) != 0:
                            pixel = int()
                        else:
                            pixel = self._arithmeticDecoder.decodeBit(cx, self._arithmeticDecoder.genericRegionStats)
                            if pixel != 0:
                                self.data.set(row * self._width + col)

                        cx0 = ((BinaryOperation.bit32ShiftL(cx0, 1)) | cxPtr0.nextPixel()) & 0x07
                        cx1 = ((BinaryOperation.bit32ShiftL(cx1, 1)) | cxPtr1.nextPixel()) & 0x1f
                        cx2 = ((BinaryOperation.bit32ShiftL(cx2, 1)) | pixel) & 0x0f

                elif template == 1:
                    cxPtr0.setPointer(0, row - 2)
                    cx0 = (cxPtr0.nextPixel() << 2)
                    cx0 |= (cxPtr0.nextPixel() << 1)
                    cx0 |= cxPtr0.nextPixel()

                    cxPtr1.setPointer(0, row - 1)
                    cx1 = (cxPtr1.nextPixel() << 2)
                    cx1 |= (cxPtr1.nextPixel() << 1)
                    cx1 |= (cxPtr1.nextPixel())

                    cx2 = int()
                    atPtr0.setPointer(adaptiveTemplateX[0], row + adaptiveTemplateY[0])
                    for col in range(self._width):
                        cx = (BinaryOperation.bit32ShiftL(cx0, 9)) | (BinaryOperation.bit32ShiftL(cx1, 4)) | (
                            BinaryOperation.bit32ShiftL(cx2, 1)) | atPtr0.nextPixel()
                        if useSkip and skipBitmap.getPixel(col, row) != 0:
                            pixel = 0
                        else:
                            pixel = self._arithmeticDecoder.decodeBit((cx, self._arithmeticDecoder.genericRegionStats))
                            if pixel != 0 :
                                self.data.set(row * self._width + col)
                        cx0 = ((BinaryOperation.bit32ShiftL(cx0, 1)) | cxPtr0.nextPixel()) & 0x0f
                        cx1 = ((BinaryOperation.bit32ShiftL(cx1, 1)) | cxPtr1.nextPixel()) & 0x1f
                        cx2 = ((BinaryOperation.bit32ShiftL(cx2, 1)) | pixel) & 0x07

                elif template == 2:
                    cxPtr0.setPointer(0, row - 2)
                    cx0 = (cxPtr0.nextPixel() << 1)
                    cx0 |= (cxPtr0.nextPixel())

                    cxPtr1.setPointer(0, row - 1)
                    cx1 = (cxPtr1.nextPixel() << 1)
                    cx1 |= (cxPtr1.nextPixel())

                    cx2 = 0

                    atPtr0.setPointer(adaptiveTemplateX[0], row + adaptiveTemplateY[0])

                    for col in range(self._width):
                        cx = (BinaryOperation.bit32ShiftL(cx0, 7)) | (BinaryOperation.bit32ShiftL(cx1, 3)) | (
                            BinaryOperation.bit32ShiftL(cx2, 1)) | atPtr0.nextPixel()
                        if useSkip and skipBitmap.getPixel(col, row) != 0:
                            pixel = 0
                        else:
                            pixel = self._arithmeticDecoder.decodeBit((cx, self._arithmeticDecoder.genericRegionStats))
                            if pixel != 0 :
                                self.data.set(row * self._width + col)

                        cx0 = ((BinaryOperation.bit32ShiftL(cx0, 1)) | cxPtr0.nextPixel()) & 0x07
                        cx1 = ((BinaryOperation.bit32ShiftL(cx1, 1)) | cxPtr1.nextPixel()) & 0x0f
                        cx2 = ((BinaryOperation.bit32ShiftL(cx2, 1)) | pixel) & 0x03

                elif template == 3:
                    cxPtr1.setPointer(0, row - 1)
                    cx1 = (cxPtr1.nextPixel() << 1)
                    cx1 |= (cxPtr1.nextPixel())
                    cx2 = 0

                    atPtr0.setPointer(adaptiveTemplateX[0], row + adaptiveTemplateY[0])

                    for col in range(self._width):
                        cx = (BinaryOperation.bit32ShiftL(cx1, 5)) | (
                        BinaryOperation.bit32ShiftL(cx2, 1)) | atPtr0.nextPixel()
                        if useSkip and skipBitmap.getPixel(col, row) != 0:
                            pixel = 0
                        else:
                            pixel = self._arithmeticDecoder.decodeBit(cx, self._arithmeticDecoder.genericRegionStats)
                            if pixel != 0:
                                self.data.set(row * self._width + col)

                        cx1 = ((BinaryOperation.bit32ShiftL(cx1, 1)) | cxPtr1.nextPixel()) & 0x1f
                        cx2 = ((BinaryOperation.bit32ShiftL(cx2, 1)) | pixel) & 0x0f

    def setPixel(self, col: int, row: int, value: int, data: FastBitSet = None) -> None:     # must be long
        if data in None: data = self.data
        index: int = (row * self._width) + col      # must be a long
        data.set(index, value == 1)

    def clear(self, defPixel: int) -> None:
        self.data.setAll((defPixel == 1))

    def duplicateRow(self, yDest: int, ySrc: int):
        for i in range(self._width):
            self.setPixel(i, yDest, self.getPixel(i, ySrc))

    def getWidth(self) -> int:      # return must be a long
        return self._width

    def getHeight(self) -> int:     # return must be a long
        return self._height

    def getPixel(self, col: int, row: int) -> int:
        return 1 if self.data.get(row*self._width + col) else 0

    def expand(self, newHeight: int, defaultPixel: int) -> None:
        newData: FastBitSet = FastBitSet(newHeight * self._width)
        for row in range(self._height):
            for col in range(self._width):
                self.setPixel(col, row, data=newData, value=self.getPixel(col, row))

        self._height = newHeight
        self.data = newData

    def setBitmapNumber(self, segmentNumber: int):
        self._bitmapNumber = segmentNumber

    def getBitmapNumber(self):
        return self._bitmapNumber

    def getBufferedImage(self):
        bytes: bytearray = self.getData(True)

        if bytes is None:
            return None

        copy: bytearray = [0] * len(bytes)
        # Array.Copy(bytes, 0, copy, 0, len);

        return copy

    def getSlice(self, x, y, width, height):
        pass

    def getData(self, switchPixelColor: bool) -> bytearray:
        pass

    def combine(self, bitmap, x, y, comb0p) -> None:
        pass

    def readGenericRefinementRegion(self, template: int, typicalPredictionGenericRefinementOn: bool,
                                    referredToBitmap: int, referenceDX: int, referenceDY: int,
                                    adaptiveTemplateX: int, adaptiveTemplateY: int) -> None:
        pass

# readTextRegion!

    def readTextRegion2(self, huffman: bool, symbolRefine: bool, noOfSymbolInstances: int,
                        logStrips: int, noOfSymbols: int, symbolCodeTable: list(list()),
                        symbolCodeLength: int, symbols, defaultPixel: int,
                        combinationOperator: int, transposed: bool, referenceCorner: int,
                        sOffset: int, huffmanFSTable: list(list()), huffmanDSTable: list(list()),
                        huffmanDTTable: list(list()), huffmanRDWTable: list(list()),
                        huffmanRDHTable: list(list()), huffmanRDXTable: list(list()),
                        huffmanRDYTable: list(list()), huffmanRSizeTable: list(list()), template: int,
                        symbolRegionAdaptiveTemplateX: int, symbolRegionAdaptiveTemplateY: int,
                        decoder: JBIG2StreamDecoder) -> None:
        pass




    def DoWhile(self, a0, referenceLine, referenceI, codingI, codingLine):
        if a0 < self._width:
            code1: int = self._mmrDecoder.get2DCode()
            code2: int = int()
            code3: int = int()

            if code1 == MMRDecoder.twoDimensionalPass:
                if referenceLine[referenceI] < self._width:
                    a0 = referenceLine[referenceI + 1]
                    referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalHorizontal:

                if (codingI & 1) != 0:
                    code1 = int()
                    while True:
                        tmp = self.easyDoWhile(code1, code3, self._mmrDecoder.getBlackCode())
                        if not tmp[0]: break
                        else:
                            code2 = tmp[1]
                            code3 = tmp[2]

                    while True:
                        tmp = self.easyDoWhile(code2, code3, self._mmrDecoder.getWhiteCode())
                        if not tmp[0]: break
                        else:
                            code2 = tmp[1]
                            code3 = tmp[2]

                else:
                    while True:
                        tmp = self.easyDoWhile(code2, code3, self._mmrDecoder.getBlackCode())
                        if not tmp[0]: break
                        else:
                            code2 = tmp[1]
                            code3 = tmp[2]

                    while True:
                        tmp = self.easyDoWhile(code1, code3, self._mmrDecoder.getWhiteCode())
                        if not tmp[0]: break
                        else:
                            code2 = tmp[1]
                            code3 = tmp[2]

                if code1 > 0 or code2 > 0:
                    a0 = codingLine[codingI + 1] = a0 + code1
                    a0 = codingLine[codingI + 1] = a0 + code2

                    while self._width > referenceLine[referenceI] <= a0:
                        referenceI += 2

            elif code1 == MMRDecoder. twoDimensionalVertical0:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI]
                if referenceLine[referenceI] < self._width:
                    referenceI += 1

            elif code1 == MMRDecoder.twoDimensionalVerticalR1:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] + 1
                if referenceLine[referenceI] < self._width:
                    referenceI += 1
                    while a0 >= referenceLine[referenceI] < self._width:
                        referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalVerticalR2:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] + 2
                if referenceLine[referenceI] < self._width:
                    referenceI += 1
                    while a0 >= referenceLine[referenceI] < self._width:
                        referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalVerticalR3:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] + 3
                if referenceLine[referenceI] < self._width:
                    referenceI += 1
                    while a0 >= referenceLine[referenceI] < self._width:
                        referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalVerticalL1:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] - 1
                if referenceI > 0: referenceI -= 1
                else: referenceI += 1
                while a0 >= referenceLine[referenceI] < self._width:
                    referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalVerticalL2:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] - 2
                if referenceI > 0: referenceI -= 1
                else: referenceI += 1
                while a0 >= referenceLine[referenceI] < self._width:
                    referenceI += 2

            elif code1 == MMRDecoder.twoDimensionalVerticalL3:
                a0 = codingLine[codingI + 1] = referenceLine[referenceI] - 3
                if referenceI > 0: referenceI -= 1
                else: referenceI += 1
                while a0 >= referenceLine[referenceI] < self._width:
                    referenceI += 2

            else:
                if self.debug:
                    print("Illegal code in JBIG2 MMR bitmap data")

            return True, codingLine, codingI

        else:
            return False

    def easyDoWhile(self, code, code3, getBC):
        if code3 >= 64:
            code3 = getBC
            code += code3
            return True, code, code3
        else: return False






