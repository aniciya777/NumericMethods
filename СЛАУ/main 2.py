from methods import utils
from methods.iterations import SeidelSolver, SimpleIterativeSolver, AbstractIterativeSolver


A = [
    [-7,  2, 40,  0],
    [ 9, -5,  0, 50],
    [25,  0,  4, -1],
    [ 0, 32,  0,  9],
]
b = [
    21,
    -14,
    13,
    21
]


solvers: dict[str, AbstractIterativeSolver] = {
    'МЕТОД ПРОСТЫХ ИТЕРАЦИЙ': SimpleIterativeSolver,
    'МЕТОД ЗЕЙДЕЛЯ': SeidelSolver
}


def show_x_with_errors(solver: AbstractIterativeSolver) -> None:
    solver.print_x(accuracy=6)
    print(f'Невязка {utils.ital("r")} = {utils.clr_int(solver.error_vector)}')
    print(f'{utils.ital("|r|")} = {utils.clr_int(solver.error)}')
    print()


for method_name, SolverClass in solvers.items():
    print(f' {method_name} '.center(100, '-'))
    solver = SolverClass(A, b)
    solver.perfect_print()
    print('Сходимость:', utils.clr_int(solver.convergence))
    solver.set_initial_approximation(fill_value=0)
    print('Матрица после преобразования:')
    solver.perfect_print()
    print(f'Матрица {utils.ital("G")}:')
    print(utils.clr_int(solver.G))
    print(f'Вектор {utils.ital("f")}:')
    print(utils.clr_int(solver.f))
    print('Начальное приближение:')
    show_x_with_errors(solver)

    for i, _ in enumerate(solver.solve(accuracy=0.001), 1):
        print(f'Итерация {i}')
        show_x_with_errors(solver)
    print()
input(f'Нажмите {utils.ital("Enter")} для выхода')
