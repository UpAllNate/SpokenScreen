from typing import Any
from common.ss_namespace_methods import NamespaceMethods

# Adds any number of arguments, in lists, or not
@NamespaceMethods.register
def flexAdd(*args : Any) -> Any:

   if len(args) == 1:
      args = args[0]

   sum = None
   for arg in args:

      print(f"value: {arg}")
      if isinstance(arg, list):
         if sum is not None:
            sum -= flexAdd(arg)
         else:
            sum = flexAdd(arg)
      else:
         if sum is not None:
            sum -= arg
         else:
            sum = arg

   return sum

# Subtracts any number of arguments, in lists, or not
@NamespaceMethods.register
def flexSubtract(*args : Any) -> Any:

   if len(args) == 1:
      args = args[0]

   diff = None
   for arg in args:

      print(f"value: {arg}")
      if isinstance(arg, list):
         if diff is not None:
            diff -= flexSubtract(arg)
         else:
            diff = flexSubtract(arg)
      else:
         if diff is not None:
            diff -= arg
         else:
            diff = arg

   return diff

# Multiplies any number of arguments, in lists, or not
@NamespaceMethods.register
def flexMultiply(*args : Any) -> Any:

   if len(args) == 1:
      args = args[0]

   product = None
   for arg in args:

      if isinstance(arg, list):
         if product is not None:
            product *= flexMultiply(arg)
         else:
            product = flexMultiply(arg)
      else:
         if product is not None:
            product *= arg
         else:
            product = arg

   return product

# Divides any number of arguments, in lists, or not
@NamespaceMethods.register
def flexDivide(*args : Any) -> Any:

   if len(args) == 1:
      args = args[0]

   quotient = None
   for arg in args:

      if isinstance(arg, list):
         if quotient is not None:
            quotient /= flexDivide(arg)
         else:
            quotient = flexDivide(arg)
      else:
         if quotient is not None:
            quotient /= arg
         else:
            quotient = arg

   return quotient