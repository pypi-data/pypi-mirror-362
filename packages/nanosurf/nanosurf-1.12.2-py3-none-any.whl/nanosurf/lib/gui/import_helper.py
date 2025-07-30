# /// Copyright (C) Nanosurf AG - All Rights Reserved (2021)
# /// Unauthorized copying of this file, via any medium is strictly prohibited
# /// https://www.nanosurf.com
# ///

import sys

def is_pyside_loaded() -> bool:
    """ checks if any pyside version is loaded """
    modules = sys.modules.keys()
    return ('PySide6' in modules) or ('PySide2' in modules)

def is_pyside6_loaded() -> bool:
    """ checks if PySide6 version is loaded """
    return 'PySide6' in sys.modules.keys()

def is_pyside2_loaded() -> bool:
    """ checks if PySide2 version is loaded """
    return 'PySide2' in sys.modules.keys()

def import_pyside2_if_none_is_detected() -> bool:
    """ Return True if PySide2 could be imported """
    if not(is_pyside_loaded()):
        import_pyside()
    return is_pyside2_loaded()

def import_pyside() -> bool:
    """ imports an supported pyside version. First PySide2 then PySide6
        Return True if an supported pyside version could be loaded
    """
    try:
        if not(is_pyside_loaded()):
            import PySide2
        if not(is_pyside_loaded()):
            import PySide6
    except ImportError:
        pass
    return is_pyside_loaded()
