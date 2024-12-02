from handy_dandy_library.file_processing import read_lines
from day13_1 import MirrorMapper, read_puzzles


def tests():
    assert MirrorMapper(read_lines("day_13_1_test_input1.txt")).mirror_summary(smudged=True) == 300
    assert MirrorMapper(read_lines("day_13_1_test_input2.txt")).mirror_summary(smudged=True) == 100


def main():
    tests()

    puzzles = read_puzzles(read_lines("day_13_1_input.txt"))
    totals = [MirrorMapper(puzzle).mirror_summary(smudged=True) for puzzle in puzzles]
    print(totals)
    t = sum(totals)
    print(t)


if __name__ == "__main__":
    main()
