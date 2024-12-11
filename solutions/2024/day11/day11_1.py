import math

from handy_dandy_library.file_processing import read_lines


class EngravedStones:
    def __init__(self, lines: list[str]):
        self.stones = [int(x) for x in lines[0].split(' ')]
        self.memo = {}

    def count_after_blinks_brute_force(self, number_of_blinks: int) -> int:
        stones = [x for x in self.stones]
        for i in range(number_of_blinks):
            next_stones = []
            for x in stones:
                if x == 0:
                    next_stones.append(1)
                    continue

                d = self.digits_count(x)
                if d & 1:
                    next_stones.append(x * 2024)
                    continue

                x_str = str(x)
                middle = d // 2
                next_stones.append(int(x_str[:middle]))
                next_stones.append(int(x_str[middle:]))
            stones = next_stones
        return len(stones)

    def count_after_blinks(self, number_of_blinks: int) -> int:
        return sum(self.blink_stone_count(stone, number_of_blinks) for stone in self.stones)

    def blink_stone_count(self, stone: int, number_of_blinks: int) -> int:
        if number_of_blinks == 0:
            return 1
        key = (stone, number_of_blinks)
        if key in self.memo:
            return self.memo[key]

        d = self.digits_count(stone)
        if stone == 0:
            result = self.blink_stone_count(1, number_of_blinks - 1)
        elif d & 1:
            result = self.blink_stone_count(stone * 2024, number_of_blinks - 1)
        else:
            middle = d // 2
            result = self.blink_stone_count(int(str(stone)[:middle]), number_of_blinks - 1)
            result += self.blink_stone_count(int(str(stone)[middle:]), number_of_blinks - 1)
        self.memo[key] = result
        return result

    @staticmethod
    def digits_count(x: int) -> int:
        if x == 0:
            return 1
        return math.floor(math.log10(x)) + 1


def tests():
    engraved_stones = EngravedStones(read_lines("puzzle11_1_test_input1.txt"))

    t1 = engraved_stones.count_after_blinks_brute_force(25)
    print(t1)
    assert t1 == 55312


def main():
    tests()

    engraved_stones = EngravedStones(read_lines("puzzle11_1.txt"))

    t2 = engraved_stones.count_after_blinks_brute_force(25)
    assert t2 == 190865


if __name__ == "__main__":
    main()
