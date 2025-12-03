from handy_dandy_library.file_processing import read_lines
from collections import Counter


def is_multi_invalid(x: str) -> bool:
    n = len(x)
    for i in range(1, n // 2 + 1):
        if n % i > 0:
            continue
        if x == x[:i] * (n // i):
            return True
    return False


def sum_multi_invalid_ids(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    product_ids = [product_id.split("-") for product_id in lines[0].split(",")]
    total = 0
    for low, high in product_ids:
        for x in range(int(low), int(high) + 1):
            if is_multi_invalid(str(x)):
                total += x
    return total


def main():
    assert sum_multi_invalid_ids("puzzle2_1_test_input.txt") == 4174379265
    t = sum_multi_invalid_ids("puzzle2_1.txt")
    print(t)


if __name__ == "__main__":
    main()
