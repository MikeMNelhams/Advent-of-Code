from handy_dandy_library.file_processing import read_lines

from day7_1 import HandReader, total_winnings


class HandReaderJackOfAllTrades(HandReader):
    CARD_ORDERING = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7,
                      '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}

    def __init__(self, hand: str):
        super(HandReaderJackOfAllTrades, self).__init__(hand)
        self.hand = self.jack_edited_hand()
        self.update_hand_data()
        self.hand_j_substituted = self.hand
        self.hand = hand

    def __repr__(self) -> str:
        return f"Hand({self.hand} -> {self.hand_j_substituted} | type: {self.hand_type})"

    def jack_edited_hand(self) -> str:
        j_frequency = self._card_counts.get('J', 0)
        if j_frequency == 0:
            return self.hand[:]

        if self.hand == "JJJJJ":
            return self.hand[:]

        reordered_most_common = sorted(self._card_counts.items(), key=lambda v: (v[1], self.CARD_ORDERING[v[0]]),
                                              reverse=True)
        highest_frequency_char_non_j = ""
        for i, frequency in enumerate(reordered_most_common):
            if frequency[0] != 'J':
                highest_frequency_char_non_j = frequency[0]
                break

        return self.hand.replace('J', highest_frequency_char_non_j)


def tests():
    assert HandReaderJackOfAllTrades("2J36J").hand_type == 3
    assert HandReaderJackOfAllTrades("JKKK2") < HandReaderJackOfAllTrades("QQQQ2")
    assert HandReaderJackOfAllTrades("2J36J").hand_j_substituted == "26366"
    assert HandReaderJackOfAllTrades("J2484").hand_j_substituted == "42484"
    assert total_winnings(read_lines("day_7_1_test_input.txt"), HandReaderJackOfAllTrades) == 5905


def main():
    tests()

    t = total_winnings(read_lines("day_7_1_input.txt"), HandReaderJackOfAllTrades)
    print(t)
    assert t == 250506580


if __name__ == "__main__":
    main()
