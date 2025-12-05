from handy_dandy_library.file_processing import read_lines


class Kitchen:
    def __init__(self, lines: list[str]):
        self.fresh_ingredient_ranges = self.__ingredient_ranges_from_lines(lines)
        self.ingredients = self.__ingredients_from_lines(lines)

    @staticmethod
    def __ingredient_ranges_from_lines(lines: list[str]) -> list[tuple[int, int]]:
        ingredient_ranges = []
        for line in lines:
            if line == "":
                return ingredient_ranges
            x = line.split("-")
            ingredient_ranges.append((int(x[0]), int(x[1])))
        raise ValueError("Input should be ingredient ranges, blank line, ingredients")

    @staticmethod
    def __ingredients_from_lines(lines: list[str]) -> list[int]:
        start_of_ingredients_index = -1
        for i, line in enumerate(lines):
            if line == "":
                start_of_ingredients_index = i
                break
        return [int(ingredient) for ingredient in lines[start_of_ingredients_index + 1:]]

    def fresh_ingredient_count(self) -> int:
        count = 0
        for x in self.ingredients:
            for ingredient_range in self.fresh_ingredient_ranges:
                if ingredient_range[0] <= x <= ingredient_range[1]:
                    count += 1
                    break
        return count

    def possible_fresh_ingredient_count(self) -> int:
        count = 0
        self.fresh_ingredient_ranges.sort(key=lambda x: (x[0], x[1]))

        n = len(self.fresh_ingredient_ranges)
        i = 0
        j = 1
        for _ in range(n + 1):
            if i == n - 1:
                break
            x0 = self.fresh_ingredient_ranges[i]
            x1 = self.fresh_ingredient_ranges[j]
            if x0[0] == x1[0]:
                i = j
                j += 1
                continue
            if x0[1] >= x1[1]:
                if j == n - 1:
                    return count + x0[1] - x0[0] + 1
                j += 1
                continue
            if x0[1] < x1[0]:
                count += x0[1] - x0[0] + 1
                i = j
                j += 1
                continue
            if x0[1] >= x1[0]:
                count += x1[0] - x0[0]
                i = j
                j += 1
                continue
            raise ZeroDivisionError("XMAS PANIC")

        last_range = self.fresh_ingredient_ranges[-1]
        count += last_range[1] - last_range[0] + 1
        return count


def main():
    test_kitchen = Kitchen(read_lines("puzzle5_1_test_input.txt"))
    assert test_kitchen.fresh_ingredient_count() == 3

    kitchen = Kitchen(read_lines("puzzle5_1.txt"))
    print(kitchen.fresh_ingredient_count())


if __name__ == "__main__":
    main()
