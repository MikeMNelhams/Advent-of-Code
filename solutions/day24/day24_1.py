from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue
from handy_dandy_library.linear_algebra import Vector3D, sign

from itertools import combinations


class Particle:
    def __init__(self, position: Vector3D, velocity: Vector3D):
        self.position = position
        self.velocity = velocity

    def __repr__(self) -> str:
        return f"{make_blue('Pos')}{self.position} | Vel{self.velocity}"

    @classmethod
    def from_line(cls, line: str):
        phrase_halves = line.split(' @ ')
        position = Vector3D(tuple(map(float, phrase_halves[0].split(", "))))
        velocity = Vector3D(tuple(map(float, phrase_halves[1].split(", "))))
        return cls(position, velocity)


def crosses_in_boundaryXY(p0: Particle, p1: Particle, boundary: tuple[float, float]) -> bool:
    v0 = p0.velocity
    v1 = p1.velocity
    denominator = v0.xy_projected_cross_product(v1)
    k = p0.position - p1.position
    mu_a_numerator = v1.xy_projected_cross_product(k)

    # Parallel
    if denominator == 0:
        # Coincidental lines may still cross
        mu_b_numerator = v0.xy_projected_cross_product(k)
        if mu_a_numerator == 0 and mu_b_numerator == 0:
            raise NotImplementedError  # None of the examples are coincidental
        return False

    r_a_x, r_a_y = p0.position.x, p0.position.y
    r_b_x, r_b_y = p1.position.x, p1.position.y
    u_a_x, u_a_y = v0.x, v0.y
    u_b_x, u_b_y = v1.x, v1.y

    intersection = p0.position + v0 * (mu_a_numerator / denominator)
    a_in_past = sign(intersection.x - r_a_x) != sign(u_a_x)
    b_in_past = sign(intersection.x - r_b_x) != sign(u_b_x)

    if a_in_past or b_in_past:
        return False

    for value in (intersection.x, intersection.y):
        if value < boundary[0] or value > boundary[1]:
            return False
    return True


def number_of_particles_that_intersect_in_boundary(particles: list[Particle],
                                                   boundary: tuple[float, float]) -> int:
    return sum(crosses_in_boundaryXY(pair[0], pair[1], boundary) for pair in combinations(particles, 2))


def read_particles(lines: list[str]) -> list[Particle]:
    return tuple(Particle.from_line(line) for line in lines)


def tests():
    particles = read_particles(read_lines("day_24_1_test_input1.txt"))

    assert crosses_in_boundaryXY(particles[0], particles[1], (7, 27))
    assert crosses_in_boundaryXY(particles[0], particles[2], (7, 27))
    assert number_of_particles_that_intersect_in_boundary(particles, (7, 27)) == 2


def main():
    tests()

    particles = read_particles(read_lines("day_24_1_input.txt"))

    t = number_of_particles_that_intersect_in_boundary(particles, (200000000000000, 400000000000000))
    print(t)


if __name__ == "__main__":
    main()
