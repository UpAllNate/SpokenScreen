import sys
import os
import imagehash
import numpy
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
from enum import Enum, auto as enumAuto
import winsound
from common.ss_Logging import logSS
from common.ss_PathClasses import SSPath
from common.ss_ColorClasses import *
from common.ss_PixelScanners import *
from typing import Any
import toml

def getDVal(d : dict, listPath : list) -> Any:
    for key in listPath:
        d = d[key]
    return d

def testColors():

    c = [
        ColorScanInstance(color=(237, 28, 36),tolerance=0,pure=ColorPure.required), # Red
        ColorScanInstance(color=(34, 177, 76),tolerance=0,pure=ColorPure.required), # Green
        ColorScanInstance(color=(0, 162, 232),tolerance=0,pure=ColorPure.required) # Green
    ]

    for i in range(1, 8):
        with Image.open('./tests/testColors_' + str(i) + '.png', mode='r') as im:
            px = getPixelRow_Pixel(im=im, row=im.height/2)
            # print(px)
            print("\n\n\n")

            logSS.info(f"Tests for image {i}, total width: {len(px)}")

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.required, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Zero tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 3, 120, 3
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.required, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Adequate tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.notRequired, ColorPure.notRequired, ColorPure.notRequired
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Non-required test... Success: {result}")
            for color in colors:
                logSS.info(color)

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 150, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.notRequired, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Required Red/Blue, Toleranced/NonRequired Green... Success: {result}")
            for color in colors:
                logSS.info(color)

class SSProfileInstance:
    def __init__(self, n, v, p) -> None:
        self.name = n
        self.version = v
        self.path = p
    
    def __str__(self) -> str:
        return f"Name: {self.name}, Version: {self.version}"

def findAllProfiles() -> list[SSProfileInstance]:
    """
    Scan for all available profiles
    """
    allProfilePaths = [ f.path for f in os.scandir(SSPath.profiles.path) if f.is_dir()]

    validProfilePaths = []
    for profilePath in allProfilePaths:
        try:
            runPath = os.path.join(profilePath,'run.toml')
            with open(runPath) as f:
                a = toml.load(f)
                profileName = a["name"]
                profileVersion = a["version"]
        except:
            pass
        else:
            validProfilePaths.append(SSProfileInstance(profileName, profileVersion,profilePath))
    
    return validProfilePaths

if __name__ == "__main__":

    allProfiles = findAllProfiles()

    for p in allProfiles:
        print(p)

    while True:
        # Screenshot is a PIL Image class PNG of (r,g,b,alpha)
        screenShot_Whole_Image = ImageGrab.grab()
        screenShot_Whole_npArray = numpy.array(screenShot_Whole_Image).tolist()
    


