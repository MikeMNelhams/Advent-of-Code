from handy_dandy_library.file_processing import read_lines
from day14_1 import RockNRoller


def test1():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))

    for _ in range(4):
        rock_roller.rotate_clockwise_90_degrees()

    start_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))
    assert start_roller == rock_roller
    assert start_roller.encoded_grid == rock_roller.encoded_grid


def test2():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))

    rock_roller.spin_cycle_one_iter()
    rock_roller_correctly_spun = RockNRoller.from_lines(read_lines("day_14_2_test_input1.txt"))
    assert rock_roller == rock_roller_correctly_spun


def test3():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))
    iters = 1_000_000_000
    roller = rock_roller.spin_cycle(iters)

    assert roller.total_load == 64


def tests():
    test1()
    test2()
    test3()


def main():
    tests()

    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_input.txt"))
    iters = 1_000_000_000

    roller = rock_roller.spin_cycle(iters)

    t = roller.total_load
    print(t)


if __name__ == "__main__":
    main()
