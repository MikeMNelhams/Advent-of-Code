from itertools import combinations
from functools import cmp_to_key
from collections import defaultdict

from handy_dandy_library.file_processing import read_lines


Rule = tuple[int, int]
Update = list[int]


def line_to_rule(line: str) -> Rule:
    integers = line.split('|')
    return [int(integers[0]), int(integers[1])]


def line_to_update(line: str) -> Update:
    integers = line.split(',')
    return [int(x) for x in integers]


def split_data(lines: list[str]) -> (list[Rule], list[Update]):
    empty_index = -1
    n = len(lines)
    for i in range(n):
        if lines[i] == "":
            empty_index = i
            break

    if empty_index == -1:
        raise ValueError

    rules = [None for _ in range(empty_index)]
    for i in range(empty_index):
        rules[i] = line_to_rule(lines[i])

    updates = [None for _ in range(empty_index + 1, n)]
    for i in range(0, n - empty_index - 1):
        updates[i] = line_to_update(lines[i + empty_index + 1])

    return rules, updates


class PageSorter:
    def __init__(self, rules: list[Rule]):
        self.rules_map = self.__calc_rules_map(rules)

    @staticmethod
    def __calc_rules_map(rules: list[Rule]):
        # Calc is short for calculator btw chat
        rules_map = defaultdict(set)
        for x, y in rules:
            rules_map[x].add(y)
        return rules_map

    def sum_middle_integers_of_already_ordered_updates(self, updates: list[Update]) -> int:
        already_sorted_updates = [u for u in updates if self.is_ordered(u)]
        return sum(self.middle_integer(u) for u in already_sorted_updates)

    def sum_middle_numbers_incorrectly_ordered_but_now_correct(self, updates: list[Update]) -> int:
        not_sorted_updates = [u for u in updates if not self.is_ordered(u)]
        compare_key = cmp_to_key(self.__compare)

        for u in not_sorted_updates:
            print(u)
            u.sort(key=compare_key)
        return sum(self.middle_integer(u) for u in not_sorted_updates)

    @staticmethod
    def middle_integer(update: Update) -> int:
        return update[len(update) // 2]

    def is_ordered(self, update: Update) -> bool:
        for x, y in combinations(update, 2):
            if x not in self.rules_map:
                continue
            if y not in self.rules_map[x] or x in self.rules_map[y]:
                return False
        return True

    def __compare(self, x: int, y: int) -> int:
        if x in self.rules_map[y]:
            return 1
        if y in self.rules_map[x]:
            return -1
        return 0


def tests():
    rules, updates = split_data(read_lines("puzzle5_1_test_input1.txt"))

    page_sorter = PageSorter(rules)
    assert page_sorter.sum_middle_integers_of_already_ordered_updates(updates) == 143


def main():
    tests()

    rules, updates = split_data(read_lines("puzzle5_1.txt"))
    page_sorter = PageSorter(rules)
    t2 = page_sorter.sum_middle_integers_of_already_ordered_updates(updates)
    assert t2 == 4790


if __name__ == "__main__":
    main()
