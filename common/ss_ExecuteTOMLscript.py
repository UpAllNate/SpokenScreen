from typing import Any
try:
    from common.methods.ss_Pixel import *
except:
    from methods.ss_Pixel import *
try:
    from common.methods.ss_Arithmetic import *
except:
    from methods.ss_Arithmetic import *

"""
These methods enable the functionality of 
"""

# Recursively dig through dictionary to retrieve value
def getDVal(d : dict, listPath : list) -> Any:
    for key in listPath:
        d = d[key]
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
    if argType == "core":
        return run["coreFeatures"][argValue]
    if argType == "colors":
        return [run["colorInstances"][color] for color in argValue]
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
    args = ["image", "row", "lowPercent", "highPercent"]
    [im, row, lowPercent, highPercent] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelRow_Percent(im, row, lowPercent, highPercent)

def seqEx_getPixelColumn_Percent(step : dict, run : dict) -> None:
    args = ["image", "column", "lowPercent", "highPercent"]
    [im, column, lowPercent, highPercent] = [getArgVal(step, arg, run) for arg in args]    
    step["result"] = getPixelColumn_Percent(im, column, lowPercent, highPercent)

def seqEx_flexAdd(step : dict, run : dict) -> None:
   inputs = [getArgVal(step, arg, run) for arg in step.keys() if arg[:5] == "input"]
   print(inputs)    
   step["result"] = flexAdd(*inputs)

"""
This dictionary is the link between the function text in a sequence step
and the actual method called.
"""
seqEx = {
    "getPixelRow_Absolute" : seqEx_getPixelRow_Absolute,
    "getPixelColumn_Absolute" : seqEx_getPixelColumn_Absolute,
    "getPixelRow_Percent" : seqEx_getPixelRow_Percent,
    "getPixelColumn_Percent" : seqEx_getPixelColumn_Percent,
    "flexAdd" : seqEx_flexAdd
}

"""
This function will accept any sequence dictionary and execute it.
The bool return is whether the sequence completes all steps
and the final step "continue" resolves to True.
"""
def executeTOMLsequence(seq : dict, run : dict) -> bool:

    stepIndexes = parseSeqStepIndexes(seq)

    print(f"\nRunning sequence {seq['name']}\n\n")

    for stepIndex in stepIndexes:
        step = seq[stepIndex]

        seqEx[step["function"]](step, run)

        if not getArgVal(step["continue"]):
            return False
    
    return True