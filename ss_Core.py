import sys
import os
import imagehash
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
from enum import Enum, auto as enumAuto
import winsound
from common.ss_Logging import logSS
from common.ss_PathClasses import SSPath
from common.ss_ColorClasses import ColorScanInstance, ColorPure
from common.ss_PixelScanners import getPixelColumn, getPixelRow, pixelSequenceScan

def testColors():
    for i in range(1, 8):
        with Image.open('./common/testColors_' + str(i) + '.png', mode='r') as im:
            px = getPixelRow(im=im, row=im.height/2)
            print(f"Image {i}, px: {px}")


if __name__ == "__main__":             
    testColors()