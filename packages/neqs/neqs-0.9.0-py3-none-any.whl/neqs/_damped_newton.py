"""
Damped Newton step
"""


#[

from __future__ import annotations

import numpy as _np
import scipy as _sp

from . import iterative as _iterative
from ._searches import damped_search

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from numbers import Real
    from . import iterative as _iterative

#]


_MIN_IMPROVEMENT_RATE = 0


def eval_step(
    guess: _iterative.GuessType,
    func: _iterative.ArrayType,
    jacob: _iterative.SparseArrayType,
    norm: float,
    eval_func: _iterative.FuncEvalType,
    eval_norm: _iterative.NormEvalType,
    *,
    min_improvement_rate: float = _MIN_IMPROVEMENT_RATE
) -> tuple[_iterative.GuessType, _iterative.ArrayType, Real, ]:
    """
    """

    direction = - _sp.sparse.linalg.spsolve(jacob, func, )

    min_norm = (1 - min_improvement_rate) * norm

    new_guess, new_func, new_step_size, = damped_search(
        direction=direction,
        prev_guess=guess,
        min_norm=min_norm,
        eval_func=eval_func,
        eval_norm=eval_norm,
    )

    return new_guess, new_func, new_step_size,

