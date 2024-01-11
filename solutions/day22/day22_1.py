from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue

from collections import defaultdict, deque
from abc import abstractmethod
from typing import Iterable


class Vector3D:
    def __init__(self, values: tuple[int, int, int]):
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

    def __eq__(self, other: Vector3D) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other: int) -> Vector3D:
        return Vector3D((self.x * other, self.y * other, self.z * other))

    def copy(self):
        return Vector3D((self.x, self.y, self.z))

    @property
    def xy_projection(self) -> Vector3D:
        return Vector3D((self.x, self.y, 0))

    @property
    def manhattan_distance_from_zero(self) -> int:
        return self.x + self.y + self.z

    @property
    def first_non_zero_dim_index(self) -> int:
        for i, value in enumerate(self.values):
            if value != 0:
                return i
        raise TypeError

    @property
    def values(self) -> list[int]:
        return [self.x, self.y, self.z]

    @classmethod
    def zero(cls):
        return cls((0, 0, 0))


class Brick:
    def __init__(self, start: Vector3D, end: Vector3D, shape: Vector3D):
        self.start = start
        self.end = end
        self.shape_length = shape.manhattan_distance_from_zero + 1
        self.xy_projection = shape.xy_projection

    def __repr__(self) -> str:
        return f"{make_blue('B')}[{self.start} -> {self.end} @ {self.start.z}]"

    def is_below(self, point: Vector3D) -> bool:
        return point.z > self.end.z

    def frontier(self) -> list[Vector3D]:
        points = [self.start + self.unit_vector * i for i in range(self.shape_length)]
        points = [point.xy_projection for point in points]
        return points

    @property
    def all_coordinates(self) -> Iterable[Vector3D]:
        return (self.start + self.unit_vector * i for i in range(self.shape_length))

    @property
    @abstractmethod
    def shape_dimension(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def unit_vector(self) -> Vector3D:
        raise NotImplementedError

    @property
    @abstractmethod
    def height_of_shape(self) -> int:
        raise NotImplementedError


class XBrick(Brick):
    __unit_vector = Vector3D((1, 0, 0))

    @property
    def shape_dimension(self) -> int:
        return 0

    @property
    def unit_vector(self) -> Vector3D:
        return self.__unit_vector

    @property
    def height_of_shape(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{make_blue('X')}{super().__repr__()}"


class YBrick(Brick):
    __unit_vector = Vector3D((0, 1, 0))

    @property
    def shape_dimension(self) -> int:
        return 1

    @property
    def unit_vector(self) -> Vector3D:
        return self.__unit_vector

    @property
    def height_of_shape(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{make_blue('Y')}{super().__repr__()}"


class ZBrick(Brick):
    __unit_vector = Vector3D((0, 0, 1))

    @property
    def shape_dimension(self) -> int:
        return 2

    @property
    def unit_vector(self) -> Vector3D:
        return self.__unit_vector

    @property
    def height_of_shape(self) -> int:
        return self.end.z - self.start.z + 1

    def frontier(self) -> list[Vector3D]:
        return [self.start.xy_projection]

    def __repr__(self) -> str:
        return f"{make_blue('Z')}{super().__repr__()}"


class CBrick(Brick):
    """Single dot, doesn't stretch in any dimension"""
    __unit_vector = Vector3D.zero()

    @property
    def shape_dimension(self) -> int:
        return -1

    @property
    def unit_vector(self) -> Vector3D:
        return self.__unit_vector

    @property
    def height_of_shape(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{make_blue('C')}{super().__repr__()}"


class BrickFactory:
    _brick_dim_to_type = {0: XBrick, 1: YBrick, 2: ZBrick, 3: CBrick}

    @classmethod
    def from_line(cls, line: str) -> Brick:
        phrase_halves = line.split('~')
        start = Vector3D(tuple(int(x) for x in phrase_halves[0].split(',')))
        end = Vector3D(tuple(int(x) for x in phrase_halves[1].split(',')))
        shape = end - start
        if shape == Vector3D.zero():
            return cls._brick_dim_to_type[3](start, end, shape)
        shape_dimension = shape.first_non_zero_dim_index
        return cls._brick_dim_to_type[shape_dimension](start, end, shape)


class BrickFrontier:
    def __init__(self, x_size: int, y_size: int):
        self.x_max = x_size + 1
        self.y_max = y_size + 1
        # x,y -> [height, brick @ height @ (x,y)]
        self.data = [[[0, None] for _ in range(self.x_max)] for _ in range(self.y_max)]

    def __repr__(self) -> str:
        return f"Frontier:\n{'\n'.join(str(row) for row in self.data)}"

    def __getitem__(self, item: tuple[int, int]) -> tuple[int, int]:
        return self.data[item[0]][item[1]]

    def __setitem__(self, key: tuple[int, int], value: tuple[int, int]) -> None:
        self.data[key[0]][key[1]] = value
        return None

    def add(self, points: list[Vector3D], height_of_shape: int, brick_index: int) -> list[int]:
        max_height_below = max(self[(point.x, point.y)][0] for point in points)
        new_height = max_height_below + height_of_shape
        if max_height_below == 0:
            for point in points:
                self[(point.x, point.y)] = [new_height, brick_index]
            return []
        intersection_bricks = set()
        for point in points:
            if self[(point.x, point.y)][0] == max_height_below:
                intersection_bricks.add(self[(point.x, point.y)][1])
            self[(point.x, point.y)] = [new_height, brick_index]
        return list(intersection_bricks)


class FallingBricks:
    """What's that in the sky? OMG RUN"""

    def __init__(self, bricks: list[Brick]):
        self.bricks = self.__sorted_bricks(bricks)

    def __len__(self) -> int:
        return len(self.bricks)

    def __getitem__(self, item: int) -> Brick:
        return self.bricks[item]

    def __repr__(self) -> str:
        return f"{self.bricks}"

    @property
    def max_x(self) -> int:
        maximum = 0
        for brick in self.bricks:
            maximum = max(maximum, brick.end.x)
        return maximum

    @property
    def max_y(self) -> int:
        maximum = 0
        for brick in self.bricks:
            maximum = max(maximum, brick.end.y)
        return maximum

    @staticmethod
    def __sort_key(b: Brick) -> int:
        return b.start.z

    def __sorted_bricks(self, bricks: list[Brick]):
        return sorted(bricks, key=self.__sort_key)

    def bricks_supported_by(self) -> list[set[int]]:
        n = len(self)
        brick_to_brick_supports = [set() for _ in range(n)]
        height_to_bricks = defaultdict(list)
        max_x = self.max_x
        max_y = self.max_y
        frontier = BrickFrontier(max_x, max_y)
        frontier.add(self[0].frontier(), self[0].height_of_shape, 0)
        height_to_bricks[0].append(0)

        for i in range(1, n):
            brick = self[i]
            brick_frontier = brick.frontier()
            brick_to_brick_supports[i] = set(frontier.add(brick_frontier, brick.height_of_shape, i))
        return brick_to_brick_supports

    def number_of_removable_blocks(self) -> int:
        vital_bricks = self.vital_bricks(self.bricks_supported_by())
        return len(self) - len(vital_bricks)

    @staticmethod
    def vital_bricks(brick_supported_by: list[set[int]]) -> set[int]:
        vital_bricks = set()
        for brick_supports in brick_supported_by[1:]:
            if len(brick_supports) == 1:
                vital_bricks.add(list(brick_supports)[0])
        return vital_bricks

    @staticmethod
    def __brick_supports(bricks_supported_by: list[list[int]]) -> list[set[int]]:
        brick_supports = [set() for _ in range(len(bricks_supported_by))]
        for i, values in enumerate(bricks_supported_by):
            for value in values:
                brick_supports[value].add(i)
        return brick_supports

    def number_of_falls_from_vital_blocks(self) -> int:
        brick_supported_by = self.bricks_supported_by()
        brick_supports = self.__brick_supports(brick_supported_by)
        total = 0
        for i in range(len(self)):
            q = deque(j for j in brick_supports[i] if len(brick_supported_by[j]) == 1)
            falling = set(q)
            falling.add(i)
            while q:
                j = q.popleft()
                for k in brick_supports[j] - falling:
                    if brick_supported_by[k] <= falling:
                        q.append(k)
                        falling.add(k)

            total += len(falling) - 1
        return total


def tests():
    falling_bricks = FallingBricks([BrickFactory.from_line(line) for line in read_lines("day_22_1_test_input.txt")])
    brick_supports = falling_bricks.bricks_supported_by()
    assert list(brick_supports[0]) == []  # A
    assert list(brick_supports[1]) == [0]  # B
    assert list(brick_supports[2]) == [0]  # C
    assert list(brick_supports[3]) == [1, 2]  # D
    assert list(brick_supports[4]) == [1, 2]  # E
    assert list(brick_supports[5]) == [3, 4]  # F
    assert list(brick_supports[6]) == [5]  # G

    assert falling_bricks.number_of_removable_blocks() == 5


def main():
    tests()

    falling_bricks = FallingBricks([BrickFactory.from_line(line) for line in read_lines("day_22_1_input.txt")])
    t = falling_bricks.number_of_removable_blocks()
    print(t)
    assert t == 515


if __name__ == "__main__":
    main()
