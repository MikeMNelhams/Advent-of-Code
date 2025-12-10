from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D
from itertools import combinations


class MovieTheatre:
    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.red_tiles = [Vector2D(tuple(int(x) for x in line.split(','))) for line in lines]
        print(self.red_tiles)

    def largest_rectangle_area(self) -> int:
        area_best = 0
        n = len(self.red_tiles)
        for i, j in combinations(range(n), 2):
            a = self.red_tiles[i]
            b = self.red_tiles[j]
            area = abs(a.x - b.x + 1) * abs(a.y - b.y + 1)
            area_best = max(area, area_best)
        return area_best


def main():
    test_movie_theatre = MovieTheatre("puzzle9_1_test_input.txt")
    assert test_movie_theatre.largest_rectangle_area() == 50

    movie_theatre = MovieTheatre("puzzle9_1.txt")
    t = movie_theatre.largest_rectangle_area()
    print(t)


if __name__ == "__main__":
    main()
