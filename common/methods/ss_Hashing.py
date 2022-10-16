from PIL.Image import Image as ImageClass
import imagehash

def computeHash_DHash(im : ImageClass, size : int = None):
    if size is None:
        return imagehash.dhash(im)
    else:
        return imagehash.dhash(im, size)

def computeHashFlatness(
                        hash : imagehash.ImageHash,
                        prevHash : imagehash.ImageHash,
                        diffTol : int, 
                        countThresh : int, 
                        currentCount : int
                        ) -> tuple(bool, imagehash.ImageHash, int):
    
    # Initialize if there is no previous hash
    if prevHash is None:
        prevHash = hash
        currentCount = 0
        flat = True
    else:
        
        # this uses the imagehash "hamming window" to find
        # the similarity between two hash's original images
        diff = hash - prevHash

        if diff <= diffTol:
            currentCount += 1
        else:
            currentCount = 0

        flat = True if currentCount >= countThresh else False

    return flat, hash, currentCount