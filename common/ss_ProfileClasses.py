
import tomli
import os
try:
    from common.ss_PathClasses import PathElement, SSPath, PathType
except:
    from ss_PathClasses import PathElement, SSPath, PathType
try:
    from common.ss_Logging import logSS
except:
    from ss_Logging import logSS



class AudioPackData:
    def __init__(self, title : str, authors : list[str] , packPath : str, adict : dict) -> None:
        self.title = title
        self.authors = authors
        self.path = packPath
        self.audioFileDict = adict

    def __str__(self):
        msg = f"AudioPack: {self.title}, Authors: "
        for i, a in enumerate(self.authors):
            msg += f"{a}"
            if i < len(self.authors) - 1:
                msg += ", "
        msg += "\n"
        return msg

class SSProfileInstance:
    def __init__(self : str, n, v : str, p : str, a : str, ali : list[AudioPackData]) -> None:
        self.name = n
        self.version = v
        self.path = p
        self.audioPacksPath = a
        self.audioPacksPathList = ali
    
    def __str__(self) -> str:
        return f"{self.name}, v{self.version}"

def findAllProfiles(reqSeq : bool, reqCol : bool, reqAud : bool) -> list[SSProfileInstance]:

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Loading profiles...")

    """
    Scan for all available profiles
    """
    allProfilePaths = [ f.path for f in os.scandir(SSPath.profiles.path) if f.is_dir()]

    validProfilePaths = []
    for profilePath in allProfilePaths:

        # Determine if valid run.toml
        try:
            runPath = os.path.join(profilePath,'run.toml')
            with open(runPath, 'rb') as f:
                a = tomli.load(f)
                profileName = a["name"]
                profileVersion = a["version"]
                _ = a["sequence"]
                _ = a["colors"]
                _ = a["initSequence"]
                _ = a["hash"]
        except KeyError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, missing key {e}")
            continue
        except FileNotFoundError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, missing run file {e}")
            continue
        except tomli.TOMLDecodeError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, cannot decode run.tomli... corrupted file: {e}")
            continue
        except Exception as e:
            logSS.critical(f"Unhandled exception at parse profiles: {e}")
            raise e

        if len(a["colors"]) == 0:
            logSS.warning(f"Invalid profile detected: {profilePath}, no colors in run.toml")
            if reqCol:
                continue
        
        if len(a["sequence"]) == 0:
            logSS.warning(f"Invalid profile detected: {profilePath}, no sequences in run.toml")
            if reqSeq:
                continue

        # At this point, run.toml is presumed to be valid
        
        # Determine if this profile has the required Audio Packs directory
        audioPath = PathElement(PathType.directory, os.path.join(profilePath, "Audio Packs"))
        if not audioPath.detect():
            logSS.warning(f"Invalid profile detected: {profilePath}, does not have Audio Packs folder")
            continue

        allValidAudioPacks : list[AudioPackData] = []

        # Scan the AudioPack directory for all folders
        audioPackPaths = [ a.path for a in os.scandir(audioPath.path) if a.is_dir()]

        # Compile only those directories with an Audio Pack Description file that contains a title and hash table
        for packDir in audioPackPaths:

            # Audio Pack Description
            filePathStr = os.path.join(packDir,'desc.toml')           
            try:
                desc = tomli.load(open(filePathStr, 'rb'))
                title = desc["title"]
                authors = desc["authors"]
            except KeyError as e:
                logSS.warning(f"Invalid Audio Pack detected in: {profilePath}, pack: {packDir} missing key {e}")
                continue
            except FileNotFoundError as e:
                logSS.warning(f"Invalid Audio Pack detected in: {profilePath}, pack: {packDir} missing desc file {e}")
                continue
            except tomli.TOMLDecodeError as e:
                logSS.warning(f"Invalid Audio Pack detected in: {profilePath}, pack: {packDir} has desc.toml that cannot be decoded")
                continue
            except Exception as e:
                logSS.critical(f"Unhandled exception at parse audio packs: {e}")
                raise e

            # Get all numerically named .wav files in pack directory
            aDict = { fileName.split('.')[0]:fileName for fileName in [f for f in os.listdir(dir) if f.endswith('.wav') and f.split('.')[0].isnumeric()]}

            if len(aDict) == 0 and reqAud:
                logSS.warning(f"Invalid Audio Pack detected in: {profilePath}, pack: {packDir} has no valid audio files")
                continue

            allValidAudioPacks.append(AudioPackData(title, authors, filePathStr, aDict))
        
        if len(allValidAudioPacks) == 0 and reqAud:
            logSS.warning(f"Invalid Profile detected in: {profilePath}, has no valid Audio Pack")
            continue

        validProfilePaths.append(SSProfileInstance(profileName, profileVersion, profilePath, audioPath.path, allValidAudioPacks))

    return validProfilePaths

