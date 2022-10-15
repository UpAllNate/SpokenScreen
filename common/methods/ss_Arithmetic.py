from typing import Any

# Adds any number of strings, or any number of numbers, in or not in lists
def flexAdd(*args : Any) -> Any:
   sum = None
   for arg in args:
      if isinstance(arg, list):
         for a in arg:
            if sum is not None:
               sum += a
            else:
               sum = a
      else:
         if sum is not None:
            sum += a
         else:
            sum = a
   return sum

# Subtracts any number of numbers, in or not in lists
def flexSubtract(*args : Any) -> Any:
   diff = None
   for arg in args:
      if isinstance(arg, list):
         for a in arg:
            if diff is not None:
               diff -= a
            else:
               diff = a
      else:
         if diff is not None:
            diff -= a
         else:
            diff = a
   return diff