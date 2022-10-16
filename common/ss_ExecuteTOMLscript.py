from typing import Any

try:
    from common.methods.ss_Pixel import *
except:
    from methods.ss_Pixel import *

try:
    from common.methods.ss_Arithmetic import *
except:
    from methods.ss_Arithmetic import *

try:
    from common.methods.ss_Hashing import *
except:
    from methods.ss_Hashing import *

try:
    from common.methods.ss_Image import *
except:
    from methods.ss_Image import *

try:
    from common.ss_PathClasses import SSPath
except:
    from ss_PathClasses import SSPath

try:
    from common.ss_ColorClasses import ColorScanInstance, ColorPure
except:
    from ss_ColorClasses import ColorScanInstance, ColorPure

import tomli, tomli_w, copy

"""
These methods enable the functionality of 
"""

# Recursively dig through dictionary to retrieve value
def getDVal(d : dict, listPath : list) -> Any:
    for key in listPath:
        try:
            d = d[key]
        except:
            d = getattr(d, key)
    return d

# Return sorted list of numeric keys (sequence step indexes)
def parseSeqStepIndexes(seq : dict) -> list[str]:

    # Get all numeric keys as integers
    # (strings sort weird... [1, 10, 11, 2, 20...])
    steps = [int(step) for step in seq if step.isnumeric()]
    steps.sort()

    # Make them strings again
    return [str(step) for step in steps]

# For a function argument in a sequence step, retrive the desired value
def getArgVal(step : dict, arg : str, run : dict) -> Any:
    try:
        a = step[arg]
    except KeyError:
        return None
    argType, argValue = a[0], a[1]
    if argType == "run":
        return getDVal(run, argValue)
    if argType == "const":
        return argValue
    if argType == "colors":
        return [copy.deepcopy(run["colorInstances"][color]) for color in argValue]
    if argType == "color":
        return run["colorInstances"][argValue]

"""
These methods wrap the base python methods in a TOMLscript interpreter
"""
def seqEx_getPixelRow_Absolute(step : dict, run : dict) -> None:
    args = ["image", "row", "lowLimit", "highLimit"]
    [im, row, lowLimit, highLimit] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelRow_Absolute(im, row, lowLimit, highLimit)

def seqEx_getPixelColumn_Absolute(step : dict, run : dict) -> None:
    args = ["image", "column", "lowLimit", "highLimit"]
    [im, column, lowLimit, highLimit] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelColumn_Absolute(im, column, lowLimit, highLimit)

def seqEx_getPixelRow_Percent(step : dict, run : dict) -> None:
    args = ["image", "percent", "lowPercent", "highPercent"]
    [im, percent, lowPercent, highPercent] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelRow_Percent(im, percent, lowPercent, highPercent)

def seqEx_getPixelColumn_Percent(step : dict, run : dict) -> None:
    args = ["image", "percent", "lowPercent", "highPercent"]
    [im, percent, lowPercent, highPercent] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelColumn_Percent(im, percent, lowPercent, highPercent)

def seqEx_flexAdd(step : dict, run : dict) -> None:
   inputs = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "input"]
   print(inputs)    
   step["result"] = flexAdd(*inputs)

def seqEx_flexSubtract(step : dict, run : dict) -> None:
   inputs = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "input"]
   print(inputs)    
   step["result"] = flexSubtract(*inputs)

def seqEx_flexMultiply(step : dict, run : dict) -> None:
   inputs = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "input"]
   print(inputs)    
   step["result"] = flexMultiply(*inputs)

def seqEx_flexDivide(step : dict, run : dict) -> None:
   inputs = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "input"]
   print(inputs)    
   step["result"] = flexDivide(*inputs)

def seqEx_computeHash_DHash(step : dict, run : dict) -> None:
    args = ["image", "size"]
    [im, size] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = computeHash_DHash(im, size)

def seqEx_screenshot(step : dict, run : dict) -> None:
    step["result"] = screenshot()

def seqEx_makeNPArray(step : dict, run : dict) -> None:
    im = getArgVal(step, "image", run)
    step["result"] = makeNPArray(im)

def seqEx_flexCropImage(step : dict, run : dict) -> None:
    args = ["image", "left", "top", "right", "bottom", "horizontalCount", "verticalCount"]
    [im, left, top, right, bottom, horCount, vertCount] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = flexCropImage(im, left, top, right, bottom, horCount, vertCount)

def seqEx_mergeImages_Vertical(step : dict, run : dict) -> None:
    images = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "image"]  
    step["result"] = mergeImages_Vertical(images)

def seqEx_saveImage(step : dict, run : dict) -> None:
    args = ["image", "fileName"]
    [im, fileNombre] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = saveImage(im, fileNombre)

def seqEx_pixelSequenceScan(step : dict, run : dict) -> None:
    args = ["pixels", "colors"]
    [pixels, colors] = [getArgVal(step, arg, run) for arg in args]
    step["result"] = pixelSequenceScan(pixels, colors)

def seqEx_computHashFlatness(step : dict, run : dict) -> None:
    args = ["hash", "differenceTolerance", "flatCountThreshold", "prevHash", "currCount"]
    [hash, diffTol, countThresh, prevHash, currCount] = [getArgVal(step, arg, run) for arg in args]
    step["result"], prevHash, currCount = computeHashFlatness(hash, prevHash, diffTol, countThresh, currCount)
    step["prevHash"] = ["const", prevHash]
    step["currCount"] = ["const", currCount]

