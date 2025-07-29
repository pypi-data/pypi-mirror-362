"""
Damped Newton step
"""


#[

import numpy as _np
import scipy as _sp
import warnings as _wa
import functools as _ft
from numbers import Real

from . import iterative as _iterative
from ._searches import damped_search

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from . import iterative as _iterative

#]


_INITIAL_KAPPA = 1e-12
_KAPPA_MULTIPLIER = 100 # 10
_KAPPA_CAP = 1e8
_MIN_IMPROVEMENT_RATE = 0
_MIN_NORM_MULTIPLIER = 1.2

# ===Matlab===
# _MIN_KAPPA = 1 % 1e-2
# _MAX_KAPPA = 1e6
# _KAPPA_MULTIPLIER = 100
# _INCLUDE_PURE_NEWTON = True

calculate_max_sv = _ft.partial(
    _sp.sparse.linalg.svds,
    k=1,
    return_singular_vectors=False,
)
eye = _np.eye
diag = _np.diag


def eval_step(
    guess: _iterative.GuessType,
    func: _iterative.ArrayType,
    jacob: _iterative.SparseArrayType,
    norm: float,
    eval_func: _iterative.FuncEvalType,
    eval_norm: _iterative.NormEvalType,
    *,
    min_improvement_rate: float = _MIN_IMPROVEMENT_RATE,
) -> tuple[_iterative.GuessType, _iterative.ArrayType, Real, ]:
    """
    """

    min_norm = _MIN_NORM_MULTIPLIER * norm
    # solve = _sp.sparse.linalg.spsolve
    # eye = _sp.sparse.eye
    # diag = _sp.sparse.diags

    solve = _sp.linalg.solve
    def lstsq(*args):
        return _sp.linalg.lstsq(*args)[0]

    newton = jacob.T @ jacob

    # num_unknowns = jacob.shape[1]
    # if num_unknowns <= 2:
    #     gradient_scale = 1
    # else:
    #     max_sv = calculate_max_sv(jacob, )
    #     gradient_scale = num_unknowns * _np.spacing(max_sv);
    # gradient = gradient_scale * eye(newton.shape[0], )

    gradient = eye(newton.shape[0], )

    B = -jacob.T @ func

    def _calculate_direction(kappa, ):
        A = newton + kappa * gradient
        try:
            _wa.simplefilter("error", _sp.linalg.LinAlgWarning, )
            direction = solve(A, B, )
            _wa.simplefilter("default", _sp.linalg.LinAlgWarning, )
        except:
            direction = lstsq(A, B, )
        return direction

    def _calculate_candidate(kappa, ):
        new_direction = _calculate_direction(kappa, )
        new_guess = guess + new_direction
        new_func = eval_func(new_guess, )
        new_norm = eval_norm(new_func, )
        return new_guess, new_func, kappa, new_norm,

    def _update_kappa(kappa, ):
        if kappa:
            return kappa * _KAPPA_MULTIPLIER
        else:
            return _INITIAL_KAPPA

    last_successful_candidate = None
    last_successful_norm = None
    last_successful_kappa = None
    kappa = 0
    while kappa < _KAPPA_CAP:
        *candidate, new_norm = _calculate_candidate(kappa, )

        if last_successful_candidate is not None and new_norm >= last_successful_norm:
            break

        if last_successful_candidate is None:
            if new_norm < min_norm:
                last_successful_candidate = candidate
                last_successful_norm = new_norm
                last_successful_kappa = kappa
                break

        else:
            last_successful_candidate = candidate
            last_successful_norm = new_norm
            last_successful_kappa = kappa

        kappa = _update_kappa(kappa, )

    if last_successful_candidate is not None:
        return last_successful_candidate

    # Fall back to a pure gradient step
    direction = B
    new_guess, new_func, new_step_size, = damped_search(
        direction=direction,
        prev_guess=guess,
        min_norm=min_norm,
        eval_func=eval_func,
        eval_norm=eval_norm,
    )
    kappa = None
    return new_guess, new_func, kappa,


