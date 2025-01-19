from handy_dandy_library.file_processing import read_lines


class ChronospatialComputer:
    def __init__(self, lines: list[str]):
        self.lines = lines

        self.a = self.__last_number_after_space(lines[0])
        self.b = self.__last_number_after_space(lines[1])
        self.c = self.__last_number_after_space(lines[2])

        self.a_start = self.a
        self.b_start = self.b
        self.c_start = self.c

        self.program = self.__program(lines[4])

        self.halted = False
        self.instruction_index = 0
        self.outs = []

    def __repr__(self) -> str:
        return f"CC[A: {self.a}, B: {self.b}, C: {self.c}]"

    def reset(self) -> None:
        self.outs.clear()
        self.a = self.a_start
        self.b = self.b_start
        self.c = self.c_start
        self.halted = False
        self.instruction_index = 0

    @staticmethod
    def __last_number_after_space(x: str) -> int:
        for i in range(len(x) - 1, -1, -1):
            char = x[i]
            if char == ' ':
                return int(x[i+1:])
        raise ValueError("Last integer after space could not be found!")

    @staticmethod
    def __program(line: str) -> list[int]:
        phrase = line.split(' ')
        return [int(x) for x in phrase[1].split(',')]

    def process_program(self) -> str:
        if len(self.program) < 2:
            return []

        while not self.halted:
            self.step()

        return ','.join([str(x) for x in self.outs])

    def step(self) -> None:
        if self.instruction_index + 1 >= len(self.program):
            self.halted = True
            return None

        opcode_instruction = self.program[self.instruction_index]
        operand = self.program[self.instruction_index + 1]

        if opcode_instruction == 0:
            self.opcode0(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 1:
            self.opcode1(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 2:
            self.opcode2(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 3:
            self.opcode3(operand)
            return None
        if opcode_instruction == 4:
            self.opcode4(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 5:
            self.opcode5(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 6:
            self.opcode6(operand)
            self.instruction_index += 2
            return None
        if opcode_instruction == 7:
            self.opcode7(operand)
            self.instruction_index += 2
            return None
        raise ValueError(f"Invalid input instruction opcode: {operand}")

    def __get_opcode_combo(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise ValueError("Invalid combo operand!")

    def __adv(self, operand) -> int:
        numerator = self.a
        denominator = 2 ** self.__get_opcode_combo(operand)
        return int(numerator / denominator)

    def opcode0(self, operand: int) -> None:
        self.a = self.__adv(operand)
        return None

    def opcode1(self, operand: int) -> None:
        self.b ^= operand
        return None

    def opcode2(self, operand: int) -> None:
        self.b = self.__get_opcode_combo(operand) % 8
        return None

    def opcode3(self, operand: int) -> None:
        if self.a == 0:
            self.instruction_index += 2
            return None

        self.instruction_index = operand
        return None

    def opcode4(self, operand: int) -> None:
        self.b ^= self.c
        return None

    def opcode5(self, operand: int) -> None:
        self.outs.append(self.__get_opcode_combo(operand) % 8)
        return None

    def opcode6(self, operand: int) -> None:
        self.b = self.__adv(operand)
        return None

    def opcode7(self, operand: int) -> None:
        self.c = self.__adv(operand)
        return None

    def determine_tauto_a(self) -> int:
        n = len(self.program)

        def run_program(a_trial):
            self.a = a_trial

            while self.instruction_index < n:
                self.step()

            outs = [x for x in self.outs]
            self.reset()
            return outs

        a_test = 0
        for i in reversed(range(n)):
            a_test <<= 3
            while run_program(a_test) != self.program[i:]:
                a_test += 1

        return a_test



def tests():
    chrono_computer = ChronospatialComputer(read_lines("puzzle17_1_test_input1.txt"))
    t1 = chrono_computer.process_program()
    assert t1 == "4,6,3,5,6,3,5,2,1,0"

    chrono_computer2 = ChronospatialComputer(read_lines("puzzle17_1_test_input2.txt"))
    chrono_computer2.process_program()
    assert chrono_computer2.b == 1

    chrono_computer3 = ChronospatialComputer(read_lines("puzzle17_1_test_input3.txt"))
    t2 = chrono_computer3.process_program()
    assert t2 == "0,1,2"

    chrono_computer4 = ChronospatialComputer(read_lines("puzzle17_1_test_input4.txt"))
    chrono_computer4.process_program()
    assert chrono_computer4.b == 26

    chrono_computer5 = ChronospatialComputer(read_lines("puzzle17_1_test_input5.txt"))
    chrono_computer5.process_program()
    assert chrono_computer5.b == 44354


def main():
    tests()

    chrono_computer = ChronospatialComputer(read_lines("puzzle17_1.txt"))
    t1 = chrono_computer.process_program()
    assert t1 == "6,1,6,4,2,4,7,3,5"


if __name__ == "__main__":
    main()
