from dataclasses import dataclass

@dataclass
class Event:
    event_type: str
    info: str