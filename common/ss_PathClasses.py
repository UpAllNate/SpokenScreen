from dataclasses import dataclass
from enum import Enum, auto as enumAuto
from pathlib import Path
try:
    from common.ss_Logging import logSS
except:
    from ss_Logging import logSS

class PathType(Enum):
    DIRECTORY = enumAuto()
    FILE = enumAuto()

class PathElement:

    def detect(self) -> bool:

        # Error check presence of directory / file
        if self.path_str is not None:
            
            if self.type == PathType.DIRECTORY:
                if not self.path_obj.is_dir():
                    self.present = False
                    if self.required:
                        logSS.error(f"Directory missing at {self.path_str}")
                        raise ImportError(f"Required directory missing at: {self.path_str}")
                    else:
                        logSS.warning(f"Directory missing at {self.path_str}")
                else:
                    self.present = True
                
            elif self.type == PathType.FILE:
                if not self.path_obj.is_file():
                    self.present = False
                    if self.required:
                        logSS.error(f"Directory missing at {self.path_str}")
                        raise ImportError(f"Required file ")
                    else:
                        logSS.warning(f"Directory missing at {self.path_str}")
                else:
                    self.present = True

        return self.present
    
    def update_path_str(self, new_path_str : str) -> None:
        self.path_str = new_path_str
        self.path_obj = Path(new_path_str)

        print("path_str update: ",self.path_str, self.path_obj)

        self.detect()

    def update_path_obj(self, new_path_obj : Path) -> None:
        self.path_obj = new_path_obj
        self.path_str = str(new_path_obj)

        print("path_obj update: ",self.path_str, self.path_obj)

        self.detect()

    def __init__(self, type : PathType, path_obj : Path = None, path_str : str = None, req : bool = False):
        
        self.type = type

        err = ""
        # Error check PathType input
        if self.type.__class__ is not PathType:
            err = "Path type must be of PathType class"
        elif self.type not in PathType:
            err = "Path type enum is not in class definition"

        if err != "":
            err = f"Incorrect path type defined: {self.type}, err: {err}, path: {self.path_str}"
            logSS.critical(err)
            raise ImportError(err)
        
        self.required = req

        # Set path string and Path object
        if path_obj is not None:
            self.update_path_obj(path_obj)
        elif path_str is not None:
            self.update_path_str(path_str)
        else:
            self.update_path_str("")

        logSS.debug(f"Path set: {path_str}")
    
    def __str__(self) -> str:
        return f"PathElement object with path: {self.path_str}"

"""
Get directory and file paths
"""
@dataclass
class SSPath:

    # Directories
    root = PathElement(
        path_obj= Path(__file__).parent.parent.resolve(),
        type= PathType.DIRECTORY
        )
    common = PathElement(
        path_obj= Path.joinpath(root.path_obj,'common'),
        type= PathType.DIRECTORY
        )
    screenshot = PathElement(
        path_obj= Path.joinpath(common.path_obj, 'screenshot'),
        type= PathType.DIRECTORY
        )
    detection = PathElement(
        path_obj= Path.joinpath(screenshot.path_obj, 'detection'),
        type= PathType.DIRECTORY
        )
    logShots = PathElement(
        path_obj= Path.joinpath(screenshot.path_obj,'logShots'),
        type= PathType.DIRECTORY
        )
    profiles = PathElement(
        path_obj= Path.joinpath(root.path_obj,'Profiles'),
        type= PathType.DIRECTORY
    )

    # Files
    file_logConfig = PathElement(
        path_obj= Path.joinpath(common.path_obj,'logging.conf'),
        type= PathType.FILE,
        req= True
    )

    # Built on script startup
    selectedProfile = PathElement(
        type= PathType.DIRECTORY
    )

    selectedAudioPack = PathElement(
        type= PathType.DIRECTORY
    )

    runTOML = PathElement(
        type= PathType.FILE
    )