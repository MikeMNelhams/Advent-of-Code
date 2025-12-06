from day6_1 import CephalopodMathTable


def main():
    test_math_table = CephalopodMathTable("puzzle6_1_test_input.txt")
    assert test_math_table.cephalopod_reduced_operation_sum() == 3263827

    math_table = CephalopodMathTable("puzzle6_1.txt")
    print(math_table.cephalopod_reduced_operation_sum())


if __name__ == "__main__":
    main()
