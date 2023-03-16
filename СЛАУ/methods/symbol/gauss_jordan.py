from __future__ import annotations
from fractions import Fraction
from typing import Generator

from .gauss import GaussSolver


class GaussJordanSolver(GaussSolver):
    def backward_iter(self, number_row: int) -> GaussJordanSolver:
        for row in range(number_row):
            self[row][-1] -= self[number_row][-1] * self[row][number_row]
            self[row][number_row] = 0
        return self

    def calculate_x_iter(self, number_row: int) -> GaussJordanSolver:
        self._x[number_row] = Fraction(self[number_row][-1], self[number_row][number_row])
        return self

    def backward(self) -> Generator[GaussJordanSolver, None, None]:
        for row in range(self._n_rows - 1, -1, -1):
            self.calculate_x_iter(row)
            self[row][row] = 1
            self[row][-1] = self.x[row]
            yield self.backward_iter(row)
