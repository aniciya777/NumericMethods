from __future__ import annotations
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import List, Any
import tabulate

from ._utils import ind, ital, clr_int
from ._matrix import Matrix, Vector


class AbstractSolver(ABC):
    BORDER = '┃'
    BORDER_INNER = '|'
    BOTH_PRINT_DISTANCE = 10

    def __init__(self, a: list[list], b: list):
        self._A = Matrix(a)
        self._b = Vector(b)
        self._A_expand = Matrix(
            r1 + [r2] for r1, r2 in zip(a, b)
        )
        self._n_rows = len(self._A_expand)
        self._n_cols = max(map(len, self._A))
        self._x = Vector([None] * self._n_rows)

    def get_table(self, is_float: bool = False, accuracy: int = 3) -> str:
        table = self._A_expand
        if is_float:
            table = [[round(float(val), accuracy) for val in row] for row in table]
        table = [list(map(clr_int, row)) for row in table]
        table = [[self.BORDER] + row[:-1] + [self.BORDER_INNER] + row[-1:] + [self.BORDER] for row in table]
        result = tabulate.tabulate(table, tablefmt="")
        return '\n'.join(result.split('\n')[1:-1])
    
    def perfect_print(self, is_float: bool = False, is_both: bool = False, accuracy: int = 3) -> AbstractSolver:
        if is_both:
            table1 = self.get_table().splitlines()
            table2 = self.get_table(is_float=True, accuracy=accuracy).splitlines()
            for s1, s2 in zip(table1, table2):
                print(s1 + ' ' * self.BOTH_PRINT_DISTANCE + s2)
        else:
            print(self.get_table(is_float=is_float, accuracy=accuracy))
        print()
        return self

    @property
    def x(self) -> Vector:
        return self._x

    @property
    def a(self) -> Matrix:
        return self._A

    @property
    def b(self) -> Vector:
        return self._b

    def __getitem__(self, item) -> Vector:
        return self._A_expand[item]

    def print_x(self, accuracy: int = 3) -> AbstractSolver:
        for i in range(self._n_rows):
            x = f"x{ind(i + 1)}"
            if isinstance(self.x[i], Fraction):
                print(f"{ital(x)} = {clr_int(round(float(self.x[i]), accuracy))} ( {clr_int(self.x[i])} )")
            else:
                print(f"{ital(x)} = {clr_int(round(float(self.x[i]), accuracy))}")
        return self

    @staticmethod
    def _swap(array: List[Any], index1: int, index2: int) -> None:
        array[index1], array[index2] = array[index2], array[index1]

    def swap_rows(self, index1: int, index2: int) -> AbstractSolver:
        self._swap(self._A, index1, index2)
        self._swap(self._A_expand, index1, index2)
        self._swap(self._b, index1, index2)
        return self

    @abstractmethod
    def solve(self) -> AbstractSolver:
        return self

    @property
    def error_vector(self) -> Vector:
        return Vector(
            float('inf') if self.x[i] is None else
                float(self.b[i] - self.a[i] * self.x)
            for i in range(self._n_rows)
        )

    @property
    def error(self) -> float:
        if None in self.x:
            return float('inf')
        return sum(value ** 2 for value in self.error_vector) ** 0.5
