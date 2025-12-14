import collections

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D
from itertools import combinations
from collections import deque


class MovieTheatre:
    INF = 10 ** 9

    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.red_tiles = [Vector2D(tuple(int(x) for x in line.split(','))) for line in lines]

    def largest_rectangle_area(self) -> int:
        area_best = 0
        n = len(self.red_tiles)
        for i, j in combinations(range(n), 2):
            a = self.red_tiles[i]
            b = self.red_tiles[j]
            area = (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)
            area_best = max(area, area_best)
        return area_best

    def largest_hull_inscribed_rectangle_area(self) -> int:
        n = len(self.red_tiles)
        pairs = []
        for i, j in combinations(range(n), 2):
            a = self.red_tiles[i]
            b = self.red_tiles[j]
            area = (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)
            pairs.append((area, i, j))
        pairs.sort(key=lambda x: x[0], reverse=True)

        compressed_x = {x: 2 * i for i, x in
                        enumerate(sorted(set(v.x for v in self.red_tiles)))}
        compressed_y = {y: 2 * i for i, y in
                        enumerate(sorted(set(v.y for v in self.red_tiles)))}

        def compressed_red_tile(index: int) -> Vector2D:
            return Vector2D((compressed_x[self.red_tiles[index].x],
                             compressed_y[self.red_tiles[index].y]))

        hull_points = set()
        for i in range(n):
            a = compressed_red_tile(i)
            b = compressed_red_tile((i + 1) % n)
            if a.x == b.x:
                for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                    hull_points.add(Vector2D((a.x, y)))

            if a.y == b.y:
                for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
                    hull_points.add(Vector2D((x, a.y)))

        hull_minx = 0
        hull_miny = self.INF

        for i in range(n):
            u = compressed_red_tile(i)
            if u.x == hull_minx:
                hull_miny = min(u.y, hull_miny)

        to_check = deque([Vector2D((hull_minx + 1, hull_miny + 1))])
        directions = (Vector2D((0, 1)), Vector2D((1, 0)),
                      Vector2D((0, -1)), Vector2D((-1, 0)))
        while to_check:
            u = to_check.pop()

            for direction in directions:
                v = u + direction
                if v not in hull_points:
                    hull_points.add(v)
                    to_check.append(v)

        for c, (area, i, j) in enumerate(pairs):
            a, c = compressed_red_tile(i), compressed_red_tile(j)
            maxx = max(a.x, c.x)
            maxy = max(a.y, c.y)
            minx = min(a.x, c.x)
            miny = min(a.y, c.y)
            if minx == maxx or miny == maxy:
                continue
            if any(Vector2D((x, y)) not in hull_points
                   for x in range(minx, maxx + 1)
                   for y in (miny, maxy)):
                continue
            if any(Vector2D((x, y)) not in hull_points
                   for y in range(miny, maxy + 1)
                   for x in (minx, maxx)):
                continue

            return area

        raise ValueError("NONE ARE INSIDE, WHAT???")


def main():
    test_movie_theatre = MovieTheatre("puzzle9_1_test_input.txt")
    assert test_movie_theatre.largest_rectangle_area() == 50

    movie_theatre = MovieTheatre("puzzle9_1.txt")
    t = movie_theatre.largest_rectangle_area()
    print(t)


if __name__ == "__main__":
    main()
