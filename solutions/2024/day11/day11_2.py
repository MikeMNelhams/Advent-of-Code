from handy_dandy_library.file_processing import read_lines

from day11_1 import EngravedStones


def tests():
    engraved_stones = EngravedStones(read_lines("puzzle11_1_test_input1.txt"))

    t1 = engraved_stones.count_after_blinks(25)
    assert t1 == 55312


def main():
    tests()
    engraved_stones = EngravedStones(read_lines("puzzle11_1.txt"))

    t2 = engraved_stones.count_after_blinks(75)
    assert t2 == 225404711855335


if __name__ == "__main__":
    main()
