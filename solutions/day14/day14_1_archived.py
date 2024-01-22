import sys

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.list_operations import binary_search
from collections import defaultdict
from bisect import bisect


CircleRockCoords = list[int, int]


class RockNRoller:
    def __init__(self, lines: list[str]):
        self.n = len(lines)
        self.m = len(lines[0])
        self.hard_rocks = self.__rock_collection(lines, rock_char='#')
        self.smooth_rocks = self.__rock_collection(lines, rock_char='O')
        self.__representation = lines

    def __repr__(self) -> str:
        return "\n".join(self.__representation)

    @staticmethod
    def __rock_collection(lines: list[str], rock_char: str) -> dict[int, list[int]]:
        rocks = defaultdict(list)

        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == rock_char:
                    rocks[j].append(i)

        for key, value in rocks.items():
            value.sort()

        return rocks

    def pad_top_with_hard_rocks(self) -> None:
        for column, hard_rocks in self.hard_rocks.items():
            for i in range(len(hard_rocks)):
                hard_rocks[i] += 1

        for i in range(self.n):
            self.hard_rocks[i] = [0] + self.hard_rocks[i]

        for smooth_rocks in self.smooth_rocks.values():
            for i in range(len(smooth_rocks)):
                smooth_rocks[i] += 1

        self.__representation = ['#'*self.m] + self.__representation
        self.n += 1
        return None

    def roll_north(self) -> None:
        for column, smooth_rocks in self.smooth_rocks.items():
            impasses = self.hard_rocks[column]
            for smooth_rock in smooth_rocks:
                # TODO finish for roll north, east, west and south
                pass

    @property
    def total_load(self) -> int:
        total = sum(self.n - smooth_rock for smooth_rocks in self.smooth_rocks.values() for smooth_rock in smooth_rocks)
        return total

    def number_of_valid_smooth_rocks_below_hard_rock(self, column: int, hard_rock: int) -> int:
        hard_rocks = self.hard_rocks[column]
        smooth_rocks = self.smooth_rocks[column]
        hard_rock_search_index, is_found = binary_search(hard_rocks, hard_rock)
        if not is_found:
            raise ValueError

        smooth_rock_interval = (hard_rock+1, self.n - 1)
        if len(hard_rocks) > 1 and hard_rock_search_index < len(hard_rocks) - 1:
            smooth_rock_interval = (hard_rock+1, hard_rocks[hard_rock_search_index+1])

        total = 0
        # TODO change this to finding start/end indices using bisect
        for element in smooth_rocks:
            if smooth_rock_interval[0] <= element <= smooth_rock_interval[1]:
                total += 1
        return total

    @property
    def total_north_rolled_load(self) -> int:
        total_load = 0
        for column, hard_rocks in self.hard_rocks.items():
            for hard_rock in hard_rocks:
                num_hard_rocks_below = self.number_of_valid_smooth_rocks_below_hard_rock(column, hard_rock)
                for i in range(num_hard_rocks_below):
                    total_load += (self.n - 1 - hard_rock - i)
        return total_load


def test2():
    rock_roller = RockNRoller(read_lines("day_14_1_test_input2.txt"))
    assert rock_roller.total_load == 136


def test1():
    rock_roller = RockNRoller(read_lines("day_14_1_test_input1.txt"))
    print(f"smooth: {rock_roller.smooth_rocks}",)
    print(f"hard: {rock_roller.hard_rocks}")
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(0, 8) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(0, 9) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(2, 5) == 2
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(3, 3) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(4, 1) == 1
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(5, 0) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(5, 2) == 1
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(5, 6) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(5, 8) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(5, 9) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(6, 2) == 1
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(6, 8) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(7, 5) == 1
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(7, 8) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(8, 4) == 0
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(9, 1) == 1
    assert rock_roller.number_of_valid_smooth_rocks_below_hard_rock(9, 5) == 1
    print(rock_roller, '\n')
    rock_roller.pad_top_with_hard_rocks()
    print(rock_roller.total_north_rolled_load)
    assert rock_roller.total_north_rolled_load == 136


def main():
    test1()
    test2()

    rock_roller = RockNRoller(read_lines("day_14_1_input.txt"))
    rock_roller.pad_top_with_hard_rocks()
    print(rock_roller.total_north_rolled_load)


if __name__ == "__main__":
    main()
