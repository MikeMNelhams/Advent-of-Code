from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D, Matrix2x2


class Arcade:
    def __init__(self, lines: list[str]):
        separated_lines = self.__claw_machine_lines(lines)
        self.claw_machines = [ClawMachine(x) for x in separated_lines]

    @staticmethod
    def __claw_machine_lines(lines: list[str]) -> list[list[str]]:
        separated_lines = []
        start = 0
        for i, line in enumerate(lines):
            if line == '':
                separated_lines.append(lines[start:i])
                start = i + 1
        separated_lines.append(lines[start:])
        return separated_lines

    def minimum_total_tokens_to_giga_win(self) -> int:
        return sum(tokens for claw_machine in self.claw_machines if (tokens := claw_machine.optimal_tokens_required()) != -1)

    def minimum_total_tokens_to_giga_win_rigged(self) -> int:
        return sum(tokens for claw_machine in self.claw_machines if (tokens := claw_machine.optimal_tokens_required_rigged()) != -1)


class ClawMachine:
    RIGGED_CONSTANT = 10_000_000_000_000

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.a = self.__a(lines[0])
        self.b = self.__b(lines[1])
        self.prize = self.__prize(lines[2])
        self.button_matrix = Matrix2x2(self.a.x, self.b.x, self.a.y, self.b.y)

    def __repr__(self) -> str:
        return f"ClawMachine[(a: {self.a}, b: {self.b}), prize: {self.prize}]"

    def is_potentially_viable(self) -> bool:
        return self.button_matrix.has_inverse()

    def optimal_press_vector(self) -> Vector2D:
        return (self.button_matrix.inverse() * self.prize).round_to_int_vector()

    def optimal_tokens_required(self) -> int:
        if not self.is_potentially_viable():
            return -1
        press_vector = self.optimal_press_vector()

        predicted_prize: Vector2D = self.button_matrix * press_vector
        if predicted_prize != self.prize:
            return -1

        return press_vector.x * 3 + press_vector.y

    def optimal_tokens_required_rigged(self) -> int:
        self.prize = Vector2D((self.prize.x + self.RIGGED_CONSTANT, self.prize.y + self.RIGGED_CONSTANT))
        return self.optimal_tokens_required()

    @staticmethod
    def __a(line: str) -> Vector2D:
        phrases = line.split('+')
        a_x = int(phrases[1].split(',')[0])
        a_y = int(phrases[2])
        return Vector2D((a_x, a_y))

    @staticmethod
    def __b(line: str) -> Vector2D:
        phrases = line.split('+')
        b_x = int(phrases[1].split(',')[0])
        b_y = int(phrases[2])
        return Vector2D((b_x, b_y))

    @staticmethod
    def __prize(line: str) -> Vector2D:
        phrases = line.split('=')
        p_x = int(phrases[1].split(',')[0])
        p_y = int(phrases[2])
        return Vector2D((p_x, p_y))


def tests():
    arcade = Arcade(read_lines("puzzle13_1_test_input1.txt"))
    assert arcade.claw_machines[0].optimal_tokens_required() == 280
    assert arcade.claw_machines[1].optimal_tokens_required() == -1
    assert arcade.claw_machines[2].optimal_tokens_required() == 200
    assert arcade.claw_machines[3].optimal_tokens_required() == -1

    assert arcade.minimum_total_tokens_to_giga_win() == 480


def main():
    tests()

    arcade = Arcade(read_lines("puzzle13_1.txt"))
    t1 = arcade.minimum_total_tokens_to_giga_win()
    print(t1)


if __name__ == "__main__":
    main()
