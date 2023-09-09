from fileinput import filename
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
import numpy
from numpy import ndarray
from typing import Union
from common.ss_namespace_methods import NamespaceMethods


@NamespaceMethods.register
def screenshot() -> ImageClass:
    return ImageGrab.grab()

@NamespaceMethods.register
def make_np_array(im : ImageClass) -> ndarray:
    return numpy.array(im)

@NamespaceMethods.register
def flexCropImage(im : Image, left, top, right, bottom, horizontalCount : int = None, verticalCount : int = None):

    if horizontalCount is None: horizontalCount = 1
    if verticalCount is None: verticalCount = 1

    if horizontalCount == 1 and verticalCount == 1:
        return im.crop((left, top, right, bottom))
    else:
        returnWidth = int((right - left + 1) / horizontalCount)
        returnHeight = int((bottom - top + 1) / verticalCount)

        returnImageList = []
        for hPiece in range(horizontalCount):
            for vPiece in range(verticalCount):
                pieceLeft = left + hPiece * returnWidth
                pieceTop = top + vPiece * returnHeight
                returnImageList.append(im.crop((pieceLeft, pieceTop, pieceLeft + returnWidth, pieceTop + returnHeight)))
        return returnImageList

@NamespaceMethods.register
def mergeImages_Vertical(*images : ImageClass | list[ImageClass]) -> Image:

    # compile list of images
    imageList : list[ImageClass] = []
    for arg in images:
        if isinstance(arg, list):
            for im in arg:
                if isinstance(im, list):
                    for i in im:
                        imageList.append(i)
                else:
                    imageList.append(im)
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
        returnImage.paste(image, (0, yOffset))
        yOffset += image.height

    return returnImage

@NamespaceMethods.register
def saveImage(im : Image, fileNombre : str) -> bool:
    try:
        im.save(fileNombre)
    except:
        return False
    else:
        return True