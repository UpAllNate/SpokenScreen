
from PIL import Image
from common.ss_Logging import logSS
from common.ss_ColorClasses import *
from common.ss_PixelScanners import *

def testColors():

    c = [
        Color(color=(237, 28, 36),tolerance=0,requirement=ColorRequirement.required), # Red
        Color(color=(34, 177, 76),tolerance=0,requirement=ColorRequirement.required), # Green
        Color(color=(0, 162, 232),tolerance=0,requirement=ColorRequirement.required) # Green
    ]

    for i in range(1, 8):
        with Image.open('./tests/testColors_' + str(i) + '.png', mode='r') as im:
            px = getPixelRow_Pixel(im=im, row=im.height/2)
            # print(px)
            print("\n\n\n")

            logSS.info(f"Tests for image {i}, total width: {len(px)}")

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].requirement, c[1].requirement, c[2].requirement = ColorRequirement.required, ColorRequirement.required, ColorRequirement.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Zero tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 3, 120, 3
            c[0].requirement, c[1].requirement, c[2].requirement = ColorRequirement.required, ColorRequirement.required, ColorRequirement.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Adequate tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].requirement, c[1].requirement, c[2].requirement = ColorRequirement.notRequired, ColorRequirement.notRequired, ColorRequirement.notRequired
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Non-required test... Success: {result}")
            for color in colors:
                logSS.info(color)

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 150, 0
            c[0].requirement, c[1].requirement, c[2].requirement = ColorRequirement.required, ColorRequirement.notRequired, ColorRequirement.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Required Red/Blue, Toleranced/NonRequired Green... Success: {result}")
            for color in colors:
                logSS.info(color)