from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D


class EasterBunnyHQBathroom:
    UP = Vector2D((-1, 0))
    RIGHT = Vector2D((0, 1))
    DOWN = Vector2D((1, 0))
    LEFT = Vector2D((0, -1))

    def __init__(self, lines: list[str]):
        self.robots = [Robot(line) for line in lines]

    def safety_factor(self, width: int, height: int) -> int:
        for robot in self.robots:
            robot.step(100, width, height)
        self.print_robots_quadrants(width, height)

        width_middle = width // 2
        height_middle = height // 2
        quadrant0 = sum(1 if robot.is_within_quadrant(Vector2D((0, 0)),
                                                      Vector2D((width_middle - 1, height_middle - 1)))
                        else 0 for robot in self.robots)
        quadrant1 = sum(1 if robot.is_within_quadrant(Vector2D((width_middle + 1, 0)),
                                                      Vector2D((width - 1, height_middle - 1)))
                        else 0 for robot in self.robots)
        quadrant2 = sum(1 if robot.is_within_quadrant(Vector2D((0, height_middle + 1)),
                                                      Vector2D((width_middle - 1, height - 1)))
                        else 0 for robot in self.robots)
        quadrant3 = sum(1 if robot.is_within_quadrant(Vector2D((width_middle + 1, height_middle + 1)),
                                                      Vector2D((width - 1, height - 1)))
                        else 0 for robot in self.robots)
        return quadrant0 * quadrant1 * quadrant2 * quadrant3

    def print_robots_quadrants(self, width: int, height: int) -> None:
        grid = [[0 for _ in range(width)] for _ in range(height)]
        for robot in self.robots:
            grid[robot.position.y][robot.position.x] += 1

        middle_width = width // 2
        middle_height = height // 2

        for i in range(width):
            grid[middle_height][i] = -1

        for j in range(height):
            grid[j][middle_width] = -1

        grid_str = '\n'.join(''.join([str(x) if x > 0 else ' ' if x == -1 else '.' for x in row]) for row in grid)
        print(grid_str)
        return None

    def attempt_secret_xmas(self, width: int, height: int, max_iterations: int=100_000) -> None:
        for i in range(max_iterations):
            print(f"Step check: {i + 1} (max: {max_iterations})")
            for robot in self.robots:
                robot.step(1, width, height)
            if not self.robots_are_overlapped(width, height):
                self.print_robots_grid(width, height)
                return None

        raise ZeroDivisionError

    def print_robots_grid(self, width: int, height: int) -> None:
        grid = [[0 for _ in range(width)] for _ in range(height)]
        for robot in self.robots:
            grid[robot.position.y][robot.position.x] += 1

        grid_str = '\n'.join(''.join([str(x) if x > 0 else '.' for x in row]) for row in grid)
        print(grid_str)
        return None

    def robots_are_overlapped(self, width: int, height: int) -> bool:
        grid = [[0 for _ in range(width)] for _ in range(height)]
        for robot in self.robots:
            if grid[robot.position.y][robot.position.x]:
                return True
            grid[robot.position.y][robot.position.x] = 1
        return False


class Robot:
    def __init__(self, line: str):
        phrases = line.split(' ')
        self.position = self.__position(phrases[0])
        self.velocity = self.__velocity(phrases[1])

    def __repr__(self) -> str:
        return f"Robot[p={self.position}, v={self.velocity}]"

    def step(self, epochs: int, width: int, height: int) -> None:
        self.position = self.position + self.velocity * epochs
        self.position = self.position.mod_vector(Vector2D((width, height)))
        return None

    def is_within_quadrant(self, top_left: Vector2D, bottom_right: Vector2D) -> bool:
        return (top_left.x <= self.position.x <= bottom_right.x) and (top_left.y <= self.position.y <= bottom_right.y)

    @staticmethod
    def __position(phrase: str) -> Vector2D:
        halves = phrase.split(',')

        x = int(halves[0].split('=')[1])
        y = int(halves[1])

        return Vector2D((x, y))

    @staticmethod
    def __velocity(phrase: str) -> Vector2D:
        halves = phrase.split(',')

        x = int(halves[0].split('=')[1])
        y = int(halves[1])

        return Vector2D((x, y))


def tests():
    ehbq_bathroom = EasterBunnyHQBathroom(read_lines("puzzle14_1_test_input1.txt"))

    t1 = ehbq_bathroom.safety_factor(11, 7)
    print(t1)
    assert t1 == 12


def main():
    tests()

    ehbq_bathroom = EasterBunnyHQBathroom(read_lines("puzzle14_1.txt"))

    t1 = ehbq_bathroom.safety_factor(101, 103)
    assert t1 == 225521010


if __name__ == "__main__":
    main()
