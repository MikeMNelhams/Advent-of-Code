from handy_dandy_library.file_processing import read_lines


class Hasher:
    def __init__(self, x: str):
        self.x = x

    @property
    def encoded(self) -> int:
        current = 0
        for char in self.x:
            current += self.encode_char(char)
            current = (current * 17) % 256
        return current

    @staticmethod
    def encode_char(char: str) -> int:
        return ord(char)


def read_single_line_csv(file_path: str, delimiter=',') -> list[str]:
    line = read_lines(file_path)
    return line[0].split(delimiter)


def total_csv_hash(phrases: list[str]) -> int:
    return sum(Hasher(phrase).encoded for phrase in phrases)


def tests():
    assert total_csv_hash(read_single_line_csv("day_15_1_test_input1.txt")) == 1320


def main():
    tests()

    t = total_csv_hash(read_single_line_csv("day_15_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
