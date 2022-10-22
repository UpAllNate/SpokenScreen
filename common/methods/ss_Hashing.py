from PIL.Image import Image as ImageClass
from time import perf_counter
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
                        flat_duration : int, 
                        start_seconds : float
                        ) -> tuple[bool, imagehash.ImageHash, float]:
    
    # Initialize if there is no previous hash
    if prevHash is None:
        prevHash = hash
        start_seconds = 0
        flat = False
        diff = 0
    else:
        
        # this uses the imagehash "hamming window" to find
        # the similarity between two hash's original images
        diff = hash - prevHash

        if diff <= diffTol:
            start_seconds += 1
        else:
            start_seconds = 0

        flat = True if start_seconds >= flat_duration else False

    print(f"count: {start_seconds}, diff: {diff}, flat: {flat}")
    return flat, hash, start_seconds