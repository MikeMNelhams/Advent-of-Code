from day11_1 import Grid


def main():
    test_grid = Grid("day11_2_test_input.txt")
    assert test_grid.unique_path_count("svr", "out") == 8
    assert test_grid.unique_path_count("fft", "dac") == 1
    assert test_grid.unique_path_count("dac", "fft") == 0
    assert test_grid.path_svr_fft_or_dac_out_count() == 2

    grid = Grid("day11_1.txt")
    t = grid.path_svr_fft_or_dac_out_count()
    assert t == 362956369749210


if __name__ == "__main__":
    main()
