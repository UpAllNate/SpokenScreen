from PIL.Image import Image as ImageClass
from time import perf_counter
from imagehash import ImageHash
from numpy import ndarray

def dhash_ndArray(arr : ndarray) -> ImageHash:
    diff = arr[:, 1:] > arr[:, :-1]
    return ImageHash(diff)

def computeHash_DHash(im_ndarray : ndarray):
    return dhash_ndArray(im_ndarray)

def computeHashFlatness(
                        hash : ImageHash,
                        prevHash : ImageHash,
                        diffTol : int, 
                        flat_duration : int, 
                        start_seconds : float
                        ) -> tuple[bool, ImageHash, float]:
    
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
            flat_time = perf_counter() - start_seconds
        else:
            start_seconds = perf_counter()

        flat = True if flat_time >= flat_duration else False

    print(f"count: {start_seconds}, diff: {diff}, flat: {flat}")
    return flat, hash, start_seconds