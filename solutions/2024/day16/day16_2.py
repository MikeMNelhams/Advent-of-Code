from handy_dandy_library.file_processing import read_lines

from day16_1 import ReindeerMaze


def tests():
    maze = ReindeerMaze(read_lines("puzzle16_1_test_input1.txt"))

    _, t1 = maze.best_path_scores
    assert t1 == 45

    maze2 = ReindeerMaze(read_lines("puzzle16_1_test_input2.txt"))
    _, t2 = maze2.best_path_scores

    assert t2 == 64


def main():
    tests()

    maze = ReindeerMaze(read_lines("puzzle16_1.txt"))
    _, t1 = maze.best_path_scores
    assert t1 == 486


if __name__ == "__main__":
    main()
