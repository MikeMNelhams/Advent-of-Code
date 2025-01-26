from handy_dandy_library.file_processing import read_lines


from functools import cache
from itertools import pairwise


def walk(keypad: str, x: int, y: int, path: str) -> str:
    i = y * 3 + x
    for direction in path:
        i += (-1, 1, -3, 3)["<>^v".index(direction)]
        yield keypad[i]


def paths_between_nodes(keypad: str, start: str, end: str) -> str:
    y1, x1 = divmod(keypad.index(start), 3)
    y2, x2 = divmod(keypad.index(end), 3)
    horizontal_chars = "<>"[x2 > x1] * abs(x2 - x1)
    vertical_chars = "^v"[y2 > y1] * abs(y2 - y1)
    for path in {horizontal_chars + vertical_chars, vertical_chars + horizontal_chars}:
        if ' ' not in walk(keypad, x1, y1, path):
            yield path + 'A'


@cache
def cost_between(keypad: str, start: str, end: str, number_of_links: int) -> int:
    if number_of_links == 0:
        return 1

    return min(cost(" ^A<v>", path, number_of_links - 1)
               for path in paths_between_nodes(keypad, start, end))


@cache
def cost(keypad: str, keys: str, number_of_links: int) -> int:
    return sum(cost_between(keypad, x, y, number_of_links) for x, y in pairwise('A' + keys))


def complexity(code: str, robots_count: int) -> int:
    return cost("789456123 0A", code, robots_count + 1) * int(code[:-1])


def total_complexity(lines: list[str], robots_count: int) -> int:
    return sum(complexity(code, robots_count) for code in lines)


def tests():
    t1 = total_complexity(read_lines("puzzle21_1_test_input1.txt"), 2)
    assert t1 == 126384


def main():
    tests()

    t1 = total_complexity(read_lines("puzzle21_1.txt"), 2)
    assert t1 == 105458


if __name__ == "__main__":
    main()