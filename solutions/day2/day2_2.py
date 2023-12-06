from handy_dandy_library.file_processing import read_lines
from day2_1 import Game


def total_power(games: list[Game]) -> int:
    return sum(game.minimum_possible_round().power() for game in games)


def total_power_from_file_path(file_path: str) -> int:
    games = [Game.from_string(game_phrase) for game_phrase in read_lines(file_path)]
    return sum(game.minimum_possible_round().power() for game in games)


def tests():
    game_phrases = read_lines("puzzle2_1_test_input.txt")
    games = [Game.from_string(game_phrase) for game_phrase in game_phrases]

    assert games[0].minimum_possible_round().power() == 48
    assert games[1].minimum_possible_round().power() == 12
    assert games[2].minimum_possible_round().power() == 1560
    assert total_power(games) == 2286

    assert total_power_from_file_path("puzzle2_1_test_input.txt") == 2286


def main():
    tests()

    t = total_power_from_file_path("puzzle2_1_input.txt")
    print(t)


if __name__ == "__main__":
    main()
