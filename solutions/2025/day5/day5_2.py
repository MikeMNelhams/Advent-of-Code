from handy_dandy_library.file_processing import read_lines
from day5_1 import Kitchen


def main():
    test_kitchen = Kitchen(read_lines("puzzle5_1_test_input.txt"))
    assert test_kitchen.possible_fresh_ingredient_count() == 14

    kitchen = Kitchen(read_lines("puzzle5_1.txt"))
    t = kitchen.possible_fresh_ingredient_count()
    print(t)
    # 341753674214273


if __name__ == "__main__":
    main()
