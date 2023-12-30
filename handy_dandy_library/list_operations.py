def binary_search(haystack: list, target):
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


def main():
    print("Do not run this file as main. This is a library file.")


if __name__ == "__main__":
    main()
