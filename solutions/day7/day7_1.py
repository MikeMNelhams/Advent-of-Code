from handy_dandy_library.file_processing import read_lines

from collections import Counter

from typing import Callable




class HandReader:
    CARD_ORDERING = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6,
                     '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}

    def __init__(self, hand: str):
        self.hand = hand
        self._card_counts = Counter(hand)
        self._most_common = self._card_counts.most_common()
        self.hand_type = self._get_hand_type()

    def __repr__(self) -> str:
        return f"Hand({self.hand} | type: {self.hand_type})"

    def _get_hand_type(self) -> int:
        if self.is_5_of_a_kind():
            return 6
        if self.is_4_of_a_kind():
            return 5
        if self.is_full_house():
            return 4
        if self.is_3_of_a_kind():
            return 3
        if self.is_two_pair():
            return 2
        if self.is_one_pair():
            return 1
        if self.is_high_card():
            return 0
        return -1

    def is_5_of_a_kind(self) -> bool:
        return self._most_common[0][1] == 5

    def is_4_of_a_kind(self) -> bool:
        return self._most_common[0][1] == 4

    def is_full_house(self) -> bool:
        return self._most_common[0][1] == 3 and self._most_common[1][1] == 2

    def is_3_of_a_kind(self) -> bool:
        return self._most_common[0][1] == 3 and self._most_common[1][1] != 2

    def is_two_pair(self) -> bool:
        return self._most_common[0][1] == 2 and self._most_common[1][1] == 2

    def is_one_pair(self) -> bool:
        return self._most_common[0][1] == 2 and self._most_common[1][1] != 2

    def is_high_card(self) -> bool:
        return self._most_common[0][1] == 1

    def lesser_hand_of_same_type(self, other) -> bool:
        for char1, char2 in zip(self.hand, other.hand):
            char1_value = self.CARD_ORDERING[char1]
            char2_value = self.CARD_ORDERING[char2]
            if char1_value < char2_value:
                return True
            elif char1_value > char2_value:
                return False
        return False

    def __eq__(self, other) -> bool:
        return self.hand == other.hand

    def __lt__(self, other) -> bool:
        if self == other:
            return False
        if self.hand_type == other.hand_type:
            return self.lesser_hand_of_same_type(other)
        return self.hand_type < other.hand_type

    def update_hand_data(self) -> None:
        self._card_counts = Counter(self.hand)
        self._most_common = self._card_counts.most_common()
        self.hand_type = self._get_hand_type()
        return None


def parse_hand_bids(lines: list[str], hand_reader: Callable=HandReader) -> list[list[HandReader, int]]:
    hands_and_bids = [line.split(' ') for line in lines]
    for i in range(len(hands_and_bids)):
        hands_and_bids[i] = (hand_reader(hands_and_bids[i][0]), int(hands_and_bids[i][1]))
    return hands_and_bids


def total_winnings(lines: list[str], hand_reader: Callable=HandReader) -> int:
    hands_and_bids = parse_hand_bids(lines, hand_reader)

    def pair(x):
        return x[0]

    hands_and_bids.sort(key=pair)
    for i, hand_bid in enumerate(hands_and_bids):
        print(f"{hand_bid[0]} is rank {i + 1}")
    total = sum(pair[1] * (i+1) for i, pair in enumerate(hands_and_bids))
    return total


def tests():
    assert HandReader("AAAAA").is_5_of_a_kind()
    assert not HandReader("AAAAK").is_5_of_a_kind()

    assert HandReader("AAAAK").is_4_of_a_kind()
    assert not HandReader("AAAKK").is_4_of_a_kind()
    assert not HandReader("AAAAA").is_4_of_a_kind()

    assert HandReader("AAAKK").is_full_house()
    assert not HandReader("AAAAK").is_3_of_a_kind()
    assert not HandReader("AAAAA").is_3_of_a_kind()
    assert not HandReader("KAKAQ").is_3_of_a_kind()
    assert HandReader("KAKQK").is_3_of_a_kind()
    assert HandReader("AKKK3").is_3_of_a_kind()
    assert HandReader("T55J5").is_3_of_a_kind()
    assert HandReader("QQQJA").is_3_of_a_kind()

    assert HandReader("AAKKQ").is_two_pair()
    assert not HandReader("AAAKK").is_two_pair()

    assert HandReader("AAKQJ").is_one_pair()
    assert not HandReader("AAKKQ").is_one_pair()

    assert HandReader("32T3K").is_one_pair()

    assert HandReader("AKQJ9").is_high_card()

    assert total_winnings(read_lines("day_7_1_test_input.txt")) == 6440

    assert HandReader("A8624") > HandReader("9TJ67")
    assert HandReader("9TJ67") < HandReader("A8624")
    assert HandReader("7227Q") > HandReader("67Q64")

    assert HandReader("23K8Q").is_high_card()


def main():
    tests()

    t = total_winnings(read_lines("day_7_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
