from __future__ import annotations
from fractions import Fraction
from typing import Generator

from ..abstract_solver import AbstractSolver
from .._matrix import Vector, Matrix


class LUSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._L: Matrix | None = None
        self._U: Matrix | None = None
        self._y: Vector | None = None

    def _find_LU(self) -> LUSolver:
        self._U = Matrix(
            [0 for j in range(self._n_cols)]
            for i in range(self._n_rows)
        )
        self._L = Matrix(
            [int(i == j) for j in range(self._n_cols)]
            for i in range(self._n_rows)
        )
        for i in range(self._n_rows):
            for j in range(self._n_cols):
                value = self._A[i][j] - self._L[i] * self._U.column(j)
                if i <= j:
                    self._U[i][j] = value
                else:
                    self._L[i][j] = Fraction(value, self._U[j][j])
        return self

    @property
    def L(self) -> Matrix:
        if self._L is None:
            self._find_LU()
        return self._L

    @property
    def U(self) -> Matrix:
        if self._U is None:
            self._find_LU()
        return self._U

    @property
    def y(self) -> Vector:
        if self._y is None:
            self.calculate_y()
        return self._y

    def solve(self) -> Generator[LUSolver, None, None]:
        self._x = self.calculate_triangle(self.U, self.y)
        yield self

    def calculate_y(self) -> LUSolver:
        self._y = self.calculate_triangle(
            Matrix(row[::-1] for row in self.L[::-1]),
            self.b[::-1]
        )[::-1]
        return self

    @staticmethod
    def calculate_triangle(a: Matrix, b: Vector) -> Vector:
        n = min(len(a), len(b))
        x = Vector([None] * n)
        for row in range(n - 1, -1, -1):
            val = b[row]
            val -= sum(a[row][i] * x[i] for i in range(row + 1, n))
            x[row] = Fraction(val, a[row][row])
        return x
