from importlib.metadata import version

from . import _api
from ._arg import RAISE  # noqa: F401
from ._cls import *  # noqa: F401,F403
from ._collect import *  # noqa: F401,F403
from ._cmp import *  # noqa: F401,F403
from ._compo import getcomponent
from ._compo import *  # noqa: F401,F403
from ._fill import fillerr, fillwhen  # noqa: F401
from ._fun import *  # noqa: F401,F403
from ._math import isnan  # noqa: F401
from ._nppd import *  # noqa: F401,F403
from ._op import argchecker, arggetter, attrchecker, attrgetter, itemchecker, itemgetter  # noqa: F401
from ._op import constantcreator, methodcaller  # noqa: F401
from .pd import convert_nested_dict_to_dataframe, convert_series_to_nested_dict  # noqa: F401
from ._seq import cycleperm, swap  # noqa: F401


try:
    __version__ = version("calcpy")
except ModuleNotFoundError:
    __version__ = "unknown"


def __getattr__(name):
    return getcomponent(_api, name)


__doc__ = """
calcpy: Facility for Python Calculation
=======================================

Main features:

- Extend Python Built-in Functions, including extended `set` operation functions, extended `str` operation functions, extended math functions.

- Unify APIs supporting both Python built-in types and numpy&pandas datatypes.

- Return value decorations: If the function raises an error or returns invalid values such as `None` and `nan`, fill the values with designated values.

- Function compositions: Combine multiple callable into one callable.

- Function decorators: Reorganize function parameters.
"""  # module level docstring
