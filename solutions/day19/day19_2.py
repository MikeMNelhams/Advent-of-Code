from handy_dandy_library.file_processing import read_lines
from day19_1 import Policy


def tests():
    lines = read_lines("day_19_1_test_input1.txt")
    policy = Policy.from_lines(lines)
    t = policy.number_of_distinct_accepted_combinations()
    assert t == 167409079868000


def main():
    tests()

    lines = read_lines("day_19_1_input.txt")
    policy = Policy.from_lines(lines)
    t = policy.number_of_distinct_accepted_combinations()
    print(t)
    assert t == 131899818301477


if __name__ == "__main__":
    main()
