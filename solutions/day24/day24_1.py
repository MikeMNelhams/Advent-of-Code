from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from itertools import combinations


class Vector:
    def __init__(self, values: tuple):
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: Vector) -> Vector:
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __neg__(self) -> Vector:
        return Vector((-self.x, -self.y, -self.z))

    def __sub__(self, other: Vector) -> Vector:
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other: float) -> Vector:
        return Vector((self.x * other, self.y * other, self.z * other))

    @property
    def magnitude2d(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    @property
    def unit_vector(self) -> Vector:
        return self * (1 / self.magnitude2d)

    def distance2d(self, other: Vector) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

    def element_mul(self, other: Vector) -> Vector:
        return Vector((self.x * other.x, self.y * other.y, self.z * other.z))


class Particle:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity

    def __repr__(self) -> str:
        return f"Pos{self.position} | Vel{self.velocity}"

    @classmethod
    def from_line(cls, line: str):
        phrase_halves = line.split(' @ ')
        position = Vector(tuple(float(x) for x in phrase_halves[0].split(", ")))
        velocity = Vector(tuple(float(x) for x in phrase_halves[1].split(", ")))
        return cls(position, velocity)


def crosses_in_boundary(p0: Particle, p1: Particle, boundary: tuple[float, float]) -> bool:
    # t > 0 and b[1] >= x + u * lambda >= b[0]
    # 3 options: Parallel, Intersects, Skew
    pass



def number_of_particles_that_intersect_in_boundary(particles: list[Particle],
                                                   boundary: tuple[float, float]) -> int:
    total = 0
    for pair in combinations(particles, 2):
        print(pair)
        total += int(crosses_in_boundary(pair[0], pair[1], boundary))
    print(total)
    return total


def read_particles(lines: list[str]) -> list[Particle]:
    return [Particle.from_line(line) for line in lines]


def tests():
    particles = read_particles(read_lines("day_24_1_test_input1.txt"))
    print(particles)
    assert crosses_in_boundary(particles[0], particles[1], (7, 27))
    assert crosses_in_boundary(particles[0], particles[2], (7, 27))
    assert number_of_particles_that_intersect_in_boundary(particles, (7, 27)) == 2


def main():
    tests()


if __name__ == "__main__":
    main()
