from handy_dandy_library.file_processing import read_lines

from day13_1 import Arcade


def tests():
    pass
    # No test cases given/useful possible ones exist o_o


def main():
    tests()

    arcade = Arcade(read_lines("puzzle13_1.txt"))
    t1 = arcade.minimum_total_tokens_to_giga_win_rigged()
    print(t1)


if __name__ == "__main__":
    main()
