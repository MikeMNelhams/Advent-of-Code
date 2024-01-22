from __future__ import annotations

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import horizontal_rule


type Grid = list[list[int, int]]


def empty_grid(number_of_rows: int, number_of_columns: int) -> Grid:
    return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]


class RockNRoller:
    HARD_ROCK_CHAR = '#'
    SMOOTH_ROCK_CHAR = 'O'
    EMPTY_CHAR = '.'
    ROCK_ENCODINGS = {EMPTY_CHAR: 0, HARD_ROCK_CHAR: 1, SMOOTH_ROCK_CHAR: 2}
    ROCK_ENCODINGS_REVERSED = {0: EMPTY_CHAR, 1: HARD_ROCK_CHAR, 2: SMOOTH_ROCK_CHAR}

    def __init__(self, encoded_grid: Grid):
        self.encoded_grid = encoded_grid
        self.n = len(encoded_grid)
        self.m = len(encoded_grid[0])

    def __repr__(self) -> str:
        return '\n'.join(''.join(self.ROCK_ENCODINGS_REVERSED[encoding] for encoding in line)
                         for line in self.encoded_grid)

    def __getitem__(self, item: tuple[int, int]):
        value = self.encoded_grid[item[0]][item[1]]
        return value

    def __eq__(self, other: RockNRoller) -> bool:
        if self.n != other.n or self.m != other.m:
            return False

        for i in range(self.n):
            for j in range(self.m):
                if self[(i, j)] != other[(i, j)]:
                    return False
        return True

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.encoded_grid))

    @property
    def hard_rock_encoding(self) -> int:
        return self.ROCK_ENCODINGS[self.HARD_ROCK_CHAR]

    @property
    def smooth_rock_encoding(self) -> int:
        return self.ROCK_ENCODINGS[self.SMOOTH_ROCK_CHAR]

    @classmethod
    def from_lines(cls, lines: list[str]):
        n = len(lines)
        m = len(lines[0])
        encoded_grid = empty_grid(n, m)

        for i, row in enumerate(lines):
            for j, char in enumerate(row):
                encoded_grid[i][j] = cls.ROCK_ENCODINGS[char]

        return cls(encoded_grid)

    def copy(self) -> RockNRoller:
        return RockNRoller(self.encoded_grid)

    def rotate_clockwise_90_degrees(self) -> None:
        new_grid = empty_grid(self.m, self.n)
        for i, row in enumerate(self.encoded_grid):
            for j, encoding in enumerate(row):
                new_grid[j][self.m - i - 1] = encoding

        self.encoded_grid = new_grid
        return None

    def rotate_anticlockwise_90_degrees(self) -> None:
        new_grid = empty_grid(self.m, self.n)
        for i, row in enumerate(self.encoded_grid):
            for j, encoding in enumerate(row):
                new_grid[self.m - j - 1][i] = encoding

        self.encoded_grid = new_grid
        return None

    def roll_north(self) -> None:
        hard_rock_encoding = self.hard_rock_encoding
        smooth_rock_encoding = self.smooth_rock_encoding

        hard_rock_positions = [[i for i in range(self.n) if self.encoded_grid[i][j] == hard_rock_encoding] + [self.n]
                               for j in range(self.m)]
        smooth_rock_positions = [[i for i in range(self.n) if self.encoded_grid[i][j] == smooth_rock_encoding]
                                 for j in range(self.m)]

        new_grid = empty_grid(self.n, self.m)

        for j, hard_rocks in enumerate(hard_rock_positions):
            for hard_rock in hard_rocks[:-1]:
                new_grid[hard_rock][j] = hard_rock_encoding

        for col_idx in range(self.m):
            hard_idx = 0
            current_smooth_rock_idx = 0
            for smooth_rock in smooth_rock_positions[col_idx]:
                hard_rock = hard_rock_positions[col_idx][hard_idx]
                while smooth_rock > hard_rock:
                    current_smooth_rock_idx = hard_rock + 1
                    hard_idx += 1
                    hard_rock = hard_rock_positions[col_idx][hard_idx]
                new_grid[current_smooth_rock_idx][col_idx] = smooth_rock_encoding
                current_smooth_rock_idx += 1

        self.encoded_grid = new_grid
        return None

    @property
    def total_load(self) -> int:
        total = 0
        smooth_rock_encoding = self.smooth_rock_encoding

        for i, row in enumerate(reversed(self.encoded_grid), 1):
            for j, encoding in enumerate(row):
                if encoding == smooth_rock_encoding:
                    total += i
        return total

    def spin_cycle_one_iter(self) -> None:
        self.roll_north()  # North
        self.rotate_clockwise_90_degrees()
        self.roll_north()  # West
        self.rotate_clockwise_90_degrees()
        self.roll_north()  # South
        self.rotate_clockwise_90_degrees()
        self.roll_north()  # East
        self.rotate_clockwise_90_degrees()
        return None

    def spin_until_stable(self, max_spins: int = 1_000_000_000) -> (int, int, Grid):
        # Using Floyd-Warshall cycle detection algorithm
        test_roller = self.copy()
        slow_pointer = 0
        fast_pointer = 0
        spin_cycles = [test_roller.encoded_grid]
        for _ in range(max_spins // 2):
            for _ in range(2):
                test_roller.spin_cycle_one_iter()
                spin_cycles.append(test_roller.encoded_grid)
            slow_pointer += 1
            fast_pointer += 2
            if spin_cycles[slow_pointer] == spin_cycles[fast_pointer]:
                return slow_pointer, fast_pointer - slow_pointer, spin_cycles[slow_pointer]
        return -1, -1, spin_cycles[-1]

    @staticmethod
    def __cycle_states(cycle_size_upper_bound: int, roller_state: Grid) -> list[RockNRoller]:
        test_roller = RockNRoller(roller_state)
        roller_states = {test_roller}
        roller_states_list = [test_roller]
        previous_set_length = 1
        for _ in range(cycle_size_upper_bound):
            test_roller.spin_cycle_one_iter()
            if test_roller not in roller_states:
                roller_states.add(test_roller.copy())
                roller_states_list.append(test_roller.copy())
            if len(roller_states) == previous_set_length:
                return roller_states_list
            previous_set_length = len(roller_states)
        raise TypeError

    def spin_cycle(self, num_iterations: int=1) -> RockNRoller:
        if num_iterations == 0:
            return self

        cycle_iter_start, cycle_length_upper_bound, slow_state = self.spin_until_stable(num_iterations)
        if cycle_iter_start == -1:
            return RockNRoller(slow_state)

        cycle_rollers = self.__cycle_states(cycle_length_upper_bound, slow_state)
        total_loads = [roller.total_load for roller in cycle_rollers]
        print(f"Cycle total loads: {total_loads}")
        print(f"cycle length: {len(cycle_rollers)}")
        roller_index = (num_iterations - cycle_iter_start) % len(cycle_rollers)
        return cycle_rollers[roller_index]


def test1():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))
    rock_roller.roll_north()

    correctly_rolled_north = RockNRoller.from_lines(read_lines("day_14_1_test_input2.txt"))
    assert rock_roller == correctly_rolled_north
    assert rock_roller.total_load == 136


def test2():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input2.txt"))
    assert rock_roller.total_load == 136


def tests():
    test1()
    test2()


def main():
    tests()

    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_input.txt"))
    rock_roller.roll_north()
    t = rock_roller.total_load
    assert t == 108889


if __name__ == "__main__":
    main()
