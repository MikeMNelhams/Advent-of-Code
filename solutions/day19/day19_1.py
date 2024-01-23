from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import find_first_char_index, find_first_char_index_from_charset

from typing import Callable

type BinaryOperator = Callable[[int, int], bool]
type Criteria = Callable[[int], bool]
type Part = dict[str, int]


def gt(a: int, b: int) -> bool:
    return a > b


def lt(a: int, b: int) -> bool:
    return a < b


def eq(a: int, b: int) -> bool:
    return a == b


class BinaryOperatorWrapper:
    def __init__(self, base_function: BinaryOperator, threshold: int):
        self.base_function = base_function
        self.threshold = threshold

    def __call__(self, x: int) -> bool:
        return self.base_function(x, self.threshold)


class Rule:
    def __init__(self, part_type: str, target: str, criteria: Criteria):
        self.part_type = part_type
        self.target = target
        self.criteria = criteria

    def __call__(self, part: Part) -> bool:
        return self.criteria(part[self.part_type])

    def __repr__(self) -> str:
        return f"{self.part_type}->{self.target}"


class RuleSet:
    CHAR_TO_OPERATORS = {'>': gt, '<': lt, '=': eq}
    OPERATOR_CHARS = {'<', '>', '='}

    def __init__(self, name: str, rules: list[Rule | str], default_target: str):
        self.name = name
        self.rules = rules
        self.is_always_default = rules[0] is str
        self.default_target = default_target

    def __call__(self, part: Part) -> str:
        if self.is_always_default:
            return self.default_target

        for rule in self.rules:
            if rule(part):
                return rule.target
        return self.default_target

    def __repr__(self) -> str:
        return f"[{self.name}({','.join(str(rule) for rule in self.rules)}) DEFAULT: {self.default_target}]"

    @classmethod
    def from_line(cls, line: str):
        # px{a<2006:qkq,m>2090:A,rfg}
        curly_bracket_index = find_first_char_index(line, '{')
        name = line[:curly_bracket_index]
        rule_phrases = line[curly_bracket_index + 1:-1].split(',')
        default_target = rule_phrases[-1]

        if len(rule_phrases) == 1:
            return cls(name, rule_phrases, default_target)

        rule_data = []
        for rule_phrase in rule_phrases[:-1]:
            phrase_halves = rule_phrase.split(':')
            target = phrase_halves[1]
            criteria_phrase = phrase_halves[0]

            operator = cls.CHAR_TO_OPERATORS[criteria_phrase[1]]
            part_type = criteria_phrase[:1]
            threshold = int(criteria_phrase[2:])

            criteria = BinaryOperatorWrapper(operator, threshold)
            rule_data.append(Rule(part_type, target, criteria))

        return cls(name, rule_data, default_target)


class Policy:
    def __init__(self, rule_sets: dict[str, RuleSet]):
        self.rule_sets = rule_sets

    def __repr__(self) -> str:
        return f"{self.rule_sets}"

    def accepts(self, part: Part) -> bool:
        outcome = "in"
        while outcome in self.rule_sets:
            rule_set = self.rule_sets[outcome]
            outcome = rule_set(part)
        return outcome == "A"

    @classmethod
    def from_lines(cls, lines: list[str]):
        empty_line_index = 0
        for i, line in enumerate(lines):
            if line == '':
                empty_line_index = i
                break
        if empty_line_index == 0:
            raise TypeError
        rule_sets = (RuleSet.from_line(line) for line in lines[:empty_line_index])
        return cls({rule_set.name: rule_set for rule_set in rule_sets})


class PartManager:
    def __init__(self, parts: list[Part], policy: Policy):
        self.parts = parts
        self.policy = policy

    def accepted_parts(self) -> list[Part]:
        return [part for part in self.parts if self.policy.accepts(part)]

    def sum_of_accepted_parts(self) -> int:
        accepted_parts = self.accepted_parts()
        return sum((sum(part.values()) for part in accepted_parts), 0)


def part_from_line(line: str) -> Part:
    data_phrases = line[1:-1].split(',')
    data_phrases_halves = [data_phrase.split('=') for data_phrase in data_phrases]
    return {data_phrase_halves[0]: int(data_phrase_halves[1]) for data_phrase_halves in data_phrases_halves}


def read_parts(lines: list[str]) -> list[Part]:
    empty_line_index = 0
    for i, line in enumerate(lines):
        if line == '':
            empty_line_index = i
            break
    if empty_line_index == 0:
        raise TypeError

    return [part_from_line(line) for line in lines[empty_line_index+1:]]


def tests():
    lines = read_lines("day_19_1_test_input1.txt")
    policy = Policy.from_lines(lines)
    parts = read_parts(lines)
    part_manager = PartManager(parts, policy)
    total_accepted_sum = part_manager.sum_of_accepted_parts()
    assert total_accepted_sum == 19114


def main():
    tests()

    lines = read_lines("day_19_1_input.txt")
    policy = Policy.from_lines(lines)
    parts = read_parts(lines)
    parts_manager = PartManager(parts, policy)
    total_accepted_sum = parts_manager.sum_of_accepted_parts()
    assert total_accepted_sum == 456651


if __name__ == "__main__":
    main()
