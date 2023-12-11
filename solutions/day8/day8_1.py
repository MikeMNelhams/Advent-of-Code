from handy_dandy_library.file_processing import read_lines


class RouteManager:
    def __init__(self):
        self.mappings: dict[str, str] = {}

    def __repr__(self) -> str:
        return self.mappings.__repr__()

    def add_node(self, name: str, left: str, right: str) -> None:
        self.mappings[name] = [left, right]
        return None

    def add_nodes(self, nodes: list[tuple[str]]) -> None:
        for node in nodes:
            self.mappings[node[0]] = [node[1], node[2]]
        return None

    def zig_zag(self, lr_code: str) -> int:
        current_node_name = "AAA"
        iter_count = 0
        i = 0
        n = len(lr_code)
        while current_node_name != "ZZZ":
            print(f"i: {i} | {current_node_name} {self.mappings[current_node_name]}")
            current_lr_code = int(lr_code[i])
            current_node_name = self.mappings[current_node_name][current_lr_code]

            if i == n - 1:
                i = 0
                iter_count += 1
            else:
                i += 1

        return iter_count * n


def read_lr(lines: list[str]) -> str:
    return "".join(['0' if char == "L" else '1' for char in "".join(lines[0])])


def read_node(line: str) -> (str, str, str):
    node_name = line[:3]
    node_left_name = line[7:10]
    node_right_name = line[12:15]
    return node_name, node_left_name, node_right_name


def read_nodes(lines: list[str]) -> list[tuple[str]]:
    return [read_node(line) for line in lines[2:]]


def zig_zag(lines: list[str]) -> int:
    lr_code = read_lr(lines)
    route_manager = RouteManager()
    nodes = read_nodes(lines)

    route_manager.add_nodes(nodes)
    return route_manager.zig_zag(lr_code)


def tests():
    assert zig_zag(read_lines("day_8_1_test_input1.txt")) == 2
    print('-' * 50)
    assert zig_zag(read_lines("day_8_1_test_input2.txt")) == 6
    pass


def main():
    tests()

    t = zig_zag(read_lines("day_8_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
