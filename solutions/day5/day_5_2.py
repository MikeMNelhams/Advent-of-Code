import sys
from bisect import insort, bisect_left, bisect_right
from handy_dandy_library.file_processing import read_lines
from day5_1 import FarmingDataReader, Map


PARTITION_DEFAULT = [0, sys.maxsize]


class IntervalPartitionsList:
    def __init__(self):
        self.interval_partitions = []

    def __len__(self):
        return len(self.interval_partitions)

    def add_mappings(self, mappings: list[Map]) -> None:
        self.interval_partitions.append(PARTITION_DEFAULT.copy())
        lowest = sys.maxsize
        highest = -1
        for mapping in mappings:
            print(f"adding mapping: {mapping}")
            low = mapping[0]
            high = mapping[1]
            highest = max(highest, high)
            if low == 0:
                lowest = min(lowest, high)
            if low != 0:
                lowest = min(lowest, low)
                insort(self.interval_partitions[-1], low)
            if high != low:
                insort(self.interval_partitions[-1], high)

        if lowest != 0:
            insort(self.interval_partitions[-1], lowest - 1)

        insort(self.interval_partitions[-1], highest + 1)
        print(self.interval_partitions[-1])
        return None

    def __repr__(self) -> str:
        return f"Mapping intervals: {self.interval_partitions}"


def location_low2_from_data_reader(farming_data_reader: FarmingDataReader) -> int:
    intervals = IntervalPartitionsList()
    seeds = farming_data_reader.parse_seed_numbers()
    maps = [farming_data_reader.parse_next_source_to_destination_map() for _ in range(7)]
    for mappings in reversed(maps):
        print(mappings)
        intervals.add_mappings(mappings)
        print('_' * 200)

    print('-'*200)
    print("FINAL")
    print(intervals)


def tests():
    farming_data_reader = FarmingDataReader("day_5_1_test_input.txt")
    location_low2_from_data_reader(farming_data_reader)


def main():
    tests()


if __name__ == "__main__":
    main()
