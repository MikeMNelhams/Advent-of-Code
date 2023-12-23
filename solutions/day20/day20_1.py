from handy_dandy_library.file_processing import read_lines
from collections import deque
from abc import ABC, abstractmethod
from typing import Callable


type PulseOutput = list[Pulse]


class Pulse:
    def __init__(self, signal: int, target: str, source: str):
        self.signal = signal
        self.target = target
        self.source = source

    def __repr__(self) -> str:
        return f"Pulse({self.source} -{self.signal}-> {self.target})"


NULL_PULSE = Pulse(-1, '', '')


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

    @property
    @abstractmethod
    def state(self) -> int:
        raise NotImplementedError


class NullModule(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__(name, [])

    def process(self, pulse: Pulse) -> PulseOutput:
        return []

    @property
    def state(self) -> int:
        return 0


class Broadcaster(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__("broadcaster", destination_names)

    def process(self, pulse: Pulse) -> PulseOutput:
        return [Pulse(pulse.signal, destination, self.name) for destination in self.destinations]

    @property
    def state(self) -> int:
        return 0


class Button(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__("button", destination_names)

    def process(self, pulse: Pulse) -> PulseOutput:
        return [Pulse(0, "broadcaster", "button")]

    @property
    def state(self) -> int:
        return 0


class FlipFlop(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__(name, destination_names)
        self.__state = 0

    def process(self, pulse: Pulse) -> PulseOutput:
        if pulse.signal == 1:
            return []
        self.__state = 1 - self.__state
        return [Pulse(self.__state, destination, self.name) for destination in self.destinations]

    @property
    def state(self) -> int:
        return self.__state


class Conjunction(PulseModule):
    def __init__(self, name: str, destination_names: list[str]):
        super().__init__(name, destination_names)
        self.inputs_known = False
        self.pulses_received = {}

    def update_inputs_before_process(self, input_module_names: list[str]) -> None:
        for input_module_name in input_module_names:
            self.pulses_received[input_module_name] = 0
        self.inputs_known = True
        return None

    def process(self, pulse: Pulse) -> PulseOutput:
        self.pulses_received[pulse.source] = pulse.signal
        if not self.inputs_known:
            raise AssertionError
        if all(value for value in self.pulses_received.values()):
            return [Pulse(0, destination, self.name) for destination in self.destinations]
        return [Pulse(1, destination, self.name) for destination in self.destinations]

    @property
    def state(self) -> int:
        return sum(pulse_received << i for i, pulse_received in self.pulses_received)


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
        self.update_conjunction_modules()

    @property
    def state(self):
        return tuple(pulse_module.state for pulse_module in self.pulse_module_map.values())

    def update_conjunction_modules(self) -> None:
        # TODO change from O(n^2 * m) to O(n^2) where m is the average # of destinations
        conjunction_modules = [pulse_module
                               for pulse_module in self.pulse_module_map.values()
                               if isinstance(pulse_module, Conjunction)]
        for conjunction_module in conjunction_modules:
            input_module_names = [pulse_module.name
                                  for pulse_module in self.pulse_module_map.values()
                                  for destination in pulse_module.destinations
                                  if destination == conjunction_module.name]
            conjunction_module.update_inputs_before_process(input_module_names)
        return None

    @property
    def total_pulse_count(self) -> int:
        return self.low_pulses_count + self.high_pulses_count

    @property
    def pulse_product(self) -> int:
        return self.low_pulses_count * self.high_pulses_count

    def push_the_button(self) -> None:
        self.pulse_deque.append(Pulse(0, "button", "MightyButtonPusher"))
        self.low_pulses_count -= 1  # The button press doesn't count as a pulse
        self.__process_stack_until_empty()
        return None

    def __process_stack_until_empty(self) -> None:
        pulse = NULL_PULSE
        while self.pulse_deque:
            pulse: Pulse = self.pulse_deque.popleft()
            self.increment_pulse_count(pulse)
            process = self.pulse_module_map.get(pulse.target, NullModule(pulse.source, [])).process
            new_pulses = process(pulse)
            if new_pulses:
                for _pulse in new_pulses:
                    self.pulse_deque.append(_pulse)
        return None

    def increment_pulse_count(self, pulse: Pulse) -> None:
        if pulse.signal == 0:
            self.low_pulses_count += 1
        else:
            self.high_pulses_count += 1
        return None


def test1():
    start_modules = PulseModuleCreator.pulse_modules(read_lines("day_20_1_test_input1.txt"))
    pulse_processor = PulseProcessor(start_modules)
    for i in range(1_000):
        print(f"Pushing the button #{i+1}")
        pulse_processor.push_the_button()
    print(pulse_processor.pulse_product, pulse_processor.low_pulses_count, pulse_processor.high_pulses_count)
    assert pulse_processor.pulse_product == 32_000_000


def test2():
    start_modules = PulseModuleCreator.pulse_modules(read_lines("day_20_1_test_input2.txt"))
    pulse_processor = PulseProcessor(start_modules)
    for i in range(1_000):
        print(f"Pushing the button #{i+1}")
        pulse_processor.push_the_button()
    print(pulse_processor.pulse_product, pulse_processor.low_pulses_count, pulse_processor.high_pulses_count)
    assert pulse_processor.pulse_product == 11_687_500


def main():
    test1()
    test2()

    start_modules = PulseModuleCreator.pulse_modules(read_lines("day_20_1_input.txt"))
    pulse_processor = PulseProcessor(start_modules)
    for i in range(1_000):
        print(f"Pushing the button #{i+1}")
        pulse_processor.push_the_button()
    print(pulse_processor.pulse_product, pulse_processor.low_pulses_count, pulse_processor.high_pulses_count)


if __name__ == "__main__":
    main()
