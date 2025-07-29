"""
"""


#[

from __future__ import annotations

import functools as _ft
import numpy as _np
import scipy as _sp

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable

#]


class _Firefly:
    """
    """
    position: _np.ndarray | None = None
    discrepancy_vector: _np.ndarray | None = None
    objective_value: float | None = None

    _MAX_ATTEMPTS_TO_GENERATE_NEW: int = 100
    _NDIMS: int | None = None
    _ORIGIN: _np.ndarray | float = 0.0
    _DISPERSION: float = 1.0
    _EVAL_FUNC: Callable | None = None
    _EVAL_NORM: Callable | None = None

    @classmethod
    def generate_new(
        klass,
    ) -> Self:
        """
        """
        self = klass()
        count_attempts = 0
        while count_attempts < klass._MAX_ATTEMPTS_TO_GENERATE_NEW:
            count_attempts += 1
            new_position = self._generate_new_position()
            if self.try_move_to(new_position, ):
                return self
        raise Exception("Failed to generate a new firefly")

    @classmethod
    def _generate_new_position(klass, /, ) -> _np.ndarray:
        """
        """
        return klass._ORIGIN + klass._DISPERSION * _np.random.normal(size=klass._NDIMS, )

    def try_move_to(
        self,
        new_position: _np.ndarray,
    ) -> bool:
        """
        """
        new_objective_value, new_discrepancy_vector = self._eval_objective_value(new_position, )
        if new_objective_value is None:
            return False
        self.position = new_position
        self.discrepancy_vector = new_discrepancy_vector
        self.objective_value = new_objective_value
        return True

    @classmethod
    def _eval_objective_value(klass, position, /, ) -> float | None:
        """
        """
        try:
            discrepancy_vector = klass._EVAL_FUNC(position, )
            objective_value = klass._EVAL_NORM(discrepancy_vector)
        except Exception as e:
            objective_value = _np.inf
            discrepancy_vector = _np.inf
        if _np.isfinite(objective_value):
            return objective_value, discrepancy_vector
        else:
            return None, None,

    def be_attracted_to(
        self,
        another: Self,
        parameters: dict[str, Any],
    ) -> None:
        """
        """
        if not self.is_attracted_to(another, ):
            raise Exception("Firefly cannot be attracted to an inferior firefly")
        distance = self.distance_from(another, )
        alpha = parameters["alpha"]
        beta = parameters["beta"]
        gamma = parameters["gamma"]
        count_attempts = 0
        while count_attempts < self._MAX_ATTEMPTS_TO_GENERATE_NEW:
            count_attempts += 1
            random = _np.random.normal(size=self._NDIMS, )
            new_position = (
                self.position
                + beta * _np.exp(-gamma * distance**2) * (another.position - self.position)
                + alpha * random
            )
            if self.try_move_to(new_position, ):
                return
        raise Exception("Failed to move firefly to a new position")

    def is_attracted_to(
        self,
        another: Self,
    ) -> bool:
        """
        """
        return self.objective_value > another.objective_value

    def distance_from(
        self,
        another: Self,
    ) -> float:
        """
        """
        return self._EVAL_NORM(self.position - another.position, )


_DEFAULT_SOLVER_SETTINGS = {
    "alpha": 0.1,
    "beta": 1.0,
    "gamma": 1.0,
    "rho": 1,
    "max_iterations": 100,
    "population": 100,
    "func_tolerance": 1e-4,
    "norm": 2,
    "dispersion": 1.0,
}


def main(
    eval_func: Callable,
    init_guess: _np.ndarray,
    iter_printer: IterPrinter | None = None,
    iter_printer_settings: dict | None = None,
    solver_settings: dict[str, Any] | None = None
) -> _np.ndarray:
    """
    """

    solver_settings = solver_settings or {}
    solver_settings = _DEFAULT_SOLVER_SETTINGS | solver_settings

    parameters = {
        "alpha": solver_settings["alpha"],
        "beta": solver_settings["beta"],
        "gamma": solver_settings["gamma"],
        "rho": solver_settings["rho"],
    }

    Firefly = _Firefly
    Firefly._NDIMS = init_guess.size
    Firefly._EVAL_FUNC = staticmethod(eval_func)
    Firefly._EVAL_NORM = staticmethod(_ft.partial(_sp.linalg.norm, ord=solver_settings["norm"], ))
    Firefly._ORIGIN = init_guess
    Firefly._DISPERSION = solver_settings["dispersion"]

    fireflies = [
        Firefly.generate_new()
        for _ in range(solver_settings["population"])
    ]

    for i in range(solver_settings["max_iterations"]):
        for anna in fireflies:
            for becky in fireflies:
                if anna is becky:
                    continue
                if not anna.is_attracted_to(becky, ):
                    continue
                anna.be_attracted_to(becky, parameters, )
                if anna.objective_value < solver_settings["func_tolerance"]:
                    break
        best_firefly = min(fireflies, key=lambda firefly: firefly.objective_value, )
        print(f"Generation {i}: {best_firefly.objective_value}")
        parameters["alpha"] *= solver_settings["rho"]
    #
    best_firefly = min(fireflies, key=lambda firefly: firefly.objective_value, )
    best_position = best_firefly.position
    best_discrepancy_vector = best_firefly.discrepancy_vector
    best_objective_value = best_firefly.objective_value
    #
    return best_position

