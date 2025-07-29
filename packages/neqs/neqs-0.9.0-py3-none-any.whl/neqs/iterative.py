"""
Iterative numerical solver boilerplate
"""


#[

import numpy as _np
import scipy as _sp
import enum as _en
import functools as _ft
from typing import Any, Callable

from .iter_printers import IterPrinter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

#]


_DEFAULT_SOLVER_SETTINGS = {
    "step_tolerance": 1e-12,
    "func_tolerance": 1e-12,
    "max_iterations": 5_000,
    "norm_order": float("inf"),
    "eval_jacob_every": 1,
    "eval_jacob_last": None,
}


class StepFailure(Exception):
    pass


ArrayType = _np.ndarray
SparseArrayType = _sp.sparse.spmatrix
FuncEvalType = Callable[[ArrayType], ArrayType]
JacobEvalType = Callable[[ArrayType], SparseArrayType]
NormEvalType = Callable[[ArrayType], float]
SettingsType = dict[str, Any]
GuessType = dict[str, Any]


_DEFAULT_ITER_PRINTER_COLUMNS = (
    "counter",
    "func_norm",
    "step_length",
    "jacob_status",
    "worst_diff_x",
    "worst_func",
)


class ExitStatus(_en.Enum, ):
    """
    """
    #[

    SUCCESS = 0, "Successfully completed",
    MAX_ITERATIONS = 1, "Maximum number of iterations reached",
    CANNOT_MAKE_FURTHER_PROGRESS = 2, "Cannot make further progress",
    ERROR_EVALUATING_STEP = 3, "Error when evaluating the next step",
    NO_SOLVER_NEEDED = -1, "No solver needed",

    @property
    def is_success(self, ) -> bool:
        return self.value[0] <= 0

    def int(self, ) -> int:
        return self.value[0]

    def __str__(self, ) -> str:
        return self.value[1]

    #]


def iterate(
    eval_step: Callable,
    *,
    eval_func: FuncEvalType,
    eval_jacob: JacobEvalType,
    init_guess: ArrayType,
    iter_printer: IterPrinter | None = None,
    iter_printer_settings: dict | None = None,
    args: tuple[Any, ...] = (),
    **kwargs,
) -> tuple[GuessType, ExitStatus]:
    """
    """

    solver_settings = _resolve_solver_settings(**kwargs, )

    args = args or ()

    if iter_printer is None:
        iter_printer = IterPrinter(
            **(iter_printer_settings or {}),
            columns=_DEFAULT_ITER_PRINTER_COLUMNS,
        )

    state = {
        "iter": 0,
        "func_eval": 0,
        "jacob_eval": 0,
        "jacob_status": False,
    }

    def _eval_func(guess: ArrayType, ) -> ArrayType:
        state["func_eval"]+= 1
        return eval_func(guess, *args, )

    def _eval_jacob(guess: ArrayType, jacob, ) -> SparseArrayType:
        eval_jacob_every_satistifed = state["iter"] % solver_settings["eval_jacob_every"] == 0 
        eval_jacob_last_satistifed = (
            state["iter"] <= solver_settings["eval_jacob_last"]
            if solver_settings["eval_jacob_last"] is not None
            else True
        )
        if eval_jacob_every_satistifed and eval_jacob_last_satistifed:
            jacob = None
        state["jacob_status"] = jacob is None
        if state["jacob_status"]:
            state["jacob_eval"] += 1
            jacob = eval_jacob(guess, *args, )
        return jacob

    eval_norm = _ft.partial(
        _sp.linalg.norm,
        ord=solver_settings["norm_order"],
    )


    curr_guess = init_guess
    prev_guess = curr_guess
    curr_func = _eval_func(curr_guess, )
    if not _np.isfinite(curr_func).all():
        raise Exception
    curr_step_size = None
    curr_jacob = None


    while True:

        curr_norm = eval_norm(curr_func, )

        iter_printer.next(
            guess=curr_guess,
            func=curr_func,
            jacob_status=state["jacob_status"],
            step_length=curr_step_size,
        )

        convergence_status = _check_convergence(
            curr_guess=curr_guess,
            prev_guess=prev_guess,
            curr_norm=curr_norm,
            eval_norm=eval_norm,
            func_tolerance=solver_settings["func_tolerance"],
            step_tolerance=solver_settings["step_tolerance"],
        )

        if convergence_status:
            exit_status = ExitStatus.SUCCESS
            break

        if state["iter"] >= solver_settings["max_iterations"]:
            exit_status = ExitStatus.MAX_ITERATIONS
            break

        curr_jacob = _eval_jacob(curr_guess, curr_jacob, )
        prev_guess = curr_guess.copy()

        try:
            curr_guess, curr_func, curr_step_size, = eval_step(
                guess=curr_guess,
                func=curr_func,
                jacob=curr_jacob,
                norm=curr_norm,
                eval_func=_eval_func,
                eval_norm=eval_norm,
            )
        except StepFailure as exception:
            exit_status = ExitStatus.CANNOT_MAKE_FURTHER_PROGRESS
            break
        except Exception as exception:
            exit_status = ExitStatus.ERROR_EVALUATING_STEP
            break

        state["iter"] += 1

    iter_printer.conclude()
    return curr_guess, exit_status,


def _resolve_solver_settings(**kwargs, ) -> SettingsType:
    """
    """
    solver_settings = dict(**_DEFAULT_SOLVER_SETTINGS, )
    for n in solver_settings.keys():
        custom_value = kwargs.get(n, None, )
        if custom_value is not None:
            solver_settings[n] = custom_value
    return solver_settings


def _check_convergence(
    curr_guess,
    prev_guess,
    curr_norm,
    step_tolerance,
    func_tolerance,
    eval_norm,
) -> bool:
    """
    """
    #[
    func_tolerance_satisfied = curr_norm < func_tolerance
    step_norm = eval_norm(curr_guess - prev_guess)
    step_tolerance_satisfied = step_norm < step_tolerance
    return func_tolerance_satisfied and step_tolerance_satisfied
    #]

