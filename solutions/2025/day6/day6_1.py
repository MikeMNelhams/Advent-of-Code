import operator
from functools import reduce
import operator as _operator

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import parse_ints_strip_spaces


class CephalopodMathTable:
    __OPERATORS = {"+": _operator.add, "*": _operator.mul}

    def __init__(self, puzzle_path: str):
        self.puzzle_path = puzzle_path

    @staticmethod
    def __human_number_grid_from_lines(lines: list[str]) -> list[list[int]]:
        return [parse_ints_strip_spaces(line) for line in lines]

    @staticmethod
    def __cephalopod_number_grid_from_lines(lines: list[str]) -> list[list[int]]:
        max_line_length = reduce(max, (len(line) for line in lines[:-1]), -1)
        for i in range(len(lines[:-1])):
            lines[i] = lines[i].ljust(max_line_length)

        column_indices = [i - 1 for i, char in enumerate(lines[-1]) if char != " "]
        column_indices = [0] + column_indices[1:] + [max_line_length]

        n = len(lines) - 1
        number_grid = []
        for column_index_index in range(1, len(column_indices)):
            m = column_indices[column_index_index] - column_indices[column_index_index - 1]
            column_index = column_indices[column_index_index]
            numbers = []
            for j in range(1, m + 1):
                digits = "".join(lines[i][column_index - j] for i in range(n)).strip()
                if digits != "":
                    numbers.append(int(digits))
            number_grid.append(numbers)
        return number_grid

    @staticmethod
    def __op_grid_from_line(line: str) -> list[str]:
        return [x for x in line.split(" ") if x != ""]

    def __human_reduced_operation_sum(self, number_grid: list[list[int]], op_grid: list[str]) -> int:
        n = len(number_grid)
        m = len(number_grid[0])
        total = 0
        for j in range(m):
            reduction_operator = self.__OPERATORS[op_grid[j]]
            total += reduce(reduction_operator, (number_grid[i][j] for i in range(n)))
        return total

    def __cephalopod_reduced_operation_sum(self, number_grid: list[list[int]], op_grid: list[str]) -> str:
        total = 0
        for i, numbers in enumerate(number_grid):
            reduction_operator = self.__OPERATORS[op_grid[i]]
            total += reduce(reduction_operator, numbers)
        return total

    def human_reduced_operation_sum(self) -> int:
        lines = read_lines(self.puzzle_path)
        number_grid = self.__human_number_grid_from_lines(lines[:-1])
        op_grid = self.__op_grid_from_line(lines[-1])
        return self.__human_reduced_operation_sum(number_grid, op_grid)

    def cephalopod_reduced_operation_sum(self) -> int:
        lines = read_lines(self.puzzle_path)
        number_grid = self.__cephalopod_number_grid_from_lines(lines)
        op_grid = self.__op_grid_from_line(lines[-1])
        return self.__cephalopod_reduced_operation_sum(number_grid, op_grid)


def main():
    test_math_table = CephalopodMathTable("puzzle6_1_test_input.txt")
    assert test_math_table.human_reduced_operation_sum() == 4277556

    math_table = CephalopodMathTable("puzzle6_1.txt")
    print(math_table.human_reduced_operation_sum())


if __name__ == "__main__":
    main()
