try:
    from common.ss_Logging import logSS
except:
    from ss_Logging import logSS

try:
    from common.ss_ColorClasses import ColorScanInstance, ColorPure
except:
    from ss_ColorClasses import ColorScanInstance, ColorPure

try:
    from common.ss_ColorMethods import clearColorScanPixels, colorWithinTolerance
except:
    from ss_ColorMethods import clearColorScanPixels, colorWithinTolerance

from PIL.Image import Image as ImageClass

def getPixelRow_Absolute(im : list[list[tuple[int,int,int,int]]], row : int, limitPixel_Low : int = None, limitPixel_High : int = None) -> list[list[int,int,int]]:
    numberOfRows = len(im)

    if limitPixel_Low is None: limitPixel_Low = 0
    if limitPixel_High is None: limitPixel_High = numberOfRows + 1

    return im[row][limitPixel_Low:limitPixel_High]

def getPixelColumn_Absolute(im : list[list[tuple[int,int,int,int]]], column : int, limitPixel_Low : int = None, limitPixel_High : int = None) -> list[list[int,int,int]]:
    numberOfColumns = len(im[0]) # How many columns

    if limitPixel_Low is None: limitPixel_Low = 0
    if limitPixel_High is None: limitPixel_High = numberOfColumns + 1

    return [(row[column][0:3]) for row in im[limitPixel_Low:limitPixel_High]]

def getPercentOfRange(low, high, percent : float):
    len = high - low
    if percent <= 0.0:
        return low
    elif percent >= 1.0:
        return high
    else:
        return percent * len + low

def getPixelRow_Percent(im : list[list[tuple[int,int,int,int]]], percent : float, limitPercent_Low : float = None, limitPercent_High : float = None) -> list[list[int,int,int]]:
    numberOfRows = len(im)
    upperLimit = numberOfRows + 1

    if limitPercent_Low is None: limitPercent_Low = 0.0
    if limitPercent_High is None: limitPercent_High = 1.0

    row = int(getPercentOfRange(0, upperLimit, percent))
    limitPixel_Low = int(getPercentOfRange(0, upperLimit, limitPercent_Low))
    limitPixel_High = int(getPercentOfRange(0, upperLimit, limitPercent_High))

    return im[row][limitPixel_Low:limitPixel_High]

def getPixelColumn_Percent(im : list[list[tuple[int,int,int,int]]], percent : float, limitPercent_Low : float = None, limitPercent_High : float = None) -> list[list[int,int,int]]:
    numberOfColumns = len(im[0])
    upperLimit = numberOfColumns + 1

    if limitPercent_Low is None: limitPercent_Low = 0.0
    if limitPercent_High is None: limitPercent_High = 1.0

    column = int(getPercentOfRange(0, upperLimit, percent))
    limitPixel_Low = int(getPercentOfRange(0, upperLimit, limitPercent_Low))
    limitPixel_High = int(getPercentOfRange(0, upperLimit, limitPercent_High))

    return [(row[column][0:3]) for row in im[limitPixel_Low:limitPixel_High]]

# Returns detection result as bool and ColorScanInstance
# of single instance or equal list length
def pixelSequenceScan(pixels : list[tuple[int,int,int]],\
     colors : list[ColorScanInstance] | ColorScanInstance)\
            -> tuple[bool, list[ColorScanInstance] | ColorScanInstance]:

    ####################################################
    #               Error Handling
    ####################################################
    if isinstance(colors,ColorScanInstance):
        _ = []
        _.append(colors)
        colors = _
        singleColorInstance = True
    else:
        singleColorInstance = False

    if not isinstance(colors[0],ColorScanInstance):
        logSS.critical(f"pixelSequenceScan received colors input of invalid type: {colors[0].__class__.__name__}")
        raise TypeError(f"pixelSequenceScan received colors input of invalid type: {colors[0].__class__.__name__}")

    ####################################################
    #               Initialize
    ####################################################
    cIndex = 0

    # Initialize all pixel return values
    colors = clearColorScanPixels(colors)

    ####################################################
    #               Loop through pixels
    ####################################################
    for px, pxColor in enumerate(pixels):

        # Check if pixel is equal to pixel color
        if colorWithinTolerance(color=pxColor, target=colors[cIndex].color, tolerance=colors[cIndex].tolerance):

            # Only for colors[0], set start on initial detection
            if colors[cIndex].startPixel is None:
                colors[cIndex].startPixel = px
            
            # Get the current pixel every time it matches
            colors[cIndex].endPixel = px

            # If the last color in the sequence matches the last pixel, set Complete
            if px == len(pixels) - 1 and cIndex == len(colors) - 1 :
                if singleColorInstance: 
                    return True, colors[0]
                else: 
                    return True, colors

        # If this pixel doesn't match the current scan color...
        elif colors[cIndex].startPixel is not None:
            logSS.debug(f"Pixel {px} color: {pxColor} doesn't match current: {colors[cIndex]}")

            # Check if there is a next color
            if cIndex != len(colors) - 1:
                logSS.debug(f"Index {cIndex} is not the last color")

                # Check if the next color matches the current  pixel
                if colorWithinTolerance(color=pxColor, target=colors[cIndex + 1].color, tolerance=colors[cIndex + 1].tolerance):
                    logSS.debug(f"Pixel {px} color: {pxColor} matches next color: {colors[cIndex+1]}")

                    # If so, increment to the next color and set
                    # the start pixel
                    cIndex += 1
                    colors[cIndex].startPixel = px
                    colors[cIndex].endPixel = px
                
                # If the next color doesn't match the current pixel...
                else:
                    logSS.debug(f"Pixel {px} color: {pxColor} doesn't match next color: {colors[cIndex+1]}")

                    # Check if this is a "pure" required color
                    if colors[cIndex].pure == ColorPure.required:
                        logSS.debug(f"Currently considered color {colors[cIndex]} is pure, must reset sequence")

                        # If so, reset the entire sequence
                        colors = clearColorScanPixels(colors)
                        cIndex = 0
                    
                    # Break regardless
                    continue
            
            # If this is the last color in the sequence, end if it's
            # a pure required color
            else:
                if colors[cIndex].pure == ColorPure.required:
                    if singleColorInstance:
                        return True, colors[0]
                    else:
                        return True, colors

    # If the entire pixel set is scanned and the sequence
    # is not completed, return false

    if colors[-1].pure == ColorPure.notRequired and colors[-1].endPixel is not None:
        if singleColorInstance:
            return True, colors[0]
        else:
            return True, colors
    else:
        if singleColorInstance:
            return False, colors[0]
        else:
            return False, colors




