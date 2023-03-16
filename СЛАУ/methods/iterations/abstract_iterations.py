from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generator, Iterable, Optional
from fractions import Fraction

from ..abstract_solver import AbstractSolver


class AbstractIterativeSolver(AbstractSolver, ABC):
    MAX_ITERATIONS = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iterations = 0
        self._max_iterations = self.MAX_ITERATIONS
        self._convergence = None
        self.set_initial_approximation()

    @abstractmethod
    def solve(self, accuracy: float) -> Generator[AbstractIterativeSolver, None, None]:
        yield self

    @property
    def convergence(self) -> bool:
        if self._convergence is None:
            self._check_convergence()
        return self._convergence

    def set_initial_approximation(self,
                                  values: Optional[Iterable[int, float, Fraction]] = None,
                                  fill_value: float = 0.0
                                  ) -> AbstractIterativeSolver:
        if values is not None:
            for i in range(self._n_rows):
                self.x[i] = values[i]
            return self
        for i in range(self._n_rows):
            self.x[i] = fill_value
        return self

    @property
    def count_iterations(self) -> int:
        return self._iterations

    def _check_convergence(self) -> bool:
        if self._convergence is None:
            self.make_convergence()
            for row in range(self._n_rows):
                if abs(self[row][row]) <= sum(abs(self[row][i]) for i in range(self._n_cols) if i != row):
                    self._convergence = False
                    break
            else:
                self._convergence = True
        return self._convergence

    def _index_max_absolute_in_row(self, row: int) -> int:
        index = 0
        max_absolute = abs(self[row][0])
        for i in range(1, self._n_cols):
            value = abs(self[row][i])
            if value > max_absolute:
                max_absolute = value
                index = i
        return index

    def make_convergence(self) -> AbstractIterativeSolver:
        indexes = [self._index_max_absolute_in_row(row) for row in range(self._n_rows)]
        for i in range(self._n_rows):
            for row in range(1, self._n_rows):
                if indexes[row] <= indexes[row - 1]:
                    self.swap_rows(row, row - 1)
                    indexes[row - 1], indexes[row] = indexes[row], indexes[row - 1]
        return self
