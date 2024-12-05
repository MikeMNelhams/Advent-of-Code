from handy_dandy_library.file_processing import read_lines

from day5_1 import PageSorter, split_data


def tests():
    rules, updates = split_data(read_lines("puzzle5_1_test_input1.txt"))

    page_sorter = PageSorter(rules)
    assert page_sorter.sum_middle_numbers_incorrectly_ordered_but_now_correct(updates) == 123


def main():
    tests()

    rules, updates = split_data(read_lines("puzzle5_1.txt"))

    page_sorter = PageSorter(rules)
    t2 = page_sorter.sum_middle_numbers_incorrectly_ordered_but_now_correct(updates)
    assert t2 == 6319


if __name__ == "__main__":
    main()
