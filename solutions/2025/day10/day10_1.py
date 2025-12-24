import itertools

from handy_dandy_library.file_processing import read_lines
from itertools import combinations, product
import numpy as np


from sympy import Matrix


class MachineOperator:
    LIGHT_ENCODING = {'.': 0, '#': 1}
    INF = 10 ** 10

    def __init__(self, line: str):
        self.line = line
        self.target_lights = self.__target_lights(line)
        self.joltage_requirements = self.__joltage_requirements(line)
        self.buttons = self.__buttons(line)

    def __target_lights(self, line: str) -> list[bool]:
        return [self.LIGHT_ENCODING[x] for x in line.split("]")[0][1:]]

    @staticmethod
    def __joltage_requirements(line: str) -> list[int]:
        return [int(x) for x in line.split("{")[1].split("}")[0].split(",")]

    @staticmethod
    def __buttons(line: str) -> list[list[int]]:
        button_strings = line.split("] ")[1].split(" {")[0].split("(")
        buttons = [[int(x) for x in button_string[:-2].split(",")] for button_string in button_strings[1:-1]]
        buttons.append([int(x) for x in button_strings[-1][:-1].split(",")])
        return buttons

    def _one_hot_encode(self, x: list[int]) -> np.array:
        y = [0 for _ in range(len(self.target_lights))]
        for i in x:
            y[i] = 1
        return np.array(y)

    def fewest_button_presses(self) -> int:
        if all(x == 0 for x in self.target_lights):
            return 0
        n = len(self.target_lights)
        m = len(self.buttons)
        for i in range(m):
            for buttons in combinations(self.buttons, i):
                totals = [0 for _ in range(n)]
                for button in buttons:
                    for x in button:
                        totals[x] += 1
                if any(x % 2 != y for x, y in zip(totals, self.target_lights)):
                    continue
                return i
        return m

    def fewest_joltage_valid_button_presses(self) -> int:
        target = np.array(self.joltage_requirements)
        buttons = [np.array(self._one_hot_encode(button)) for button in self.buttons]
        system = buttons + [target]
        system = np.column_stack(system)
        system = Matrix(np.column_stack(system)).T
        reduced_row_echelon_system = np.array(system.rref()[0])
        b = reduced_row_echelon_system[:, -1].T

        n_max = sum(abs(x) for x in b)
        m = len(self.buttons)
        rank = 0
        pivot_indices = [0 for _ in range(m)]
        for j in range(m):
            if np.sum(np.abs(reduced_row_echelon_system[:, j])) == 1:
                pivot_indices[j] = 1
                rank += 1
        nullity = m - rank
        if nullity == 0:
            return n_max
        u = []
        u_max_presses = []
        for i, j in enumerate(pivot_indices):
            if j == 1:
                continue
            u.append(reduced_row_echelon_system[:, i])
            button = buttons[i].astype(np.float64)
            v = np.divide(target, button, out=button, where=button != 0)
            u_max_presses.append(int(np.min(v, initial=self.INF, where=v != 0)))
        u = np.column_stack(u)
        best_solution = self.INF
        for i, coefficients in enumerate(product(*[range(x + 1) for x in u_max_presses])):
            c = np.array(coefficients)
            v = b - u @ c
            if np.any(v < 0):
                continue
            y = np.sum(np.abs(v)) + np.sum(c)
            y_residual = abs(y - int(y))
            if y_residual > 0.001:
                continue
            best_solution = min(best_solution, y)
        return best_solution


def fewest_button_presses(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    return sum(MachineOperator(line).fewest_button_presses() for line in lines)


def main():
    assert fewest_button_presses("day10_1_test_input.txt") == 7

    t = fewest_button_presses("day10_1.txt")
    assert t == 415


if __name__ == "__main__":
    main()
