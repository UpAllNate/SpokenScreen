from typing import Any

# Adds any number of strings, or any number of numbers, in lists, or not
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

# Subtracts any number of numbers, in lists, or not
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

# Multiplies any number of numbers, in lists, or not
def flexMultiply(*args : Any) -> Any:
   product = None
   for arg in args:
      if isinstance(arg, list):
         for a in arg:
            if product is not None:
               product *= a
            else:
               product = a
      else:
         if product is not None:
            product *= a
         else:
            product = a
   return product

# Divides any number of numbers, in lists, or not
def flexDivide(*args : Any) -> Any:
   quotient = None
   for arg in args:
      if isinstance(arg, list):
         for a in arg:
            if quotient is not None:
               quotient /= a
            else:
               quotient = a
      else:
         if quotient is not None:
            quotient /= a
         else:
            quotient = a
   return quotient