def seqEx_saveHash_IfNew(step : dict, run : dict) -> None:
    args = ["hash", "seq", "seqStr", "differenceTolerance"]
    [hash, seqDict, seqStr, diffTol] = [getArgVal(step, arg, run) for arg in args]

    seqHashObjectList : list[imagehash.ImageHash] = seqDict["hashObjectList"]

    for i, seqHash in enumerate(seqHashObjectList):
        if hash - seqHash <= diffTol:
            step["result"] = False
            return
    
    # hash is a new find!
    newHashID : int = run["hashCount"][1]
    run["hashCount"][1] += 1

    # update run hash database
    runHashes : dict = run["hash"]
    runHashes[newHashID] = [seqStr, str(hash), "", ""]

    # update seq hash lists
    seqHashIDList : list[int] = seqDict["hashIDList"]
    seqHashIDList.append(newHashID)
    seqHashObjectList.append(hash)

    step["result"] = True
    print("recorded new hash")

    return



"""
This dictionary is the link between the function text in a sequence step
and the actual method called.
"""
seqEx = {
    "getPixelRow_Absolute" : seqEx_getPixelRow_Absolute,
    "getPixelColumn_Absolute" : seqEx_getPixelColumn_Absolute,
    "getPixelRow_Percent" : seqEx_getPixelRow_Percent,
    "getPixelColumn_Percent" : seqEx_getPixelColumn_Percent,
    "flexAdd" : seqEx_flexAdd,
    "flexSubtract" : seqEx_flexSubtract,
    "flexMultiply" : seqEx_flexMultiply,
    "flexDivide" : seqEx_flexDivide,
    "computeHash_DHash" : seqEx_computeHash_DHash,
    "makeNPArray" : seqEx_makeNPArray,
    "flexCropImage" : seqEx_flexCropImage,
    "mergeImages_Vertical" : seqEx_mergeImages_Vertical,
    "saveImage" : seqEx_saveImage,
    "screenshot" : seqEx_screenshot,
    "pixelSequenceScan" : seqEx_pixelSequenceScan,
    "computeHashFlatness" : seqEx_computHashFlatness,
    "saveHash_IfNew" : seqEx_saveHash_IfNew
}

def initRun(filename_Run) -> dict:
    
    with open(filename_Run, 'rb') as f:
        run : dict = tomli.load(f)

    # create colorInstances dict
    run["colorInstances"] = {}

    # fill colorInstances with objects
    colors : dict = run["colors"]
    for key in colors.keys():
        (r, g, b) = colors[key]["color"]["r"], colors[key]["color"]["g"], colors[key]["color"]["b"]
        purity = ColorPure.required if colors[key]["pureReq"] == True else ColorPure.notRequired
        tolerance = colors[key]["tolerance"]

        run["colorInstances"][key] = ColorScanInstance((r,g,b), tolerance, purity)

    sequenceKeys : list(str) = run["sequence"].keys()

    # verify all sequences have a hashList
    for key in sequenceKeys:
        seq = run["sequence"][key]
        seq["hashIDList"] = []
        seq["hashObjectList"] = []

    # Check if the seq association is a valid
    # run["sequence"] key. If so, put the
    # hash definition values into the seq
    # runtime lists
    #
    # Entries in run["hash"] are:
    # {ID : (seqStr, hash, line text, character)}
    hashCount = 0
    for hashIDNumber in run["hash"]:
        hashCount += 1

        sequenceKey : str = run["hash"][hashIDNumber][0]
        hashObject = imagehash.hex_to_hash(run["hash"][hashIDNumber][1])

        if sequenceKey in sequenceKeys:
            run["sequence"][sequenceKey]["hashIDList"].append(hashIDNumber)
            run["sequence"][sequenceKey]["hashObjectList"].append(hashObject)
        else:
            logSS.critical(f"Invalid sequence key in hash table: {sequenceKey}. Revise run.toml.")
            raise ValueError(f"Invalid sequence key in hash table: {sequenceKey}. Revise run.toml.")

    run["hashCount"] = ["const", hashCount]

    return run

def updateRun(filename_Run, run : dict) -> None:

    exportRun = copy.deepcopy(run)

    sequenceKeys : list(str) = exportRun["sequence"].keys()

    # get rid of the sequence local hash lists
    for key in sequenceKeys:
        seq = exportRun["sequence"][key]
        try:
            seq.pop("hashIDList")
        except:
            pass
        try:
            seq.pop("hashObjectList")
        except:
            pass
    
    # get rid of the ColorScanInstance objects in run
    try:
        exportRun.pop("colorInstances")
    except:
        pass

    


"""
This function will accept any sequence dictionary and execute it.
The bool return is whether the sequence completes all steps
and the final step "continue" does not resolve to false.
"""
def executeTOMLsequence(seq : dict, run : dict) -> bool:

    stepIndexes = parseSeqStepIndexes(seq)

    for i, stepIndex in enumerate(stepIndexes):
        step = seq[stepIndex]

        funName = step["function"]
        #print(f"Step {stepIndex}: {funName}")
        seqEx[step["function"]](step, run)

        continueVal = getArgVal(step, "continue", run)

        if isinstance(continueVal, bool) and not continueVal:
            return False
    
    return True