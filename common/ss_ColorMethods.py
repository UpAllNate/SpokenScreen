try:
    from common.ss_ColorClasses import Color, ColorRequirement
except:
    from ss_ColorClasses import Color, ColorRequirement

def clearColorScanPixels(colors : list[Color] | Color) -> list[Color] | Color:
    
    # Initialize all pixel return values
    if isinstance(colors, Color):
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