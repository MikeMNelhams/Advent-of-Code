from handy_dandy_library.file_processing import read_lines

from itertools import product


class KeyLockTester:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.keys, self.locks = self.__keys_and_locks(lines)
        self.total_pairs = len(self.keys) * len(self.locks)

    def __keys_and_locks(self, lines: list[str]) -> (list[tuple], list[tuple]):
        locks = []
        keys = []

        width = len(lines[0])

        height = 0
        n = len(lines)
        for i in range(n):
            if lines[i] == '':
                break
            height += 1

        number_of_fittables = (n + 1) // (height + 1)

        for i in range(number_of_fittables):
            row_index = (height + 1) * i
            is_lock = lines[row_index][0] == '#'

            if is_lock:
                locks.append(self.__read_lock(lines, row_index, width, height))
            else:
                keys.append(self.__read_key(lines, row_index, width, height))

        return keys, locks

    @staticmethod
    def __read_lock(lines: list[str], row_index: int, width: int, height: int) -> tuple[int]:
        code = [-1 for _ in range(width)]

        for i in range(height):
            line = lines[row_index + i]
            none_found = True
            for j, char in enumerate(line):
                if char == '#':
                    code[j] += 1
                    none_found = False
            if none_found:
                break

        return tuple(code)

    @staticmethod
    def __read_key(lines: list[str], row_index: int, width: int, height: int) -> tuple[int]:
        code = [-1 for _ in range(width)]

        for i in range(height):
            line = lines[row_index + i]
            none_found = True
            for j, char in enumerate(line):
                if char == '.':
                    code[j] += 1
                    none_found = False
            if none_found:
                break

        return tuple(code)

    @property
    def valid_fits_count(self) -> int:
        total = 0
        for key, lock in product(self.keys, self.locks):
            for i, (k_c, l_c) in enumerate(zip(key, lock)):
                if k_c < l_c:
                    total += 1
                    break
        return self.total_pairs - total


def tests():
    key_lock_tester = KeyLockTester(read_lines("puzzle25_1_text_input1.txt"))

    assert key_lock_tester.valid_fits_count == 3


def main():
    tests()

    key_lock_tester = KeyLockTester(read_lines("puzzle25_1.txt"))
    assert key_lock_tester.valid_fits_count == 2933


if __name__ == "__main__":
    main()
