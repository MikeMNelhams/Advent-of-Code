from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D


class TopographicMap:
    up = Vector2D((-1, 0))
    right = Vector2D((0, 1))
    down = Vector2D((1, 0))
    left = Vector2D((0, -1))

    def __init__(self, lines: list[str]):
        self.n = len(lines)
        self.m = len(lines[0])
        self.lines = lines

    def trailhead_scores(self) -> int:
        total = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.lines[i][j] == '0':
                    total += self.__trailhead_score(Vector2D((i, j)))
        return total

    def trailhead_ratings(self) -> int:
        total = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.lines[i][j] == '0':
                    total += self.__trailhead_rating(Vector2D((i, j)))
        return total

    def is_within_bounds(self, coordinate: Vector2D) -> bool:
        return (0 <= coordinate.x < self.n) and (0 <= coordinate.y < self.n)

    def __trailhead_score(self, start: Vector2D) -> int:
        trailheads_connected = set()

        to_check = [start]
        while to_check:
            current = to_check.pop()
            next_value = int(self.lines[current.x][current.y]) + 1

            if next_value == 10:
                trailheads_connected.add(current)
                continue
            up = current + self.up
            right = current + self.right
            down = current + self.down
            left = current + self.left

            if self.is_within_bounds(up) and int(self.lines[up.x][up.y]) == next_value:
                to_check.append(up)
            if self.is_within_bounds(right) and int(self.lines[right.x][right.y]) == next_value:
                to_check.append(right)
            if self.is_within_bounds(down) and int(self.lines[down.x][down.y]) == next_value:
                to_check.append(down)
            if self.is_within_bounds(left) and int(self.lines[left.x][left.y]) == next_value:
                to_check.append(left)

        return len(trailheads_connected)

    def __trailhead_rating(self, start: Vector2D) -> int:

        total = 0

        to_check = [start]
        while to_check:
            current = to_check.pop()
            next_value = int(self.lines[current.x][current.y]) + 1

            if next_value == 10:
                total += 1
                continue
            up = current + self.up
            right = current + self.right
            down = current + self.down
            left = current + self.left

            if self.is_within_bounds(up) and int(self.lines[up.x][up.y]) == next_value:
                to_check.append(up)
            if self.is_within_bounds(right) and int(self.lines[right.x][right.y]) == next_value:
                to_check.append(right)
            if self.is_within_bounds(down) and int(self.lines[down.x][down.y]) == next_value:
                to_check.append(down)
            if self.is_within_bounds(left) and int(self.lines[left.x][left.y]) == next_value:
                to_check.append(left)

        return total


def tests():
    topographic_map = TopographicMap(read_lines("puzzle10_1_test_input1.txt"))
    t1 = topographic_map.trailhead_scores()

    assert t1 == 36


def main():
    tests()

    topographic_map = TopographicMap(read_lines("puzzle10_1.txt"))
    t2 = topographic_map.trailhead_scores()
    assert t2 == 782


if __name__ == "__main__":
    main()
