from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D


class LanternfishWarehouse:
    UP = Vector2D((0, -1))
    RIGHT = Vector2D((1, 0))
    DOWN = Vector2D((0, 1))
    LEFT = Vector2D((-1, 0))

    encodings = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT}

    def __init__(self, lines: list[str]):
        grid_lines = []
        instructions = ''
        for i, line in enumerate(lines):
            if line == '':
                grid_lines = lines[:i]
                instructions = lines[i+1]
                break
        if not grid_lines:
            raise ValueError

        self.lines = grid_lines
        self.n = len(grid_lines)
        self.m = len(grid_lines[0])
        self.walls = set()
        self.boxes = set()
        self.robot_start_position = Vector2D((-1, -1))

        for j in range(self.n):
            for i in range(self.m):
                char = grid_lines[j][i]

                if char == '#':
                    self.walls.add(Vector2D((i, j)))
                elif char == 'O':
                    self.boxes.add((Vector2D((i, j))))
                elif char == '@':
                    self.robot_start_position = Vector2D((i, j))

        if self.robot_start_position.x == -1:
            raise ValueError

        self.robot_position = self.robot_start_position
        self.robot_directions = [self.encodings[x] for x in instructions]

    def __repr__(self) -> str:
        chars = [['.' for _ in range(self.m)] for _ in range(self.n)]
        for j in range(self.n):
            for i in range(self.m):
                coordinate = Vector2D((i, j))
                if coordinate in self.walls:
                    chars[j][i] = '#'
                if coordinate in self.boxes:
                    chars[j][i] = 'O'
                if coordinate == self.robot_position:
                    chars[j][i] = '@'
        return '\n'.join(''.join(row) for row in chars)

    def robot_follow_instructions(self) -> None:
        for direction in self.robot_directions:
            self.step(direction)
        return None

    def step(self, direction: Vector2D) -> None:
        to_check = [self.robot_position]
        while to_check:
            coordinate = to_check.pop()
            coordinate_moved = coordinate + direction

            if coordinate_moved in self.walls:
                return None
            if coordinate_moved in self.boxes:
                to_check.append(coordinate_moved)
                continue

            position_ahead_of_robot = self.robot_position + direction
            if coordinate_moved == position_ahead_of_robot:
                self.robot_position = self.robot_position + direction
                return None
            self.robot_position = self.robot_position + direction
            self.boxes.remove(position_ahead_of_robot)
            self.boxes.add(coordinate_moved)
            return None

    def boxes_gps_total(self) -> int:
        total = 0
        for box in self.boxes:
            total += box.y * 100 + box.x
        return total


def tests():
    warehouse = LanternfishWarehouse(read_lines("puzzle15_1_test_input1.txt"))

    warehouse.robot_follow_instructions()
    t1 = warehouse.boxes_gps_total()
    assert t1 == 2028

    warehouse2 = LanternfishWarehouse(read_lines("puzzle15_1_test_input2.txt"))

    warehouse2.robot_follow_instructions()
    t2 = warehouse2.boxes_gps_total()
    assert t2 == 10092


def main():
    tests()

    warehouse = LanternfishWarehouse(read_lines("puzzle15_1.txt"))

    warehouse.robot_follow_instructions()
    t1 = warehouse.boxes_gps_total()
    assert t1 == 1371036


if __name__ == "__main__":
    main()
