import operator

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import find_first_char_index

from functools import reduce


COLOURS_EMPTY = {"red": 0, "green": 0, "blue": 0}


class Round:
    DEFAULT_MAX_COLOURS = {"red": 12, "green": 13, "blue": 14}

    def __init__(self, round_number: int, red: int, green: int, blue: int):
        self.round_number = round_number
        self.colours = {"red": red, "green": green, "blue": blue}
        self.__max_colours = Round.DEFAULT_MAX_COLOURS

    @classmethod
    def from_colours(cls, round_number: int, colours: dict[str, int]):
        return cls(round_number, **colours)

    @classmethod
    def from_string(cls, round_number: int, round_string: str):
        round_colour_data = round_string.split(', ')
        colours = COLOURS_EMPTY.copy()
        for phrase in round_colour_data:
            colour_info = phrase.split(' ')
            colour_count, colour_name = colour_info[0], colour_info[1]
            colours[colour_name] += int(colour_count)
        return cls.from_colours(round_number, colours)

    def __repr__(self) -> str:
        return f"Round({self.round_number}, {self.colours})"

    def is_possible(self) -> bool:
        return all(self.__max_colours[colour] >= colour_count for colour, colour_count in self.colours.items())

    def power(self) -> int:
        return reduce(operator.mul, self.colours.values())


class Game:
    def __init__(self, game_id: int, game_rounds: list[Round]):
        self.game_id = game_id
        self.rounds = game_rounds

    @classmethod
    def from_string(cls, game_string: str):
        colon_index = find_first_char_index(game_string, target_char=':')
        game_id = int(game_string[5:colon_index])
        game_rounds = [Round.from_string(i, game_round) for i, game_round in
                       enumerate(cls.__split_game_str(game_string, colon_index))]
        return cls(game_id, game_rounds)

    @staticmethod
    def __split_game_str(game_string: str, round_start_index: int) -> str:
        return game_string[round_start_index + 2:].split('; ')

    def __repr__(self) -> str:
        return f"Game #: {self.game_id} Rounds: {self.rounds}"

    def is_possible(self) -> bool:
        return all(game_round.is_possible() for game_round in self.rounds)

    def minimum_possible_round(self) -> Round:
        maximal_colours = COLOURS_EMPTY.copy()

        for game_round in self.rounds:
            for colour, colour_count in game_round.colours.items():
                maximal_colours[colour] = max(maximal_colours[colour], colour_count)

        return Round.from_colours(-1, maximal_colours)


def total_valid_game_ids(games: list[Game]):
    return sum(game.game_id if game.is_possible() else 0 for game in games)


def total_valid_game_ids_from_file_path(file_path: str) -> int:
    games = [Game.from_string(game_phrase) for game_phrase in read_lines(file_path)]
    return total_valid_game_ids(games)


def tests():
    assert total_valid_game_ids_from_file_path("puzzle2_1_test_input.txt") == 8


def main():
    tests()

    total = total_valid_game_ids_from_file_path("puzzle2_1_input.txt")
    print(total)


if __name__ == "__main__":
    main()
