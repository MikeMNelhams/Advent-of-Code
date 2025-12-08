from day7_1 import TachyonGrid


def main():
    test_tachyon_grid = TachyonGrid("puzzle7_1_test_input.txt")
    assert test_tachyon_grid.simulate_paths_count() == 40

    tachyon_grid = TachyonGrid("puzzle7_2.txt")
    print(tachyon_grid.simulate_paths_count())


if __name__ == "__main__":
    main()
