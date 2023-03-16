from __future__ import annotations
from typing import Generator

from .simple_iterations import SimpleIterativeSolver


class SeidelSolver(SimpleIterativeSolver):
    def _solve(self, accuracy: float) -> Generator[SeidelSolver, None, None]:
        while self.error > accuracy and self._iterations < self._max_iterations:
            self._iterations += 1
            for i in range(self._n_rows):
                self.x[i] = self.G[i] * self.x + self.f[i]
            yield self
