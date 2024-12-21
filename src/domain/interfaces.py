from abc import ABC, abstractmethod
from typing import Protocol

class TimerState(Protocol):
    is_running: bool
    is_resting: bool
    remaining_time: int
    last_update: float

class ITimer(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def rest(self) -> None:
        pass

class ISettings(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

class ISoundPlayer(ABC):
    @abstractmethod
    def play(self, sound_file: str) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass