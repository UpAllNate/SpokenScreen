try:
    from common.ss_ColorClasses import ColorScanInstance, ColorPure
except:
    from ss_ColorClasses import ColorScanInstance, ColorPure

def clearColorScanPixels(colors : list[ColorScanInstance] | ColorScanInstance) -> list[ColorScanInstance] | ColorScanInstance:
    
    # Initialize all pixel return values
    if isinstance(c, ColorScanInstance):
        colors.startPixel = None
        colors.endPixel = None
    else:
        for c in colors:
            c.startPixel = None
            c.endPixel = None
    return colors

# Checks that all color bands are within tolerance of target
def colorWithinTolerance(color : tuple[int, int, int], target : tuple[int, int, int], tolerance : int = 0) -> bool:
    for (bC, bT) in list(zip(color, target)):
        if bC > bT + tolerance or bC < bT - tolerance:
            return False
    return True