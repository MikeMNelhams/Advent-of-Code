from day15_1 import Hasher, read_single_line_csv

type DataEntry = tuple[str, str, int] | tuple[str, str]


class HashMap:
    OPERATION_CHARS = ('=', '-')

    def __init__(self):
        self.data = [{} for _ in range(256)]

    def process(self, entry: DataEntry) -> None:
        if entry[1] not in self.OPERATION_CHARS:
            raise TypeError
        hash_key = Hasher(entry[0]).encoded
        if entry[1] == '-':
            self.data[hash_key].pop(entry[0], None)
            return None
        self.data[hash_key][entry[0]] = entry[2]
        return None

    @property
    def total_focusing_power(self):
        total_power = 0
        for lenses in self.data:
            for i, (key_unhashed, focal_length) in enumerate(lenses.items()):
                total_power += (Hasher(key_unhashed).encoded + 1) * (i+1) * focal_length
        return total_power


def read_data_from_csv_phrase(phrase: str) -> DataEntry:
    final_char = phrase[-1]
    if final_char == '-':
        return phrase[:-1], final_char
    return phrase[:-2], phrase[-2], int(final_char)


def tests():
    hashmap = HashMap()
    data_entries = list(read_data_from_csv_phrase(phrase)
                        for phrase in read_single_line_csv("day_15_1_test_input1.txt"))

    for entry in data_entries:
        hashmap.process(entry)

    assert hashmap.total_focusing_power == 145


def main():
    tests()

    hashmap = HashMap()

    data_entries = list(read_data_from_csv_phrase(phrase) for phrase in read_single_line_csv("day_15_1_input.txt"))

    for entry in data_entries:
        hashmap.process(entry)

    t = hashmap.total_focusing_power
    print(t)


if __name__ == "__main__":
    main()
