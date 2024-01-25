from handy_dandy_library.file_processing import read_lines
from day11_1 import galaxy_brain_sum


def main():
    t = galaxy_brain_sum(read_lines("day_11_1_input.txt"), expansion_rate=1_000_000 - 1)
    print(t)


if __name__ == "__main__":
    main()
