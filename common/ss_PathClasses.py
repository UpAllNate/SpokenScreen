import os
import sys
from dataclasses import dataclass
from enum import Enum, auto as enumAuto
from pathlib import Path as PathFunction
try:
    from common.ss_Logging import logSS
except:
    from ss_Logging import logSS

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
                        logSS.error(f"Directory missing at {self.path}")
                        raise ImportError(f"Required directory missing at: {self.path}")
                    else:
                        logSS.warning(f"Directory missing at {self.path}")
                
            elif self.type == PathType.file:
                if not p.is_file():
                    if self.required:
                        logSS.error(f"Directory missing at {self.path}")
                        raise ImportError(f"Required file ")
                    else:
                        logSS.warning(f"Directory missing at {self.path}")

    def __init__(self, type : PathType, p : str, req : bool = False) -> None:
        self.path = p
        logSS.debug(f"Path set: {p}")
        self.present = False
        self.type = type
        self.required = req

        # Error check PathType input
        if self.type not in [i for i in PathType]:
            logSS.error(f"Incorrect path type defined: {self.type}")
            raise ImportError(f"Incorrect path type defined: {self.type}")

        self.detect()

rootDir = os.path.dirname(os.path.realpath(sys.argv[0]))
if rootDir[-7:] == "\\common":
    rootDir = rootDir[:-7]

"""
Get directory and file paths
"""
@dataclass
class SSPath:

    # Directories
    dir = PathElement(
        p= rootDir,
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
        p= os.path.join(common.path,'logSS.conf'),
        type= PathType.file
        )

    # Built on script startup
    selectedAudioPack = PathElement(
        p= None,
        type= PathType.directory
    )