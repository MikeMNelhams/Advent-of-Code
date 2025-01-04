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
        self.__set_initial_values(lines)
        self.required_z_count = self.__required_z_count(lines)
        self.parents_map = self.__parent_map(lines)

    def __set_initial_values(self, lines: list[str]) -> None:
        for line in lines:
            if line == '':
                break

            phrases = line.split(": ")
            self.values[phrases[0]] = int(phrases[1])
        return None

    @staticmethod
    def __required_z_count(lines: list[str]) -> int:
        i = 0
        for line in lines:
            if line == '':
                break
            i += 1

        count = 0
        for line in lines[i+1:]:
            _, z = line.split(" -> ")
            if z[0] == 'z':
                count += 1
        return count

    @staticmethod
    def __z_from_index(z_index: int) -> str:
        z_index_str = str(z_index)
        if len(z_index_str) == 1:
            z_index_str = '0' + z_index_str
        return f"z{z_index_str}"

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
            x_value = self.__process_operation(x2, y2, operation2)
        else:
            x_value = self.values[x]

        if y not in self.values:
            x3, y3, operation3 = self.parents_map[y]
            y_value = self.__process_operation(x3, y3, operation3)
        else:
            y_value = self.values[y]

        return self.OPERATOR_MAP[operation](x_value, y_value)

    @property
    def final_integer(self) -> int:
        z_index = 0
        while z_index < self.required_z_count:
            z = self.__z_from_index(z_index)
            x, y, operation = self.parents_map[z]
            z_processed = self.__process_operation(x, y, operation)
            self.values[z] = z_processed
            z_index += 1

        final_int = 0
        for i in range(z_index):
            z = self.__z_from_index(i)
            final_int += (1 << i) * self.values[z]
        return final_int


def tests():
    wire_untangler = WireUntangler(read_lines("puzzle24_1_test_input1.txt"))
    assert wire_untangler.final_integer == 4

    wire_untangler2 = WireUntangler(read_lines("puzzle24_1_test_input2.txt"))
    print(wire_untangler2.parents_map)
    assert wire_untangler2.final_integer == 2024


def main():
    tests()

    wire_untangler = WireUntangler(read_lines("puzzle24_1.txt"))
    t1 = wire_untangler.final_integer
    assert t1 == 55544677167336


if __name__ == "__main__":
    main()
