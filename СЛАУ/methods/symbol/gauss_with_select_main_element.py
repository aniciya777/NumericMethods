from __future__ import annotations
from .gauss import GaussSolver


class GaussWithSelectMainElementSolver(GaussSolver):
    def forward_iter(self, number_row: int) -> GaussWithSelectMainElementSolver:
        maximum_index = number_row
        maximum_value = abs(float(self[number_row][number_row]))
        for i in range(number_row + 1, self._n_rows):
            value = abs(float(self[i][number_row]))
            if value > maximum_value:
                maximum_index = i
                maximum_value = value
        if maximum_index != number_row:
            self.swap_rows(number_row, maximum_index)
        if maximum_value:
            return super().forward_iter(number_row)
        raise Exception(f"Главный элемент {number_row + 1}-го столбца равен нулю")
