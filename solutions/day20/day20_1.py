from handy_dandy_library.file_processing import read_lines
from collections import deque
from abc import ABC, abstractmethod
from typing import Callable


type PulseOutput = list[tuple[int, str]]
type Pulse = list[int, str] | tuple[int, str]


class PulseModule(ABC):
    def __init__(self, name: str, destination_names: list[str]):
        self.destinations = destination_names
        self.name = name

    def __repr__(self) -> str:
        name_repr = self.name
        class_name = self.__class__.__name__.lower()
        if class_name == self.name:
            name_repr = ''
        return f"{class_name.capitalize()}({name_repr}, {self.destinations})"

    @abstractmethod
    def process(self, pulse: Pulse) -> PulseOutput:
        raise NotImplementedError


class Broadcaster(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__("broadcaster", destination_names)

    def process(self, pulse: Pulse) -> PulseOutput:
        return [(pulse[0], destination) for destination in self.destinations]


class Button(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__("button", destination_names)

    def process(self, pulse: Pulse) -> PulseOutput:
        return [(0, "broadcaster")]


class FlipFlop(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__(name, destination_names)
        self.state = 0

    def process(self, pulse: Pulse) -> PulseOutput:
        if pulse[0] == 1:
            return []
        self.state = 1 - self.state
        return [(self.state, destination) for destination in self.destinations]


class Conjunction(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__(name, destination_names)
        self.pulses_received = {}

    def process(self, pulse: Pulse) -> PulseOutput:
        # TODO the conjunction nodes needs to know all its input nodes
        # self.pulses_received[pulse[1]] = pulse[0]

        if len(self.pulses_received) == 0:
            print("O length")
            return [(0, destination) for destination in self.destinations]

        if all(value == 1 for value in self.pulses_received.values()):
            print("All 1s")
            return [(1, destination) for destination in self.destinations]

        print(f"Missing a 1 from: {self.pulses_received}")
        return [(0, destination) for destination in self.destinations]


class PulseModuleCreator:
    PULSE_MODULE_NAME_MAP: dict[str, Callable] = {'b': {'r': Broadcaster, 'u': Button}, '%': FlipFlop, '&': Conjunction}

    @classmethod
    def pulse_modules(cls, lines: list[str]) -> list[PulseModule]:
        modules = [cls.__module_from_line(line) for line in lines]
        print(modules)
        return modules

    @classmethod
    def __module_from_line(cls, line: str):
        line_halves = line.split(" -> ")
        name_phrase = line_halves[0]
        destinations = line_halves[1].split(", ")
        module_class = cls.class_callable_from_name(name_phrase)
        name = name_phrase[1:]
        if name_phrase[0] == 'b':
            name = name_phrase[0] + name
        return module_class(name, destinations)

    @classmethod
    def class_callable_from_name(cls, name: str):
        class_callable = cls.PULSE_MODULE_NAME_MAP[name[0]]
        i = 1
        while type(class_callable) is dict:
            class_callable = class_callable[name[i]]
        return class_callable


class PulseProcessor:
    def __init__(self, pulse_modules: list[PulseModule]):
        self.pulse_module_map = {pulse_module.name: pulse_module
                                         for pulse_module in pulse_modules}
        self.button = Button('', ["broadcaster"])
        self.pulse_module_map["button"] = self.button
        self.pulse_deque: deque[Pulse] = deque()
        self.low_pulses_count = 0
        self.high_pulses_count = 0

    @property
    def total_pulse_count(self) -> int:
        return self.low_pulses_count + self.high_pulses_count

    def push_the_button(self) -> None:
        self.pulse_deque.append((0, "button"))
        self.low_pulses_count -= 1  # The button press doesn't count as a pulse
        self.__process_stack_until_empty()
        return None

    def __process_stack_until_empty(self) -> None:
        pulse = None
        while self.pulse_deque:
            pulse: Pulse = self.pulse_deque.popleft()
            self.increment_pulse_count(pulse)
            process = self.pulse_module_map[pulse[1]].process
            new_pulses = process(pulse)
            if new_pulses:
                for _pulse in new_pulses:
                    self.pulse_deque.append(_pulse)
            print(f"Popped: {pulse} | Remaining: {self.pulse_deque}")
            if self.total_pulse_count > 10_000:
                raise ZeroDivisionError
        return None

    def increment_pulse_count(self, pulse: tuple[int, str]) -> None:
        if pulse[0] == 0:
            self.low_pulses_count += 1
        else:
            self.high_pulses_count += 1
        return None


def tests():
    start_modules = PulseModuleCreator.pulse_modules(read_lines("day_20_1_test_input1.txt"))
    pulse_processor = PulseProcessor(start_modules)
    pulse_processor.push_the_button()
    print(pulse_processor.total_pulse_count, pulse_processor.low_pulses_count, pulse_processor.high_pulses_count)


def main():
    tests()


if __name__ == "__main__":
    main()
