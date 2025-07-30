# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring



def _showArgsError(args):
    raise TypeError(f"{len(args)} extra parameters gived: {args}")

def _checkAndShowParamTypeError(varName, var, varType):
    if not isinstance(var, varType):
        s = None
        if isinstance(varType, type):
            s = varType.__name__
        elif isinstance(varType, (tuple, list, set)):
            if isinstance(varType, set):
                varType = list(varType)
            if len(varType) == 1:
                s = varType[0].__name__
            elif len(varType) == 2:
                s = varType[0].__name__ + " or " + varType[1].__name__
            elif len(varType) >= 3:
                bl = varType[:-1]
                s = ", ".join([i.__name__ for i in bl]) + " or " + varType[-1].__name__
        raise TypeError(f"The parameter \"{varName}\" must be {s}, but gived {type(var).__name__}.")
