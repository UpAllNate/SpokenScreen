from typing import Any

def getDVal(d : dict, listPath : list) -> Any:
    for key in listPath:
        d = d[key]
    return d