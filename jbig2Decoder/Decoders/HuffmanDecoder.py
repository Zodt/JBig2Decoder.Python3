from Decoders.DecodeIntResult import DecodeIntResult

class HuffmanDecoder():
    jbig2HuffmanLOW: int = 0xfffffffd
    jbig2HuffmanOOB: int = 0xfffffffe
    jbig2HuffmanEOT: int = 0xffffffff

    _reader = None # Big2StreamReader()

    huffmanTableA = [[0, 1, 4, 0x000], [16, 2, 8, 0x002],
                     [272, 3, 16, 0x006], [65808, 3, 32, 0x007], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableB = [[0, 1, 0, 0x000], [1, 2, 0, 0x002], [2, 3, 0, 0x006], [3, 4, 3, 0x00e], [11, 5, 6, 0x01e],
                     [75, 6, 32, 0x03e], [0, 6, jbig2HuffmanOOB, 0x03f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableC = [[0, 1, 0, 0x000], [1, 2, 0, 0x002], [2, 3, 0, 0x006], [3, 4, 3, 0x00e], [11, 5, 6, 0x01e],
                     [0, 6, jbig2HuffmanOOB, 0x03e], [75, 7, 32, 0x0fe], [-256, 8, 8, 0x0fe],
                     [-257, 8, jbig2HuffmanLOW, 0x0ff], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableD = [[1, 1, 0, 0x000], [2, 2, 0, 0x002], [3, 3, 0, 0x006], [4, 4, 3, 0x00e], [12, 5, 6, 0x01e],
                     [76, 5, 32, 0x01f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableE = [[1, 1, 0, 0x000], [2, 2, 0, 0x002], [3, 3, 0, 0x006], [4, 4, 3, 0x00e], [12, 5, 6, 0x01e],
                     [76, 6, 32, 0x03e], [-255, 7, 8, 0x07e], [-256, 7, jbig2HuffmanLOW, 0x07f],
                     [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableF = [[0, 2, 7, 0x000], [128, 3, 7, 0x002], [256, 3, 8, 0x003], [-1024, 4, 9, 0x008],
                     [-512, 4, 8, 0x009], [-256, 4, 7, 0x00a], [-32, 4, 5, 0x00b], [512, 4, 9, 0x00c],
                     [1024, 4, 10, 0x00d], [-2048, 5, 10, 0x01c], [-128, 5, 6, 0x01d], [-64, 5, 5, 0x01e],
                     [-2049, 6, jbig2HuffmanLOW, 0x03e], [2048, 6, 32, 0x03f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableG = [[-512, 3, 8, 0x000], [256, 3, 8, 0x001], [512, 3, 9, 0x002], [1024, 3, 10, 0x003],
                     [-1024, 4, 9, 0x008], [-256, 4, 7, 0x009], [-32, 4, 5, 0x00a], [0, 4, 5, 0x00b],
                     [128, 4, 7, 0x00c], [-128, 5, 6, 0x01a], [-64, 5, 5, 0x01b], [32, 5, 5, 0x01c], [64, 5, 6, 0x01d],
                     [-1025, 5, jbig2HuffmanLOW, 0x01e], [2048, 5, 32, 0x01f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableH = [[0, 2, 1, 0x000], [0, 2, jbig2HuffmanOOB, 0x001], [4, 3, 4, 0x004], [-1, 4, 0, 0x00a],
                     [22, 4, 4, 0x00b], [38, 4, 5, 0x00c], [2, 5, 0, 0x01a], [70, 5, 6, 0x01b], [134, 5, 7, 0x01c],
                     [3, 6, 0, 0x03a], [20, 6, 1, 0x03b], [262, 6, 7, 0x03c], [646, 6, 10, 0x03d], [-2, 7, 0, 0x07c],
                     [390, 7, 8, 0x07d], [-15, 8, 3, 0x0fc], [-5, 8, 1, 0x0fd], [-7, 9, 1, 0x1fc], [-3, 9, 0, 0x1fd],
                     [-16, 9, jbig2HuffmanLOW, 0x1fe], [1670, 9, 32, 0x1ff], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableI = [[0, 2, jbig2HuffmanOOB, 0x000], [-1, 3, 1, 0x002], [1, 3, 1, 0x003], [7, 3, 5, 0x004],
                     [-3, 4, 1, 0x00a], [43, 4, 5, 0x00b], [75, 4, 6, 0x00c], [3, 5, 1, 0x01a], [139, 5, 7, 0x01b],
                     [267, 5, 8, 0x01c], [5, 6, 1, 0x03a], [39, 6, 2, 0x03b], [523, 6, 8, 0x03c], [1291, 6, 11, 0x03d],
                     [-5, 7, 1, 0x07c], [779, 7, 9, 0x07d], [-31, 8, 4, 0x0fc], [-11, 8, 2, 0x0fd], [-15, 9, 2, 0x1fc],
                     [-7, 9, 1, 0x1fd], [-32, 9, jbig2HuffmanLOW, 0x1fe], [3339, 9, 32, 0x1ff],
                     [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableJ = [[-2, 2, 2, 0x000], [6, 2, 6, 0x001], [0, 2, jbig2HuffmanOOB, 0x002], [-3, 5, 0, 0x018],
                     [2, 5, 0, 0x019], [70, 5, 5, 0x01a], [3, 6, 0, 0x036], [102, 6, 5, 0x037], [134, 6, 6, 0x038],
                     [198, 6, 7, 0x039], [326, 6, 8, 0x03a], [582, 6, 9, 0x03b], [1094, 6, 10, 0x03c],
                     [-21, 7, 4, 0x07a], [-4, 7, 0, 0x07b], [4, 7, 0, 0x07c], [2118, 7, 11, 0x07d], [-5, 8, 0, 0x0fc],
                     [5, 8, 0, 0x0fd], [-22, 8, jbig2HuffmanLOW, 0x0fe], [4166, 8, 32, 0x0ff],
                     [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableK = [[1, 1, 0, 0x000], [2, 2, 1, 0x002], [4, 4, 0, 0x00c], [5, 4, 1, 0x00d], [7, 5, 1, 0x01c],
                     [9, 5, 2, 0x01d], [13, 6, 2, 0x03c], [17, 7, 2, 0x07a], [21, 7, 3, 0x07b], [29, 7, 4, 0x07c],
                     [45, 7, 5, 0x07d], [77, 7, 6, 0x07e], [141, 7, 32, 0x07f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableL = [[1, 1, 0, 0x000], [2, 2, 0, 0x002], [3, 3, 1, 0x006], [5, 5, 0, 0x01c], [6, 5, 1, 0x01d],
                     [8, 6, 1, 0x03c], [10, 7, 0, 0x07a], [11, 7, 1, 0x07b], [13, 7, 2, 0x07c], [17, 7, 3, 0x07d],
                     [25, 7, 4, 0x07e], [41, 8, 5, 0x0fe], [73, 8, 32, 0x0ff], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableM = [[1, 1, 0, 0x000], [2, 3, 0, 0x004], [7, 3, 3, 0x005], [3, 4, 0, 0x00c], [5, 4, 1, 0x00d],
                     [4, 5, 0, 0x01c], [15, 6, 1, 0x03a], [17, 6, 2, 0x03b], [21, 6, 3, 0x03c], [29, 6, 4, 0x03d],
                     [45, 6, 5, 0x03e], [77, 7, 6, 0x07e], [141, 7, 32, 0x07f], [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableN = [[0, 1, 0, 0x000], [-2, 3, 0, 0x004], [-1, 3, 0, 0x005], [1, 3, 0, 0x006], [2, 3, 0, 0x007],
                     [0, 0, jbig2HuffmanEOT, 0]]

    huffmanTableO = [[0, 1, 0, 0x000], [-1, 3, 0, 0x004], [1, 3, 0, 0x005], [-2, 4, 0, 0x00c], [2, 4, 0, 0x00d],
                     [-4, 5, 1, 0x01c], [3, 5, 1, 0x01d], [-8, 6, 2, 0x03c], [5, 6, 2, 0x03d], [-24, 7, 4, 0x07c],
                     [9, 7, 4, 0x07d], [-25, 7, jbig2HuffmanLOW, 0x07e], [25, 7, 32, 0x07f],
                     [0, 0, jbig2HuffmanEOT, 0]]

    def __init__(self, reader):
        self._reader = reader

    def decodeInt(self, table: list) -> DecodeIntResult:
        length: int = 0
        prefix: int = 0

        index: int = 0

        while table[index][2] != self.jbig2HuffmanEOT:
            while length < table[index][1]:
                bit = self._reader.readBit()
                prefix = (prefix << 1) | bit
                length += 1
            if prefix == table[index][3]:

                if table[index][2] == self.jbig2HuffmanOOB:
                    return DecodeIntResult(self, -1, False)

                decodedInt: int = int()

                if table[index][2] == self.jbig2HuffmanLOW:
                    readBits = self._reader.readBits(32)
                    decodedInt = table[index][0] - readBits

                elif table[index][2] > 0:
                    readBits = self._reader.readBits(table[index][2])
                    decodedInt = table[index][0] + readBits

                else:
                    decodedInt = table[index][0]

                return DecodeIntResult(self, decodedInt, True)

        return DecodeIntResult(self, -1, False)

    def buildTable(self, table: list, length: int) -> list:
        i: int = int()
        j: int = int()
        k: int = int()
        prefix: int = int()
        tab = []

        for i in range(length):
            j = i
            while j < length and table[j][1] == 0: j += 1

            if j == length:
                break

            for k in range(j+1, length):
                if 0 < table[k][1] < table[j][1]:
                    j = k

            if j != 1:
                tab = table[j]
                for k in range(j, i, -1):
                    table[k] = table[k-1]
                table[i] = tab
        table[i] = table[length]

        i = 0
        table[i + 1][3] = prefix + 1

        while table[i][2] != self.jbig2HuffmanEOT:
            prefix <<= int(table[i][1] - table[i-1][1])
            table[i][3] = prefix + 1
            i += 1

        return table

