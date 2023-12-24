from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules


MIRROR_ENCODING = {'.': 0, '|': 1, '-': 2, '\\': 3, '/': 4}
MIRROR_REVERSE_ENCODING = {0: '.', 1: '|', 2: '-', 3: '\\', 4: '/'}

type Grid = list[list[int]]


class UnitVector:
    UNIT_VECTOR_CODENAMES = {"up": 0, "right": 1, "down": 2, "left": 3}
    UNIT_VECTOR_NAMES_FROM_VECTOR = {(1, 0): "right", (0, 1): "down", (-1, 0): "left", (0, -1): "up"}

    def __init__(self, values: tuple[int, int]):
        self.x = values[0]
        self.y = values[1]
        self.direction_name = self.UNIT_VECTOR_NAMES_FROM_VECTOR.get(values, "not_unit_vector")

    def __eq__(self, other: UnitVector) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    @classmethod
    def UP(cls):
        return cls((0, -1))

    @classmethod
    def RIGHT(cls):
        return cls((1, 0))

    @classmethod
    def DOWN(cls):
        return cls((0, 1))

    @classmethod
    def LEFT(cls):
        return cls((-1, 0))


class Vector(UnitVector):
    def __init__(self, values: tuple[int, int]):
        super().__init__(values)

    def __add__(self, other: Vector) -> Vector:
        return Vector((self.x + other.x, self.y + other.y))

    @property
    def rotated_right(self) -> Vector:
        return Vector((self.y * -abs(self.y), self.x))

    @property
    def rotated_left(self) -> Vector:
        return Vector((self.y, self.x * -abs(self.x)))


class Light:
    def __init__(self, coordinate: Vector, direction: Vector):
        self.coordinate = coordinate
        self.direction = direction

    def __copy__(self) -> Light:
        return Light(self.coordinate, self.direction)

    def __repr__(self) -> str:
        return f"L({self.coordinate}, {self.direction.direction_name})"

    def copy(self) -> Light:
        return self.__copy__()

    @property
    def x(self) -> int:
        return self.coordinate.x

    @property
    def y(self) -> int:
        return self.coordinate.y

    @property
    def rotated_right(self) -> Light:
        return Light(self.coordinate, self.direction.rotated_right)

    @property
    def rotated_left(self) -> Light:
        return Light(self.coordinate, self.direction.rotated_left)

    @property
    def moved_forwards1(self) -> Light:
        return Light(self.coordinate + self.direction, self.direction)

    def new_lights_according_to_mirror_code(self, mirror_code: int) -> list[Light]:
        # TODO Swap this logic to a while + dict approach.
        if mirror_code == 0:
            return [self.copy()]
        if mirror_code == 1:
            if self.direction.direction_name in ("left", "right"):
                return [Light(self.coordinate, Vector.UP()),
                        Light(self.coordinate, Vector.DOWN())]
            if self.direction.direction_name in ("up", "down"):
                return [self.copy()]
        if mirror_code == 2:
            if self.direction.direction_name in ("up", "down"):
                return [Light(self.coordinate, Vector.LEFT()),
                        Light(self.coordinate, Vector.RIGHT())]
            if self.direction.direction_name in ("left", "right"):
                return [self.copy()]
        if mirror_code == 3:
            if self.direction.direction_name in ("left", "right"):
                return [self.rotated_right]
            if self.direction.direction_name in ("up", "down"):
                return [self.rotated_left]
        if mirror_code == 4:
            if self.direction.direction_name in ("left", "right"):
                return [self.rotated_left]
            if self.direction.direction_name in ("up", "down"):
                return [self.rotated_right]
        raise TypeError


class EnergyGrid:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.grid = [[[0, 0, 0, 0] for _ in range(self.m)] for _ in range(self.n)]

    def __repr__(self) -> str:
        return '\n'.join([''.join(['#' if any(direction == 1 for direction in directions)
                                   else '.' for directions in line])
                          for line in self.grid])

    @property
    def total_energy(self) -> int:
        return sum(int(any(directions)) for line in self.grid for directions in line)


class MirrorGrid:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])

    def __repr__(self) -> str:
        lines = ['\t' + str(line) for line in self.grid]
        return pad_with_horizontal_rules('\n'.join(lines))

    def print_mirrors(self) -> None:
        lines = [''.join(['\t' + str(MIRROR_REVERSE_ENCODING[char]) for char in line])
                 for line in self.grid]
        print(pad_with_horizontal_rules('\n'.join(lines)))
        return None

    @classmethod
    def from_lines(cls, lines: list[str]):
        mirror_grid_encoding = [[MIRROR_ENCODING[char] for char in line] for line in lines]
        return cls(mirror_grid_encoding)

    def light_outside_grid(self, light: Light) -> bool:
        x_coord_is_invalid = light.x < 0 or light.x > self.n - 1
        y_coord_is_invalid = light.y < 0 or light.y > self.m - 1
        invalid_coord = x_coord_is_invalid or y_coord_is_invalid
        return invalid_coord

    def energized_grid(self, start_light: Light = Light(Vector((-1, 0)), Vector.RIGHT())) -> EnergyGrid:
        energy_grid = EnergyGrid(self.n, self.m)
        lights_to_simulate = [start_light]
        while lights_to_simulate:
            light = lights_to_simulate.pop()
            light = light.moved_forwards1
            direction_code = Vector.UNIT_VECTOR_CODENAMES[light.direction.direction_name]
            if not self.light_outside_grid(light) and not energy_grid.grid[light.y][light.x][direction_code]:
                energy_grid.grid[light.y][light.x][direction_code] = 1
                mirror_code = self.grid[light.y][light.x]
                lights = light.new_lights_according_to_mirror_code(mirror_code)
                for new_light in lights:
                    lights_to_simulate.append(new_light)
        return energy_grid

    def max_energy(self) -> EnergyGrid:
        max_energy = 0
        iter_thruples = ((self.__start_top_light, self.m, Vector.DOWN()),
                         (self.__start_right_light, self.n, Vector.RIGHT()),
                         (self.__start_left_light, self.n, Vector.LEFT()),
                         (self.__start_up_light, self.m, Vector.UP()))

        for thruple in iter_thruples:
            for i in range(thruple[1]):
                energy_grid = self.energized_grid(thruple[0](i, thruple[2]))
                max_energy = max(max_energy, energy_grid.total_energy)
        return max_energy

    @staticmethod
    def __start_top_light(i, start_direction) -> Light:
        return Light(Vector((i, -1)), start_direction)

    @staticmethod
    def __start_right_light(i, start_direction) -> Light:
        return Light(Vector((-1, i)), start_direction)

    def __start_left_light(self, i, start_direction) -> Light:
        return Light(Vector((self.m, i)), start_direction)

    def __start_up_light(self, i, start_direction) -> Light:
        return Light(Vector((i, self.n)), start_direction)


def tests():
    mirror_grid = MirrorGrid.from_lines(read_lines("day_16_1_test_input1.txt"))
    mirror_grid.print_mirrors()
    energized_grid = mirror_grid.energized_grid()
    assert energized_grid.total_energy == 46


def main():
    tests()

    mirror_grid = MirrorGrid.from_lines(read_lines("day_16_1_input.txt"))
    energized_grid = mirror_grid.energized_grid()

    t = energized_grid.total_energy
    print(t)


if __name__ == "__main__":
    main()
