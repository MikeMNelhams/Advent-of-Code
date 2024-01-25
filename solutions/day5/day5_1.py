from __future__ import annotations
from handy_dandy_library.file_processing import read_lines

import sys

from functools import reduce
from itertools import chain


class Map:
    def __init__(self, map_ranges: tuple[int]):
        self.interval_mappings = self.__get_interval_mappings(map_ranges)
        self.vals = map_ranges

    def __getitem__(self, item: int):
        return self.interval_mappings[item]

    def __repr__(self) -> str:
        return f"Map{self.interval_mappings}"

    @staticmethod
    def __get_interval_mappings(map_ranges: list[int]) -> tuple[int]:
        start = map_ranges[1]
        end = start + map_ranges[2] - 1
        addition_coefficient = map_ranges[0] - start
        return start, end, addition_coefficient

    def overlaps(self, other: Map) -> bool:
        first_overlap_check = self.interval_mappings[1] > other.interval_mappings[0]
        return first_overlap_check or other.interval_mappings[1] > self.interval_mappings[0]

    def is_within_mapping(self, source: int) -> bool:
        return self.interval_mappings[0] <= source <= self.interval_mappings[1]

    def destination_assuming_valid(self, source: int) -> int:
        return source + self.interval_mappings[2]

    @property
    def inverted(self) -> Map:
        return Map((self.vals[1], self.vals[0], self.vals[2]))


class FarmingDataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.__lines = read_lines(file_path)
        self.__start_index = 0
        self.n = len(self.__lines)

    def lines(self, end_index: int) -> list[str]:
        start_index = self.start_index
        return self.__lines[start_index:start_index + end_index]

    @property
    def start_index(self) -> int:
        return self.__start_index

    def seed(self) -> list[int]:
        seeds_phrase = None

        for i, line in enumerate(self.__lines):
            if line == '':
                seeds_phrase = ''.join(self.lines(i))
                self.__start_index = i + 1
                break

        seed_numbers = [int(seed) for seed in seeds_phrase[6:].split(' ') if seed != '']
        return seed_numbers

    def parse_next_source_to_destination_map(self) -> list[Map]:
        map_numbers_phrase = None

        for i, line in enumerate(self.__lines[self.__start_index:]):
            if self.start_index + i == self.n - 1:
                self.__start_index += 1
                map_numbers_phrase = self.lines(i + 1)
                break

            if line == '':
                self.__start_index += 1
                map_numbers_phrase = self.lines(i - 1)
                self.__start_index += i
                break

        map_numbers = [Map(tuple(int(number) for number in line.split(' '))) for line in map_numbers_phrase]
        return map_numbers


class Farmer:
    def __init__(self, start_seeds: list[int], start_maps: list[list[Map]]):
        self.start_seeds = start_seeds
        self.start_maps = start_maps

    @classmethod
    def from_farming_data_reader(cls, farming_data_reader: FarmingDataReader):
        seeds = farming_data_reader.seed()
        maps = [farming_data_reader.parse_next_source_to_destination_map() for _ in range(7)]
        return cls(seeds, maps)

    @staticmethod
    def __destination(seeds: list[int], mappings: Map) -> list[int]:
        next_seeds = seeds.copy()
        for i, seed in enumerate(seeds):
            for mapping in mappings:
                if mapping.is_within_mapping(seed):
                    next_seeds[i] = mapping.destination_assuming_valid(seed)
                    break
        return next_seeds

    @property
    def lowest_location(self) -> int:
        final_seeds = reduce(self.__destination, self.start_maps, self.start_seeds)
        return min(final_seeds)

    @property
    def transformed_seeds(self) -> list[int]:
        new_seeds = self.start_seeds.copy()
        for i in range(0, len(self.start_seeds), 2):
            new_seeds[i + 1] = new_seeds[i] + new_seeds[i + 1] - 1
        new_seeds.sort()
        return new_seeds

    @property
    def lowest_possible_location(self) -> int:
        seed_ends = (s for s in self.__seed_endpoints if self.in_transformed_seed_range(s))
        return min(self.seed_to_location(s) for s in seed_ends)

    @property
    def __seed_endpoints(self) -> list[int]:
        return reduce(invert_maps, reversed(self.start_maps), (0, sys.maxsize))

    def seed_to_location(self, seed: int) -> int:
        return reduce(destination_from_maps, self.start_maps, seed)

    def in_transformed_seed_range(self, test_seed: int) -> bool:
        s = self.transformed_seeds
        return any(s[i] <= test_seed <= s[i + 1] for i in range(0, len(s), 2))


def invert_maps(output_ends: list[int], maps: list[Map]) -> list[int]:
    map_ends = (((_map.vals[0], _map.vals[1]), (_map.vals[0] + _map.vals[2] - 1, _map.vals[0] + _map.vals[2] - 1))
                for _map in maps)

    input_src_ends = list(set(x for y, x in chain.from_iterable(map_ends)))
    if input_src_ends[0] > 0:
        input_src_ends = [0, input_src_ends[0] - 1] + input_src_ends
    if input_src_ends[-1] < sys.maxsize:
        input_src_ends = input_src_ends + [input_src_ends[-1] + 1, sys.maxsize]

    inverted_maps = [_map.inverted for _map in maps]
    output_src_ends = (destination_from_maps(y, inverted_maps) for y in output_ends)

    return list(set(output_src_ends) | set(input_src_ends))


def destination_from_maps(x: int, maps: list[Map]) -> int:
    for _map in maps:
        if _map.is_within_mapping(x):
            return _map.destination_assuming_valid(x)
    return x


def tests():
    farming_data_reader = FarmingDataReader("day_5_1_test_input.txt")
    farmer = Farmer.from_farming_data_reader(farming_data_reader)
    t = farmer.lowest_location
    assert t == 35


def main():
    tests()

    farming_data_reader = FarmingDataReader("day_5_1_input.txt")
    farmer = Farmer.from_farming_data_reader(farming_data_reader)
    t = farmer.lowest_location
    print(t)
    assert t == 107430936


if __name__ == "__main__":
    main()
