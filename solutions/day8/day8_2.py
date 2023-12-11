from handy_dandy_library.file_processing import read_lines
from day8_1 import RouteManager, read_nodes, read_lr
import math


class RouteManager2(RouteManager):
    def start_nodes(self) -> list[str]:
        return [node for node in self.mappings if node[-1] == 'A']

    @staticmethod
    def are_all_end_nodes(nodes: list[str]) -> bool:
        return all(node[-1] == 'Z' for node in nodes)

    def zig_zag(self, lr_code: str) -> int:
        current_node_names = self.start_nodes()
        iter_count = 0
        i = 0
        n = len(lr_code)
        print(current_node_names)

        looping_constants = [0 for _ in current_node_names]

        for j, current_node_name in enumerate(current_node_names):
            while current_node_name[-1] != 'Z':
                print(f"i: {i} | {current_node_name} {self.mappings[current_node_name]}")
                # print(f"i: {i} | {current_node_name} {self.mappings[current_node_name]}")
                current_lr_code = int(lr_code[i])
                current_node_name = self.mappings[current_node_name][current_lr_code]

                if i == n - 1:
                    i = 0
                else:
                    i += 1
                iter_count += 1
            looping_constants[j] = iter_count
            i = 0
            iter_count = 0
        print(looping_constants)
        return math.lcm(*looping_constants)


def zig_zag(lines: list[str]) -> int:
    lr_code = read_lr(lines)
    route_manager = RouteManager2()
    nodes = read_nodes(lines)

    route_manager.add_nodes(nodes)
    return route_manager.zig_zag(lr_code)


def tests():
    assert zig_zag(read_lines("day_8_2_test_input.txt")) == 6


def main():
    tests()

    t = zig_zag(read_lines("day_8_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
