"""
The python Plus - Pyplus
================
the python's plus library.\n
"""

from .core import *
from .tools import *
from . import tools, science

if get_config("import.lazy", True, ALL):
    class LazyImport:
        def __init__(self, module_name):
            self.module_name = module_name
            self._module = None

        def __getattr__(self, name):
            from importlib import import_module
            if self._module is None:
                self._module = import_module(self.module_name)
            return getattr(self._module, name)
    advancedlib = LazyImport("advancedlib.all")
    modulelib = LazyImport("modulelib")

__version__ = get_version("main")
