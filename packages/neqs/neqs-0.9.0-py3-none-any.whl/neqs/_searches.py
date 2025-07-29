
#[

from __future__ import annotations

from . import iterative as _iterative

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from numbers import Real

#]


_DAMPING_FACTOR = 0.9
_IMPROVEMENT_RATE = 0.9
_MIN_STEP = 1e-10
_INIT_STEP_SIZE = 1


def damped_search(
    direction: _iterative.ArrayType,
    prev_guess: _iterative.GuessType,
    min_norm: _iterative.ArrayType,
    eval_func: _iterative.FuncEvalType,
    eval_norm: _iterative.NormEvalType,
    *,
    init_step_size: float = _INIT_STEP_SIZE,
    min_step: float = _MIN_STEP,
    damping_factor: float = _DAMPING_FACTOR,
) -> tuple[_iterative.GuessType, _iterative.ArrayType, Real, ]:
    """
    """

    new_step_size = None

    while True:
        if new_step_size is None:
            new_step_size = init_step_size
        else:
            new_step_size = damping_factor * new_step_size
        if new_step_size < 1e-10:
            raise _iterative.StepFailure
        new_guess = prev_guess + new_step_size * direction
        new_func = eval_func(new_guess, )
        new_norm = eval_norm(new_func, )
        if new_norm < min_norm:
            break

    return new_guess, new_func, new_step_size,

