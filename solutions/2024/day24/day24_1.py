from typing import Callable

from handy_dandy_library.file_processing import read_lines


ParentMap = dict[str, tuple[str, str, str]]


class WireUntangler:

    OPERATOR_MAP = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "XOR": lambda x, y: x ^ y
    }

    def __init__(self, lines: list[str]):
        self.values = {}
        self.lines = lines

        self.__set_initial_values(lines)
        self.required_x_count, self.required_y_count, self.required_z_count = self.__required_xyz_count(lines)
        self.parents_map = self.__parent_map(lines)

    def __set_initial_values(self, lines: list[str]) -> None:
        for line in lines:
            if line == '':
                break

            phrases = line.split(": ")
            self.values[phrases[0]] = int(phrases[1])
        return None

    @staticmethod
    def __required_xyz_count(lines: list[str]) -> (int, int, int):
        i = 0

        for line in lines:
            if line[0] == 'y':
                break
            i += 1

        x_count = i
        y_count = 1

        for line in lines[i+1:]:
            if line == '':
                break
            y_count += 1
            i += 1

        z_count = 0
        for line in lines[i+2:]:
            _, z = line.split(" -> ")
            if z[0] == 'z':
                z_count += 1
        return x_count, y_count, z_count

    @staticmethod
    def __padded_key_from_index(index: int, key: str) -> str:
        index_str = str(index)
        if len(index_str) == 1:
            index_str = '0' + index_str
        return f"{key}{index_str}"

    @staticmethod
    def __parent_map(lines: list[str]) -> ParentMap:
        i = 0
        for line in lines:
            if line == '':
                break
            i += 1

        inverse_parent_map = {}
        for line in lines[i+1:]:
            xy, z = line.split(" -> ")
            x, operation, y = xy.split(" ")
            inverse_parent_map[z] = (x, y, operation)

        return inverse_parent_map

    def __process_operation(self, x: str, y: str, operation: str) -> int:
        if x not in self.values:
            x2, y2, operation2 = self.parents_map[x]
            if x2[0] == 'z' or y2[0] == 'z':
                print((x2, y2, operation2), x)
                raise ZeroDivisionError
            x_value = self.__process_operation(x2, y2, operation2)
        else:
            x_value = self.values[x]

        if y not in self.values:
            x3, y3, operation3 = self.parents_map[y]
            if x3[0] == 'z' or y3[0] == 'z':
                print((x3, y3, operation3), y)
                raise ZeroDivisionError
            y_value = self.__process_operation(x3, y3, operation3)
        else:
            y_value = self.values[y]

        return self.OPERATOR_MAP[operation](x_value, y_value)

    def reset(self) -> None:
        self.values = {}
        for i in range(self.required_x_count):
            self.values[self.__padded_key_from_index(i, 'x')] = 0

        for i in range(self.required_x_count):
            self.values[self.__padded_key_from_index(i, 'y')] = 0

        return None

    @property
    def final_integer(self) -> int:
        z_index = 0
        while z_index < self.required_z_count:
            z = self.__padded_key_from_index(z_index, 'z')
            x, y, operation = self.parents_map[z]
            z_processed = self.__process_operation(x, y, operation)
            self.values[z] = z_processed
            z_index += 1

        final_int = 0
        for i in range(z_index):
            z = self.__padded_key_from_index(i, 'z')
            final_int += (1 << i) * self.values[z]
        return final_int

    def swapped_pairs_checking(self, expected_value_operation: Callable[[int, int], int]) -> None:
        # Relies on the fact that the bit graphs are disjoint
        for i in range(self.required_x_count):
            self.reset()
            self.values[self.__padded_key_from_index(i, 'x')] = 1
            self.values[self.__padded_key_from_index(i, 'y')] = 1

            x = 0
            for j in range(self.required_x_count):
                x += (1 << j) * self.values[self.__padded_key_from_index(j, 'x')]
            y = 0
            for j in range(self.required_y_count):
                y += (1 << j) * self.values[self.__padded_key_from_index(j, 'y')]

            expected_value = expected_value_operation(x, y)

            final_integer = self.final_integer
            difference = bin(final_integer ^ expected_value)[2:]
            print(f"Changing index: {self.__padded_key_from_index(i, '')} to 1. Difference: {difference}")

        return None

    def swapped_pairs_in_addition(self) -> str:
        swapped_bits = set()

        for w, (x, y, operation) in self.parents_map.items():
            if w[0] == 'z' and operation != "XOR" and w != f"z{self.required_z_count - 1}":
                swapped_bits.add(w)
            if operation == "XOR" and w[0] not in "xyz" and x[0] not in "xyz" and y[0] not in "xyz":
                swapped_bits.add(w)
            if operation == "AND" and x != "x00" and y != "x00":
                for _, (x2, y2, operation2) in self.parents_map.items():
                    if (w == x2 or w == y2) and operation2 != "OR":
                        swapped_bits.add(w)
            elif operation == "XOR":
                for _, (x2, y2, operation2) in self.parents_map.items():
                    if (w == x2 or w == y2) and operation2 == "OR":
                        swapped_bits.add(w)

        return ",".join(sorted(x for x in swapped_bits))


def tests():
    wire_untangler = WireUntangler(read_lines("puzzle24_1_test_input1.txt"))
    assert wire_untangler.final_integer == 4

    wire_untangler2 = WireUntangler(read_lines("puzzle24_1_test_input2.txt"))
    assert wire_untangler2.final_integer == 2024


def main():
    tests()

    wire_untangler = WireUntangler(read_lines("puzzle24_1.txt"))
    t1 = wire_untangler.final_integer
    assert t1 == 55544677167336


if __name__ == "__main__":
    main()
