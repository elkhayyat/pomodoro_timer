from dataclasses import dataclass
from typing import Optional


@dataclass
class TimerSettings:
    work_duration: int  # in seconds
    rest_duration: int  # in seconds
    sound_file: str

    @classmethod
    def default(cls) -> 'TimerSettings':
        return cls(
            work_duration=25 * 60,  # 25 minutes
            rest_duration=5 * 60,  # 5 minutes
            sound_file="src/assets/ringing.mp3"
        )


@dataclass
class TimerStateData:
    is_running: bool = False
    is_resting: bool = False
    remaining_time: Optional[int] = None
    last_update: float = 0.0
