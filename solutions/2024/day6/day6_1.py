from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules


class GuardPredictor:
    guard_states = {'^': Vector2D((0, 1)), '>': Vector2D((1, 0)),
                    'v': Vector2D((0, -1)), '<': Vector2D((-1, 0))}
    guard_arrow_from_direction = {Vector2D((0, 1)): '^', Vector2D((1, 0)): '>',
                                  Vector2D((0, -1)): 'v', Vector2D((-1, 0)): '<'}
    direction_encodings = {Vector2D((0, 1)): 0, Vector2D((1, 0)): 1,
                           Vector2D((0, -1)): 2, Vector2D((-1, 0)): 3}

    def __init__(self, lines: list[str]):
        self.n = len(lines)
        self.m = len(lines[0])
        self.__lines = lines
        self.start_position, self.start_direction = self.__start_info_from_lines(lines)
        self.guard_position, self.guard_direction = self.start_position, self.start_direction
        obstacles = self.__obstacles_from_lines(lines)
        self.obstacles_by_row = self.__obstacles_by_row(obstacles)
        self.obstacles_by_column = self.__obstacles_by_column(obstacles)

        self.cells_covered = [[0 for _ in range(self.m)] for _ in range(self.n)]

    def __repr__(self) -> str:
        lines = [''.join(char if char not in self.guard_states else '.' for char in line) for line in self.__lines]
        if self.guard_position.x == -1:
            return pad_with_horizontal_rules('\n'.join(lines))
        line_to_edit = lines[self.guard_position.x]
        line_to_edit = [char if j != self.guard_position.y else self.guard_arrow_from_direction[self.guard_direction]
                        for j, char in enumerate(line_to_edit)]
        lines[self.guard_position.x] = ''.join(line_to_edit)
        return pad_with_horizontal_rules('\n'.join(lines))

    def print_recent_movement(self) -> None:
        lines = [[char if char not in self.guard_states else '.' for char in line] for line in self.__lines]

        if 0 <= self.guard_position.x < self.n and 0 <= self.guard_position.y < self.m:
            line_to_edit = lines[self.guard_position.x]
            line_to_edit = [char if j != self.guard_position.y else self.guard_arrow_from_direction[self.guard_direction]
                            for j, char in enumerate(line_to_edit)]
            lines[self.guard_position.x] = line_to_edit

        for i, line in enumerate(lines):
            for j in range(self.m):
                if self.cells_covered[i][j] == 0:
                    continue
                line[j] = str(self.cells_covered[i][j])
        print(pad_with_horizontal_rules('\n'.join(''.join(line) for line in lines)))
        return None

    def __start_info_from_lines(self, lines: list[str]) -> (Vector2D, Vector2D):
        for i in range(self.n):
            for j in range(self.m):
                if lines[i][j] in self.guard_states:
                    return Vector2D((i, j)), self.guard_states[lines[i][j]]
        raise ZeroDivisionError

    def __obstacles_from_lines(self, lines: list[str]) -> list[Vector2D]:
        return [Vector2D((i, j)) for i in range(self.n) for j in range(self.m) if lines[i][j] == '#']

    def __obstacles_by_row(self, obstacles: list[Vector2D]) -> list[set[int]]:
        obstacles_by_row = [set() for _ in range(self.n)]
        for obstacle in obstacles:
            obstacles_by_row[obstacle.y].add(obstacle.x)
        return obstacles_by_row

    def __obstacles_by_column(self, obstacles: list[Vector2D]) -> list[set[int]]:
        obstacles_by_column = [set() for _ in range(self.m)]
        for obstacle in obstacles:
            obstacles_by_column[obstacle.x].add(obstacle.y)
        return obstacles_by_column

    def cell_coverage(self) -> int:
        for _ in range(100_000):
            x, y = self.guard_position.x, self.guard_position.y
            self.cells_covered[x][y] = 1
            self.progress_guard()
            if not (0 <= self.guard_position.x < self.n) or not (0 <= self.guard_position.y < self.n):
                return sum(1 if x > 0 else 0 for row in self.cells_covered for x in row)

        raise ZeroDivisionError

    def progress_guard(self) -> None:
        if self.guard_direction == self.guard_states['^']:
            self.progress_guard_up()
            return None

        if self.guard_direction == self.guard_states['>']:
            self.progress_guard_right()
            return None

        if self.guard_direction == self.guard_states['v']:
            self.progress_guard_down()
            return None

        if self.guard_direction == self.guard_states['<']:
            self.progress_guard_left()
            return None

    def progress_guard_up(self) -> None:
        self.guard_position += Vector2D((-1, 0))
        if self.guard_position.x in self.obstacles_by_row[self.guard_position.y]:
            self.guard_direction = self.guard_states['>']
            self.guard_position -= Vector2D((-1, 0))
        return None

    def progress_guard_right(self) -> None:
        self.guard_position += Vector2D((0, 1))
        if self.guard_position.y in self.obstacles_by_column[self.guard_position.x]:
            self.guard_direction = self.guard_states['v']
            self.guard_position -= Vector2D((0, 1))
        return None

    def progress_guard_down(self) -> None:
        self.guard_position += Vector2D((1, 0))
        if self.guard_position.x in self.obstacles_by_row[self.guard_position.y]:
            self.guard_direction = self.guard_states['<']
            self.guard_position -= Vector2D((1, 0))
        return None

    def progress_guard_left(self) -> None:
        self.guard_position += Vector2D((0, -1))
        if self.guard_position.y in self.obstacles_by_column[self.guard_position.x]:
            self.guard_direction = self.guard_states['^']
            self.guard_position -= Vector2D((0, -1))
        return None

    def unique_obstacles_that_create_loop_count_brute_force(self) -> int:
        self.cell_coverage()
        total = 0
        number_of_cells_checked = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.cells_covered[i][j] != 1:
                    continue
                if Vector2D((i, j)) == self.start_position:
                    continue
                print(f"Number of cells checked: {number_of_cells_checked}")
                number_of_cells_checked += 1
                obstacle = Vector2D((i, j))
                self.obstacles_by_row[obstacle.y].add(obstacle.x)
                self.obstacles_by_column[obstacle.x].add(obstacle.y)
                self.guard_position = self.start_position
                self.guard_direction = self.start_direction

                new_cells_covered = [[0 for _ in range(self.m)] for _ in range(self.n)]
                directions_covered = [[set() for _ in range(self.m)] for _ in range(self.n)]

                for _ in range(10_000):
                    x, y = self.guard_position.x, self.guard_position.y
                    new_cells_covered[x][y] = 1
                    directions_covered[x][y].add(self.direction_encodings[self.guard_direction])
                    self.progress_guard()
                    x, y = self.guard_position.x, self.guard_position.y
                    if not (0 <= self.guard_position.x < self.n) or not (0 <= self.guard_position.y < self.n):
                        self.obstacles_by_row[obstacle.y].remove(obstacle.x)
                        self.obstacles_by_column[obstacle.x].remove(obstacle.y)
                        break
                    cell_repeated = new_cells_covered[x][y] == 1
                    if cell_repeated and self.direction_encodings[self.guard_direction] in directions_covered[x][y]:
                        self.obstacles_by_row[obstacle.y].remove(obstacle.x)
                        self.obstacles_by_column[obstacle.x].remove(obstacle.y)
                        total += 1
                        break
        return total


def tests():
    guard_predictor = GuardPredictor(read_lines("puzzle6_1_test_input1.txt"))

    t1 = guard_predictor.cell_coverage()
    assert t1 == 41


def main():
    tests()

    guard_predictor = GuardPredictor(read_lines("puzzle6_1.txt"))
    t2 = guard_predictor.cell_coverage()
    assert t2 == 5564

    guard_predictor.print_recent_movement()

if __name__ == "__main__":
    main()
