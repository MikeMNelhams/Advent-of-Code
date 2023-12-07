from handy_dandy_library.file_processing import read_lines
from collections import Counter

from day7_1 import HandReader


CARD_ORDERING2 = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7,
                  '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}


class HandReaderJackOfAllTrades(HandReader):
    def __init__(self, hand: str):
        super(HandReaderJackOfAllTrades, self).__init__(hand)
        hand_copy = hand[:]
        self.edit_most_common_jack_substituted()
        self.hand_type = self._get_hand_type()
        self.hand_j_substituted = self.hand[:]
        self.hand = hand_copy

    def edit_most_common_jack_substituted(self) -> None:
        base_count_copy = Counter(self.hand)
        j_frequency = base_count_copy.get('J', 0)
        if j_frequency == 0:
            return None

        if self.hand == "JJJJJ":
            return None

        highest_frequency_char_non_j = None
        for frequency in self._most_common:
            if frequency[0] != 'J':
                highest_frequency_char_non_j = frequency[0]
                break

        self.hand = self.hand.replace('J', highest_frequency_char_non_j)

        base_count_copy[highest_frequency_char_non_j] += j_frequency
        del base_count_copy[j_frequency]
        self._most_common = base_count_copy.most_common()
        return None

    def __repr__(self) -> str:
        return f"Hand({self.hand} -> {self.hand_j_substituted} | type: {self.hand_type})"

    def lesser_hand_of_same_type(self, other) -> bool:
        for char1, char2 in zip(self.hand, other.hand):
            char1_value = CARD_ORDERING2[char1]
            char2_value = CARD_ORDERING2[char2]
            if char1_value < char2_value:
                return True
            elif char1_value > char2_value:
                return False
        return False


def parse_hand_bids2(lines: list[str]) -> list[list[HandReader, int]]:
    hands_and_bids = [line.split(' ') for line in lines]
    for i in range(len(hands_and_bids)):
        hands_and_bids[i] = (HandReaderJackOfAllTrades(hands_and_bids[i][0]), int(hands_and_bids[i][1]))
    return hands_and_bids


def total_winnings2(lines: list[str]) -> int:
    hands_and_bids = parse_hand_bids2(lines)

    def pair(x):
        return x[0]
    #   KJKKQ was rank 949
    #   K2222 was rank 950

    hands_and_bids.sort(key=pair)
    for i, hand_bid in enumerate(hands_and_bids):
        print(f"{hand_bid[0]} is rank {i+1}")
    total = sum(pair[1] * (i+1) for i, pair in enumerate(hands_and_bids))
    return total


def tests():
    assert HandReaderJackOfAllTrades("JKKK2") < HandReaderJackOfAllTrades("QQQQ2")
    assert total_winnings2(read_lines("day_7_1_test_input.txt")) == 5905


def main():
    tests()

    t = total_winnings2(read_lines("day_7_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
