from __future__ import annotations
from fractions import Fraction
from typing import Iterable

import tabulate


class Vector(list):
    def _check_other_vector(self, other: Vector) -> None:
        if not isinstance(other, list):
            raise TypeError(f'unsupported operand type(s) for +: {type(self)} and {type(other)}')
        if len(self) != len(other):
            raise ValueError('Vector must have the same length')

    def __add__(self, other: Vector) -> Vector:
        self._check_other_vector(other)
        return Vector(value1 + value2 for value1, value2 in zip(self, other))

    def __radd__(self, other: Vector) -> Vector:
        return self + other

    def __iadd__(self, other: Vector) -> Vector:
        self._check_other_vector(other)
        for i in range(len(self)):
            self[i] += other[i]
        return self

    def __sub__(self, other: Vector) -> Vector:
        self._check_other_vector(other)
        return Vector(value1 - value2 for value1, value2 in zip(self, other))

    def __rsub__(self, other: Vector) -> Vector:
        return (self - other) * -1

    def __isub__(self, other: Vector) -> Vector:
        self._check_other_vector(other)
        for i in range(len(self)):
            self[i] -= other[i]
        return self

    def __mul__(self, other: Vector | int | float | Fraction) -> Vector | int | float | Fraction:
        if type(other) in (int, float, Fraction):
            return Vector(value * other for value in self)
        if isinstance(other, list):
            self._check_other_vector(other)
            return sum(value1 * value2 for value1, value2 in zip(self, other))
        raise TypeError

    def __rmul__(self, other: Vector | int | float | Fraction) -> Vector | int | float | Fraction:
        return self * other

    def __imul__(self, other: int | float | Fraction) -> Vector:
        if type(other) in (int, float, Fraction):
            for i in range(len(self)):
                self[i] *= other[i]
            return self
        raise TypeError

    def __str__(self) -> str:
        str_vector = [str(value) for value in self]
        return '[ ' + tabulate.tabulate([str_vector], tablefmt='plain') + ' ]'

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item):
        if isinstance(item, int):
            return super().__getitem__(item)
        if isinstance(item, slice):
            return Vector(super().__getitem__(item))
        raise TypeError


class Matrix(list):
    def __init__(self, _iterable: Iterable[list] = None):
        if _iterable is not None:
            super().__init__(Vector(row) for row in _iterable)

    def column(self, index: int) -> Vector:
        return Vector(row[index] for row in self)

    def __str__(self) -> str:
        str_matrix = [map(str, row) for row in self]
        str_matrix = tabulate.tabulate(str_matrix, tablefmt='plain', numalign="decimal", stralign="center")
        return str_matrix

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item):
        if isinstance(item, int):
            return super().__getitem__(item)
        if isinstance(item, slice):
            return Matrix(super().__getitem__(item))
        raise TypeError
