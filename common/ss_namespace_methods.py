
class NamespaceMethods():

    methods = {}

    @classmethod
    def register(clsself, cls):
        NamespaceMethods.methods[cls.__name__] = cls
