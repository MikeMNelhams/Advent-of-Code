import time
from collections import deque


from handy_dandy_library.file_processing import read_lines

from day22_1 import evolve_secret_repeat, evolve_secret


class BananaMaximiser:
    def __init__(self, lines: list[str]):
        self.buyer_secret_starts = [int(line) for line in lines]

    def maximum_bananas(self) -> int:
        maximum = 0
        maximum_sequence = (None, None, None, None)
        last_digits = [[secret_start] for secret_start in self.buyer_secret_starts]

        for i, secret_start in enumerate(self.buyer_secret_starts):
            x = secret_start
            for _ in range(2000):
                x = evolve_secret(x)
                last_digits[i].append(x % 10)

        difference_maps = [{} for _ in range(len(self.buyer_secret_starts))]

        window = deque([])
        for i, (digits, difference_map) in enumerate(zip(last_digits, difference_maps)):
            window.clear()
            for j in range(4):
                window.append(digits[j + 1] - digits[j])

            for j in range(4, 1999):
                sequence = tuple(window)
                if sequence not in difference_map:
                    difference_map[sequence] = last_digits[i][j]
                window.popleft()
                window.append(digits[j + 1] - digits[j])

        number_of_buyers = len(self.buyer_secret_starts)

        for a0 in range(-9, 10):
            print(f"trying sequence starting w/: {a0}")
            for a1 in range(-9, 10):
                for a2 in range(-9, 10):
                    for a3 in range(-9, 10):
                        sequence = (a0, a1, a2, a3)
                        if not self.__is_valid_sequence(sequence):
                            continue

                        total = sum(difference_maps[i].get(sequence, 0) for i in range(number_of_buyers))

                        if total > maximum:
                            maximum_sequence = sequence
                            maximum = total
        print(f"maximum sequence: {maximum_sequence}")
        return maximum

    @staticmethod
    def __is_valid_sequence(sequence: tuple[int]) -> bool:
        # Reduce the search space. The following are either impossible or provable sub-optimal.
        a, b, c, d = sequence[0], sequence[1], sequence[2], sequence[3]
        s1 = a + b
        s2 = c + d
        s3 = b + c
        s4 = s1 + c
        s5 = s3 + d
        s6 = s1 + s2
        return abs(s1) <= 9 and abs(s2) <= 9 and abs(s3) <= 9 and abs(s4) <= 9 and abs(s5) <= 9 and abs(s6) <= 9 and s6 != -9


def tests():
    banana_maximiser = BananaMaximiser(read_lines("puzzle22_2_test_input1.txt"))
    t1 = banana_maximiser.maximum_bananas()
    assert t1 == 23


def main():
    tests()
    t0 = time.perf_counter()
    banana_maximiser = BananaMaximiser(read_lines("puzzle22_1.txt"))

    t1 = banana_maximiser.maximum_bananas()
    assert t1 == 1619
    print(f"time taken: {time.perf_counter() - t0}")


if __name__ == "__main__":
    main()
