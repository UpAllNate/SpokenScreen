from PIL import Image
import imagehash

def computeHash_DHash(im : Image, size : int = None):
    if size is None:
        return imagehash.dhash(im)
    else:
        return imagehash.dhash(im, size)