from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue

from typing import Iterable


class Vector3D:
    def __init__(self, values: tuple[int, int, int]):
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

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


class Brick:
    def __init__(self, start: Vector3D, end: Vector3D):
        self.start = start
        self.end = end
        shape = end - start
        self.shape_dimension = shape.first_non_zero_dim_index
        self.shape_length = shape.manhattan_distance_from_zero + 1
        self.__unit_vector = Vector3D(tuple(1 if i == self.shape_dimension else 0 for i in range(3)))
        shape.z = 0
        self.xy_projection = shape

    def __repr__(self) -> str:
        return f"{make_blue('B')}[{self.start} -> {self.end} @ {self.start.z}]"
    
    @staticmethod
    def __on_segment(p, q, r) -> bool:
        if max(p.x, r.x) >= q.x >= min(p.x, r.x) and max(p.y, r.y) >= q.y >= min(p.y, r.y):
            return True
        return False

    def intersections(self, other: Brick) -> list[int]:
        # # Returns the xy projection intersection
        # if self.shape_dimension == 2:
        #     # Both dots
        #     if other.shape_dimension == 2:
        #         if self.xy_projection == other.xy_projection:
        #             return [0]
        #     # ONLY Self dot
        #     else:
        #         valid_x = other.start.x <= self.xy_projection.x <= other.end.x
        #         valid_y = other.start.y <= self.xy_projection.y <= other.end.y
        #         if valid_x and valid_y:
        #             return [0]
        # # Other dot
        # elif other.shape_dimension == 2:
        #     valid_x = self.start.x <= other.xy_projection.x <= self.end.x
        #     valid_y = self.start.y <= other.xy_projection.y <= self.end.y
        #     if valid_x and valid_y:
        #         return [0]
        # # Parallel and neither are dots
        # elif self.shape_dimension == other.shape_dimension:
        #     if self.start.x <= other.start.x <= self.end.x:
        #         return list(range(self.shape_length - (self.end.x - other.start.x),self.shape_length))
        #     if self.start.y <= other.start.y <= self.end.x:
        #         return list(range(self.shape_length - (self.end.y - other.start.y),self.shape_length))
        #     if other.start.x <= self.start.x <= other.end.x:
        #         return list(range(other.end.x - self.start.x))
        #     if other.start.y <= self.start.y <= other.end.y:
        #         return list(range(other.end.y - self.start.y))
        # # Regular intersection between a horizontal and a vertical
        # else:
        #     self_is_horizontal = self.shape_dimension == 0
        #     if self_is_horizontal:
        #         if self.start.x <= other.xy_projection.x <= self.end.x:
        #             return
        #     else:
        # return []

#     |
#     |
# ----#----
#     |

    @property
    def all_coordinates(self) -> Iterable[Vector3D]:
        return (self.start + self.__unit_vector * i for i in range(self.shape_length))

    @classmethod
    def from_line(cls, line: str):
        phrase_halves = line.split('~')
        start = Vector3D(tuple(int(x) for x in phrase_halves[0].split(',')))
        end = Vector3D(tuple(int(x) for x in phrase_halves[1].split(',')))
        return cls(start, end)


class FallingBricks:
    """What's that in the sky? OMG RUN"""
    def __init__(self, bricks: list[Brick]):
        self.bricks = self.__sorted_bricks(bricks)

    def __getitem__(self, item: int) -> Brick:
        return self.bricks[item]

    def __repr__(self) -> str:
        return f"{self.bricks}"

    def bricks_supporting(self, brick_index: int) -> list[int]:
        if brick_index == 0:
            return []

        comparison_brick = self[brick_index]

        max_coordinates_left_to_check = comparison_brick.shape_length
        occlusions = [0 for _ in range(max_coordinates_left_to_check)]
        supporting_indices = []

        for i in range(brick_index-1, -1, -1):
            print(f"Checking brick: {brick_index} supported by {i}")
            if max_coordinates_left_to_check == 0:
                return supporting_indices
            intersections = comparison_brick.insersections(self[i])
            unoccluded_intersections = [x for x in intersections if not occlusions[x]]
            if any(unoccluded_intersections):
                for intersection in unoccluded_intersections:
                    occlusions[intersection] = 1
                supporting_indices.append(i)
                max_coordinates_left_to_check -= 1
        print(f"Supporting brick {brick_index} are: {supporting_indices}")
        print('-' * 50)
        supporting_indices.reverse()
        return supporting_indices

    @staticmethod
    def __sort_key(b: Brick) -> int:
        return b.start.z

    def __sorted_bricks(self, bricks: list[Brick]):
        return sorted(bricks, key=self.__sort_key)


def tests():
    falling_bricks = FallingBricks([Brick.from_line(line) for line in read_lines("day_22_1_test_input.txt")])
    print(falling_bricks)
    assert falling_bricks.bricks_supporting(0) == []  # A
    assert falling_bricks.bricks_supporting(1) == [0]  # B
    assert falling_bricks.bricks_supporting(2) == [0]  # C
    assert falling_bricks.bricks_supporting(3) == [1, 2]  # D
    assert falling_bricks.bricks_supporting(4) == [1, 2]  # E
    assert falling_bricks.bricks_supporting(5) == [3, 4]  # F
    assert falling_bricks.bricks_supporting(6) == [5]  # G


def main():
    tests()


if __name__ == "__main__":
    main()
