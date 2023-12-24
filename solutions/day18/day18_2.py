from handy_dandy_library.file_processing import read_lines
from day18_1 import Digger, ColorVector


def read_coordinates_hexadecimal_encoded(lines: list[str]) -> list[ColorVector]:
    return [ColorVector.from_line_but_hexadecimal_twist(line) for line in lines]


def tests():
    color_vectors = read_coordinates_hexadecimal_encoded(read_lines("day_18_1_test_input1.txt"))
    digger = Digger(color_vectors)

    assert digger.area == 952408144115


def main():
    tests()

    color_vectors = read_coordinates_hexadecimal_encoded(read_lines("day_18_1_input.txt"))
    digger = Digger(color_vectors)
    t = digger.area
    print(t)


if __name__ == "__main__":
    main()
