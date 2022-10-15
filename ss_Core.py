import sys
import os
import imagehash
import numpy
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
from enum import Enum, auto as enumAuto
import winsound
from common.ss_Logging import logSS
from common.ss_PathClasses import PathElement, PathType, SSPath, Path
from common.ss_ColorClasses import *
from common.methods.ss_Pixel import *
from common.ss_ProfileClasses import findAllProfiles, AudioPackData, ProfileInstance
from typing import Any
import tomli
import time
from common.ss_ExecuteTOMLscript import executeTOMLsequence

# Returns valid selection
def chooseFromList(prompt : str, l : list) -> int:
    choosing = True
    selectionMenu = prompt + "\n\n"

    while choosing:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for i, p in enumerate(l):
            selectionMenu += f"[{i}] : {str(p)}\n"

        selectionMenu += "\nPlease enter the selection number: "

        try:
            selection = int(input(selectionMenu))
        except KeyboardInterrupt:
            exit()
        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("That is not a number.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            if selection < 0 or selection >= len(l):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("That is not a valid selection")
                time.sleep(2)
            else:
                choosing = False

if __name__ == "__main__":

    allProfiles = findAllProfiles(reqSeq= True, reqCol= True, reqAud= True)

    profile = allProfiles[chooseFromList("Please choose from the following profiles:", allProfiles)]

    audioPack = profile.audioPacksList[chooseFromList("Please choose from the following audio packs:", profile.audioPacksList)]

    SSPath.selectedProfile.path = profile.path
    SSPath.selectedProfile.detect()

    SSPath.selectedAudioPack.path = audioPack.path
    SSPath.selectedAudioPack.detect()

    SSPath.runTOML.path = os.path.join(SSPath.selectedProfile.path, "run.toml")
    SSPath.runTOML.detect()

    run = tomli.load(open(SSPath.runTOML.path, 'rb'))

    while True:

        # Generate Core Features
        im = ImageGrab.grab()
        run["coreFeatures"]["screenShot_Whole_Image"] = im
        run["coreFeatures"]["screenShot_Whole_npArray"] = numpy.array(im)

        # Execute all sequences
        for seq in run["sequence"]:
            executeTOMLsequence(seq, run)