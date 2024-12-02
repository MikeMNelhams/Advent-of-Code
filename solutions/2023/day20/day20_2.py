from handy_dandy_library.file_processing import read_lines
from day20_1 import PulseProcessor, PulseModuleCreator
from functools import reduce
import operator


def main():
    start_modules = PulseModuleCreator.pulse_modules(read_lines("day_20_1_input.txt"))
    pulse_processor = PulseProcessor(start_modules)
    cycle_numbers = pulse_processor.cycle_lengths([(name, 0) for name in ("mp", "qt", "qb", "ng")])
    print(cycle_numbers)
    t = reduce(operator.mul, cycle_numbers)
    print(t)


if __name__ == "__main__":
    main()
