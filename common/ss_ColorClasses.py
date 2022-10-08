from enum import Enum, auto as enumAuto

class ColorPure(Enum):
    required = enumAuto()
    notRequired = enumAuto()

class ColorScanInstance:
    def __init__(self, color : tuple[int,int,int], tolerance : int, pure : ColorPure) -> None:
        self.color = color
        self.pure = pure
        self.tolerance = tolerance
        self.startPixel = 0
        self.endPixel = 0
    
    def __str__(self) -> str:
        return f"Color: ({self.color[0]},{self.color[1]},{self.color[2]}), startPixel: {self.startPixel}, endPixel: {self.endPixel}"