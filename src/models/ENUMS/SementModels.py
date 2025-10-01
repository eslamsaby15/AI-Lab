from typing import List
from dataclasses import dataclass

@dataclass
class Segment:
    speaker: str
    text: str


@dataclass
class DiarizationResult:
    segments: List[Segment]