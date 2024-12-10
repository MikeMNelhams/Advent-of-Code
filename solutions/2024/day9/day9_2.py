import time

from handy_dandy_library.file_processing import read_lines

from day9_1 import FileCompactor


def tests():
    file_compactor = FileCompactor(read_lines("puzzle9_1_test_input1.txt"))

    t1 = file_compactor.compacted_file_checksum2()
    print(f"total: {t1}")
    assert t1 == 2858


def main():
    tests()
    t0 = time.perf_counter()
    file_compactor = FileCompactor(read_lines("puzzle9_1.txt"))

    t2 = file_compactor.compacted_file_checksum2()
    print(t2)
    assert t2 == 6349492251099

    print(time.perf_counter() - t0)


if __name__ == "__main__":
    main()
