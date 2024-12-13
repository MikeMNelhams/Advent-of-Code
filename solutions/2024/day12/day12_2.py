from handy_dandy_library.file_processing import read_lines

from day12_1 import RegionMetrics


def tests():
    region_metrics = RegionMetrics(read_lines("puzzle12_1_test_input1.txt"))
    t1 = region_metrics.total_discounted_fence_price()
    assert t1 == 80

    region_metrics2 = RegionMetrics(read_lines("puzzle12_2_test_input1.txt"))
    t2 = region_metrics2.total_discounted_fence_price()
    assert t2 == 236

    region_metrics3 = RegionMetrics(read_lines("puzzle12_2_test_input2.txt"))
    t3 = region_metrics3.total_discounted_fence_price()
    assert t3 == 368

    region_metrics4 = RegionMetrics(read_lines("puzzle12_1_test_input3.txt"))
    t4 = region_metrics4.total_discounted_fence_price()
    assert t4 == 1206


def main():
    tests()
    region_metrics = RegionMetrics(read_lines("puzzle12_1.txt"))
    t1 = region_metrics.total_discounted_fence_price()
    print(t1)


if __name__ == "__main__":
    main()
