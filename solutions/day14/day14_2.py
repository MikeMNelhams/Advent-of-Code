from handy_dandy_library.file_processing import read_lines
from day14_1 import RockNRoller


def tests():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))



def main():
    tests()


if __name__ == "__main__":
    main()
