from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector3D

from day24_1 import Particle, read_particles


def plane(particle0: Particle, particle1: Particle):
    displacement = particle0.position - particle1.position
    velocity_difference = particle0.velocity - particle1.velocity
    velocity_plane_normal = particle0.velocity.cross(particle1.velocity)
    return displacement.cross(velocity_difference), displacement.dot(velocity_plane_normal)


def line(r, a, s, b, t, c):
    x = r * a.x + s * b.x + t * c.x
    y = r * a.y + s * b.y + t * c.y
    z = r * a.z + s * b.z + t * c.z
    return Vector3D((x, y, z))


def find_rock_start(particle1: Particle, particle2: Particle, particle3: Particle) -> Vector3D:
    # Rock travels in line described by intersection between planes described by intersecting hailstone velocities
    # If you were to solve the system linearly, it would be 9 unknowns, 9 equations (9x9 matrix inversion)
    # With only 2 hailstone, you get 7 unknowns, 3 equations, so you need 3 linearly independent hailstones
    # Instead we can directly compute w/ geometry, since we know the specific case solution.

    a, A = plane(particle1, particle2)
    b, B = plane(particle1, particle3)
    c, C = plane(particle2, particle3)

    w = line(A, b.cross(c), B, c.cross(a), C, a.cross(b))
    t = a.dot(b.cross(c))
    w *= 1 / t

    w1 = particle1.velocity - w
    w2 = particle2.velocity - w
    ww = w1.cross(w2)

    E = ww.dot(particle2.position.cross(w2))
    F = ww.dot(particle1.position.cross(w1))
    G = particle1.position.dot(ww)

    rock = line(E, w1, -F, w2, G, ww)
    rock *= 1 / ww.dot(ww)
    return rock


def solve(particles: list[Particle]):
    n = len(particles)

    particle1 = particles[0]
    particle2 = None
    particle3 = None

    i = 0
    for i in range(1, n):
        if particle1.velocity.linearly_independent(particles[i].velocity):
            particle2 = particles[i]
            break

    for j in range(i + 1, n):
        linearly_independent_check1 = particle1.velocity.linearly_independent(particles[j].velocity)
        linearly_independent_check2 = particle2.velocity.linearly_independent(particles[j].velocity)
        if linearly_independent_check1 and linearly_independent_check2:
            particle3 = particles[j]
            break

    if particle2 is None or particle3 is None:
        raise TypeError

    rock = find_rock_start(particle1, particle2, particle3)
    return rock.manhattan_distance_from_zero


def tests():
    particles = read_particles(read_lines("day_24_1_test_input1.txt"))
    t = solve(particles)
    assert t == 47


def main():
    tests()

    particles = read_particles(read_lines("day_24_1_input.txt"))
    t = solve(particles)
    print(t)


if __name__ == "__main__":
    main()
