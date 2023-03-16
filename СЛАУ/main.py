from methods import utils, AbstractSolver
from methods.symbol import GaussSolver, GaussJordanSolver, GaussWithSelectMainElementSolver, LUSolver


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


solvers: dict[str, AbstractSolver] = {
    'МЕТОД ГАУССА': GaussSolver,
    'МЕТОД ГАУССА-ЖОРДАНА': GaussJordanSolver,
    'МЕТОД ГАУССА С ВЫБОРОМ ГЛАВНОГО ЭЛЕМЕНТА': GaussWithSelectMainElementSolver,
}


for method_name, SolverClass in solvers.items():
    print(f' {method_name} '.center(100, '-'))
    solver = SolverClass(A, b)
    solver.perfect_print()
    print('Прямой ход')
    for i, _ in enumerate(solver.forward(), 1):
        print('строка', i)
        solver.perfect_print(is_both=True)
    print('Обратный ход')
    for i, _ in enumerate(solver.backward()):
        if isinstance(solver, GaussJordanSolver):
            print('строка', len(A) - i)
            solver.perfect_print(is_both=True)
    solver.print_x()
    print(f'Невязка {utils.ital("r")} = {utils.clr_int(solver.error_vector)}')
    print(f'{utils.ital("|r|")} = {utils.clr_int(solver.error)}')
    print()


print(' МЕТОД LU-РАЗЛОЖЕНИЯ '.center(100, '-'))
print(f'Дана система {utils.ital("A⋅x=b")}')
solver = LUSolver(A, b)
next(solver.solve())
solver.perfect_print()
print(f'Матрица {utils.ital("L")}:')
print(utils.clr_int(solver.L))
print(f'Матрица {utils.ital("U")}:')
print(utils.clr_int(solver.U))
print(f'Теперь {utils.ital("L⋅U⋅x=b")}')
print(f'Решим систему {utils.ital("L⋅y=b")}')
print(f'{utils.ital("y")} = {utils.clr_int(solver.y)}')
print(f'Решим систему {utils.ital("U⋅x=y")}')
solver.print_x()
print(f'Невязка {utils.ital("r")} = {utils.clr_int(solver.error_vector)}')
print(f'{utils.ital("|r|")} = {utils.clr_int(solver.error)}')
print()
input(f'Нажмите {utils.ital("Enter")} для выхода')
