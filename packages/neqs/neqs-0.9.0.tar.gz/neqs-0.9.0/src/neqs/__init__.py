"""
"""


#[

import importlib.metadata as _md
import functools as _ft

from .iterative import iterate, ExitStatus
from . import _damped_newton as _damped_newton
from . import _levenberg as _levenberg
from ._firefly import main as firefly
from .iter_printers import IterPrinter

#]


damped_newton = _ft.partial(iterate, _damped_newton.eval_step, )
levenberg = _ft.partial(iterate, _levenberg.eval_step, )


__version__ = _md.version(__name__)
__doc__ = _md.metadata(__name__).json["description"]

