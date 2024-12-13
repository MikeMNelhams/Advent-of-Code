from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D


from collections import defaultdict


class RegionMetrics:
    UP = Vector2D((-1, 0))
    RIGHT = Vector2D((0, 1))
    DOWN = Vector2D((1, 0))
    LEFT = Vector2D((0, -1))

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.n = len(lines)
        self.m = len(lines[0])

    def total_fence_price(self) -> int:
        total = 0

        regions = self.__regions()

        for region_name, region in regions.items():
            area = len(region)
            perimeter = 0
            for plot in region:
                up = plot + self.UP
                right = plot + self.RIGHT
                down = plot + self.DOWN
                left = plot + self.LEFT
                region_set = set(region)
                for coordinate in (up, right, down, left):
                    if not self.is_within_bounds(coordinate):
                        perimeter += 1
                        continue
                    if coordinate in region_set:
                        continue
                    name = self.lines[coordinate.y][coordinate.x]
                    if name != region_name:
                        perimeter += 1
            total += area * perimeter

        return total

    def total_discounted_fence_price(self) -> int:
        total = 0
        regions = self.__regions()

        for region_name, region in regions.items():
            area = len(region)
            region_name = region_name[0]

            if len(region) <= 2:
                total += area * 4
                continue

            perimeter = 0
            for plot in region:
                up = plot + self.UP
                right = plot + self.RIGHT
                down = plot + self.DOWN
                left = plot + self.LEFT

                is_up_valid = not self.is_within_bounds(up) or self.lines[up.y][up.x] != region_name
                is_right_valid = not self.is_within_bounds(right) or self.lines[right.y][right.x] != region_name
                is_down_valid = not self.is_within_bounds(down) or self.lines[down.y][down.x] != region_name
                is_left_valid = not self.is_within_bounds(left) or self.lines[left.y][left.x] != region_name

                if is_left_valid and is_up_valid:
                    perimeter += 1  # NW exterior corner
                if is_up_valid and is_right_valid:
                    perimeter += 1  # NE exterior corner
                if is_right_valid and is_down_valid:
                    perimeter += 1  # SE exterior corner
                if is_down_valid and is_left_valid:
                    perimeter += 1  # SW exterior corner

                up_right = up + self.RIGHT
                up_left = up + self.LEFT
                down_right = down + self.RIGHT
                down_left = down + self.LEFT

                is_up_left_valid = self.is_within_bounds(up_left) and self.lines[up_left.y][up_left.x] != region_name
                is_up_right_valid = self.is_within_bounds(up_right) and self.lines[up_right.y][up_right.x] != region_name
                is_down_right_valid = self.is_within_bounds(down_right) and self.lines[down_right.y][down_right.x] != region_name
                is_down_left_valid = self.is_within_bounds(down_left) and self.lines[down_left.y][down_left.x] != region_name

                if not is_left_valid and not is_up_valid and is_up_left_valid:
                    perimeter += 1  # NW interior corner
                if not is_up_valid and not is_right_valid and is_up_right_valid:
                    perimeter += 1  # NE interior corner
                if not is_right_valid and not is_down_valid and is_down_right_valid:
                    perimeter += 1  # SE interior corner
                if not is_down_valid and not is_left_valid and is_down_left_valid:
                    perimeter += 1  # SW interior corner

            total += area * perimeter

        return total

    def __regions(self) -> dict[str, list[Vector2D]]:
        all_checked = set()
        regions = defaultdict(set)
        for j in range(self.n):
            for i in range(self.m):
                start = Vector2D((i, j))

                if start in all_checked:
                    continue

                checked = set()
                start_plot = self.lines[j][i]
                to_check = [start]

                plot_name_new = start_plot + str(start)

                regions[plot_name_new].add(start)
                all_checked.add(start)

                while to_check:
                    plot = to_check.pop()

                    if plot in checked:
                        continue

                    checked.add(plot)

                    up = plot + self.UP
                    right = plot + self.RIGHT
                    down = plot + self.DOWN
                    left = plot + self.LEFT

                    for coordinate in (up, right, down, left):
                        if not self.is_within_bounds(coordinate):
                            continue
                        plot_name = self.lines[coordinate.y][coordinate.x]
                        if plot_name != start_plot:
                            continue
                        if coordinate not in regions[plot_name_new]:
                            regions[plot_name_new].add(coordinate)
                            all_checked.add(coordinate)
                        to_check.append(coordinate)
        return regions

    def is_within_bounds(self, coordinate: Vector2D) -> bool:
        return (0 <= coordinate.x < self.m) and (0 <= coordinate.y < self.n)


def tests():
    region_metrics = RegionMetrics(read_lines("puzzle12_1_test_input1.txt"))
    t1 = region_metrics.total_fence_price()
    assert t1 == 140

    region_metrics2 = RegionMetrics(read_lines("puzzle12_1_test_input2.txt"))
    t2 = region_metrics2.total_fence_price()
    assert t2 == 772

    region_metrics3 = RegionMetrics(read_lines("puzzle12_1_test_input3.txt"))
    t3 = region_metrics3.total_fence_price()
    assert t3 == 1930


def main():
    tests()

    region_metrics = RegionMetrics(read_lines("puzzle12_1.txt"))
    t1 = region_metrics.total_fence_price()
    assert t1 == 1424006


if __name__ == "__main__":
    main()
