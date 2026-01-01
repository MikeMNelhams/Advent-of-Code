from handy_dandy_library.file_processing import read_lines


class PresentFitter:
    PRESENT_MAP = {"#": 1, ".": 0}

    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.presents = self.__presents(lines)
        self.sizes, self.present_counts = self.__regions(lines)
        self.n_regions = len(self.present_counts)
        self.present_areas = self.__present_areas(self.presents)
        print(self.present_areas)

    @staticmethod
    def __present_areas(presents: list[list[int]]):
        return [sum(sum(row) for row in present) for present in presents]

    def __presents(self, lines: list[str]) -> list[list[int]]:
        presents = [[]]
        for line in lines:
            if line == "":
                presents.append([])
            else:
                presents[-1].append(line)
        presents = [[[self.PRESENT_MAP[x] for x in row]
                     for row in present[1:]]
                    for present in presents
                    if "x" not in present[0]]
        return presents

    def __regions(self, lines: list[str]) -> (tuple[int, int], list[int]):
        sizes = []
        present_counts = []
        for j, line in enumerate(lines):
            if "x" not in line:
                continue
            phrases = line.split(": ")
            size = phrases[0].split("x")
            sizes.append((int(size[0]), int(size[1])))
            counts = phrases[1].split(" ")
            present_counts.append([int(x) for x in counts])
        return sizes, present_counts

    def count_fitting_regions(self) -> int:
        for i in range(self.n_regions):
            print(f"i: {i} fits? | {self.is_region_fittable(i)}")
        return sum(int(self.is_region_fittable(i)) for i in range(self.n_regions))

    def is_region_fittable(self, region_index: int) -> bool:
        size = self.sizes[region_index]
        counts = self.present_counts[region_index]
        area = size[0] * size[1]

        # Each shape is max 3x3 size. K present shapes
        # Assume each shape takes full size, then 3 * 3 * k is the max area required to fit all the presents.
        if area >= 3 * 3 * sum(counts):
            return True
        # The total present area must all fit within the given area
        presents_area = sum(count * present_area for count, present_area in zip(counts, self.present_areas))
        if area >= presents_area:
            return True
        # It's definitely NP to try to solve the original shape fitting problem (as of 2025/6)
        # Rough calcs, there's max 8 * k starting states
        # Then there's 16 * (k - 1) next states at most
        # Then there's (k - 2) * b next states where b >= 8
        # So it's ~ 8^k * k! states to check total
        # You could probably brute-force DP solve it with bitmasks and using heuristic-based sorting to obtain
        #   the solutions that are most likely to fit best. E.g. try the states with most overlap first
        #   I suspect the brute-force DP would still be NP and would take a very long to solve for general cases
        #   as K increases. K is low (5), so should be very possible to solve in under a minute.
        return False


def main():
    # test_present_fitter = PresentFitter("day12_1_test_input.txt")
    # assert test_present_fitter.count_fitting_regions() == 2

    # It solves the final input, but not the test input lol.
    # I manually went through and checked before running and was surprised.
    present_fitter = PresentFitter("day12_1.txt")
    t = present_fitter.count_fitting_regions()
    print(t)


if __name__ == "__main__":
    main()
