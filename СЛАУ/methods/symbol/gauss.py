from __future__ import annotations
from fractions import Fraction
from typing import Generator

from ..abstract_solver import AbstractSolver


class GaussSolver(AbstractSolver):
    def forward_iter(self, number_row: int) -> GaussSolver:
        if self[number_row][number_row] == 0:
            for row in range(number_row + 1, self._n_rows):
                if self[row][number_row]:
                    self.swap_rows(row, number_row)
                    break
            else:
                raise Exception('Перестановка строк не помогла')
        for row in range(number_row + 1, self._n_rows):
            coeff = Fraction(self[row][number_row], self[number_row][number_row])
            for col in range(self._n_cols + 1):
                self[row][col] -= self[number_row][col] * coeff
        return self

    def forward(self) -> Generator[GaussSolver, None, None]:
        for row in range(self._n_rows - 1):
            yield self.forward_iter(row)

    def backward_iter(self, number_row: int) -> GaussSolver:
        pass

    def calculate_x_iter(self, number_row: int) -> GaussSolver:
        val = self[number_row][-1]
        val -= sum(self[number_row][i] * self._x[i] for i in range(number_row + 1, self._n_cols))
        self._x[number_row] = Fraction(val, self[number_row][number_row])
        return self

    def backward(self) -> Generator[GaussSolver, None, None]:
        for row in range(self._n_rows - 1, -1, -1):
            yield self.calculate_x_iter(row)

    def solve(self) -> Generator[GaussSolver, None, None]:
        yield from self.forward()
        yield from self.backward()
