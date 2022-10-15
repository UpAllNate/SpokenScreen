from PIL import Image, ImageGrab
from PIL.Image import Image
import numpy
from numpy import ndarray

def screenshot() -> Image:
    return ImageGrab.grab()

def makeNPArray(im : Image) -> ndarray:
    return numpy.array(im)

def flexCropImage(im : Image, left, top, right, bottom, horizontalCount : int = None, verticalCount : int = None) -> Image | list(Image):

    if horizontalCount is None: horizontalCount = 1
    if verticalCount is None: verticalCount = 1

    if horizontalCount == 1 and verticalCount == 1:
        return im.crop(left, top, right, bottom)
    else:
        returnWidth = int((right - left) / horizontalCount)
        returnHeight = int((bottom - top) / verticalCount)

        returnImageList = []
        for hPiece in range(horizontalCount):
            for vPiece in range(verticalCount):
                pieceLeft = left + hPiece * returnWidth
                pieceTop = top + vPiece * returnHeight
                returnImageList.append(im.crop(pieceLeft, pieceTop, returnWidth, returnHeight))

        return returnImageList

def mergeImages_Vertical(*images : Image | list[Image]) -> Image:

    # compile list of images
    imageList : list[Image] = []
    for arg in images:
        if isinstance(arg, list):
            imageList.extend(arg)
        else:
            imageList.append(arg)

    # find total image height
    totalHeight = 0
    for image in imageList:
        totalHeight += image.height

    # create new image to hold all others
    returnImage = Image.new('RGBA', (imageList[0].width, totalHeight))

    # paste images, top to bottom
    yOffset = 0
    for image in imageList:
        image.paste(returnImage, (0, yOffset))
        yOffset += image.height

    return returnImage

