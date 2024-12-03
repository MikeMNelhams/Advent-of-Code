from handy_dandy_library.file_processing import read_lines


def total_product_from_line(line: str) -> int:
    phrases = line.split("mul")
    total = 0
    for phrase in phrases:
        m = len(phrase)
        if m < 5:
            continue
        if phrase[0] != '(':
            continue
        if not phrase[1].isnumeric():
            continue
        first_closed_bracket_index = -1
        i = 1
        while i < m:
            char = phrase[i]
            if char == ')':
                first_closed_bracket_index = i
                break
            if not char == ',' and not char.isnumeric():
                break
            i += 1
        else:
            continue
        if first_closed_bracket_index - 1 < 3:
            continue
        integers = phrase[1:first_closed_bracket_index].split(',')
        if len(integers) != 2:
            continue
        total += int(integers[0]) * int(integers[1])

    return total


def total_product_from_lines(lines: list[str]) -> int:
    return sum(total_product_from_line(line) for line in lines)


def tests():
    assert total_product_from_lines(read_lines("puzzle3_1_test_input1.txt")) == 161
    assert total_product_from_lines(read_lines("puzzle3_1.txt")) == 187833789


def main():
    tests()

    t2 = total_product_from_lines(read_lines("puzzle3_1.txt"))
    print(t2)


if __name__ == "__main__":
    main()
