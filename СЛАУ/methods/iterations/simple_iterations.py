from __future__ import annotations
from typing import Generator

from .._matrix import Vector, Matrix
from .abstract_iterations import AbstractIterativeSolver


class SimpleIterativeSolver(AbstractIterativeSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._g: Matrix | None = None
        self._f: Vector | None = None

    def _solve(self, accuracy: float) -> Generator[SimpleIterativeSolver, None, None]:
        while self.error > accuracy and self._iterations < self._max_iterations:
            self._iterations += 1
            new_x = Vector(
                self.G[i] * self.x + self.f[i]
                for i in range(self._n_rows)
            )
            self.set_initial_approximation(new_x)
            yield self

    def solve(self, accuracy: float) -> Generator[SimpleIterativeSolver, None, None]:
        if not self.convergence:
            raise ValueError("Матрица не сходящаяся (не имеет диагонального преобладания)")
        yield from self._solve(accuracy)

    def find_G(self) -> Matrix:
        self._g = Matrix(
            Vector(
                    -self[i][j] / self[i][i]
                if i != j else
                    0
                for j in range(self._n_cols)
            )
            for i in range(self._n_rows)
        )
        return self._g

    def find_f(self) -> Vector:
        self._f = Vector(
            self.b[i] / self[i][i]
            for i in range(self._n_rows)
        )
        return self._f

    def make_convergence(self) -> SimpleIterativeSolver:
        self._f = None
        self._g = None
        return super().make_convergence()

    @property
    def f(self) -> Vector:
        if self._f is None:
            self.find_f()
        return self._f

    @property
    def G(self) -> Matrix:
        if self._g is None:
            self.find_G()
        return self._g
