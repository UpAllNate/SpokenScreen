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