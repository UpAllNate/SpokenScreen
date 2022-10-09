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

def getPixelRow_Pixel(im : list[list[tuple[int,int,int,int]]], row : int,\
    limitPercent_Low : float = 0.0, limitPercent_High : float = 1.0) -> list[tuple[int,int,int]]:
    imLen = len(im)
    ll = int(imLen * limitPercent_Low)
    if ll < 0: ll = 0
    lh = int(imLen * limitPercent_High) + 1 # In python, ranges exclude the upper limit
    if lh > imLen: lh = imLen
    return im[row][ll:lh]

def getPixelColumn_Pixel(im : list[list[tuple[int,int,int,int]]], column : int, \
    limitPercent_Low : float = 0.0, limitPercent_High : float = 1.0) -> list[tuple[int,int,int]]:
    imLen = len(im[0])
    ll = int(imLen * limitPercent_Low)
    if ll < 0: ll = 0
    lh = int(imLen * limitPercent_High) + 1 # In python, ranges exclude the upper limit
    if lh > imLen: lh = imLen
    return [(row[column][0:3]) for row in im[ll:lh]]

def getPixelRow_Percent(im : list[list[tuple[int,int,int,int]]], percent : float, \
    limitPercent_Low : float = 0.0, limitPercent_High : float = 1.0) -> list[tuple[int,int,int]]:
    imLen = len(im)
    row = int(percent * imLen)
    if row >= imLen: row = imLen - 1
    return getPixelRow_Pixel(im=im, row=row, limitPercent_Low=limitPercent_Low, limitPercent_High=limitPercent_High)

def getPixelColumn_Percent(im : list[list[tuple[int,int,int,int]]], percent : float, \
    limitPercent_Low : float = 0.0, limitPercent_High : float = 1.0) -> list[tuple[int,int,int]]:
    imLen = len(im[0])
    column = int(percent * imLen)
    if column >= imLen: column = imLen - 1
    return getPixelColumn_Pixel(im=im, column=column, limitPercent_Low=limitPercent_Low, limitPercent_High=limitPercent_High)

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




