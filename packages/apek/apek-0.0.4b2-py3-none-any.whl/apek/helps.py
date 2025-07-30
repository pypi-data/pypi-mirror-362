# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring



from re import search as _search
from colorama import Fore as _fore, init as _colorinit
from ._text import text
from ._base import _showArgsError, _checkAndShowParamTypeError
_colorinit(autoreset=True)



def upgradeLog(*args, ver="0.0.3", lang="en"):
    """
    Print the upgrade log.
    
    Args:
        *args:
            A TypeError will be raised when too many arguments are passed.
        ver (str, optional):
            Keyword argument.
            Specify the version number for which to retrieve the log.
            The Defaults to the latest version.
        lang (str, optional):
            Keyword argument.
            Specifies the language for printing logs.
            The default is "en".
    
    Returns:
        None
    
    Raises:
        TypeError: This error is raised when too many arguments are passed.
        ValueError: This error is raised when the provided version number does not conform to the "x.y.z" format.
    """
    if args:
        _showArgsError(args)
    _checkAndShowParamTypeError("ver", ver, str)
    _checkAndShowParamTypeError("lang", lang, str)
    if not _search("^\\d+\\.\\d+\\.\\d+$", ver):
        raise ValueError(f"{text[lang]['helps.function.updateLog.versionFormatError']}{_fore.GREEN}{repr(ver)}{_fore.RESET}")
    r = text[lang].get("helps.upgradeLogs." + ver.replace(".", "_"))
    if r is None:
        raise ValueError(f"{text[lang]['helps.function.updateLog.versionNotFound']}{_fore.GREEN}{ver}{_fore.RESET}")
    print(r)
