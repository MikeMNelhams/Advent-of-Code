from handy_dandy_library.file_processing import read_lines

from day24_1 import WireUntangler


def tests():
    wire_untangler = WireUntangler(read_lines("puzzle24_2_test_input1.txt"))
    wire_untangler.swapped_pairs_checking(lambda x, y: x & y)
    pass


def main():
    tests()

    wire_untangler = WireUntangler(read_lines("puzzle24_1.txt"))

    wire_untangler.swapped_pairs_checking(lambda x, y: x + y)
    t1 = wire_untangler.swapped_pairs_in_addition()
    assert t1 == "gsd,kth,qnf,tbt,vpm,z12,z26,z32"


if __name__ == "__main__":
    main()
