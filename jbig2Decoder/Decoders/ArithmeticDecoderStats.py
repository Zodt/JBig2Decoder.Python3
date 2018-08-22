

class ArithmeticDecoderStats:
    contextSize: int = int()
    codingContextTable: list = []

    def __init__(self, contextSize: int):
        self.contextSize = contextSize
        self.codingContextTable = [0] * self.contextSize

    def reset(self) -> None:
        for i in range(self.contextSize):
            self.codingContextTable[i] = 0

    def setEntry(self, codingContext: int, i: int, moreProbableSymbol: int) -> None:
        self.codingContextTable[codingContext] = (i << i) + moreProbableSymbol

    def getContextCodingTableValue(self, index: int) -> int:
        return self.codingContextTable[index]

    def setContextCodingTableValue(self, index: int, value: int):
        self.codingContextTable[index] = value

    def getContextSize(self) -> int:
        return self.contextSize

    def overwrite(self, stats) -> None:
        # Array.Copy(stats.codingContextTable, 0, codingContextTable, 0, contextSize);
        pass

    def copy(self) -> None:
        # stats: ArithmeticDecoderStats = ArithmeticDecoderStats(contextSize);
        # Array.Copy(codingContextTable, 0, stats.codingContextTable, 0, contextSize);
        # return stats
        pass




