from handy_dandy_library.file_processing import read_lines
from day3_1 import total_product_from_lines


def total_allowed_product_from_line(line: str) -> int:
    m = len(line)

    if m < 8:
        return 0

    allow_multiplication = True
    total = 0

    i = 0
    while i < m - 8:
        if is_match(line[i:i+7], "don't()"):
            allow_multiplication = False
            i += 7
            continue
        if is_match(line[i:i+4], "do()"):
            allow_multiplication = True
            i += 4
            continue
        if allow_multiplication and is_match(line[i:i+4], "mul("):
            i += 4
            valid_multiplication = True
            a_string = ""
            while i < m - 1:
                char = line[i]
                if char == ',':
                    i += 1
                    break
                if not char.isnumeric():
                    valid_multiplication = False
                    break
                a_string += char
                i += 1
            else:
                return total

            if not valid_multiplication:
                continue

            b_string = ""

            while i < m:
                char = line[i]
                if char == ')':
                    break
                if not char.isnumeric():
                    valid_multiplication = False
                    break
                b_string += char
                i += 1

            if not valid_multiplication:
                continue

            total += int(a_string) * int(b_string)

        i += 1

    return total


def is_match(phrase: str, target: str) -> bool:
    if len(phrase) < len(target):
        raise ZeroDivisionError

    return all(char_p == char_t for char_p, char_t in zip(phrase, target))


def total_allowed_product_from_lines(lines: list[str]) -> int:
    return sum(total_allowed_product_from_line(line) for line in lines)


def tests():
    assert total_allowed_product_from_lines(read_lines("puzzle3_2_test_input1.txt")) == 48
    t1 = total_allowed_product_from_lines(read_lines("puzzle3_2_test_input5.txt"))
    t2 = total_product_from_lines(read_lines("puzzle3_2_test_input5_simple.txt"))
    assert t1 == t2

    t1 = total_allowed_product_from_lines(read_lines("puzzle3_2_test_input6.txt"))
    t2 = total_product_from_lines(read_lines("puzzle3_2_test_input6_simple.txt"))
    assert t1 == t2


def main():
    tests()

    t3 = total_allowed_product_from_lines(read_lines("puzzle3_1.txt"))
    assert t3 == 94455185


if __name__ == "__main__":
    main()
