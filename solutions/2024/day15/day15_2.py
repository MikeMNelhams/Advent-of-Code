from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D


class LanternfishDoubleWarehouse:
    UP = Vector2D((0, -1))
    RIGHT = Vector2D((1, 0))
    DOWN = Vector2D((0, 1))
    LEFT = Vector2D((-1, 0))

    encodings = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT}
    reverse_encodings = {UP: '^', RIGHT: '>', DOWN: 'V', LEFT: '<'}

    def __init__(self, lines: list[str]):
        grid_lines = []
        instructions = ''
        for i, line in enumerate(lines):
            if line == '':
                grid_lines = lines[:i]
                instructions = lines[i + 1]
                break
        if not grid_lines:
            raise ValueError

        self.n = len(grid_lines)
        self.m = len(grid_lines[0] * 2)

        self.walls = set()
        self.left_boxes = set()
        self.right_boxes = set()
        self.robot_start_position = Vector2D((-1, -1))

        for j in range(self.n):
            for i in range(len(grid_lines[0])):
                char = grid_lines[j][i]

                if char == '#':
                    self.walls.add(Vector2D((i * 2, j)))
                    self.walls.add(Vector2D((i * 2 + 1, j)))

                elif char == 'O':
                    self.left_boxes.add((Vector2D((i * 2, j))))
                    self.right_boxes.add((Vector2D((i * 2 + 1, j))))

                elif char == '@':
                    self.robot_start_position = Vector2D((i * 2, j))

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
                elif coordinate in self.left_boxes:
                    chars[j][i] = '['
                elif coordinate in self.right_boxes:
                    chars[j][i] = ']'
                elif coordinate == self.robot_position:
                    chars[j][i] = '@'
        return '\n'.join(''.join(row) for row in chars)

    def robot_follow_instructions(self) -> None:
        for direction in self.robot_directions:
            self.step(direction)
        return None

    def step(self, direction: Vector2D) -> None:
        ahead_of_robot = self.robot_position + direction
        if ahead_of_robot in self.walls:
            return None
        if ahead_of_robot not in self.left_boxes and ahead_of_robot not in self.right_boxes:
            self.robot_position = ahead_of_robot
            return None

        if direction == self.LEFT:
            self.__try_move_left(direction)
            return None
        elif direction == self.RIGHT:
            self.__try_move_right(direction)
            return None

        self.__try_move_vertical(direction)
        return None

    def __try_move_vertical(self, direction: Vector2D) -> None:
        # Pushing up/down
        # 1.   2.   3.  4.   5.
        # ..  .[]  [].  [].  [][]
        # []  [].  .[]  [].  .[].

        ahead_of_robot = self.robot_position + direction
        to_check_are_movable = [ahead_of_robot]  # Always the LEFT [
        if ahead_of_robot in self.right_boxes:
            to_check_are_movable = [ahead_of_robot + self.LEFT]
        to_move = []
        to_move_set = set()
        while to_check_are_movable:
            block = to_check_are_movable.pop()
            ahead_of_block = block + direction
            ahead_of_right_block = ahead_of_block + self.RIGHT

            if ahead_of_block in self.walls or ahead_of_right_block in self.walls:
                return None

            left_is_blocked_by_left = ahead_of_block in self.left_boxes

            if block not in to_move_set:
                if block in self.right_boxes:
                    to_move.append(block + self.LEFT)
                    to_move_set.add(block + self.LEFT)
                else:
                    to_move.append(block)
                    to_move_set.add(block)

            if left_is_blocked_by_left:
                # Case 4
                to_check_are_movable.append(ahead_of_block)
                continue

            left_is_blocked_by_right = ahead_of_block in self.right_boxes
            right_is_blocked_by_left = ahead_of_right_block in self.left_boxes

            if not left_is_blocked_by_right and not right_is_blocked_by_left:
                continue

            # Case 5
            if left_is_blocked_by_right and right_is_blocked_by_left:
                to_check_are_movable.append(ahead_of_block + self.LEFT)
                to_check_are_movable.append(ahead_of_right_block)
                continue

            # Case 3
            if left_is_blocked_by_right and not right_is_blocked_by_left:
                to_check_are_movable.append(ahead_of_block + self.LEFT)
                continue

            # Case 2
            if right_is_blocked_by_left and not left_is_blocked_by_right:
                to_check_are_movable.append(ahead_of_right_block)
                continue

        if not to_move:
            return None

        self.robot_position = ahead_of_robot
        for block in to_move:
            right_block = block + self.RIGHT
            self.left_boxes.remove(block)
            self.right_boxes.remove(right_block)
        for block in to_move:
            right_block = block + self.RIGHT
            self.left_boxes.add(block + direction)
            self.right_boxes.add(right_block + direction)
        return None

    def __try_move_left(self, direction: Vector2D) -> None:
        ahead_of_robot = self.robot_position + direction * 2
        to_check_are_movable = [ahead_of_robot]
        to_move = []
        while to_check_are_movable:
            block = to_check_are_movable.pop()
            ahead_of_block = block + direction
            if ahead_of_block in self.walls:
                return None

            to_move.append(block)
            if ahead_of_block in self.right_boxes:
                to_check_are_movable.append(ahead_of_block + direction)

        if not to_move:
            return None

        ahead_of_robot2 = ahead_of_robot - direction
        self.robot_position = ahead_of_robot2

        for block in reversed(to_move):
            self.left_boxes.remove(block)
            self.right_boxes.add(block)
            previous = block + direction
            if previous in self.right_boxes:
                self.right_boxes.remove(previous)
            self.left_boxes.add(previous)

        self.right_boxes.remove(ahead_of_robot2)
        return None

    def __try_move_right(self, direction: Vector2D):
        ahead_of_robot = self.robot_position + direction * 2
        to_check_are_movable = [ahead_of_robot]
        to_move = []
        while to_check_are_movable:
            block = to_check_are_movable.pop()
            ahead_of_block = block + direction
            if ahead_of_block in self.walls:
                return None

            to_move.append(block)
            if ahead_of_block in self.left_boxes:
                to_check_are_movable.append(ahead_of_block + direction)

        if not to_move:
            return None

        ahead_of_robot2 = ahead_of_robot - direction
        self.robot_position = ahead_of_robot2

        for block in to_move:
            self.right_boxes.remove(block)
            self.left_boxes.add(block)
            previous = block + direction
            if previous in self.left_boxes:
                self.left_boxes.remove(previous)
            self.right_boxes.add(previous)

        self.left_boxes.remove(ahead_of_robot2)
        return None

    def boxes_gps_total(self) -> int:
        total = 0
        for box in self.left_boxes:
            total += box.y * 100 + box.x
        return total


def tests():
    warehouse = LanternfishDoubleWarehouse(read_lines("puzzle15_2_test_input1.txt"))

    warehouse.robot_follow_instructions()
    print(warehouse)

    warehouse2 = LanternfishDoubleWarehouse(read_lines("puzzle15_1_test_input2.txt"))

    warehouse2.robot_follow_instructions()
    t2 = warehouse2.boxes_gps_total()
    assert t2 == 9021


def main():
    tests()

    warehouse = LanternfishDoubleWarehouse(read_lines("puzzle15_1.txt"))

    warehouse.robot_follow_instructions()
    t1 = warehouse.boxes_gps_total()
    assert t1 == 1392847


if __name__ == "__main__":
    main()
