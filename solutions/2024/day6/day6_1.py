from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules


from collections import defaultdict


class GuardPredictor:
    guard_states = {'^': Vector2D((0, 1)), '>': Vector2D((1, 0)),
                    'v': Vector2D((0, -1)), '<': Vector2D((-1, 0))}
    guard_arrow_from_direction = {Vector2D((0, 1)): '^', Vector2D((1, 0)): '>',
                                  Vector2D((0, -1)): 'v', Vector2D((-1, 0)): '<'}
    direction_encodings = {Vector2D((0, 1)): 0, Vector2D((1, 0)): 1,
                           Vector2D((0, -1)): 2, Vector2D((-1, 0)): 3}
    movements_from_direction = {Vector2D((0, 1)): Vector2D((-1, 0)), Vector2D((1, 0)): Vector2D((0, 1)),
                                Vector2D((0, -1)): Vector2D((1, 0)), Vector2D((-1, 0)): Vector2D((0, -1))}

    def __init__(self, lines: list[str]):
        self.n = len(lines)
        self.m = len(lines[0])
        self.__lines = lines
        start_info = self.__start_info_from_lines(lines)
        self.start_position: Vector2D = start_info[0]
        self.start_direction: Vector2D = start_info[1]
        self.guard_position = self.start_position
        self.guard_direction = self.start_direction
        obstacles = self.__obstacles_from_lines(lines)
        self.obstacles = set(obstacles)

        self.cells_covered = [[0 for _ in range(self.m)] for _ in range(self.n)]

        self._directions = tuple(self.direction_encodings.keys())
        self.jump_table = {}
        self._prev_jump_spot = self.start_position

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
        self.guard_position = self.start_position
        self.guard_direction = self.start_direction

        for _ in range(10_000):
            x, y = self.guard_position.x, self.guard_position.y
            self.cells_covered[x][y] = 1

            self.progress_guard(True)
            if not (0 <= self.guard_position.x < self.n) or not (0 <= self.guard_position.y < self.n):
                return sum(1 if x > 0 else 0 for row in self.cells_covered for x in row)

        raise RuntimeError

    def turn_right(self) -> None:
        next_direction = (self.direction_encodings[self.guard_direction] + 1) % 4
        self.guard_direction = self._directions[next_direction]
        return None

    def progress_guard(self, is_recording_jump_table: bool = False, new_obstacle: Vector2D = None) -> None:
        key = (self.guard_position, self.guard_direction)

        use_jump_table = new_obstacle is None or (self.guard_position.x != new_obstacle.x and self.guard_position.y != new_obstacle.y)
        if use_jump_table and key in self.jump_table:
            steps = self.jump_table[key]
            self.guard_position += self.movements_from_direction[self.guard_direction] * steps
            self.turn_right()
        else:
            previous_position = self.guard_position

            self.guard_position += self.movements_from_direction[self.guard_direction]

            if self.guard_position in self.obstacles:
                if is_recording_jump_table:
                    self.jump_table[(self._prev_jump_spot, self.guard_direction)] = previous_position.manhattan_distance(self._prev_jump_spot)

                self.turn_right()
                self.guard_position = previous_position
                if is_recording_jump_table:
                    self._prev_jump_spot = self.guard_position
        return None

    def unique_obstacles_that_create_loop_count(self) -> int:
        total = 0

        self.cell_coverage()

        self.guard_position = self.start_position
        self.guard_direction = self.start_direction
        obstacles_checked = 0

        positions_checked = {self.start_position}

        for _ in range(10_000):
            previous_position = self.guard_position
            previous_direction = self.guard_direction
            self.progress_guard(new_obstacle=self.guard_position)
            if not (0 <= self.guard_position.x < self.n) or not (0 <= self.guard_position.y < self.n):
                return total

            if self.guard_position in positions_checked:
                continue

            obstacles_checked += 1
            positions_checked.add(self.guard_position)

            obstacle = self.guard_position
            branch_direction = self.guard_direction

            self.guard_position = previous_position
            self.guard_direction = previous_direction

            if self.does_guard_loop(obstacle):
                total += 1

            self.guard_position = obstacle
            self.guard_direction = branch_direction

        raise ZeroDivisionError

    def does_guard_loop(self, obstacle: Vector2D) -> bool:
        self.obstacles.add(obstacle)

        directions_covered = defaultdict(set)

        for _ in range(10_000):
            self.progress_guard(new_obstacle=obstacle)
            if not (0 <= self.guard_position.x < self.n) or not (0 <= self.guard_position.y < self.n):
                self.obstacles.remove(obstacle)
                return False
            guard_direction_encoding = self.direction_encodings[self.guard_direction]
            direction_repeated = guard_direction_encoding in directions_covered[self.guard_position]
            if direction_repeated:
                self.obstacles.remove(obstacle)
                return True
            directions_covered[self.guard_position].add(guard_direction_encoding)
        raise RuntimeError


def tests():
    guard_predictor = GuardPredictor(read_lines("puzzle6_1_test_input1.txt"))

    t1 = guard_predictor.cell_coverage()
    assert t1 == 41


def main():
    tests()

    guard_predictor = GuardPredictor(read_lines("puzzle6_1.txt"))
    t2 = guard_predictor.cell_coverage()
    assert t2 == 5564


if __name__ == "__main__":
    main()
