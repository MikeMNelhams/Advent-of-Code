from handy_dandy_library.file_processing import read_lines


RollList = list[tuple[int, int]]


class PaperRollGrid:
    def __init__(self, lines: list[str]):
        self.grid = [[x for x in row] for row in lines]
        self.n = len(lines)
        self.m = len(lines[0])

    def count_future_accessible_rolls(self) -> int:
        total = 0
        for _ in range(100_000):
            removables = self.removable_rolls()
            count = len(removables)
            if count == 0:
                return total
            total += count
            for i, j in removables:
                self.grid[i][j] = "."
        raise RuntimeError("You ruined christmas!")

    def removable_rolls(self) -> RollList:
        removable_rolls = []
        removable_rolls += self.removable_middle_rolls()
        removable_rolls += self.removable_top_rolls()
        removable_rolls += self.removable_bottom_rolls()
        removable_rolls += self.removable_left_rolls()
        removable_rolls += self.removable_right_rolls()
        removable_rolls += self.removable_corner_rolls()
        return removable_rolls

    def count_accessible_rolls(self) -> int:
        return len(self.removable_rolls())

    def removable_corner_rolls(self) -> RollList:
        removable_rolls = []
        corner_indices = [0, -1]
        for i in corner_indices:
            for j in corner_indices:
                if self.grid[i][j] == "@":
                    removable_rolls.append((i, j))
        return removable_rolls

    def removable_left_rolls(self) -> RollList:
        removable_rolls = []
        for i in range(1, self.n - 1):
            if self.grid[i][0] != "@":
                continue
            neighbour_rolls = sum(int(self.grid[i + u][v] == "@")
                                  for u in range(-1, 2)
                                  for v in range(0, 2)) - 1
            if neighbour_rolls < 4:
                removable_rolls.append((i, 0))
        return removable_rolls

    def removable_right_rolls(self) -> RollList:
        removable_rolls = []
        for i in range(1, self.n - 1):
            if self.grid[i][-1] != "@":
                continue
            neighbour_rolls = sum(int(self.grid[i + u][v - 1] == "@")
                                  for u in range(-1, 2)
                                  for v in range(-1, 1)) - 1
            if neighbour_rolls < 4:
                removable_rolls.append((i, -1))
        return removable_rolls

    def removable_bottom_rolls(self) -> RollList:
        removable_rolls = []
        for j in range(1, self.m - 1):
            if self.grid[-1][j] != "@":
                continue
            neighbour_rolls = sum(int(self.grid[u - 1][j + v] == "@")
                                  for u in range(-1, 1)
                                  for v in range(-1, 2)) - 1
            if neighbour_rolls < 4:
                removable_rolls.append((-1, j))
        return removable_rolls

    def removable_top_rolls(self) -> RollList:
        removable_rolls = []
        for j in range(1, self.m - 1):
            if self.grid[0][j] != "@":
                continue
            neighbour_rolls = sum(int(self.grid[u][j + v] == "@")
                                  for u in range(0, 2)
                                  for v in range(-1, 2)) - 1
            if neighbour_rolls < 4:
                removable_rolls.append((0, j))
        return removable_rolls

    def removable_middle_rolls(self) -> RollList:
        removable_rolls = []
        for i in range(1, self.n - 1):
            for j in range(1, self.m - 1):
                if self.grid[i][j] != "@":
                    continue
                neighbour_rolls = sum(int(self.grid[i + u][j + v] == "@")
                                      for u in range(-1, 2)
                                      for v in range(-1, 2)) - 1
                if neighbour_rolls < 4:
                    removable_rolls.append((i, j))
        return removable_rolls


def accessible_paper_rolls_count(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    grid = PaperRollGrid(lines)
    return grid.count_accessible_rolls()


def main():
    assert accessible_paper_rolls_count("puzzle4_1_test_input.txt") == 13
    t = accessible_paper_rolls_count("puzzle4_1.txt")
    print(t)


if __name__ == "__main__":
    main()
