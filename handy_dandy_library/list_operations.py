from typing import TypeVar, Iterable

T = TypeVar('T')


def binary_search(haystack: list, target) -> (int, bool):
    first = 0
    last = len(haystack) - 1
    found = False
    found_at_index = 0

    while first <= last and not found:
        found_at_index = 0
        midpoint = int((last - first) / 2 + first)
        if haystack[midpoint] == target:
            found_at_index = midpoint
            found = True
        else:
            if target < haystack[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    return found_at_index, found


def consecutive_pairs(sequence: list[T]) -> Iterable[tuple[T, T]]:
    return zip(sequence, sequence[1:] + [sequence[0]])


def main():
    print("Do not run this file as main. This is a library file.")


if __name__ == "__main__":
    main()
