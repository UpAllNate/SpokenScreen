from typing import Any

# Adds any number of strings, or any number of numbers, in or not in lists
def flexAdd(*args : Any) -> Any:
   if isinstance(args[0], str) or (isinstance(args[0], list) and isinstance(args[0][0], str)):
      sum = ""
   else:
      sum = 0
   for arg in args:
      if isinstance(arg, list):
         for a in arg:
            sum += a
      else:
         sum += arg
   return sum
