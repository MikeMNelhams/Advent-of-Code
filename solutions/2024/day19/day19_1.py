from handy_dandy_library.file_processing import read_lines


from functools import cache


class TowelPatternChecker:
    valid_colors = "grubw"

    def __init__(self, lines: list[str]):
        self.patterns = self.__patterns(lines[0])
        self.pattern_set = set(self.patterns)
        self.towels = [x for x in lines[2:]]

    @staticmethod
    def __patterns(line: str) -> list[str]:
        return line.split(', ')

    @cache
    def is_possible(self, towel: str) -> bool:
        if len(towel) == 1:
            return towel in self.pattern_set
        if towel in self.pattern_set:
            return True
        for i in range(1, len(towel)):
            x = self.is_possible(towel[:i])
            y = self.is_possible(towel[i:])
            if x and y:
                return True
        return False

    def possible_towel_count(self) -> int:
        total = 0

        for i, towel in enumerate(self.towels):
            print(f"checking towel # {i}: {towel}")
            total += self.is_possible(towel)
        return total

    def possible_towel_combinations(self) -> int:
        total = 0
        for i, towel in enumerate(self.towels):
            print(f"checking towel # {i}: {towel}")
            total += self.is_possible_count(towel)
        return total

    @cache
    def is_possible_count(self, towel: str) -> int:
        if len(towel) == 0:
            return 1
        return sum(self.is_possible_count(towel[len(pattern):])
                   for pattern in self.patterns
                   if towel.startswith(pattern))


def tests():
    toweler = TowelPatternChecker(read_lines("puzzle19_1_test_input1.txt"))

    t1 = toweler.possible_towel_count()
    assert t1 == 6


def main():
    tests()

    toweler = TowelPatternChecker(read_lines("puzzle19_1.txt"))
    t1 = toweler.possible_towel_count()
    assert t1 == 324


if __name__ == "__main__":
    main()
