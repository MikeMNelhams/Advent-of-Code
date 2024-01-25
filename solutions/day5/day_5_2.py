from day5_1 import FarmingDataReader, Farmer


def tests():
    farming_data_reader = FarmingDataReader("day_5_1_test_input.txt")
    farmer = Farmer.from_farming_data_reader(farming_data_reader)

    t = farmer.lowest_possible_location
    assert t == 46


def main():
    tests()

    farming_data_reader = FarmingDataReader("day_5_1_input.txt")
    farmer = Farmer.from_farming_data_reader(farming_data_reader)

    t = farmer.lowest_possible_location
    assert t == 23738616


if __name__ == "__main__":
    main()
