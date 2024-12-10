import time

from handy_dandy_library.file_processing import read_lines

from day10_1 import TopographicMap


def test():
    topographic_map = TopographicMap(read_lines("puzzle10_1_test_input1.txt"))

    t1 = topographic_map.trailhead_ratings()
    assert t1 == 81


def main():
    test()
    t0 = time.perf_counter()
    topographic_map = TopographicMap(read_lines("puzzle10_1.txt"))

    t2 = topographic_map.trailhead_ratings()
    assert t2 == 1694
    print(t2)
    print(f"time: {time.perf_counter() - t0}")


if __name__ == "__main__":
    main()
