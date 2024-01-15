from handy_dandy_library.file_processing import read_lines

from functools import cache


# This solution is edited, sourced originally from: https://aoc-puzzle-solver.streamlit.app/

def part2(lines: list[str]):
    @cache
    def dfs(sequence, groups):
        if not groups:
            return '#' not in sequence
        seq_len = len(sequence)
        if seq_len - sum(groups) - len(groups) + 1 < 0:
            return 0
        group_len = groups[0]
        has_holes = any(sequence[x] == '.' for x in range(group_len))
        if seq_len == group_len:
            return not has_holes
        can_use = not has_holes and sequence[group_len] != '#'
        if sequence[0] == '#':
            return dfs(sequence[group_len+1:].lstrip('.'), tuple(groups[1:])) if can_use else 0
        if not can_use:
            return dfs(sequence[1:].lstrip('.'), groups)
        return dfs(sequence[1:].lstrip('.'), groups) + dfs(sequence[group_len+1:].lstrip('.'), tuple(groups[1:]))

    total = 0
    for line in lines:
        sequence, groups = line.split()
        sequence = '?'.join([sequence] * 5).lstrip('.')
        groups = [int(g) for g in groups.split(',')] * 5
        total += dfs(sequence, tuple(groups))

    return total


def unfold_line(line: str) -> str:
    input_halves = line.split(' ')
    nonogram_numbers = input_halves[1].split(',') * 5
    nonogram_string = (input_halves[0] + '?') * 5
    nonogram_string = nonogram_string[:-1]

    nonogram_numbers_string = ",".join(nonogram_numbers)
    return f"{nonogram_string} {nonogram_numbers_string}"


def unfold(lines: list[str]) -> list[str]:
    return [unfold_line(line) for line in lines]


t = part2(read_lines("day_12_1_input.txt"))
print(t)
