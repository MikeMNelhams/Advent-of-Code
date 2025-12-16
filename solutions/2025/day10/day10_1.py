from handy_dandy_library.file_processing import read_lines
from itertools import combinations


class MachineOperator:
    LIGHT_ENCODING = {'.': 0, '#': 1}

    def __init__(self, line: str):
        self.target_lights = self.__target_lights(line)
        self.joltage_requirements = self.__joltage_requirements(line)
        self.buttons = self.__buttons(line)
        print(self.buttons)

    def __target_lights(self, line: str) -> list[bool]:
        return [self.LIGHT_ENCODING[x] for x in line.split("]")[0][1:]]

    @staticmethod
    def __joltage_requirements(line: str) -> set[int]:
        return set(int(x) for x in line.split("{")[1].split("}")[0].split(","))

    @staticmethod
    def __buttons(line: str) -> list[list[int]]:
        button_strings = line.split("] ")[1].split(" {")[0].split("(")
        buttons = [[int(x) for x in button_string[:-2].split(",")] for button_string in button_strings[1:-1]]
        buttons.append([int(x) for x in button_strings[-1][:-1].split(",")])
        return buttons

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


def fewest_button_presses(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    return sum(MachineOperator(line).fewest_button_presses() for line in lines)


def main():
    assert fewest_button_presses("day10_1_test_input.txt") == 7

    t = fewest_button_presses("day10_1.txt")


if __name__ == "__main__":
    main()
