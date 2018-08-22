from  Image.JBig2Image import JBIG2Bitmap

class BitmapPointer:
    _x: int = int()
    _y: int = int()
    _width: int = int()
    _height: int = int()
    _bits: int = int()
    _count: int = int()
    _output: bool = bool()
    _bitmap: JBIG2Bitmap = None

    def __init__(self, bitmap: JBIG2Bitmap):
        self._bitmap = bitmap
        self._height = bitmap.getHeight()
        self._width = bitmap.getWidth()

    def setPointer(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

        self._output = True

        if self._y < 0 or self._y >= self._height or self._x >= self._width:
            self._output = False

        self._count = self._y * self._width

    def nextPixel(self) -> int:
        if not self._output:
            return 0
        elif self._x < 0 or self._x >= self._width:
            self._x += 1
            return 0

        return 1 if self._bitmap.data.get(int(self._count + self._x + 1)) else 0

















