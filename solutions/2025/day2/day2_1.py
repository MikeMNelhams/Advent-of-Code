from handy_dandy_library.file_processing import read_lines


def is_invalid(x: str) -> bool:
    n = len(x)
    if n & 1:
        return False
    return x[:n//2] == x[n//2:]


def sum_invalid_ids(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    product_ids = [product_id.split("-") for product_id in lines[0].split(",")]
    total = 0
    for low, high in product_ids:
        for x in range(int(low), int(high) + 1):
            if is_invalid(str(x)):
                total += x
    return total


def main():
    assert sum_invalid_ids("puzzle2_1_test_input.txt") == 1_227_775_554
    t = sum_invalid_ids("puzzle2_1.txt")
    print(t)


if __name__ == "__main__":
    main()
