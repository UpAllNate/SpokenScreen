import sys
import os
import imagehash
from pathlib import Path as PathFunction
import logging
import logging.config
from PIL import Image, ImageGrab
from enum import Enum, auto as enumAuto
import winsound
import time
from datetime import datetime

# Set up logging if this is __main__
if __name__ == "__main__":

    # Verify that file exists: .\common\logging.conf
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    file = os.path.join(dir, "common\\logging.conf")

    p = PathFunction(file)
    if not p.is_file():
        raise ImportError(f"Logging config file file missing at {dir}")

    """
    Set up logging. There are two logs:
        The stream printed directly to console
        The detailed info printed to a rotating log file in .\logging.conf
    """
    logging.config.fileConfig(file, disable_existing_loggers=False)

class PathType(Enum):
    directory = enumAuto()
    file = enumAuto()

class PathElement:
    def detect(self) -> bool:
        # Error check presence of directory / file
        if self.path is not None:
            p = PathFunction(self.path)
            if self.type == PathType.directory:
                if not p.is_dir():
                    if self.required:
                        logging.error(f"Directory missing at {self.path}")
                        raise ImportError(f"Required directory missing at: {self.path}")
                    else:
                        logging.warning(f"Directory missing at {self.path}")
                
            elif self.type == PathType.file:
                if not p.is_file():
                    if self.required:
                        logging.error(f"Directory missing at {self.path}")
                        raise ImportError(f"Required file ")
                    else:
                        logging.warning(f"Directory missing at {self.path}")

    def __init__(self, type : PathType, p : str, req : bool = False) -> None:
        self.path = p
        logging.debug(f"Path set: {p}")
        self.present = False
        self.type = type
        self.required = req

        # Error check PathType input
        if self.type not in [i for i in PathType]:
            logging.error(f"Incorrect path type defined: {self.type}")
            raise ImportError(f"Incorrect path type defined: {self.type}")

        self.detect()

def getPixelRow(im : Image, row : int) -> list[tuple[int,int,int]]:
    return [im.getpixel((i, row)) for i in range(im.width)]

def getPixelColumn(im : Image, column : int) -> list[tuple[int,int,int]]:
    return [im.getpixel((column, i)) for i in range(im.height)]

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
def ColorWithinTolerance(color : tuple[int, int, int], target : tuple[int, int, int], tolerance : int = 0) -> bool:
    if len(color) != len(target):
        logging.error(f"ColorWithinTolerance received color and target of different lengths: {len(color)}, {len(target)}")
        return False
    for (bC, bT) in list(zip(color, target)):
        if bC > bT + tolerance or bC < bT - tolerance:
            return False
    return True


# Returns detection result as bool and ColorScanInstance
# of single instance or equal list length
def pixelSequenceScan(pixels : list[tuple[int,int,int]],\
     colors : list[ColorScanInstance] | ColorScanInstance)\
            -> tuple(bool, list[ColorScanInstance] | ColorScanInstance):

    ####################################################
    #               Error Handling
    ####################################################
    if isinstance(colors,ColorScanInstance):
        colors = list(colors)
        singleColorInstance = True
    else:
        singleColorInstance = False

    if not isinstance(colors[0],ColorScanInstance):
        logging.error(f"Attempted to run pixelSequenceScan with invalid input: Not instance or list of ColorScanInstance")
        return False, colors

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
        if ColorWithinTolerance(
            color=colors[cIndex].color,
            target=pxColor,
            tolerance=colors[cIndex].tolerance
            ):

            # Only for pixel 0, set start on initial detection
            if colors[cIndex].startPixel is None:
                colors[cIndex].startPixel = px
            
            # Get the current pixel every time it matches
            colors[cIndex].endPixel = px

            # If the last color in the sequence matches the last pixel, set the endPixel
            if px == len(pixels) - 1 and cIndex == len(colors) - 1 :
                if singleColorInstance: 
                    return True, colors[0]
                else: 
                    return True, colors

        # If this pixel doesn't match the current scan color...
        elif colors[cIndex].startPixel is not None:

            # Check if there is a next color
            if cIndex != len(colors) - 1:

                # Check if the next color matches the current  pixel
                if ColorWithinTolerance(
                    color=colors[cIndex + 1].color,
                    target=pxColor,
                    tolerance=colors[cIndex + 1].tolerance
                    ):

                    # If so, increment to the next color and set
                    # the start pixel
                    cIndex += 1
                    colors[cIndex].startPixel = px
                    colors[cIndex].endPixel = px
                
                # If the next color doesn't match the current pixel...
                else:

                    # Check if this is a "pure" required color
                    if colors[cIndex].pure == ColorPure.required:

                        # If so, reset the entire sequence
                        colors = clearColorScanPixels(colors)
                        cIndex = 0
                    
                    # Break regardless
                    break
            
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

    colors = clearColorScanPixels(colors)

    if singleColorInstance:
        return False, colors[0]
    else:
        return False, colors

if __name__ == "__main__":             
    """
    Get directory and file paths
    """
    class SSPath:

        # Directories
        dir = PathElement(
            p= os.path.dirname(
                os.path.realpath(sys.argv[0])
                ),
            type= PathType.directory
            )
        common = PathElement(
            p= os.path.join(dir.path,'common'),
            type= PathType.directory
            )
        AudioPacks = PathElement(
            p= os.path.join(dir.path,'Audio Packs'),
            type= PathType.directory
            )
        screenshot = PathElement(
            p= os.path.join(common.path, 'screenshot'),
            type= PathType.directory
            )
        detection = PathElement(
            p= os.path.join(screenshot.path, 'detection'),
            type= PathType.directory
            )
        logShots = PathElement(
            p= os.path.join(screenshot.path,'logShots'),
            type= PathType.directory
            )
        
        # Files
        file_logConfig = PathElement(
            p= os.path.join(common.path,'logging.conf'),
            type= PathType.file
            )

        # Built on script startup
        selectedAudioPack = PathElement(
            p= None,
            type= PathType.directory
        )