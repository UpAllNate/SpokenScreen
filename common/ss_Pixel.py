try:
    from common.ss_Logging import logSS
except:
    from ss_Logging import logSS

try:
    from common.ss_ColorClasses import Color, ColorRequirement
except:
    from ss_ColorClasses import Color, ColorRequirement

import numpy
from common.ss_namespace_methods import NamespaceMethods

@NamespaceMethods.register
def get_pixel_row_absolute(im : numpy.ndarray, row : int, limitPixel_Low : int = None, limitPixel_High : int = None) -> numpy.ndarray:
    row_count = len(im)
    column_count = len(im[0])

    if limitPixel_Low is None: limitPixel_Low = 0
    if limitPixel_High is None: limitPixel_High = column_count + 1

    return im[row][limitPixel_Low:limitPixel_High]

@NamespaceMethods.register
def get_pixel_column_absolute(im : list[list[tuple[int,int,int,int]]], column : int, limitPixel_Low : int = None, limitPixel_High : int = None) -> list[list[int,int,int]]:
    row_count = len(im)
    column_count = len(im[0])

    if limitPixel_Low is None: limitPixel_Low = 0
    if limitPixel_High is None: limitPixel_High = row_count + 1

    return [row[column][:3] for row in im[limitPixel_Low:limitPixel_High]]

@NamespaceMethods.register
def get_percent_of_range(low, high, percent : float):
    len = high - low
    if percent <= 0.0:
        return low
    elif percent >= 1.0:
        return high
    else:
        return percent * len + low

@NamespaceMethods.register
def get_pixel_row_percent(
    im : list[list[tuple[int,int,int,int]]],
    percent : float,
    limitPercent_Low : float = None,
    limitPercent_High : float = None
) -> list[list[int,int,int]]:
    
    numberOfRows = len(im)
    numberOfColumns = len(im[0])

    if limitPercent_Low is None: limitPercent_Low = 0.0
    if limitPercent_High is None: limitPercent_High = 1.0

    row = int(get_percent_of_range(0, numberOfRows, percent))
    limitPixel_Low = int(get_percent_of_range(0, numberOfColumns, limitPercent_Low))
    limitPixel_High = int(get_percent_of_range(0, numberOfColumns, limitPercent_High))

    return im[row][limitPixel_Low:limitPixel_High]

@NamespaceMethods.register
def get_pixel_column_percent(
    im : list[list[tuple[int,int,int,int]]],
    percent : float,
    limitPercent_Low : float = None,
    limitPercent_High : float = None
) -> list[list[int,int,int]]:
    
    numberOfRows = len(im)
    numberOfColumns = len(im[0])

    if limitPercent_Low is None: limitPercent_Low = 0.0
    if limitPercent_High is None: limitPercent_High = 1.0

    column = int(get_percent_of_range(0, numberOfColumns + 1, percent))
    limitPixel_Low = int(get_percent_of_range(0, numberOfRows, limitPercent_Low))
    limitPixel_High = int(get_percent_of_range(0, numberOfRows, limitPercent_High))

    return [row[column] for row in im[limitPixel_Low:limitPixel_High]]

# Returns detection result as bool and ColorScanInstance
# of single instance or equal list length
@NamespaceMethods.register
def pixel_sequence_scan(pixels : list[tuple[int,int,int]],\
     colors : list[Color] | Color)\
            -> tuple[bool, list[Color] | Color]:

    ####################################################
    #               Error Handling
    ####################################################
    if isinstance(colors,Color):
        _ = []
        _.append(colors)
        colors = _
        singleColorInstance = True
    else:
        singleColorInstance = False

    if not isinstance(colors[0],Color):
        # logSS.critical(f"pixelSequenceScan received colors input of invalid type: {colors[0].__class__.__name__}")
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
                # logSS.debug(f"First color: {colors[cIndex]}, starts here")
            
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
            # logSS.debug(f"Pixel {px} color: {pxColor} doesn't match current: {colors[cIndex]}")

            # Check if there is a next color
            if cIndex != len(colors) - 1:
                # logSS.debug(f"Index {cIndex} is not the last color")

                # Check if the next color matches the current  pixel
                if colorWithinTolerance(color=pxColor, target=colors[cIndex + 1].color, tolerance=colors[cIndex + 1].tolerance):
                    # logSS.debug(f"Pixel {px} color: {pxColor} matches next color: {colors[cIndex+1]}")

                    # If so, increment to the next color and set
                    # the start pixel
                    cIndex += 1
                    colors[cIndex].startPixel = px
                    colors[cIndex].endPixel = px
                
                # If the next color doesn't match the current pixel...
                else:
                    # logSS.debug(f"Pixel {px} color: {pxColor} doesn't match next color: {colors[cIndex+1]}")

                    # Check if this is a "pure" required color
                    if colors[cIndex].requirement == ColorRequirement.required:
                        # logSS.debug(f"Currently considered color {colors[cIndex]} is pure, must reset sequence")

                        # If so, reset the entire sequence
                        colors = clearColorScanPixels(colors)
                        cIndex = 0
                    
                    # Break regardless
                    continue
            
            # If this is the last color in the sequence, end if it's
            # a pure required color
            else:
                if colors[cIndex].requirement == ColorRequirement.required:
                    if singleColorInstance:
                        return True, colors[0]
                    else:
                        return True, colors

    # If the entire pixel set is scanned and the sequence
    # is not completed, return false

    if colors[-1].requirement == ColorRequirement.notRequired and colors[-1].endPixel is not None:
        if singleColorInstance:
            return True, colors[0]
        else:
            return True, colors
    else:
        if singleColorInstance:
            return False, colors[0]
        else:
            return False, colors




