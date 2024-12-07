from typing import Callable

from handy_dandy_library.file_processing import read_lines


BivariateOperator = Callable[[int, int], int]


class Calibrator:
    def __init__(self, lines: list[str]):
        self.operation_challenges = tuple(OperationChallenge(line) for line in lines)

    def possible_challenges_sum(self) -> list[int]:
        operators = [lambda x, y: x + y, lambda x, y: x * y]
        return sum(challenge.target for challenge in self.operation_challenges if challenge.is_possible(operators))

    def possible_challenges_sum2(self) -> list[int]:
        operators = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(str(x) + str(y))]
        return sum(challenge.target for challenge in self.operation_challenges if challenge.is_possible(operators))


class OperationChallenge:
    def __init__(self, line: str):
        target, phrase = line.split(':')
        integers = phrase[1:].split(' ')
        self.target = int(target)
        self.integers = tuple(int(x) for x in integers)
        self.n = len(integers)

    def __repr__(self) -> str:
        return f"{self.target}: [{self.integers}]"

    def is_possible(self, operators: list[BivariateOperator]) -> bool:
        to_check = [(self.integers[0], 1)]
        while to_check:
            a, i = to_check.pop()

            if a > self.target:
                continue

            if i == self.n:
                if a == self.target:
                    return True
                continue

            b = self.integers[i]

            for operator in operators:
                to_check.append((operator(a, b), i + 1))

        return False


def tests():
    calibrator = Calibrator(read_lines("puzzle7_1_test_input1.txt"))

    t1 = calibrator.possible_challenges_sum()
    assert t1 == 3749

    calibrator2 = Calibrator(read_lines("puzzle7_1_test_input2.txt"))
    assert calibrator2.possible_challenges_sum() == 48


def main():
    tests()

    calibrator = Calibrator(read_lines("puzzle7_1.txt"))

    t2 = calibrator.possible_challenges_sum()
    assert t2 == 28_730_327_770_375


if __name__ == "__main__":
    main()
